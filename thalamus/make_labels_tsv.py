"""Make segmentation labels file."""
import pandas as pd

indexes = []
names = []
colors = []

with open("Thalamic_Nuclei-ColorLUT.txt", "r") as f:
    for fullline in f:
        line = fullline.strip()
        if not line or not line[0] in "123456789":
            continue
        roinum, roilabel, r, g, b, a = line.split()
        indexes.append(int(roinum))
        names.append(roilabel)
        colors.append("%02x%02x%02x" % (int(r), int(g), int(b)))

df = pd.DataFrame({"index": indexes, "name": names, "color": colors})

df.to_csv("atlas-hcpthalamus.tsv", index=False, sep="\t")
