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

cd "${REPO_ROOT}"
# ATLASPACK_BASE_URL overrides the download location (e.g. a mirror, or a
# file:// URL pointing at dist/<version> to test a release before uploading).
base_url="${ATLASPACK_BASE_URL:-https://github.com/${GITHUB_REPO}/releases/download/${version}}"
work_dir="$(mktemp -d)"
trap 'rm -rf "${work_dir}"' EXIT

curl -fsSL -o "${work_dir}/SHA256SUMS" "${base_url}/SHA256SUMS"

fetch_and_extract() {
    local asset="$1"
    echo "Downloading ${asset}"
    curl -fSL --retry 3 -o "${work_dir}/${asset}" "${base_url}/${asset}"
    (cd "${work_dir}" && grep " ${asset}\$" SHA256SUMS | sha256_tool -c -)
    tar -xzf "${work_dir}/${asset}" -C "${REPO_ROOT}"
}

fetch_and_extract "$(dataset_asset "${version}")"
sha256_tool -c --quiet "${DATASET_SUMS}"
echo "Verified ${DATASET_DIR}/ against ${DATASET_SUMS}"

if [ "${with_sources}" -eq 1 ]; then
    fetch_and_extract "$(sources_asset "${version}")"
    sha256_tool -c --quiet "${SOURCES_SUMS}"
    echo "Verified regeneration sources against ${SOURCES_SUMS}"
fi
