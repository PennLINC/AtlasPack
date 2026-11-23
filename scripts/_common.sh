# Shared settings and helpers for the AtlasPack data scripts.
# Source this file; do not run it directly.

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GITHUB_REPO="PennLINC/AtlasPack"

# The released BIDS-Atlas dataset (tracked text files plus untracked images).
DATASET_DIR="AtlasPack"

# Checksum manifests, tracked in git. Paths inside are relative to REPO_ROOT.
DATASET_SUMS="checksums/atlaspack.sha256"
SOURCES_SUMS="checksums/sources.sha256"

# Large inputs and intermediates for regenerating the atlases.
# These are released as a separate asset and are not tracked in git.
SOURCE_GLOBS=(
    "transforms/*.h5"
    "Schaefer/*.nii.gz"
    "Schaefer/*.label.gii"
    "subcortical_merged/*.nii.gz"
    "subcortex_merged/*.nii.gz"
)

dataset_asset() { printf 'atlaspack-%s.tar.gz' "$1"; }
sources_asset() { printf 'atlaspack-sources-%s.tar.gz' "$1"; }

if command -v sha256sum > /dev/null 2>&1; then
    sha256_tool() { sha256sum "$@"; }
else
    sha256_tool() { shasum -a 256 "$@"; }
fi

# List the regeneration source files present on disk, relative to REPO_ROOT.
list_source_files() {
    (
        cd "${REPO_ROOT}"
        shopt -s nullglob
        for pattern in "${SOURCE_GLOBS[@]}"; do
            for f in ${pattern}; do
                printf '%s\n' "${f}"
            done
        done
    ) | LC_ALL=C sort
}

# List every file in the dataset directory, relative to REPO_ROOT.
list_dataset_files() {
    (
        cd "${REPO_ROOT}"
        find "${DATASET_DIR}" -type f ! -name '._*' ! -name '.DS_Store'
    ) | LC_ALL=C sort
}

# Print the sorted paths listed in a checksum manifest.
manifest_paths() {
    sed -E 's/^[0-9a-f]{64} [ *]//' "$1" | LC_ALL=C sort
}

# Fail unless a version is a plain tag name (e.g. 0.2.0 or 1.0.0rc1), so it
# is safe to use in paths and URLs.
validate_version() {
    if ! printf '%s' "$1" | grep -Eq '^[0-9A-Za-z][0-9A-Za-z._+-]*$' \
        || printf '%s' "$1" | grep -q '\.\.'; then
        echo "Invalid version '$1': use a tag name like 0.2.0" >&2
        exit 1
    fi
}

# Fail unless two sorted path lists (given as files) are identical,
# printing the differences.
require_same_paths() {
    local label="$1" expected="$2" actual="$3"
    if ! diff "${expected}" "${actual}" > /dev/null; then
        echo "${label}: file set does not match the manifest" >&2
        diff "${expected}" "${actual}" | grep '^[<>]' | sed 's/^</  missing:/; s/^>/  unexpected:/' >&2
        exit 1
    fi
}

# Fail unless a tarball holds only regular files whose paths are exactly
# the paths in the manifest. Run this before extracting anything.
check_tarball_members() {
    local tarball="$1" manifest="$2" tmp
    tmp="$(mktemp -d)"
    manifest_paths "${manifest}" > "${tmp}/expected"
    tar -tzf "${tarball}" | LC_ALL=C sort > "${tmp}/actual"
    # In verbose listings the first character is the entry type ("-" = file).
    tar -tvzf "${tarball}" > "${tmp}/verbose"
    if grep -v '^-' "${tmp}/verbose" > /dev/null; then
        echo "$(basename "${tarball}"): contains entries that are not regular files" >&2
        rm -rf "${tmp}"
        exit 1
    fi

    (require_same_paths "$(basename "${tarball}")" "${tmp}/expected" "${tmp}/actual") || {
        rm -rf "${tmp}"
        exit 1
    }
    rm -rf "${tmp}"
}
