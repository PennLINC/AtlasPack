# AtlasPack

Combined cortical/subcortical atlases for XCP-D, QSIPrep, and ASLPrep.
The `CIT168`, `thalamus`, `cerebellum`, `hippocampus_and_amygdala`, and `Schaefer`
directories contain scripts that download the atlases from the
internet and process them so they are in NLin6 and NLin2009cAsym space.
The labels are also converted to tsvs with `index` and `name` columns.


## Downloading the atlases

The atlases are distributed as assets on each
[GitHub release](https://github.com/PennLINC/AtlasPack/releases).
You do not need DataLad, git-annex, or a clone of this repository.

```bash
VERSION=0.2.0
curl -fsSLO "https://github.com/PennLINC/AtlasPack/releases/download/${VERSION}/atlaspack-${VERSION}.tar.gz"
curl -fsSLO "https://github.com/PennLINC/AtlasPack/releases/download/${VERSION}/SHA256SUMS"
sha256sum --ignore-missing -c SHA256SUMS   # on macOS: shasum -a 256 --ignore-missing -c SHA256SUMS
tar -xzf "atlaspack-${VERSION}.tar.gz"
```

This creates an `AtlasPack/` directory in
[BIDS-Atlas](https://bids-specification.readthedocs.io/) layout:

```
AtlasPack/
    dataset_description.json
    atlas-4S<N>Parcels_description.json
    tpl-fsLR/
        tpl-fsLR_atlas-4S<N>Parcels_den-91k_dseg.{dlabel.nii,json,tsv}
    tpl-MNI152NLin6Asym/
        tpl-MNI152NLin6Asym_atlas-4S<N>Parcels_res-01_dseg.{nii.gz,json,tsv}
    tpl-MNI152NLin2009cAsym/
        tpl-MNI152NLin2009cAsym_atlas-4S<N>Parcels_res-01_dseg.{nii.gz,json,tsv}
```

`<N>` is 156, 256, ..., 1056 (100-1000 Schaefer parcels plus 56 non-cortical regions).

The same data are available as a Docker image, with the dataset at `/AtlasPack`:

```dockerfile
COPY --from=pennlinc/atlaspack:0.2.0 /AtlasPack /path/to/AtlasPack
```

Earlier copies of these atlases (the DataLad/OSF dataset, the Box tarball, and OSF project `ahf9u`)
are superseded by the GitHub releases.


### How the data are versioned

The JSON and TSV files are tracked in git under `AtlasPack/`.
The images are too large for git, so they are attached to the release instead,
and their SHA-256 checksums are tracked in git in `checksums/atlaspack.sha256`.
So each release tag records exactly which files that release contains.

To fill a clone of this repository with the images for a release:

```bash
git checkout 0.2.0
scripts/fetch_data.sh 0.2.0            # atlas images only
scripts/fetch_data.sh --sources 0.2.0  # also the ~730 MB regeneration inputs
```


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


## Regenerating the atlases

Requirements:

- curl, tar, and sha256sum (or shasum)
- jupyter (`nbconvert`)
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

Steps:

1. `scripts/fetch_data.sh --sources <version>` to get the transforms and intermediate files.
2. `bash 01_combine_subcortical.sh`
3. `bash 02_supplement_schaefers.sh`
4. Copy any changed outputs into `AtlasPack/tpl-<space>/` under their BIDS names.
5. `scripts/update_checksums.sh`, then commit the changes to `AtlasPack/` and `checksums/`.


## Making a release (maintainers)

1. Make sure `AtlasPack/` and the regeneration sources are complete on disk
   (`scripts/fetch_data.sh --sources <previous version>`, plus any regenerated files),
   and that `scripts/update_checksums.sh` produces no changes.
2. Merge to `main` and pull.
3. `scripts/make_release.sh <new version>`.
   This checks every file against the manifests, builds the tarballs in `dist/`,
   and creates a **draft** GitHub release on the current commit.
4. Review the draft on GitHub and publish it.
   Publishing runs `.github/workflows/docker.yml`, which builds and pushes
   `pennlinc/atlaspack:<version>` and `:latest` from the release assets.
   That workflow needs the `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` repository secrets.
