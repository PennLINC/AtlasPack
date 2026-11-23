#!/usr/bin/env bash
# Combine the subcortical atlases and build the 4S CIFTI atlases.
#
# Inputs (fetch with `scripts/fetch_data.sh --sources <version>`):
#   transforms/*.h5, Schaefer/Atlas_ROIs.2.nii.gz, Schaefer/tpl-fsLR_hemi-*
# Outputs are written to the repository root and to Schaefer/,
# subcortical_merged/, and subcortex_merged/.
set -euo pipefail

cd "$(dirname "$0")"

for f in \
    transforms/tpl-MNI152NLin2009cAsym_from-MNI152NLin2009aSym_mode-image_xfm.h5 \
    transforms/tpl-MNI152NLin6Asym_from-MNI152NLin2009aSym_mode-image_xfm.h5 \
    transforms/tpl-MNI152NLin6Asym_from-MNI152NLin2009cAsym_mode-image_xfm.h5 \
    transforms/tpl-MNI152NLin6Asym_from-MNI152NLin6Sym_mode-image_xfm.h5 \
    Schaefer/Atlas_ROIs.2.nii.gz; do
    if [ ! -f "${f}" ]; then
        echo "Missing input ${f}. Run: scripts/fetch_data.sh --sources <version>" >&2
        exit 1
    fi
done

jupyter nbconvert --to html --execute JointAtlas.ipynb
