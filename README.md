# Combining cortical and subcortical atlases for use in XCPD and QSIPrep

There are many popular brain atlases, but they're all in different versions of MNI space. They also cover 
different structures. We want to get them all into one MNI version correctly - using the templateflow 
framework - so they can be used to make structural and functional connectivity matrices.

## Things to worry about

We ultimately want square connectivity matrices with exactly the same regions represented in the rows/columns to come out of xcpd 
and qsiprep. Here are some of the problems we will run into:

 1. Some regions are so small that when they're mapped to a low-res BOLD/DWI volume they will disappear. Should we allow this? 
    In some cases they are from dividing a region into subcomponents. We could recombine them.
 2. Regions may overlap each other from different atlases. Which should have precedence?
 3. For DWI the regions need to be defined *all in the same image*. BOLD regions can be in different images and you can calculate 
    connectivity from their timeseries later. But this isn't possible for DWI. Therefore, we can't include Tian and dwi/CIT168 atlases 
    in the same image

## Strategy to for making the cross-software atlases

Due to worry #3 we are going to pick subcortical atlases that DO NOT have multiple resolutions. Since extremely popular cortical 
atlases have multiple resolutions (i.e. Schaefer) multiple subcortical atlases would explode the number of combined atlases.
For example you would need cortical100+subcortical100, cortical100+subcortical200 ... cortical1000+subcortical1000.

### QSIPrep atlases

| Atlas Name     | MNI Version                | Subcortical | Cerebellum | Thick   |
| :------------: | :------------------------: | :---------: | :--------: | :-----: |
|     AAL116     |           NLin6            |     Yes     |    Yes     |   Yes   |
|    Aicha384    |           NLin6            |     Yes     |     No     |   Yes   |
| Brainnetome246 |           NLin6            |     Yes     |     No     |   No    |
|   Gordon333    |           NLin6            |     No      |     No     |   NOO   |
|    power264    |           NLin6            |     Yes     |    Yes     | Spheres |
|    Schaefer    |           NLin6            |     No      |     No     |   No    |

### XCPD atlases

Should go here


