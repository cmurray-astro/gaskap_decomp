# Modified by Claire Murray based on prepare--grs.py by Manuel Riener

import os

from gausspyplus.prepare import GaussPyPrepare
from gausspyplus.plotting import plot_spectra

from gausspyplus.utils import spectral_cube_functions

#  Initialize the 'GaussPyPrepare' class and read in the parameter settings from 'gausspy+.ini'.
prepare = GaussPyPrepare(config_file="gausspy+.ini")

#  The following lines will override the corresponding parameter settings defined in 'gausspy+.ini'.
slices = spectral_cube_functions.get_list_slice_params(
    path_to_file="smc_HI_cube_askap.fits", ncols=8, nrows=8
)
for i, slice in enumerate(slices):
    test, head = spectral_cube_functions.make_subcube(
        slice,
        path_to_file="smc_HI_cube_askap.fits",
        save=True,
        overwrite=True,
        path_to_output_file="sub_cubes/smc_HI_cube_askap_sub_" + str(i) + ".fits",
    )

    prepare.path_to_file = os.path.join(
        "sub_cubes", "smc_HI_cube_askap_sub_" + str(i) + ".fits"
    )

    #  Directory in which all files produced by GaussPy+ are saved.
    prepare.dirpath_gpy = "decomposition"
    #  Prepare the data cube for the decomposition
    prepare.prepare_cube()
    #  (Optional) Produce a FITS image with the estimated root-mean-square values
    prepare.produce_noise_map()

    #  (Optional) Plot some of the spectra and the estimated signal ranges

    #  Filepath to pickled dictionary of the prepared data.
    path_to_pickled_file = os.path.join(
        "decomposition", "gpy_prepared", "smc_HI_cube_askap_sub_" + str(i) + ".pickle"
    )
    #  Directory in which the plots are saved.
    path_to_plots = os.path.join("decomposition", "gpy_plots")
    #  Here we select a subregion of the data cube, whose spectra we want to plot.
    pixel_range = {"x": [30, 34], "y": [25, 29]}
    plot_spectra(
        path_to_pickled_file,
        path_to_plots=path_to_plots,
        signal_ranges=True,
        pixel_range=pixel_range,
    )

components = [
    "decomposition/gpy_maps/smc_HI_cube_askap_sub_" + str(i) + "_noise_map.fits"
    for i in range(64)
]
new_map, new_head = spectral_cube_functions.combine_fields(
    components,
    ncols=8,
    nrows=8,
    path_to_output_file="decomposition/gpy_maps/smc_HI_cube_askap_noise_map.fits",
    save=True,
)
