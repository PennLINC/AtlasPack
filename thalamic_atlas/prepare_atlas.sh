#!/bin/bash

# Downloads, transforms, and standardizes the Thalamic atlas from
# E. Najdenovska*, Y. Aléman-Gómez*, G. Battistella, M. Descoteaux, P. Hagmann,
# S. Jacquemont, P. Maeder, J.-P. Thiran, E. Fornari and M. Bach Cuadra, Sci.
# Data. 5:180270 doi: 10.1038/sdata.2018.270 (2018). *Equally contributed
# authors.

# download the 3d image
wget 'https://zenodo.org/record/1405484/files/Thalamus_Nuclei-HCP-MaxProb.nii.gz'
# download the lookup table
wget 'https://zenodo.org/record/1405484/files/Thalamic_Nuclei-ColorLUT.txt'

# This atlas is in MNI152NLin2009aSym. We want it in 2009cAsym and NLin6

# To NLin6Asym
antsApplyTransforms \
    -d 3 \
    -i Thalamus_Nuclei-HCP-MaxProb.nii.gz \
    -o tpl-MNI152NLin6Asym_atlas-hcpthalamic_res-01_dseg.nii.gz  \
    -t ../transforms/tpl-MNI152NLin6Asym_from-MNI152NLin2009aSym_mode-image_xfm.h5 \
    -r ${TEMPLATEFLOW_HOME}/tpl-MNI152NLin6Asym/tpl-MNI152NLin6Asym_res-01_desc-brain_mask.nii.gz \
    --interpolation GenericLabel \
    -v 1

# To 2009cAsym
antsApplyTransforms \
    -d 3 \
    -i Thalamus_Nuclei-HCP-MaxProb.nii.gz \
    -o tpl-MNI152NLin2009cAsym_atlas-hcpthalamic_res-01_dseg.nii.gz  \
    -t ../transforms/tpl-MNI152NLin2009cAsym_from-MNI152NLin2009aSym_mode-image_xfm.h5 \
    -r ${TEMPLATEFLOW_HOME}/tpl-MNI152NLin2009cAsym/tpl-MNI152NLin2009cAsym_res-01_desc-brain_mask.nii.gz \
    --interpolation GenericLabel \
    -v 1

python make_labels_tsv.py