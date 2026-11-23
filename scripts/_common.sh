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
