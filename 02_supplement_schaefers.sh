datalad run \
  --explicit \
  --expand both \
  -m "add merged subcortical atlas to Schaefer parcellations" \
  -i "tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-01_dseg.nii.gz" \
  -i "tpl-MNI152NLin2009cAsym_atlas-SubcorticalMerged_res-01_dseg.nii.gz" \
  -i "tpl-MNI152NLin2009cAsym_atlas-SubcorticalMerged_res-01_dseg.tsv" \
  -i "Schaefer/tpl-MNI152NLin6Asym_atlas-Schaefer2018v0143_res-01_desc-*dseg.nii.gz" \
  -i "Schaefer/tpl-MNI152NLin2009cAsym_atlas-Schaefer2018v0143_res-01_desc-*dseg.nii.gz" \
  -i "Schaefer/atlas-Schaefer2018v0143_desc-*ParcelsAllNetworks_dseg.tsv" \
  -i "atlas-4S*Parcels_dseg.tsv" \
  -o "tpl-MNI152NLin*_atlas-4S*Parcels_res-01_dseg.nii.gz" \
  "jupyter nbconvert --to notebook --execute --allow-errors Volumetric4S.ipynb"


