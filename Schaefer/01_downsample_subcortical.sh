#!/bin/bash

# Downsample 1 mm3 subcortical atlas to 2 mm3
antsApplyTransforms \
    -d 3 \
    -i ../subcortical_merged/tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-01_dseg.nii.gz \
    -o ../subcortical_merged/tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-02_dseg.nii.gz \
    -r ${TEMPLATEFLOW_HOME}/tpl-MNI152NLin6Asym/tpl-MNI152NLin6Asym_res-02_desc-brain_mask.nii.gz \
    --interpolation GenericLabel \
    -v 1
