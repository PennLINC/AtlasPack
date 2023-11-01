"""Separate out the hippocampus and amygdala ROIs from the atlas."""
import nibabel as nb
import numpy as np
import pandas as pd

if __name__ == "__main__":
    df = pd.read_table("atlas-HCP_dseg.tsv")
    df_sel = df.loc[
        df["label"].str.startswith("HIPPOCAMPUS")
        | df["label"].str.startswith("AMYGDALA")
    ]
    df_sel = df_sel[["index", "label"]]
    df_sel = df_sel.replace(
        {
            "label": {
                "HIPPOCAMPUS_LEFT": "LH_Hippocampus",
                "HIPPOCAMPUS_RIGHT": "RH_Hippocampus",
                "AMYGDALA_LEFT": "LH_Amygdala",
                "AMYGDALA_RIGHT": "RH_Amygdala",
            },
        }
    )
    df_sel.to_csv("atlas-HPandAMYG_dseg.tsv", sep="\t", na_rep="n/a", index=False)

    # Find values associated with hippocampus and amygdala.
    rois_to_retain = df_sel["index"].values

    # Split out hippocampus and amygdala from 1.6 mm atlas
    img = nb.load("tpl-MNI152NLin6Asym_atlas-HCP_res-06_dseg.nii.gz")
    data = img.get_fdata()
    masked_data = np.isin(data, rois_to_retain) * data
    sel_img = nb.Nifti1Image(masked_data, affine=img.affine, header=img.header)
    sel_img.to_filename("tpl-MNI152NLin6Asym_atlas-HPandAMYG_res-06_dseg.nii.gz")
