#!/bin/bash

# Download and transform the MDTB atlas from
# King, M., Hernandez-Castillo, C.R., Poldrack, R.R., Ivry, R., and Diedrichsen, J. (2019).
# Functional Boundaries in the Human Cerebellum revealed by a Multi-Domain Task Battery. Nat. Neurosci.

# Get the atlas description
wget https://github.com/DiedrichsenLab/cerebellar_atlases/raw/master/King_2019/atlas_description.json

# Get the labels (already in TSV!!)
wget https://github.com/DiedrichsenLab/cerebellar_atlases/raw/master/King_2019/atl-MDTB10.tsv

# Get the actual atlas
wget https://github.com/DiedrichsenLab/cerebellar_atlases/raw/master/King_2019/atl-MDTB10_space-MNI_dseg.nii

# This is in a strange volume, but in coordinate space it's
# "..._space-MNI.nii: volume file aligned to FNIRT MNI space", which is NLin6Asym.

# Resample it into the official TemplateFlow volume
# To NLin6Asym (no transform)
antsApplyTransforms \
    -d 3 \
    -i atl-MDTB10_space-MNI_dseg.nii \
    -o tpl-MNI152NLin6Asym_atlas-MDTB10_res-01_dseg.nii.gz  \
    -r ${TEMPLATEFLOW_HOME}/tpl-MNI152NLin6Asym/tpl-MNI152NLin6Asym_res-01_desc-brain_mask.nii.gz \
    --interpolation GenericLabel \
    -v 1

# To 2009cAsym
antsApplyTransforms \
    -d 3 \
    -i atl-MDTB10_space-MNI_dseg.nii \
    -o tpl-MNI152NLin2009cAsym_atlas-MDTB10_res-01_dseg.nii.gz  \
    -t ${TEMPLATEFLOW_HOME}/tpl-MNI152NLin2009cAsym/tpl-MNI152NLin2009cAsym_from-MNI152NLin6Asym_mode-image_xfm.h5 \
    -r ${TEMPLATEFLOW_HOME}/tpl-MNI152NLin2009cAsym/tpl-MNI152NLin2009cAsym_res-01_desc-brain_mask.nii.gz \
    --interpolation GenericLabel \
    -v 1

