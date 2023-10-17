"""Generate sidecar JSON files for the 4S atlases."""
import json

import pandas as pd
from tqdm import tqdm


def generate_subcortical_metadata():
    """Generate the metadata for each atlas."""
    cb_sidecar = {
        "Authors": [
            "King, M.",
            "Hernandez-Castillo, C.R.",
            "Poldrack, R.R.",
            "Ivry, R.",
            "Diedrichsen, J.",
        ],
        "License": "Creative Commons license CC BY-ND (Attribution - No derivatives)",
        "Curators": [
            "Diedrichsen J",
        ],
        "Name": "Multi-domain task battery (MDTB) cerebellar parcellation",
        "Description": (
            "King et al. (2019) provided an extensive characterization of the functional "
            "organization of the cerebellum of 24 healthy, young participants. "
            "The contast are for for 47 task conditions, "
            "accounted for the activity caused by left hand, right hand, and eye movements. "
            "All contrast maps are relative to the mean activitiy across all tasks. "
            "The parcellation into 10 regions is defined from the task-evoked activity across "
            "all tasks."
        ),
        "ReferencesAndLinks": [
            "https://github.com/DiedrichsenLab/cerebellar_atlases",
            (
                "King, M., Hernandez-Castillo, C.R., Poldrack, R.R., Ivry, R., and "
                "Diedrichsen, J. (2019). Functional Boundaries in the Human Cerebellum revealed"
                "by a Multi-Domain Task Battery. Nat. Neurosci."
            ),
        ],
    }

    thalamic_sidecar = {
        "Authors": [
            "E. Najdenovska",
            "Y. Aléman-Gómez",
            "G. Battistella",
            "M. Descoteaux",
            "P. Hagmann",
            "S. Jacquemont",
            "P. Maeder",
            "J.P. Thiran",
            "E. Fornari",
            "M. Bach Cuadra",
        ],
        "License": (
            "Creative Commons Attribution Share Alike 4.0 International "
            "https://creativecommons.org/licenses/by-sa/4.0/legalcode"
        ),
        "Name": "HCP Thalamic Parcellation",
        "Description": (
            "Regions are based on a probabilistic atlas of anatomical subparts of the thalamus "
            "built upon a relatively large dataset where the individual thalamic parcellation "
            "was done by employing a recently proposed automatic diffusion-based clustering "
            "method."
        ),
        "ReferencesAndLinks": [
            "doi: 10.1038/sdata.2018.270",
            "https://zenodo.org/record/1405484/files/Thalamus_Nuclei-HCP-MaxProb.nii.gz",
            "https://zenodo.org/record/1405484/files/Thalamic_Nuclei-ColorLUT.txt",
            (
                "Najdenovska, E., Alemán-Gómez, Y., Battistella, G. et al. In-vivo probabilistic "
                "atlas of human thalamic nuclei based on diffusion-weighted magnetic resonance "
                "imaging. Sci Data 5, 180270 (2018). https://doi.org/10.1038/sdata.2018.270"
            ),
        ],
    }

    subcortical_sidecar = {
        "Authors": [
            "W.M. Pauli",
            "A.N. Nili",
            "J.M. Tyszka",
        ],
        "Curators": [
            "W.M. Pauli",
            "A.N. Nili",
            "J.M. Tyszka",
            "M. Okamoto",
        ],
        "License": (
            "MIT: https://github.com/jmtyszka/CIT168-SubCorticalAtlas/blob/master/LICENSE.md"
        ),
        "Name": "CIT168",
        "Description": (
            "Parcellations based on high spatial resolution, three-dimensional templates, "
            "using high-accuracy diffeomorphic registration of T1- and T2- weighted structural "
            "images from 168 typical adults between 22 and 35 years old. NOTE: Atlases "
            "originally assigned the same label to structures in each hemisphere. "
            "Here we have split the regions into hemispheres. "
            "Additionally, the SNC, PBP and VTA regions have been merged into a single structure."
        ),
        "ReferencesAndLinks": [
            "https://neurovault.org/collections/3145/",
            "https://osf.io/jkzwp/wiki/home/",
            "https://github.com/jmtyszka/CIT168-SubCorticalAtlas",
            (
                "Pauli, W., Nili, A. & Tyszka, J. A high-resolution probabilistic in vivo atlas "
                "of human subcortical brain nuclei. Sci Data 5, 180063 (2018). "
                "https://doi.org/10.1038"
            ),
        ],
    }

    hcp_sidecar = {
        "Authors": [
            "M.F. Glasser",
            "S.N. Sotiropoulos",
            "J.A. Wilson",
            "T.S. Coalson",
            "B. Fischl",
            "J.L. Andersson",
            "J. Xu",
            "S. Jbabdi",
            "M. Webster",
            "J.R. Polimeni",
            "D.C. Van Essen",
            "M. Jenkinson",
            "The WU-Minn HCP Consortium",
        ],
        "License": (
            "https://github.com/Washington-University/HCPpipelines/blob/"
            "21c0867c7f3a59554b9e28f5fe5cddd41e159170/LICENSE.md"
        ),
        "Name": "HCP Subcortical Parcellation",
        "Description": (
            "The hippocampus and amygdala regions from the HCP subcortical atlas were selected."
        ),
        "ReferencesAndLinks": [
            (
                "https://github.com/Washington-University/HCPpipelines/blob/"
                "21c0867c7f3a59554b9e28f5fe5cddd41e159170/global/templates/"
                "170494_Greyordinates/Atlas_ROIs.1.60.nii.gz"
            ),
            (
                "Glasser, M. F., Sotiropoulos, S. N., Wilson, J. A., Coalson, T. S., Fischl, B., "
                "Andersson, J. L., ... & Wu-Minn HCP Consortium. (2013). "
                "The minimal preprocessing pipelines for the Human Connectome Project. "
                "Neuroimage, 80, 105-124."
            ),
        ],
    }

    merged_sidecar = {
        "Authors": [
            "M. Cieslak",
            "T. Salo",
            "E. Feczko",
            "T.D. Satterthwaite",
        ],
        "License": "Creative Commons license CC BY-ND (Attribution - No derivatives)",
        "BIDSVersion": "1.8.0",
        "Curators": [
            "M. Cieslak",
            "T. Salo",
            "E. Feczko",
            "T.D. Satterthwaite",
        ],
        "Name": "Non-Cortical Atlases in Template Space NCATS",
        "Description": (
            "A set of non-cortical atlases that have been merged together in template space."
        ),
        "ReferencesAndLinks": [
            "https://github.com/PennLINC/AtlasPack",
        ],
        "RegionNames": {
            "Pu": "Putamen",
            "Ca": "Caudate Nucleus",
            "NAC": "Nucleus Acumbens",
            "EXA": "Extended Amygdala",
            "GPi": "Globus Pallidus, Internal",
            "GPe": "Globus Pallidus, External",
            "VeP": "Ventral Pallidum",
            "SNc": "Substantia Nigra, Pars Compacta",
            "SNr": "Substantia Nigra, Pars Reticulata",
            "STH": "Subthalamic Nucleus",
            "HTH": "Hypothalamus",
            "PBP": "Parabrachial Pigmented Nucleus",
            "VTA": "Ventral Tegmental Area",
            "RN": "Red Nucleus",
            "HN": "Habenular Nuclei",
            "MN": "Mammilary Nucleus",
        },
        "Resolution": {
            "01": "1mm, isotropic",
        },
        # These match up with the `atlas_name` column
        "SourceAtlases": {
            "CIT168Subcortical": subcortical_sidecar,
            "Cerebellum": cb_sidecar,
            "ThalamusHCP": thalamic_sidecar,
            "HCPSubcortical": hcp_sidecar,
        },
    }

    with open("../subcortex_merged/atlas-SubcorticalMerged_dseg.json", "w") as atl_json:
        json.dump(merged_sidecar, atl_json, indent=4)


def combine_metadata(n_parcels):
    """Combine metadata."""
    atlas_name = f"4S{n_parcels + 52}"
    schf_name = "Schaefer2018v0143"

    subcortical_metadata_file = "../subcortex_merged/atlas-SubcorticalMerged_dseg.json"
    subcortical_labels_file = (
        "../subcortex_merged/"
        "tpl-MNI152NLin6Asym_atlas-SubcorticalMerged_res-01_dseg.tsv"
    )
    schaefer_labels_file = (
        f"../Schaefer/atlas-{schf_name}_desc-{n_parcels}ParcelsAllNetworks_dseg.tsv"
    )
    schaefer_nifti_metadata_file = (
        f"../Schaefer/atlas-{schf_name}_desc-{n_parcels}ParcelsAllNetworks_dseg.json"
    )
    merged_cifti_metadata_file = f"../4S/tpl-fsLR_atlas-{atlas_name}Parcels_dseg.json"
    merged_nifti_metadata_file = (
        f"../4S/tpl-MNI152NLin6Asym_atlas-{atlas_name}Parcels_dseg.json"
    )
    merged_labels_file = f"../4S/atlas-{atlas_name}Parcels_dseg.tsv"

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

    # fmt:off
    atlas_metadata["Name"] = f"{atlas_name}: Schaefer Supplemented with Subcortical Structures"
    # fmt:on
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
    merged_labels.to_csv(
        merged_labels_file, sep="\t", index_label="index", na_rep="n/a"
    )


if __name__ == "__main__":
    generate_subcortical_metadata()
    for n_parcels in tqdm([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]):
        combine_metadata(n_parcels)
