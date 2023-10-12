#!/usr/bin/env python
"""Split up the CIT168 atlas."""
import sys

import nibabel as nb
import numpy as np
import pandas as pd

sys.path.append("..")

from utils import verify_atlas  # noqa: E402

if __name__ == "__main__":
    input_cit_file, output_cit_prefix = sys.argv[1:]

    cit168_subcortical = {"node_names": [], "node_ids": []}

    with open("labels.txt") as f:
        for line in f:
            split = line.strip().split()
            if not len(split) == 2:
                continue
            node_id, node_name = line.strip().split()
            cit168_subcortical["node_names"].append(node_name)
            # they started at 0, wtf
            cit168_subcortical["node_ids"].append(int(node_id) + 1)

    cit_168_img = nb.load(input_cit_file)
    cit168_data = cit_168_img.get_fdata().astype(np.uint32)

    # Merge the smaller regions together
    cit_lut = {
        node_id: region_label
        for node_id, region_label in zip(
            cit168_subcortical["node_ids"], cit168_subcortical["node_names"]
        )
    }
    cit168_data[cit168_data == 10] = 7
    cit168_data[cit168_data == 11] = 7
    cit_region7_label = "_".join([cit_lut[7], cit_lut[10], cit_lut[11]])
    cit_lut[7] = cit_region7_label
    del cit_lut[10], cit_lut[11]
    merged_cit_ids = sorted(cit_lut.keys())
    merged_cit_labels = [cit_lut[node_id] for node_id in merged_cit_ids]
    merged_cit_config = {"node_ids": merged_cit_ids, "node_names": merged_cit_labels}
    verify_atlas(merged_cit_config, cit168_data)

    # Add 100 to the LH regions to separate them
    offsetmask = np.zeros_like(cit168_data)
    midvoxel = offsetmask.shape[0] // 2
    offsetmask[midvoxel:, :, :] = 100
    hemi_cit_data = (cit168_data + offsetmask) * (cit168_data > 0)

    # Split regions into hemispheres
    cit_hemi_labels = [f"CIT168Subcortical_LH-{name}" for name in merged_cit_labels] + [
        f"CIT168Subcortical_RH-{name}" for name in merged_cit_labels
    ]
    cit_hemi_ids = merged_cit_ids + [_id + 100 for _id in merged_cit_ids]
    cit_hemi_config = {"node_ids": cit_hemi_ids, "node_names": cit_hemi_labels}
    verify_atlas(cit_hemi_config, hemi_cit_data)

    labeldf = pd.DataFrame({"index": cit_hemi_ids, "name": cit_hemi_labels})
    labeldf.to_csv(f"{output_cit_prefix}.tsv", sep="\t", index=False)

    final_nii = nb.Nifti1Image(
        hemi_cit_data,
        cit_168_img.affine,
        header=cit_168_img.header,
    )

    final_nii.to_filename(f"{output_cit_prefix}.nii.gz")
