"""Download fsLR-32k CIFTI versions of the Schaefer 2018 7-network atlses."""
import itertools
import os

import nibabel as nb
import numpy as np
import pandas as pd
import wget
from tqdm import tqdm


def reorient(in_file, target_file, out_file):
    """Run a modified version of nipype.interfaces.images.Reorient.

    The subcortical atlas is in RAS, but the structural label file from DCAN is LAS.
    """
    target_img = nb.load(target_file)
    orig_img = nb.load(in_file)

    assert np.array_equal(np.abs(target_img.affine), np.abs(orig_img.affine))

    # Find transform from current (approximate) orientation to
    # target, in nibabel orientation matrix and affine forms
    target_orientation = "".join(nb.aff2axcodes(target_img.affine))
    orig_ornt = nb.io_orientation(orig_img.affine)
    targ_ornt = nb.orientations.axcodes2ornt(target_orientation)
    transform = nb.orientations.ornt_transform(orig_ornt, targ_ornt)

    reoriented = orig_img.as_reoriented(transform)

    # Image may be reoriented
    if reoriented is not orig_img:
        reoriented.to_filename(out_file)
    else:
        out_file = in_file

    return out_file


def download_schaefer_cifti(n_parcels):
    """Download Schaefer files from official source."""
    # github link
    # NOTE: Same SHA as Schaefer script.
    remote_path = (
        "https://github.com/ThomasYeoLab/CBIG/raw/eca7bc9f63d732834f74b44beac30af360608347/"
        "stable_projects/brain_parcellation/Schaefer2018_LocalGlobal/Parcellations/"
        "HCP/fslr32k/cifti"
    )
    pwd = os.getcwd()

    out_file = (
        "tpl-fsLR_atlas-Schaefer2018v0143_den-32k_"
        f"desc-{n_parcels}ParcelsAllNetworks_dseg.dlabel.nii"
    )
    if not os.path.isfile(out_file):
        remote_filename = f"Schaefer2018_{n_parcels}Parcels_7Networks_order.dlabel.nii"
        wget.download(os.path.join(remote_path, remote_filename), pwd)
        os.rename(remote_filename, out_file)


def download_templates():
    """Download templates."""
    import os
    import shutil

    from templateflow.api import get as get_template

    rh = str(
        get_template(
            template="fsLR",
            hemi="R",
            density="32k",
            desc="nomedialwall",
            suffix="dparc",
            extension=".label.gii",
        )
    )
    lh = str(
        get_template(
            template="fsLR",
            hemi="L",
            density="32k",
            desc="nomedialwall",
            suffix="dparc",
            extension=".label.gii",
        )
    )
    if not os.path.exists(os.path.basename(rh)):
        shutil.copy2(rh, os.path.basename(rh))

    if not os.path.exists(os.path.basename(lh)):
        shutil.copy2(lh, os.path.basename(lh))


def prepare_subcortical_atlas(n_parcels):
    """Create "label list file" to use with ``wb_command -volume-label-import``."""
    labels_file = "../subcortical_merged/tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-01_dseg.tsv"
    atlas_file = "../subcortical_merged/tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-02_dseg.nii.gz"
    resampled_atlas_file = (
        "../subcortical_merged/"
        "tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-02_desc-resampled_dseg.nii.gz"
    )
    target_file = "Atlas_ROIs.2.nii.gz"
    labels_df = pd.read_table(labels_file, index_col="index")
    out_labels_file = (
        "tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-02_"
        f"desc-Schaefer2018v0143x{n_parcels}Parcels_labellist.txt"
    )
    out_atlas_file = (
        "tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-02_"
        f"desc-Schaefer2018v0143x{n_parcels}Parcels_dseg.nii.gz"
    )
    out_str = ""

    possible_color_combos = [range(10, 255), range(10, 255), range(10, 255)]
    all_color_combos = list(itertools.product(*possible_color_combos))

    # Create index to linearly sample across all possible colors
    last_parcel_idx = labels_df.index.values[-1]
    n_colors = len(all_color_combos)
    color_skip = n_colors // last_parcel_idx
    colors = np.arange(n_colors)
    color_idx = colors[::color_skip]
    selected_color_combos = [all_color_combos[i] for i in color_idx]

    continuous_index = n_parcels + 1

    # Ensure atlas has same affine as target file
    resampled_atlas_file = reorient(atlas_file, target_file, resampled_atlas_file)
    atlas_img = nb.load(resampled_atlas_file)

    atlas_arr = atlas_img.get_fdata()
    new_atlas_arr = np.zeros(atlas_arr.shape, dtype=np.int16)

    for index, row in labels_df.iterrows():
        # Update the label file.
        # Map atlas labels into continuous index.
        label = row["label"]
        out_str += f"{label}\n"
        r, g, b = selected_color_combos[index]
        out_str += f"{continuous_index} {r} {g} {b} 255\n"

        # Update the atlas
        # Map atlas indices to continous index,
        # but shift based on the Schaefer atlas that will be added.
        new_atlas_arr[atlas_arr == index] = continuous_index

        continuous_index += 1

    new_atlas_img = nb.Nifti1Image(
        new_atlas_arr,
        affine=atlas_img.affine,
        header=atlas_img.header,
    )
    new_atlas_img.to_filename(out_atlas_file)

    with open(out_labels_file, "w") as fo:
        fo.write(out_str)


if __name__ == "__main__":
    download_templates()

    for n_parcels in tqdm([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]):
        download_schaefer_cifti(n_parcels)
        prepare_subcortical_atlas(n_parcels)
