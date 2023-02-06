#!/bin/bash

# Get the schaefer atlases from the 2019 update.
python schaefer_ordering_mapper.py

for order in 100 200 300 400 500 600 700 800 900 1000
do
    original=Schaefer2018_${order}Parcels_7Networks_order_FSLMNI152_1mm.nii.gz
    # Resample it into the official TemplateFlow volume
    # To NLin6Asym (no transform)
    antsApplyTransforms \
        -d 3 \
        -i ${original} \
        -o tpl-MNI152NLin6Asym_res-01_atlas-Schaefer2018v0143_desc-${order}ParcelsAllNetworks_dseg.nii.gz  \
        -r ${TEMPLATEFLOW_HOME}/tpl-MNI152NLin6Asym/tpl-MNI152NLin6Asym_res-01_desc-brain_mask.nii.gz \
        --interpolation GenericLabel \
        -v 1

    # To 2009cAsym
    antsApplyTransforms \
        -d 3 \
        -i ${original} \
        -o tpl-MNI152NLin2009cAsym_res-01_atlas-Schaefer2018v0143_desc-${order}ParcelsAllNetworks_dseg.nii.gz  \
        -t ${TEMPLATEFLOW_HOME}/tpl-MNI152NLin2009cAsym/tpl-MNI152NLin2009cAsym_from-MNI152NLin6Asym_mode-image_xfm.h5 \
        -r ${TEMPLATEFLOW_HOME}/tpl-MNI152NLin2009cAsym/tpl-MNI152NLin2009cAsym_res-01_desc-brain_mask.nii.gz \
        --interpolation GenericLabel \
        -v 1
done
