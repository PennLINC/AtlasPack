import os

import pandas as pd
import wget
from tqdm import tqdm

# github link
remote_path = 'https://github.com/ThomasYeoLab/CBIG/raw/eca7bc9f63d732834f74b44beac30af360608347/stable_projects/brain_parcellation/Schaefer2018_LocalGlobal/Parcellations/MNI'
pwd = os.getcwd()


def map_schaefer_orders(n_parcels):
    # download schaefer files from official source
    file7 = 'Schaefer2018_{0}Parcels_7Networks_order_FSLMNI152_2mm.Centroid_RAS.csv'.format(n_parcels)
    file17 = 'Schaefer2018_{0}Parcels_17Networks_order_FSLMNI152_2mm.Centroid_RAS.csv'.format(n_parcels)
    wget.download(os.path.join(remote_path, 'Centroid_coordinates', file7), pwd)
    wget.download(os.path.join(remote_path, 'Centroid_coordinates', file17), pwd)
    centroids_inorder = pd.read_csv(file7)
    centroids_outorder = pd.read_csv(file17)

    # Check that the templateflow files are consistent with the official versions
    centroids_inorder.rename(
        columns={'ROI Label': 'ROILabel7', 'ROI Name': 'ROIName7'},
        inplace=True)
    centroids_outorder.rename(
        columns={'ROI Label': 'ROILabel17', 'ROI Name': 'ROIName17'},
        inplace=True)

    coord_merge = pd.merge(centroids_inorder, centroids_outorder)
    coord_merge.rename(columns={"ROILabel7": "index"}, inplace=True)
    coord_merge["name"] = coord_merge["ROIName7"]
    assert coord_merge.shape[0] == centroids_inorder.shape[0]

    # save out
    coord_merge.to_csv(
        'atlas-Schaefer2018_desc-{}ParcelsAllNetworks_dseg.tsv'.format(n_parcels),
        sep="\t", index=False)


def download_image(n_parcels):
    # download schaefer files from official source
    file7 = 'Schaefer2018_{0}Parcels_7Networks_order_FSLMNI152_1mm.nii.gz'.format(n_parcels)
    file17 = 'Schaefer2018_{0}Parcels_17Networks_order_FSLMNI152_1mm.nii.gz'.format(n_parcels)
    wget.download(os.path.join(remote_path, file7), pwd)
    wget.download(os.path.join(remote_path, file17), pwd)


if __name__ == "__main__":
    for order in tqdm([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]):
        map_schaefer_orders(order)
        download_image(order)

