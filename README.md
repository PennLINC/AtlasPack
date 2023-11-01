# AtlasPack

Combined cortical/subcortical atlases for XCP-D, QSIPrep, and ASLPrep.
The `CIT168`, `thalamus`, `cerebellum`, `hippocampus_and_amygdala`, and `Schaefer`
directories contain scripts that download the atlases from the
internet and process them so they are in NLin6 and NLin2009cAsym space.
The labels are also converted to tsvs with `index` and `name` columns.


# Harmonizing the QSIPrep and XCP-D atlases

There are many versions of MNI space.
Unfortunately, many useful atlases are in different versions of MNI space.

Similarly, there are many different brain atlases, each covering different parts of the brain.
It makes sense to combine multiple atlases so we have one parcellation of many brain parts -
but we first have to be certain that the atlases are aligned to the same version of the MNI template.


## Additional between-template transforms

Aligning between versions of MNI templates can be done robustly using TemplateFlow's methodology.
The authors generously shared their code and data with us,
allowing us to create some additional between-template transforms that
are not currently included in TemplateFlow.

In this code repository you can find some scripts where the extra transforms were created.

XCP-D mainly uses MNI152NLin6Asym (FSL, HCP) and MNI152NLin2009cAsym (fmriprep default).

QSIPrep only supports MNI152NLin2009cAsym.

The scripts used to create these transforms are in the `registration_scripts` directory.


## Which atlases were included?


### Thalamus (HCP)

https://zenodo.org/record/1405484

This atlas is in ICBM 2009a Nonlinear Symmetric – 1×1x1mm template, AKA `MNI152NLin2009aSym`.

The NIfTI-1 files representing a digital atlas of seven thalamic subparts per hemisphere,
specifically the maximum likelihood atlas (`Thalamus_Nuclei-HCP-MaxProb.nii.gz`) in MNI space.
The region corresponding to each labeled thalamic part respectively is given in the look-up table
`Thalamic_Nuclei-ColorLUT.txt`.
The NIFTI files can be visualised with the main available tools such as tkmedit, freeview, or 3D-Slicer.

The atlas was built from a subset of the Human Connectome Project (HCP) database
(https://db.humanconnectome.org).

Reference:

> Najdenovska, E., Alemán-Gómez, Y., Battistella, G., Descoteaux, M., Hagmann, P.,
> Jacquemont, S., Maeder, P., Thiran, J., Fornari, E., & Bach Cuadra, M. (2018).
> In-vivo probabilistic atlas of human thalamic nuclei based on diffusion-weighted magnetic
> resonance imaging.
> *Scientific data*, 5(1), 1-11.


### Cerebellum (Diedrichsen)

We downloaded the cerebellar atlas from
https://github.com/DiedrichsenLab/cerebellar_atlases/blob/master/King_2019/atl-MDTB10_space-MNI_dseg.nii.
This atlas is in NLin6 space and the shasum of the repository was `fd12c94`.
Atlas is in FNIRT space - standard FSL space is MNI152NLin6Asym.

Reference:

> King, M., Hernandez-Castillo, C. R., Poldrack, R. A., Ivry, R. B., & Diedrichsen, J. (2019).
> Functional boundaries in the human cerebellum revealed by a multi-domain task battery.
> *Nature neuroscience*, 22(8), 1371-1378.


### Subcortex (CIT168)

We used the CIT168 atlas for subcortical regions.
There are a couple problems with this atlas for our purposes:

 1. The ROIs are not separated into Left and Right hemisphere
 2. Regions 7, 10 and 11 are not likely to survive resampling
 3. There is no thalamus or hippocampus
 4. Region 15 is likely to be outside of any brain mask

We need to get these into shape so we can add them to the other atlases.
The CIT168 atlas does not separate regions into hemispheres,
so we need to split it into left and right hemispheres.
We do this based on the midline of the x-axis.

Reference:

> Pauli, W. M., Nili, A. N., & Tyszka, J. M. (2018).
> A high-resolution probabilistic in vivo atlas of human subcortical brain nuclei.
> *Scientific data*, 5(1), 1-13.


### Hippocampus and Amygdala (HCP)

The CIT168 atlas does not include hippocampus or amygdala,
so we have added these structures, taken from the HCP subcortical CIFTI structures atlas.

The NIfTI file is `tpl-MNI152NLin6Asym_res-06_atlas-HCP_dseg.nii.gz` from TemplateFlow.

Reference:

> Glasser, M. F., Sotiropoulos, S. N., Wilson, J. A., Coalson, T. S., Fischl, B.,
> Andersson, J. L., ... & Wu-Minn HCP Consortium. (2013).
> The minimal preprocessing pipelines for the Human Connectome Project.
> *Neuroimage*, 80, 105-124.


### Cortex (Schaefer)

We used cortical structures from each of the ten resolutions (100 - 1000 parcels)
of the Schaefer 2018 atlas (v0143).

Reference:

> Schaefer, A., Kong, R., Gordon, E. M., Laumann, T. O., Zuo, X. N., Holmes, A. J.,
> Eickhoff, S. B., & Yeo, B. T. (2018).
> Local-global parcellation of the human cerebral cortex from intrinsic functional connectivity MRI.
> *Cerebral cortex*, 28(9), 3095-3114.


## Requirements

- git
- git-annex
- git-annex-remote-osf
- datalad
- wget
- ANTS (antsApplyTransforms)
- Connectome Workbench (wb_command)
- AFNI (3dresample)
- Singularity (only to generate transforms)
- Python 3.8+
    - nibabel
    - numpy
    - pandas
    - scipy
    - tqdm
    - wget


## To regenerate the atlases

1. `bash 01_combine_subcortical.sh`
2. `bash 02_supplement_schaefers.sh`
