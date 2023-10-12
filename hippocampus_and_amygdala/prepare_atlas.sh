#!/bin/bash

# Download the lookup table
wget https://github.com/PennLINC/xcp_d/blob/8a07b53b8a1bb921cd8ca3dc2d23fd09da7982fd/xcp_d/data/atlases/atlas-HCP_dseg.tsv

# Download the 1.6 mm atlas
wget https://github.com/Washington-University/HCPpipelines/blob/21c0867c7f3a59554b9e28f5fe5cddd41e159170/global/templates/170494_Greyordinates/Atlas_ROIs.1.60.nii.gz
mv Atlas_ROIs.1.60.nii.gz tpl-MNI152NLin6Asym_atlas-HCP_res-06_dseg.nii.gz

python split_regions.py
