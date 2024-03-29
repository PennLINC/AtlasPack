#!/bin/bash

# Downloads and splits the CIT168 atlas. Atlas is described in
# A high-resolutionprobabilistic in vivo atlas of humansubcortical brain nuclei
# In Scientific Data by Wolfgang M. Pauli, Amanda N. Nili & J. Michael Tyszka

# It does not break up regions
# by hemisphere, so we do that and make a new look-up table

# download the lookup table
wget 'https://osf.io/download/6qrcb'
mv 6qrcb labels.txt

# download in NLin6: convert it to RAS+ to match templateflow
wget 'https://osf.io/download/2qswg'
mv 2qswg tpl-MNI152NLin6Asym_atlas-CIT168_res-01_desc-LAS_dseg.nii.gz
3dresample \
    -orient LPI \
    -inset tpl-MNI152NLin6Asym_atlas-CIT168_res-01_desc-LAS_dseg.nii.gz \
    -prefix tpl-MNI152NLin6Asym_atlas-CIT168_res-01_desc-RAS_dseg.nii.gz

# download in 2009cAsym: This one is already in RAS+
wget 'https://osf.io/download/vak6p'
mv vak6p tpl-MNI152NLin2009cAsym_atlas-CIT168_res-01_desc-RAS_dseg.nii.gz

python split_up_cit168.py \
    tpl-MNI152NLin6Asym_atlas-CIT168_res-01_desc-RAS_dseg.nii.gz \
    tpl-MNI152NLin6Asym_atlas-CIT168_res-01_desc-LRSplit_dseg

python split_up_cit168.py \
    tpl-MNI152NLin2009cAsym_atlas-CIT168_res-01_desc-RAS_dseg.nii.gz \
    tpl-MNI152NLin2009cAsym_atlas-CIT168_res-01_desc-LRSplit_dseg

# They're the same so make one that covers both
cp tpl-MNI152NLin2009cAsym_atlas-CIT168_res-01_desc-LRSplit_dseg.tsv atl-CIT168.tsv