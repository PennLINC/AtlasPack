"""Download fsLR-32k CIFTI versions of the Schaefer 2018 7-network atlses."""
import itertools
import json
import os

import nibabel as nb
import numpy as np
import pandas as pd
import wget
from tqdm import tqdm


def download_image(n_parcels):
    """Download Schaefer files from official source."""
    # github link
    # NOTE: Same SHA as schaefer_map script.
    remote_path = (
        "https://github.com/ThomasYeoLab/CBIG/raw/eca7bc9f63d732834f74b44beac30af360608347/"
        "stable_projects/brain_parcellation/Schaefer2018_LocalGlobal/Parcellations/"
        "HCP/fslr32k/cifti"
    )
    pwd = os.getcwd()

    remote_filename = f"Schaefer2018_{n_parcels}Parcels_7Networks_order.dlabel.nii"
    wget.download(os.path.join(remote_path, remote_filename), pwd)

    out_file = os.path.join(
        pwd,
        (
            "tpl-fsLR_atlas-Schaefer2018v0143_den-32k_"
            f"desc-{n_parcels}ParcelsAllNetworks_dseg.dlabel.nii"
        ),
    )
    os.rename(os.path.join(pwd, remote_filename), out_file)


def prepare_subcortical_atlas(n_parcels):
    """Create "label list file" to use with ``wb_command -volume-label-import``."""
    labels_file = os.path.abspath(
        "../tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-01_dseg.tsv",
    )
    atlas_file = os.path.abspath(
        "../tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-01_dseg.nii.gz",
    )
    labels_df = pd.read_table(labels_file, index_col="index")
    out_labels_file = (
        "tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-01_"
        f"desc-Schaefer2018v0143{n_parcels}Parcels_labellist.txt"
    )
    out_atlas_file = (
        "tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-01_"
        f"desc-Schaefer2018v0143{n_parcels}Parcels_dseg.nii.gz"
    )
    out_str = ""

    possible_color_combos = [range(255), range(255), range(255)]
    all_color_combos = list(itertools.product(*possible_color_combos))

    continuous_index = n_parcels + 1
    subcortical_img = nb.load(atlas_file)
    subcortical_arr = subcortical_img.get_fdata()
    new_subcortical_arr = np.zeros(subcortical_arr.shape, dtype=np.int16)

    for index, row in labels_df.iterrows():
        # Update the label file.
        # Map atlas labels into continuous index.
        label = row["label"]
        out_str += f"{label}\n"
        r, g, b = all_color_combos[index]
        out_str += f"{continuous_index} {r} {g} {b} 1\n"

        # Update the atlas
        # Map atlas indices to continous index,
        # but shift based on the Schaefer atlas that will be added.
        new_subcortical_arr[subcortical_arr == index] = continuous_index

        continuous_index += 1

    new_subcortical_img = nb.Nifti1Image(
        new_subcortical_arr,
        affine=subcortical_img.affine,
        header=subcortical_img.header,
    )
    new_subcortical_img.to_filename(out_atlas_file)

    with open(out_labels_file, "w") as fo:
        fo.write(out_str)


def combine_metadata(n_parcels):
    """Combine metadata."""
    atlas_name = "Schaefer2018v0143"

    subcortical_metadata_file = os.path.abspath("../atlas-SubcorticalMerged_dseg.json")
    subcortical_labels_file = os.path.abspath(
        "../tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-01_dseg.tsv",
    )
    schaefer_labels_file = os.path.abspath(
        f"../schaefer_map/atlas-{atlas_name}_desc-{n_parcels}ParcelsAllNetworks_dseg.tsv",
    )
    schaefer_nifti_metadata_file = os.path.abspath(
        f"../schaefer_map/atlas-{atlas_name}_desc-{n_parcels}ParcelsAllNetworks_dseg.json"
    )
    schaefer_metadata_file = (
        f"tpl-MNI152NLin6Asym_atlas-{atlas_name}Merged_res-01_"
        f"desc-{n_parcels}Parcels_dseg.json"
    )
    out_labels_file = (
        f"tpl-MNI152NLin6Asym_atlas-{atlas_name}Merged_res-01_"
        f"desc-{n_parcels}Parcels_dseg.tsv"
    )

    with open(subcortical_metadata_file, "r") as fo:
        subcortical_metadata = json.load(fo)

    with open(schaefer_nifti_metadata_file, "r") as fo:
        schaefer_nifti_metadata = json.load(fo)

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
        "Name": atlas_name,
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

    subcortical_metadata["SourceAtlases"][atlas_name] = schaefer_metadata
    # Add info about space and resolution.
    # Remove resolution field, since this is CIFTI data
    subcortical_metadata.pop("Resolution")
    # Add density field
    subcortical_metadata["Density"] = {
        "91k": (
            "91282 vertices. 32492 surface vertices per hemisphere. "
            "26298 subcortical voxels, at 1mm isotropic resolution."
        ),
        "32k": "32492 vertices per hemisphere. No subcortical data.",
    }
    # Taken from https://bids-specification.readthedocs.io/en/stable/05-derivatives/02-common-data-types.html#examples_1
    # The VolumeReference applies to the merged atlases, but not the Schaefer-only atlases.
    subcortical_metadata["SpatialReference"] = {
        "VolumeReference": "https://templateflow.s3.amazonaws.com/tpl-MNI152NLin6Asym_res-01_T1w.nii.gz",
        "CIFTI_STRUCTURE_CORTEX_LEFT": (
            "https://github.com/mgxd/brainplot/raw/master/brainplot/Conte69_Atlas/"
            "Conte69.L.midthickness.32k_fs_LR.surf.gii"
        ),
        "CIFTI_STRUCTURE_CORTEX_RIGHT": (
            "https://github.com/mgxd/brainplot/raw/master/brainplot/Conte69_Atlas/"
            "Conte69.R.midthickness.32k_fs_LR.surf.gii"
        ),
    }
    # Add descriptions of column names
    subcortical_metadata.update(schaefer_nifti_metadata)

    with open(schaefer_metadata_file, "w") as fo:
        json.dump(subcortical_metadata, fo, sort_keys=True, indent=4)

    subcortical_labels = pd.read_table(subcortical_labels_file, index_col="index")
    schaefer_labels = pd.read_table(schaefer_labels_file, index_col="index")
    schaefer_labels["atlas_name"] = atlas_name
    merged_labels = pd.concat(
        (schaefer_labels, subcortical_labels),
        axis=0,
        join="outer",
        ignore_index=True,
    )
    merged_labels.to_csv(out_labels_file, sep="\t", index_label="index", na_rep="n/a")


if __name__ == "__main__":
    for n_parcels in tqdm([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]):
        # download_image(n_parcels)
        prepare_subcortical_atlas(n_parcels)
        combine_metadata(n_parcels)
