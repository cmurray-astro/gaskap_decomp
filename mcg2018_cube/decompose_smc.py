# Modified by Claire Murray based on decompose--grs.py by Manuel Riener

import os, glob

from gausspyplus.decompose import GaussPyDecompose
from gausspyplus.plotting import plot_spectra
from gausspyplus.utils import spectral_cube_functions

#  The following lines will override the corresponding parameter settings defined in 'gausspy+.ini'.

filenames = glob.glob("decomposition/gpy_prepared/smc_HI_cube_askap_sub_*.pickle")
fileprefs = [f.split("gpy_prepared/")[1] for f in filenames]
donenames = glob.glob(
    "decomposition/gpy_decomposed/smc_HI_cube_askap_sub_*_g+_fit_fin.pickle"
)
doneprefs = [f.split("gpy_decomposed/")[1] for f in donenames]
doneprefs = [f.split("_g+_fit")[0] for f in doneprefs]
doneprefs = [f + ".pickle" for f in doneprefs]

notdones = [f for f in fileprefs if f not in doneprefs]
filenames = ["decomposition/gpy_prepared/" + f for f in notdones]
print(filenames)

for i, filename in enumerate(filenames):
    print(filename)
    if (filename != 'decomposition/gpy_prepared/smc_HI_cube_askap_sub_40.pickle') and (filename != 'decomposition/gpy_prepared/smc_HI_cube_askap_sub_16.pickle') and (filename != 'decomposition/gpy_prepared/smc_HI_cube_askap_sub_24.pickle') and (filename != 'decomposition/gpy_prepared/smc_HI_cube_askap_sub_32.pickle') :
        filestr = filename.split(".pickle")[0]
        filestr = filestr.split("sub_")[1]
        #  Filepath to pickled dictionary of the prepared data.

        #  Initialize the 'GaussPyDecompose' class and read in the parameter settings from 'gausspy+.ini'.
        decompose = GaussPyDecompose(config_file="gausspy+.ini")

        decompose.path_to_pickle_file = filename
        #  First smoothing parameter
        decompose.alpha1 = 1.13
        #  Second smoothing parameter
        decompose.alpha2 = 2.06
        #  We set the upper limit for the reduced chi-square deliberately to a low value to enforce the best fitting results for each individual spectrum.
        decompose.rchi2_limit = 2.0
        #  Suffix for the filename of the pickled dictionary with the decomposition results.
        decompose.suffix = "_g+"
        #  Start the decomposition.
        decompose.decompose()

        #  (Optional) Produce a FITS image showing the number of fitted components
        decompose.produce_component_map()
        #  (Optional) Produce a FITS image showing the reduced chi-square values
        decompose.produce_rchi2_map()

        #  (Optional) Plot some of the spectra and the decomposition results

        #  Filepath to pickled dictionary of the prepared data.
        path_to_pickled_file = decompose.path_to_pickle_file

        #  Filepath to pickled dictionary with the decomposition results
        path_to_decomp_pickle = os.path.join(
            "decomposition",
            "gpy_decomposed",
            "smc_HI_cube_askap_sub_" + filestr + "_g+_fit_fin.pickle",
        )

        #  Directory in which the plots are saved.
        path_to_plots = os.path.join("decomposition", "gpy_plots")
        #  Here we select a subregion of the data cube, whose spectra we want to plot.
        pixel_range = {"x": [30, 34], "y": [25, 29]}
        plot_spectra(
            path_to_pickled_file,
            path_to_plots=path_to_plots,
            path_to_decomp_pickle=path_to_decomp_pickle,
            signal_ranges=True,
            pixel_range=pixel_range,
        )
        del decompose

components = [
    "decomposition/gpy_maps/smc_HI_cube_askap_sub_" + str(i) + "_g+_rchi2_map.fits"
    for i in range(64)
]
new_map, new_head = spectral_cube_functions.combine_fields(
    components,
    ncols=8,
    nrows=8,
    path_to_output_file="decomposition/gpy_maps/galfa_llcc_g+_rchi2_map.fits",
    save=True,
)

components = [
    "decomposition/gpy_maps/smc_HI_cube_askap_sub_" + str(i) + "_g+_component_map.fits"
    for i in range(64)
]
new_map, new_head = spectral_cube_functions.combine_fields(
    components,
    ncols=8,
    nrows=8,
    path_to_output_file="decomposition/gpy_maps/galfa_llcc_g+_component_map.fits",
    save=True,
)
