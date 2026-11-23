#!/usr/bin/env bash
# Add the merged subcortical atlas to the volumetric Schaefer parcellations.
#
# Run 01_combine_subcortical.sh first; this script reads its outputs
# (subcortical_merged/*, Schaefer/*_dseg.nii.gz, atlas-4S*Parcels_dseg.tsv)
# and writes tpl-MNI152NLin*_atlas-4S*Parcels_res-01_dseg.nii.gz to the
# repository root.
#
# The released BIDS-Atlas dataset lives in AtlasPack/. After regenerating,
# copy changed images into AtlasPack/tpl-<space>/ under their BIDS names,
# then run scripts/update_checksums.sh and commit the manifest changes.
set -euo pipefail

cd "$(dirname "$0")"

jupyter nbconvert --to html --execute Volumetric4S.ipynb
