for order in 100 200 300 400 500 600 700 800 900 1000
do
    echo $order
    # Select the appropriate subcortical file and labels file
    subcort_nii="tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-01_desc-Schaefer2018v0143{$order}Parcels_dseg.nii.gz"
    subcort_labels="tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-01_desc-Schaefer2018v0143{$order}Parcels_labellist.txt"
    subcort_niilabel="tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-01_desc-Schaefer2018v0143{$order}ParcelsLabels_dseg.nii.gz"
    subcort_cifti="tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-01_desc-Schaefer2018v0143{$order}Parcels_dseg.dlabel.nii"

    # Select the appropriate Schaefer file
    schaefer_cifti="tpl-fsLR_atlas-Schaefer2018v0143_den-32k_desc-{$order}ParcelsAllNetworks_dseg.dlabel.nii"

    # Set the output file
    merged_cifti="../tpl-fsLR_atlas-Merged_den-91k_desc-{$order}ParcelsAllNetworks_dseg.dlabel.nii"

    # Run wb_command -volume-label-import <input> <label-list-file> <output> -discard-others
    wb_command -volume-label-import $subcort_nii $subcort_labels $subcort_niilabel -discard-others

    # Run wb_command -cifti-convert -from-nifti <nifti-in> <cifti-template> <cifti-out>
    wb_command -cifti-convert -from-nifti $subcort_niilabel $schaefer_cifti $subcort_cifti

    # Run wb_command -cifti-merge <cifti-out> -cifti <subcortical-cifti> -cifti <schaefer>
    wb_command -cifti-merge $merged_cifti -cifti $subcort_cifti -cifti $schaefer_cifti
done