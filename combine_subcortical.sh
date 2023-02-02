datalad run \
  --explicit \
  --expand outputs \
  -m "Download and combine some atlases" \
  -i "transforms/tpl-MNI152NLin2009cAsym_from-MNI152NLin2009aSym_mode-image_xfm.h5" \
  -i "transforms/tpl-MNI152NLin6Asym_from-MNI152NLin2009aSym_mode-image_xfm.h5" \
  -i "transforms/tpl-MNI152NLin6Asym_from-MNI152NLin2009cAsym_mode-image_xfm.h5" \
  -i "transforms/tpl-MNI152NLin6Asym_from-MNI152NLin6Sym_mode-image_xfm.h5" \
  -i "JointAtlas.ipynb" \
  -o "tpl-MNI152NLin2009cAsym_atlas-SubcorticalMerged_res-01_dseg.nii.gz" \
  -o "tpl-MNI152NLin2009cAsym_atlas-SubcorticalMerged_res-01_dseg.tsv" \
  -o "tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-01_dseg.nii.gz" \
  -o "tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-01_dseg.tsv" \
  -o "schaefer_map/*_dseg.nii.gz" \
  -o "schaefer_map/*_dseg.tsv" \
  "jupyter run JointAtlas.ipynb"


