datalad run \
  --explicit \
  --expand both \
  -m "add merged subcortical atlas to Schaefer parcellations" \
  -i "subcortical_merged/tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-01_dseg.nii.gz" \
  -i "subcortical_merged/tpl-MNI152NLin2009cAsym_atlas-SubcorticalMerged_res-01_dseg.nii.gz" \
  -i "subcortical_merged/tpl-MNI152NLin2009cAsym_atlas-SubcorticalMerged_res-01_dseg.tsv" \
  -i "Schaefer/tpl-MNI152NLin6Asym_atlas-Schaefer2018v0143_res-01_desc-*dseg.nii.gz" \
  -i "Schaefer/tpl-MNI152NLin2009cAsym_atlas-Schaefer2018v0143_res-01_desc-*dseg.nii.gz" \
  -i "Schaefer/atlas-Schaefer2018v0143_desc-*ParcelsAllNetworks_dseg.tsv" \
  -i "atlas-4S*Parcels_dseg.tsv" \
  -o "tpl-MNI152NLin*_atlas-4S*Parcels_res-01_dseg.nii.gz" \
  -o "volumetric4S.html" \
  "jupyter nbconvert --to html --execute Volumetric4S.ipynb"
