# AtlasPack

Combined cortical/subcortical atlases for xcp-d and qsiprep.
The `CIT168`, `thalamic_atlas`, `cerebellum` and `schaefer_map`
directories contain scripts that download the atlases from the
internet and process them so they are in NLin6 and NLin2009cAsym
space. The labels are also converted to tsvs with `index` and `name`
columns.


# Harmonizing the QSIPrep and XCP-D atlases

There are many versions of MNI space. Unfortunately, many useful atlases are in
different versions of MNI space.

Similarly, there are many different brain atlases, each covering different parts
of the brain. It makes sense to combine multiple atlases so we have one
parcellation of many brain parts - but we first have to be certain that the
atlases are aligned to the same version of the MNI template.


## Additional between-template transforms.

Aligning between versions of MNI templates can be done robustly using
TemplateFlow's methodology. The authors generously shared their code and data
with us, allowing us to create some additional between-template transforms that
are not currently included in TemplateFlow.

In this code repository you can find some scripts where the extra transforms
were created.

XCP-D mainly uses MNI152NLin6Asym (FSL, HCP) and MNI152NLin2009cAsym (fmriprep default).

QSIPrep only supports MNI152NLin2009cAsym.

The scripts used to create these transforms are in the `registration_scripts` directory.


## Which atlases were included?


### Thalamus

https://zenodo.org/record/1405484

This atlas is in ICBM 2009a Nonlinear Symmetric – 1×1x1mm template , AKA `MNI152NLin2009aSym`

From *In-vivo probabilistic atlas of human thalamic nuclei based on diffusion
weighted magnetic resonance imaging* by E. Najdenovska, Y. Aléman-Gómez, et al.
from Lausanne.

The NIfTI-1 files representing a digital atlas of seven thalamic subparts per
hemisphere, specifically the maximum likelihood atlas
(Thalamus_Nuclei-HCP-MaxProb.nii.gz) in MNI space. The region corresponding to
each labeled thalamic part respectively is given in the look-up table
Thalamic_Nuclei-ColorLUT.txt.  The NIFTI files can be visualised with the main
available tools such as tkmedit, freeview or 3D-Slicer.

The atlas was built from a subset of the Human Connectome Project (HCP) database
(https://db.humanconnectome.org).


### Cerebellar

We downloaded the cerebellar atlas from
https://github.com/DiedrichsenLab/cerebellar_atlases/blob/master/King_2019/atl-MDTB10_space-MNI_dseg.nii.
This atlas is in NLin6 space and the shasum of the repository was  fd12c94.
Atlas is in FNIRT space - standard FSL space is MNI152NLin6Asym


### Subcortical (CIT168)

A high-resolution probabilistic in vivo atlas of humansubcortical brain nuclei
In Scientific Data by Wolfgang M. Pauli, Amanda N. Nili & J. Michael Tyszka

We used the CIT168 atlas for subcortical regions. There are a couple problems
with this atlas for our purposes

 1. The ROIs are not separated into Left and Right hemisphere
 2. Regions 7, 10 and 11 are not likely to survive resampling
 3. There is no thalamus or hippocampus
 4. Region 15 is likely to be outside of any brain mask

We need to get these into shape so we can add them to the other atlases. The
CIT168 atlas does not separate regions into hemispheres, so we need to split it
into left and right hemispheres.  We do this based on the midline of the x-axis.


### Cortical (Schaefer)

Schaefer atlases were downloaded from
https://github.com/ThomasYeoLab/CBIG/raw/eca7bc9f63d732834f74b44beac30af360608347/stable_projects/brain_parcellation/Schaefer2018_LocalGlobal/Parcellations/.

For CIFTIs the `Schaefer2018_<n_parcels>Parcels_7Networks_order.dlabel.nii` files were downloaded from the
`HCP/fslr32k/cifti` subfolder.
For NIfTIs the `Schaefer2018_<n_parcels>Parcels_7Networks_order_FSLMNI152_1mm.nii.gz` files were downloaded
from the `MNI` subfolder.

For the CIFTI files, the medial walls were removed.
