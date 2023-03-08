#!/bin/bash
# The NIFTI-to-CIFTI procedure was figured out by Eric Feczko.
# The reorientation step in 02_prepare_atlas.py was part of Feczko's solution,
# though he used fslorient instead of nibabel.
structure_labelfile="Atlas_ROIs.2.nii.gz"

for order in 100 200 300 400 500 600 700 800 900 1000
do
    echo $order
    # There are 52 subcortical parcels
    n_parcels=$((order + 52))

    # Select the appropriate subcortical file and labels file
    subcort_nii="tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-02_desc-Schaefer2018v0143${order}Parcels_dseg.nii.gz"
    subcort_nii_resampled="tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-02_desc-Schaefer2018v0143${order}ParcelsResampled_dseg.nii.gz"
    subcort_labels="tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-02_desc-Schaefer2018v0143${order}Parcels_labellist.txt"
    subcort_niilabel="tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-02_desc-Schaefer2018v0143${order}ParcelsLabels_dseg.nii.gz"
    subcort_cifti="tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_desc-Schaefer2018v0143${order}Parcels_dseg.dlabel.nii"

    # Select the appropriate Schaefer file
    schaefer_cifti="tpl-fsLR_atlas-Schaefer2018v0143_den-32k_desc-${order}ParcelsAllNetworks_dseg.dlabel.nii"

    # Set the output file
    merged_cifti="../tpl-fsLR_atlas-4S${n_parcels}Parcels_den-91k_dseg.dlabel.nii"

    # Run wb_command -volume-label-import <input> <label-list-file> <output> -discard-others
    echo "    Converting NIFTI atlas to NIFTI label file."
    wb_command -volume-label-import $subcort_nii $subcort_labels $subcort_niilabel

    # Convert the NIFTI file to CIFTI
    # The structure label file indicates the CIFTI label
    # (e.g., CORTEX_LEFT, CORTEX_RIGHT) for each voxel.
    # I downloaded ours from https://github.com/DCAN-Labs/DCAN-HCP/blob/\
    # 92913242419d492aee733a45d454ea319fbaac35/global/templates/standard_mesh_atlases/Atlas_ROIs.2.nii.gz.
    # It should match the MNI152NLin6Asym 2 mm3 template.
    echo "    Converting NIFTI label file to CIFTI"
    wb_command -cifti-create-label $subcort_cifti -volume $subcort_niilabel $structure_labelfile

    # Run wb_command -cifti-merge <cifti-out> -cifti <subcortical-cifti> -cifti <schaefer>
    echo "    Merging atlases"
    wb_command -cifti-merge-dense COLUMN $merged_cifti -cifti $subcort_cifti -cifti $schaefer_cifti
done
