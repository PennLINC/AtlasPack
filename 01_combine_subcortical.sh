datalad run \
  --explicit \
  --expand outputs \
  -m "Download and combine some atlases" \
  -i "transforms/tpl-MNI152NLin2009cAsym_from-MNI152NLin2009aSym_mode-image_xfm.h5" \
  -i "transforms/tpl-MNI152NLin6Asym_from-MNI152NLin2009aSym_mode-image_xfm.h5" \
  -i "transforms/tpl-MNI152NLin6Asym_from-MNI152NLin2009cAsym_mode-image_xfm.h5" \
  -i "transforms/tpl-MNI152NLin6Asym_from-MNI152NLin6Sym_mode-image_xfm.h5" \
  -i "JointAtlas.ipynb" \
  -o "JointAtlas.ipynb" \
  -o "tpl-MNI152NLin2009cAsym_atlas-SubcorticalMerged_res-01_dseg.nii.gz" \
  -o "tpl-MNI152NLin2009cAsym_atlas-SubcorticalMerged_res-01_dseg.tsv" \
  -o "tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-01_dseg.nii.gz" \
  -o "tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-01_dseg.tsv" \
  -o "Schaefer/*_dseg.nii.gz" \
  -o "Schaefer/*_dseg.tsv" \
  "jupyter nbconvert --to notebook --execute --allow-errors JointAtlas.ipynb"
