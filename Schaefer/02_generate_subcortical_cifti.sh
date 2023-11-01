#!/bin/bash
# The NIFTI-to-CIFTI procedure was figured out by Eric Feczko.
# The reorientation step in 02_prepare_atlas.py was part of Feczko's solution,
# though he used fslorient instead of nibabel.
structure_labelfile="Atlas_ROIs.2.nii.gz"

for order in 100 200 300 400 500 600 700 800 900 1000
do
    echo $order

    # There are 56 subcortical parcels
    n_parcels=$((order + 56))

    # First, we remove a bunch of vertices from the Schaefer atlases
    # Split the Schaefer into right and left hemispheres
    schaefer_cifti_32k="tpl-fsLR_atlas-Schaefer2018v0143_den-32k_desc-${order}ParcelsAllNetworks_dseg.dlabel.nii"
    schaefer_lh="tpl-fsLR_atlas-Schaefer2018v0143_den-32k_hemi-L_desc-${order}ParcelsAllNetworks_dseg.label.gii"
    schaefer_rh="tpl-fsLR_atlas-Schaefer2018v0143_den-32k_hemi-R_desc-${order}ParcelsAllNetworks_dseg.label.gii"
    wb_command -cifti-separate $schaefer_cifti_32k COLUMN \
        -label CORTEX_LEFT $schaefer_lh \
        -label CORTEX_RIGHT $schaefer_rh

    # Run wb_command -volume-label-import <input> <label-list-file> <output> -discard-others
    echo "    Converting NIFTI atlas to NIFTI label file."
    subcort_nii="tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-02_desc-Schaefer2018v0143x${order}Parcels_dseg.nii.gz"
    subcort_labels="tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-02_desc-Schaefer2018v0143x${order}Parcels_labellist.txt"
    subcort_niilabel="tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-02_desc-Schaefer2018v0143x${order}ParcelsLabels_dseg.nii.gz"
    wb_command -volume-label-import $subcort_nii $subcort_labels $subcort_niilabel

    # Combine the NIFTI file, Schaefer left hemisphere, and Schaefer right hemisphere into a CIFTI
    # The structure label file indicates the CIFTI label
    # (e.g., CORTEX_LEFT, CORTEX_RIGHT) for each voxel.
    # I downloaded ours from https://github.com/DCAN-Labs/DCAN-HCP/blob/\
    # 92913242419d492aee733a45d454ea319fbaac35/global/templates/standard_mesh_atlases/Atlas_ROIs.2.nii.gz.
    # It should match the MNI152NLin6Asym 2 mm3 template.
    echo "    Converting NIFTI label file to CIFTI"
    lh_template="tpl-fsLR_hemi-L_den-32k_desc-nomedialwall_dparc.label.gii"
    rh_template="tpl-fsLR_hemi-R_den-32k_desc-nomedialwall_dparc.label.gii"
    merged_cifti="../tpl-fsLR_atlas-4S${n_parcels}Parcels_den-91k_dseg.dlabel.nii"
    wb_command -cifti-create-label $merged_cifti \
        -volume $subcort_niilabel $structure_labelfile \
        -left-label $schaefer_lh -roi-left $lh_template \
        -right-label $schaefer_rh -roi-right $rh_template
done
