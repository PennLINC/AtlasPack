#!/bin/bash

# Download the lookup table.
wget https://raw.githubusercontent.com/PennLINC/xcp_d/8a07b53b8a1bb921cd8ca3dc2d23fd09da7982fd/xcp_d/data/atlases/atlas-HCP_dseg.tsv

# Download the 1.6 mm atlas.
wget https://github.com/Washington-University/HCPpipelines/raw/master/global/templates/170494_Greyordinates/Atlas_ROIs.1.60.nii.gz
mv Atlas_ROIs.1.60.nii.gz tpl-MNI152NLin6Asym_atlas-HCP_res-06_dseg.nii.gz

# Separate out the hippocampus and amygdala from the atlas.
python split_regions.py

# Resample to 1 mm in MNI152NLin6Asym (no transform).
antsApplyTransforms \
    -d 3 \
    -i tpl-MNI152NLin6Asym_atlas-HPandAMYG_res-06_dseg.nii.gz \
    -o tpl-MNI152NLin6Asym_atlas-HPandAMYG_res-01_dseg.nii.gz  \
    -r ${TEMPLATEFLOW_HOME}/tpl-MNI152NLin6Asym/tpl-MNI152NLin6Asym_res-01_desc-brain_mask.nii.gz \
    --interpolation GenericLabel \
    -v 1

# Warp to MNI152NLin2009cAsym at 1 mm resolution.
antsApplyTransforms \
    -d 3 \
    -i tpl-MNI152NLin6Asym_atlas-HPandAMYG_res-06_dseg.nii.gz \
    -o tpl-MNI152NLin2009cAsym_atlas-HPandAMYG_res-01_dseg.nii.gz  \
    -t ${TEMPLATEFLOW_HOME}/tpl-MNI152NLin2009cAsym/tpl-MNI152NLin2009cAsym_from-MNI152NLin6Asym_mode-image_xfm.h5 \
    -r ${TEMPLATEFLOW_HOME}/tpl-MNI152NLin2009cAsym/tpl-MNI152NLin2009cAsym_res-01_desc-brain_mask.nii.gz \
    --interpolation GenericLabel \
    -v 1
