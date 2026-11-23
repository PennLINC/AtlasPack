#!/usr/bin/env bash
# Download the atlas images (and optionally the regeneration sources) for a
# release into this repository clone, then verify every file against the
# checksum manifests tracked in git.
#
# Usage: scripts/fetch_data.sh [--sources] <version>
#   <version>   a release tag, e.g. 0.2.0. Check out the matching tag first so
#               the checksum manifests match the release.
#   --sources   also download the large regeneration inputs (~730 MB).
#
# Requires: curl, tar, and sha256sum or shasum.
set -euo pipefail

source "$(dirname "$0")/_common.sh"

with_sources=0
version=""
for arg in "$@"; do
    case "${arg}" in
        --sources) with_sources=1 ;;
        -h | --help)
            sed -n '2,12p' "$0"
            exit 0
            ;;
        *) version="${arg}" ;;
    esac
done

if [ -z "${version}" ]; then
    echo "Usage: $0 [--sources] <version>" >&2
    exit 1
fi

validate_version "${version}"
cd "${REPO_ROOT}"

# ATLASPACK_BASE_URL overrides the download location (e.g. a mirror, or a
# file:// URL pointing at dist/<version> to test a release before uploading).
base_url="${ATLASPACK_BASE_URL:-https://github.com/${GITHUB_REPO}/releases/download/${version}}"
work_dir="$(mktemp -d)"
trap 'rm -rf "${work_dir}"' EXIT

curl -fsSL -o "${work_dir}/SHA256SUMS" "${base_url}/SHA256SUMS"

# Download an asset, check it against the release SHA256SUMS, and extract it
# only if it contains exactly the files listed in the git-tracked manifest.
# (SHA256SUMS comes from the same place as the asset, so the manifest check is
# what keeps a bad archive from writing anywhere else in the repository.)
fetch_and_extract() {
    local asset="$1" manifest="$2"
    echo "Downloading ${asset}"
    curl -fSL --retry 3 -o "${work_dir}/${asset}" "${base_url}/${asset}"
    (cd "${work_dir}" && grep -E "^[0-9a-f]+ [ *]${asset//./\\.}\$" SHA256SUMS | sha256_tool -c -)
    check_tarball_members "${work_dir}/${asset}" "${manifest}"
    tar -xzf "${work_dir}/${asset}" -C "${REPO_ROOT}"
    sha256_tool -c --quiet "${manifest}"
}

fetch_and_extract "$(dataset_asset "${version}")" "${DATASET_SUMS}"
manifest_paths "${DATASET_SUMS}" > "${work_dir}/expected"
list_dataset_files > "${work_dir}/actual"
require_same_paths "${DATASET_DIR}/" "${work_dir}/expected" "${work_dir}/actual"
echo "Verified ${DATASET_DIR}/ against ${DATASET_SUMS}"

if [ "${with_sources}" -eq 1 ]; then
    fetch_and_extract "$(sources_asset "${version}")" "${SOURCES_SUMS}"
    manifest_paths "${SOURCES_SUMS}" > "${work_dir}/expected"
    list_source_files > "${work_dir}/actual"
    require_same_paths "Regeneration sources" "${work_dir}/expected" "${work_dir}/actual"
    echo "Verified regeneration sources against ${SOURCES_SUMS}"
fi
