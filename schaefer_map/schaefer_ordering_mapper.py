"""Match Schaefer atlases' orders across networks."""
import json
import os

import pandas as pd
import wget
from tqdm import tqdm

# github link
remote_path = (
    "https://github.com/ThomasYeoLab/CBIG/raw/eca7bc9f63d732834f74b44beac30af360608347/"
    "stable_projects/brain_parcellation/Schaefer2018_LocalGlobal/Parcellations/MNI"
)
pwd = os.getcwd()


def _get_network(node_label):
    return node_label.split("_")[2]


def map_schaefer_orders(n_parcels):
    """Map the Schaefer parcel orders across network maps."""
    file7 = f"Schaefer2018_{n_parcels}Parcels_7Networks_order_FSLMNI152_2mm.Centroid_RAS.csv"
    file17 = f"Schaefer2018_{n_parcels}Parcels_17Networks_order_FSLMNI152_2mm.Centroid_RAS.csv"
    wget.download(os.path.join(remote_path, "Centroid_coordinates", file7), pwd)
    wget.download(os.path.join(remote_path, "Centroid_coordinates", file17), pwd)
    centroids_inorder = pd.read_csv(file7)
    centroids_outorder = pd.read_csv(file17)

    # Check that the templateflow files are consistent with the official versions
    centroids_inorder.rename(
        columns={"ROI Label": "index_7network", "ROI Name": "label_7network"},
        inplace=True,
    )
    centroids_outorder.rename(
        columns={"ROI Label": "index_17network", "ROI Name": "label_17network"},
        inplace=True,
    )

    coord_merge = pd.merge(centroids_inorder, centroids_outorder)
    coord_merge.rename(columns={"index_7network": "index"}, inplace=True)
    coord_merge["label"] = coord_merge["label_7network"].str.replace("7Networks_", "")
    assert coord_merge.shape[0] == centroids_inorder.shape[0]

    coord_merge["network_label"] = coord_merge["label_7network"].apply(_get_network)
    coord_merge["network_label_17network"] = coord_merge["label_17network"].apply(_get_network)

    # Sort columns and drop unused ones
    coord_merge = coord_merge[
        [
            "index",
            "label",
            "network_label",
            "label_7network",
            "index_17network",
            "label_17network",
            "network_label_17network",
        ]
    ]

    # save out
    coord_merge.to_csv(
        f"atlas-Schaefer2018_desc-{n_parcels}ParcelsAllNetworks_dseg.tsv",
        sep="\t",
        index=False,
        na_rep="n/a",  # for BIDS
    )

    # Write out file-specific metadata.
    # We could add "Levels" here, but not sure if it's worth it.
    merge_dict = {
        "label_7network": {
            "LongName": "Node label from Schaefer 7-network atlas",
            "Description": (
                "The label of the node as it appears in the canonical Schaefer 7-network atlas."
            ),
        },
        "index_17network": {
            "LongName": "Node index from Schaefer 17-network atlas",
            "Description": (
                "The corresponding integer value of this node in the 17-network Schaefer atlas "
                "imaging file."
            ),
        },
        "label_17network": {
            "LongName": "Node label from Schaefer 17-network atlas",
            "Description": (
                "The label of the node as it appears in the canonical Schaefer 17-network atlas."
            ),
        },
        "network_label_17network": {
            "LongName": "Network label from Schaefer 17-network atlas",
            "Description": (
                "The name of the network this node is assigned to in the Schaefer 17-network "
                "atlas."
            ),
        },
    }
    with open(
        f"atlas-Schaefer2018_desc-{n_parcels}ParcelsAllNetworks_dseg.json", "w"
    ) as fo:
        json.dump(merge_dict, fo, sort_keys=True, indent=4)


def download_image(n_parcels):
    """Download Schaefer files from official source."""
    file7 = f"Schaefer2018_{n_parcels}Parcels_7Networks_order_FSLMNI152_1mm.nii.gz"
    file17 = f"Schaefer2018_{n_parcels}Parcels_17Networks_order_FSLMNI152_1mm.nii.gz"
    wget.download(os.path.join(remote_path, file7), pwd)
    wget.download(os.path.join(remote_path, file17), pwd)


if __name__ == "__main__":
    for order in tqdm([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]):
        map_schaefer_orders(order)
        # download_image(order)
