import os
import subprocess
from glob import glob
import nibabel as nb
import numpy as np
from copy import deepcopy
from scipy.stats import mode

tfbase = os.getenv("TEMPLATEFLOW_HOME")
transform_image = tfbase + "/tpl-MNI152NLin2009cAsym/tpl-MNI152NLin2009cAsym_from-MNI152NLin6Asym_mode-image_xfm.h5"


def match_partitions(data1, data2):
    """Match the regions in data1 to the regions in data2"""

    data1_ids = np.unique(data1)
    data1_ids = data1_ids[data1_ids > 0].tolist()
    data2_ids = np.unique(data2)
    data2_ids = data2_ids[data2_ids > 0].tolist()

    mapping = {}
    for data1_id in data1_ids:
        region_mask = data1 == data1_id
        mapping[data1_id], = mode(data2[region_mask]).mode

    return mapping


def remap_values(original_data, mapping):
    remapped = np.zeros_like(original_data)
    for old_value, new_value in mapping.items():
        remapped[original_data==old_value] = new_value
    return remapped




def verify_atlas(atlas_config, atlas_data):
    data_regions = np.unique(atlas_data)
    data_regions = data_regions[data_regions > 0].tolist()
    for node_id, node_name in zip(atlas_config['node_ids'], atlas_config['node_names']):
        if node_id not in data_regions:
            raise Exception("%d: %s not in atlas data" % (node_id, node_name))

    if not len(atlas_config['node_ids']) == len(atlas_config['node_names']):
        raise Exception("Inconsistent number of node names and ids")

    missing_regions = set(atlas_config['node_ids']).difference(data_regions)
    if  missing_regions:
        raise Exception("%s present in data but not in labels" % str(missing_regions))


def add_atlas_to_another(atlas1_config, atlas1_data,
                         atlas2_config, atlas2_data):
    """
    Add atlas2 into atlas1. Ensure the labels are updated
    so there is no overlap
    """

    # Verify inputs
    verify_atlas(atlas1_config, atlas1_data)
    verify_atlas(atlas2_config, atlas2_data)
    atlas2_data = atlas2_data.copy()

    # What is the largest number in atlas1? This will be the minimum
    # value in the new ids for atlas2 after it's been added to atlas1
    merged_atlas_min = np.max(atlas1_data) + 2
    atlas2_id_mapping = dict(
        zip(atlas2_config['node_ids'],
            np.argsort(atlas2_config['node_ids']) + merged_atlas_min))
    atlas2_merged_ids = [atlas2_id_mapping[node_id] for node_id in
                         atlas2_config['node_ids']]

    # Make sure that any voxels that are labeled in the base image
    # are NOT overwritten by the new atlas data
    atlas2_data[atlas1_data > 0] = 0

    # Ensure that we have not clobbered any regions by doing so
    verify_atlas(atlas2_config, atlas2_data)

    # Change their node ids so they don't conflict with the base
    remapped_atlas2 = remap_values(atlas2_data, atlas2_id_mapping)

    merged_image_data = atlas1_data + remapped_atlas2
    merged_image_labels = atlas1_config['node_names'] + \
                          atlas2_config['node_names']
    merged_image_ids = atlas1_config['node_ids'] + atlas2_merged_ids
    merged_atlas_config = {"node_names": merged_image_labels,
                           "node_ids": merged_image_ids}
    verify_atlas(merged_atlas_config, merged_image_data)
    return merged_atlas_config, merged_image_data
