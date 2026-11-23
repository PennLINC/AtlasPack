#!/usr/bin/env bash
# Rewrite the checksum manifests in checksums/ from the files on disk.
#
# Run this after regenerating or editing any atlas file, and commit the result.
# The manifests are what tie a git commit to the exact released data.
#
# Usage: scripts/update_checksums.sh
set -euo pipefail

source "$(dirname "$0")/_common.sh"
cd "${REPO_ROOT}"
mkdir -p checksums

# Write "<hash>  <path>" lines. Some sha256sum builds (e.g. Git Bash) mark
# binary mode with "*"; strip it so manifests are identical on every platform.
hash_list() {
    while IFS= read -r f; do
        sha256_tool "${f}"
    done | sed -E 's/^([0-9a-f]+) [ *]/\1  /'
}

dataset_files="$(list_dataset_files)"
if [ -z "${dataset_files}" ]; then
    echo "No files found in ${DATASET_DIR}/" >&2
    exit 1
fi

printf '%s\n' "${dataset_files}" | hash_list > "${DATASET_SUMS}"
echo "Wrote ${DATASET_SUMS} ($(wc -l < "${DATASET_SUMS}" | tr -d ' ') files)"

source_files="$(list_source_files)"
if [ -n "${source_files}" ]; then
    printf '%s\n' "${source_files}" | hash_list > "${SOURCES_SUMS}"
    echo "Wrote ${SOURCES_SUMS} ($(wc -l < "${SOURCES_SUMS}" | tr -d ' ') files)"
else
    echo "No source files on disk; leaving ${SOURCES_SUMS} unchanged"
fi
