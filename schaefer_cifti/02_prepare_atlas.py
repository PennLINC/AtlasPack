"""Download fsLR-32k CIFTI versions of the Schaefer 2018 7-network atlses."""
import itertools
import json
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
    # NOTE: Same SHA as schaefer_map script.
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
    if not os.path.isfile(os.path.basename(rh)):
        shutil.copyfile(rh, os.path.basename(rh))

    if not os.path.isfile(os.path.basename(lh)):
        shutil.copyfile(lh, os.path.basename(lh))


def prepare_subcortical_atlas(n_parcels):
    """Create "label list file" to use with ``wb_command -volume-label-import``."""
    labels_file = "../tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-01_dseg.tsv"
    atlas_file = "tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-02_dseg.nii.gz"
    resampled_atlas_file = (
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


def combine_metadata(n_parcels):
    """Combine metadata."""
    atlas_name = f"4S{n_parcels + 52}"
    schf_name = "Schaefer2018v0143"

    subcortical_metadata_file = "../atlas-SubcorticalMerged_dseg.json"
    subcortical_labels_file = "../tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-01_dseg.tsv"
    schaefer_labels_file = (
        f"../schaefer_map/atlas-{schf_name}_desc-{n_parcels}ParcelsAllNetworks_dseg.tsv"
    )
    schaefer_nifti_metadata_file = (
        f"../schaefer_map/atlas-{schf_name}_desc-{n_parcels}ParcelsAllNetworks_dseg.json"
    )
    merged_cifti_metadata_file = f"../tpl-fsLR_atlas-{atlas_name}Parcels_dseg.json"
    merged_nifti_metadata_file = f"../tpl-MNI152NLin6Asym_atlas-{atlas_name}Parcels_dseg.json"
    merged_labels_file = f"../atlas-{atlas_name}Parcels_dseg.tsv"

    with open(subcortical_metadata_file, "r") as fo:
        subcortical_metadata = json.load(fo)

    with open(schaefer_nifti_metadata_file, "r") as fo:
        schaefer_nifti_metadata = json.load(fo)

    # Base merged metadata on subcortical metadata
    atlas_metadata = subcortical_metadata.copy()

    schaefer_metadata = {
        "Authors": [
            "A Schaefer",
            "R Kong",
            "E.M. Gordon",
            "T.O. Laumann",
            "X. Zuo",
            "A.J. Holmes",
            "S.B. Eickhoff",
            "B.T. Yeo",
        ],
        "Curators": [
            "A Schaefer",
            "R Kong",
            "E.M. Gordon",
            "T.O. Laumann",
            "X. Zuo",
            "A.J. Holmes",
            "S.B. Eickhoff",
            "B.T. Yeo",
        ],
        "License": (
            "MIT: https://github.com/ThomasYeoLab/CBIG/blob/"
            "a8c7a0bb845210424ef1c46d1435fec591b2cf3d/LICENSE.md"
        ),
        "Name": schf_name,
        "Description": (
            "Resting state fMRI data from 1489 subjects were registered using surface-based "
            "alignment. A gradient weighted markov random field approach was employed to "
            "identify cortical parcels ranging from 100 to 1000 parcels. "
            "More details can be found in Schaefer et al. 2018."
        ),
        "ReferencesAndLinks": [
            (
                "https://github.com/ThomasYeoLab/CBIG/tree/master/stable_projects/"
                "brain_parcellation/Schaefer2018_LocalGlobal"
            ),
            (
                "Schaefer, A., Kong, R., Gordon, E. M., Laumann, T. O., Zuo, X. N., "
                "Holmes, A. J., Eickhoff, S. B., & Yeo, B. T. (2018). "
                "Local-global parcellation of the human cerebral cortex from intrinsic "
                "functional connectivity MRI. Cerebral cortex, 28(9), 3095-3114."
            ),
        ],
    }

    atlas_metadata["Name"] = f"{atlas_name}: Schaefer Supplemented with Subcortical Structures"
    atlas_metadata["Description"] = (
        f"A set of non-cortical atlases and the Schaefer {n_parcels}-parcel cortical atlas, "
        "that have been merged together in template space."
    )
    atlas_metadata["SourceAtlases"][schf_name] = schaefer_metadata

    # Add descriptions of column names
    atlas_metadata.update(schaefer_nifti_metadata)

    with open(merged_nifti_metadata_file, "w") as fo:
        json.dump(atlas_metadata, fo, sort_keys=True, indent=4)

    # Add info about space and resolution.
    # Remove resolution field, since this is CIFTI data
    atlas_metadata.pop("Resolution")
    # Add density field
    atlas_metadata["Density"] = {
        "91k": (
            "91282 vertices. "
            "29696 surface vertices in left hemisphere. "
            "29716 surface vertices in right hemisphere. "
            "31870 subcortical voxels, at 2 mm isotropic resolution."
        ),
        "32k": "32492 vertices per hemisphere. No subcortical data.",
    }
    # Taken from https://bids-specification.readthedocs.io/en/stable/05-derivatives/\
    # 02-common-data-types.html#examples_1
    # The VolumeReference applies to the merged atlases, but not the Schaefer-only atlases.
    atlas_metadata["SpatialReference"] = {
        "VolumeReference": (
            "https://templateflow.s3.amazonaws.com/tpl-MNI152NLin6Asym_res-01_T1w.nii.gz"
        ),
        "CIFTI_STRUCTURE_CORTEX_LEFT": (
            "https://github.com/mgxd/brainplot/raw/master/brainplot/Conte69_Atlas/"
            "Conte69.L.midthickness.32k_fs_LR.surf.gii"
        ),
        "CIFTI_STRUCTURE_CORTEX_RIGHT": (
            "https://github.com/mgxd/brainplot/raw/master/brainplot/Conte69_Atlas/"
            "Conte69.R.midthickness.32k_fs_LR.surf.gii"
        ),
    }

    with open(merged_cifti_metadata_file, "w") as fo:
        json.dump(atlas_metadata, fo, sort_keys=True, indent=4)

    subcortical_labels = pd.read_table(subcortical_labels_file, index_col="index")
    schaefer_labels = pd.read_table(schaefer_labels_file, index_col="index")
    schaefer_labels["atlas_name"] = atlas_name
    merged_labels = pd.concat(
        (schaefer_labels, subcortical_labels),
        axis=0,
        join="outer",
        ignore_index=True,
    )
    # Start index at 1
    merged_labels.index = merged_labels.index + 1
    merged_labels.to_csv(merged_labels_file, sep="\t", index_label="index", na_rep="n/a")


if __name__ == "__main__":
    download_templates()

    for n_parcels in tqdm([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]):
        download_schaefer_cifti(n_parcels)
        prepare_subcortical_atlas(n_parcels)
        combine_metadata(n_parcels)
