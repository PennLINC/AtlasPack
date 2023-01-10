#!/usr/bin/env python
# Do CIT168
from merge_atlases import *
cit168_subcortical = {
    "node_names": [],
    "node_ids": []
}

with open("data/2009cAsym/CIT168labels.txt") as f:
    for line in f:
        node_id, node_name = line.strip().split(",")
        cit168_subcortical['node_names'].append("CIT168Subcortical_" + node_name)
        cit168_subcortical['node_ids'].append(int(node_id)+1) # they started at 0, wtf

cit168_data = nb.load(
    "data/2009cAsym/tpl-MNI152NLin2009cAsym_res-01_atlas-CIT168_desc-LPS_dseg.nii.gz"
).get_fdata().astype(np.uint32)


# Merge the smaller regions together
cit_lut = {node_id: region_label for node_id, region_label in
           zip(cit168_subcortical['node_ids'],
               cit168_subcortical['node_names'])}
cit168_data[cit168_data==10] = 7
cit168_data[cit168_data==11] = 7
cit_region7_label = "_".join([cit_lut[7], cit_lut[10], cit_lut[11]])
cit_lut[7] = cit_region7_label
del cit_lut[10], cit_lut[11]
merged_cit_ids = sorted(cit_lut.keys())
merged_cit_labels = [cit_lut[node_id] for node_id in merged_cit_ids]
merged_cit_config = {"node_ids": merged_cit_ids, "node_names":merged_cit_labels}
verify_atlas(merged_cit_config, cit168_data)

# Add 100 to the LH regions to separate them
offsetmask = np.zeros_like(cit168_data)
midvoxel = offsetmask.shape[0] // 2
offsetmask[midvoxel:, :, :] = 100
hemi_cit_data = (cit168_data + offsetmask) * (cit168_data > 0)

# Split regions into hemispheres
cit_hemi_labels = [name + "_rh" for name in merged_cit_labels] + \
             [name + "_lh" for name in merged_cit_labels]
cit_hemi_ids = merged_cit_ids + [_id + 100 for _id in merged_cit_ids]
cit_hemi_config = {
    "node_ids": cit_hemi_ids,
    "node_names": cit_hemi_labels
}
verify_atlas(cit_hemi_config, hemi_cit_data)