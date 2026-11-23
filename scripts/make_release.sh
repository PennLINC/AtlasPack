#!/usr/bin/env bash
# Package the atlases and create a DRAFT GitHub release with them attached.
#
# The release is tied to the current commit, and the script refuses to run
# unless every file on disk matches the checksum manifests in that commit, so
# the git tag, the manifests, and the release assets always describe the same
# data. Review the draft on GitHub, then publish it; publishing triggers the
# Docker image build.
#
# Usage: scripts/make_release.sh [--no-upload] <version>
#   --no-upload   only build the assets in dist/; do not touch GitHub.
#
# Requires: git, tar, sha256sum or shasum, and gh (unless --no-upload).
set -euo pipefail

source "$(dirname "$0")/_common.sh"

upload=1
version=""
for arg in "$@"; do
    case "${arg}" in
        --no-upload) upload=0 ;;
        -h | --help)
            sed -n '2,14p' "$0"
            exit 0
            ;;
        *) version="${arg}" ;;
    esac
done

if [ -z "${version}" ]; then
    echo "Usage: $0 [--no-upload] <version>" >&2
    exit 1
fi

validate_version "${version}"
cd "${REPO_ROOT}"
commit="$(git rev-parse HEAD)"

# 1. The commit must be clean, so the release matches what is in git.
if [ -n "$(git status --porcelain -- "${DATASET_DIR}" checksums)" ]; then
    echo "Uncommitted changes in ${DATASET_DIR}/ or checksums/. Commit them first." >&2
    exit 1
fi

# 2. If the tag already exists (locally or on GitHub), it must point at HEAD.
#    Otherwise gh would attach these assets to a tag on a different commit.
tag_commits="$(git rev-parse -q --verify "refs/tags/${version}^{commit}" || true)"
if [ "${upload}" -eq 1 ]; then
    tag_commits="${tag_commits} $(git ls-remote origin "refs/tags/${version}^{}" "refs/tags/${version}" | cut -f1 | tail -1)"
fi

for tag_commit in ${tag_commits}; do
    if [ "${tag_commit}" != "${commit}" ]; then
        echo "Tag ${version} already exists at ${tag_commit}, not HEAD (${commit})." >&2
        exit 1
    fi
done

# 3. Every manifest entry must exist and match, and nothing may be unlisted.
work_dir="$(mktemp -d)"
trap 'rm -rf "${work_dir}"' EXIT

echo "Verifying ${DATASET_SUMS}"
sha256_tool -c --quiet "${DATASET_SUMS}"
manifest_paths "${DATASET_SUMS}" > "${work_dir}/dataset_expected"
list_dataset_files > "${work_dir}/dataset_actual"
require_same_paths "${DATASET_DIR}/ (run scripts/update_checksums.sh)" \
    "${work_dir}/dataset_expected" "${work_dir}/dataset_actual"

echo "Verifying ${SOURCES_SUMS}"
sha256_tool -c --quiet "${SOURCES_SUMS}"
manifest_paths "${SOURCES_SUMS}" > "${work_dir}/sources_expected"
list_source_files > "${work_dir}/sources_actual"
require_same_paths "Regeneration sources (run scripts/update_checksums.sh)" \
    "${work_dir}/sources_expected" "${work_dir}/sources_actual"

# 4. Build the assets. COPYFILE_DISABLE keeps macOS from adding ._ files.
#    validate_version guarantees dist_dir stays inside dist/.
dist_dir="${REPO_ROOT}/dist/${version}"
rm -rf "${dist_dir}"
mkdir -p "${dist_dir}"

dataset_tar="$(dataset_asset "${version}")"
sources_tar="$(sources_asset "${version}")"

COPYFILE_DISABLE=1 tar -czf "${dist_dir}/${dataset_tar}" -T "${work_dir}/dataset_expected"
COPYFILE_DISABLE=1 tar -czf "${dist_dir}/${sources_tar}" -T "${work_dir}/sources_expected"

# 5. Check the built tarballs themselves, so a file that changed after step 3
#    cannot end up in a release that disagrees with the manifests.
echo "Verifying built tarballs"
for pair in "${dataset_tar}:${DATASET_SUMS}" "${sources_tar}:${SOURCES_SUMS}"; do
    tarball="${dist_dir}/${pair%%:*}"
    manifest="${REPO_ROOT}/${pair#*:}"
    check_tarball_members "${tarball}" "${manifest}"
    rm -rf "${work_dir}/extract"
    mkdir -p "${work_dir}/extract"
    tar -xzf "${tarball}" -C "${work_dir}/extract"
    (cd "${work_dir}/extract" && sha256_tool -c --quiet "${manifest}")
done
rm -rf "${work_dir}/extract"

cp "${DATASET_SUMS}" "${dist_dir}/atlaspack.sha256"
cp "${SOURCES_SUMS}" "${dist_dir}/sources.sha256"
(
    cd "${dist_dir}"
    sha256_tool "${dataset_tar}" "${sources_tar}" atlaspack.sha256 sources.sha256 \
        | sed -E 's/^([0-9a-f]+) [ *]/\1  /' > SHA256SUMS
)

echo "Built release assets in ${dist_dir}:"
ls -l "${dist_dir}"

if [ "${upload}" -eq 0 ]; then
    exit 0
fi

# 6. Create the draft release on the current commit.
if ! git merge-base --is-ancestor "${commit}" "origin/main" 2> /dev/null; then
    echo "Warning: ${commit} is not on origin/main." >&2
fi

gh release create "${version}" \
    --repo "${GITHUB_REPO}" \
    --draft \
    --target "${commit}" \
    --title "AtlasPack ${version}" \
    --notes "$(
        cat << EOF
Atlas data for AtlasPack ${version} (commit ${commit}).

- \`${dataset_tar}\`: the BIDS-Atlas dataset (extracts to \`AtlasPack/\`).
- \`${sources_tar}\`: inputs and intermediates for regenerating the atlases.
- \`SHA256SUMS\`: checksums of the assets above.

\`\`\`bash
curl -fsSLO https://github.com/${GITHUB_REPO}/releases/download/${version}/${dataset_tar}
tar -xzf ${dataset_tar}
\`\`\`
EOF
    )" \
    "${dist_dir}/${dataset_tar}" \
    "${dist_dir}/${sources_tar}" \
    "${dist_dir}/atlaspack.sha256" \
    "${dist_dir}/sources.sha256" \
    "${dist_dir}/SHA256SUMS"

echo "Draft release ${version} created. Review and publish it on GitHub."
