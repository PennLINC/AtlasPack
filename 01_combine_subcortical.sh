datalad run \
  --explicit \
  --expand both \
  -m "Download and combine some atlases" \
  -i "transforms/tpl-MNI152NLin2009cAsym_from-MNI152NLin2009aSym_mode-image_xfm.h5" \
  -i "transforms/tpl-MNI152NLin6Asym_from-MNI152NLin2009aSym_mode-image_xfm.h5" \
  -i "transforms/tpl-MNI152NLin6Asym_from-MNI152NLin2009cAsym_mode-image_xfm.h5" \
  -i "transforms/tpl-MNI152NLin6Asym_from-MNI152NLin6Sym_mode-image_xfm.h5" \
  -i "JointAtlas.ipynb" \
  -i "Schaefer/Atlas_ROIs.2.nii.gz" \
  -i "Schaefer/tpl-fsLR_hemi-*" \
  -o "JointAtlas.ipynb" \
  -o "tpl-MNI152NLin2009cAsym_atlas-SubcorticalMerged_res-01_dseg.nii.gz" \
  -o "tpl-MNI152NLin2009cAsym_atlas-SubcorticalMerged_res-01_dseg.tsv" \
  -o "tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-01_dseg.nii.gz" \
  -o "tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-01_dseg.tsv" \
  -o "Schaefer/*_dseg.nii.gz" \
  -o "Schaefer/*_dseg.tsv" \
  -o "Schaefer/tpl-fsLR_hemi-*" \
  "jupyter nbconvert --to html --execute JointAtlas.ipynb"
