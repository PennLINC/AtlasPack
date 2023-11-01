# This is an example script to show how NIFTI-to-CIFTI conversion is done.
# Written by Eric Feczko.
subcort_nii="tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-02_desc-Schaefer2018v0143100Parcels_dseg.nii.gz"
subcort_labels="tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-02_desc-Schaefer2018v0143100Parcels_labellist.txt"
subcort_niilabel="nifti_labels_file.nii.gz"
subcort_niilabel_flipped="nifti_labels_file_flipped.nii.gz"
cifti_91k="Tian_Subcortex_S3_3T_32k.dlabel.nii"
subcort_cifti="nifti_to_cifti_dseg.dlabel.nii"
structure_labelfile="Atlas_ROIs.2.nii.gz"

# Create the nifti label file from the nifti and labellist
wb_command -volume-label-import $subcort_nii $subcort_labels $subcort_niilabel
# Explicitly set the sform of the nifti label file.
# There was a mismatch between the dseg file and the atlas ROIs, in the x direction.
cp $subcort_niilabel $subcort_niilabel_flipped
fslorient -setsform -2 0 0 90 0 2 0 -126 0 0 2 -72 0 0 0 1 $subcort_niilabel_flipped
# Create the dseg file.
# The structure label file indicates the CIFTI label
# (e.g., CORTEX_LEFT, CORTEX_RIGHT) for each voxel.
# I downloaded ours from https://github.com/DCAN-Labs/DCAN-HCP/blob/\
# 92913242419d492aee733a45d454ea319fbaac35/global/templates/standard_mesh_atlases/Atlas_ROIs.2.nii.gz.
# It should match the MNI152NLin6Asym 2 mm3 template.
wb_command -cifti-create-label $subcort_cifti -volume $subcort_niilabel_flipped $structure_labelfile
