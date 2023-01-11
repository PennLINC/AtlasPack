import os
import wget
import numpy as np
import pandas as pd

# github link
remote_path = 'https://github.com/ThomasYeoLab/CBIG/raw/master/stable_projects/brain_parcellation/Schaefer2018_LocalGlobal/Parcellations/MNI'
pwd = os.getcwd()
tfhome = os.getenv("TEMPLATEFLOW_HOME")
tf_schaefer_file = tfhome + "/tpl-MNI152NLin2009cAsym/tpl-MNI152NLin2009cAsym_atlas-Schaefer2018_desc-{}Parcels{}Networks_dseg.tsv"

def map_schaefer_orders(n_parcels):

    # download schaefer files from official source
    file7 = 'Schaefer2018_{0}Parcels_7Networks_order_FSLMNI152_2mm.Centroid_RAS.csv'.format(n_parcels)
    file17 = 'Schaefer2018_{0}Parcels_17Networks_order_FSLMNI152_2mm.Centroid_RAS.csv'.format(n_parcels)
    wget.download(os.path.join(remote_path, 'Centroid_coordinates', file7), pwd)
    wget.download(os.path.join(remote_path, 'Centroid_coordinates', file17), pwd)
    centroids_inorder = pd.read_csv(file7)
    centroids_outorder = pd.read_csv(file17)

    # Load the templateflow version of the schaefer files
    tf_tsv_7 = tf_schaefer_file.format(n_parcels, 7)
    tf_tsv_7_df = pd.read_csv(tf_tsv_7, sep="\t")
    tf_tsv_17 = tf_schaefer_file.format(n_parcels, 17)
    tf_tsv_17_df = pd.read_csv(tf_tsv_17, sep="\t")

    # Check that the templateflow files are consistent with the official versions
    assert (centroids_inorder["ROI Label"] == tf_tsv_7_df['index']).all()
    assert (centroids_outorder["ROI Label"] == tf_tsv_17_df['index']).all()
    centroids_inorder["tf_label_7"] = tf_tsv_7_df['name']
    centroids_inorder["tf_color_7"] = tf_tsv_7_df['color']
    centroids_outorder["tf_label_17"] = tf_tsv_17_df['name']
    centroids_outorder["tf_color_17"] = tf_tsv_17_df['color']
    centroids_inorder.rename(
        columns={'ROI Label': 'ROILabel7', 'ROI Name': 'ROIName7'},
        inplace=True)
    centroids_outorder.rename(
        columns={'ROI Label': 'ROILabel17', 'ROI Name': 'ROIName17'},
        inplace=True)

    coord_merge = pd.merge(centroids_inorder, centroids_outorder)
    coord_merge.rename(columns={"ROILabel7": "index"}, inplace=True)
    assert coord_merge.shape[0] == centroids_inorder.shape[0]

    # save out
    coord_merge.to_csv(
        'atlas-Schaefer2018_desc-{}ParcelsAllNetworks_dseg.tsv'.format(n_parcels),
        sep="\t")

for order in [100, 200, 300, 400, 500, 600, 800, 1000]:
    map_schaefer_orders(order)

