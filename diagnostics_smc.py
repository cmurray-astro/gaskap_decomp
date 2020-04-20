# @Author: riener
# @Date:   2019-04-02T17:42:46+02:00
# @Filename: decompose--grs.py
# @Last modified by:   riener
# @Last modified time: 2019-04-08T10:33:48+02:00


import os, glob

from gausspyplus.decompose import GaussPyDecompose
from gausspyplus.plotting import plot_spectra
from gausspyplus.utils import spectral_cube_functions

filenames = glob.glob(
    "decomposition/gpy_decomposed/smc_HI_cube_askap_sub_*_g+_fit_fin.pickle"
)
fileprefs = [f.split("_g+_fit")[0] for f in filenames]
fileprefs = [f.split("sub_")[1] for f in fileprefs]

donenames = glob.glob(
    "decomposition/gpy_maps/smc_HI_cube_askap_sub_*_g+_component_map_MW.fits"
)
doneprefs = [f.split("_g+_fit")[0] for f in donenames]
doneprefs = [f.split("sub_")[1] for f in doneprefs]

prefs = [f for f in fileprefs if f not in doneprefs]

for i, filestr in enumerate(prefs):
    #  Initialize the 'GaussPyDecompose' class and read in the parameter settings from 'gausspy+.ini'.
    decompose = GaussPyDecompose(config_file="gausspy+.ini")

    #  Filepath to pickled dictionary of the prepared data.
    decompose.path_to_pickle_file = os.path.join(
        'decomposition', 'gpy_prepared', "smc_HI_cube_askap_sub_" + filestr +'.pickle')
    #
    # # #  Filepath to pickled dictionary of the prepared data.
    path_to_pickled_file = decompose.path_to_pickle_file
     # Filepath to pickled dictionary with the decomposition results
    path_to_decomp_pickle = os.path.join(
        "decomposition",
        "gpy_decomposed",
        "smc_HI_cube_askap_sub_" + filestr + "_g+_fit_fin.pickle",
    )
    print(path_to_decomp_pickle)

    decompose.load_final_results(path_to_decomp_pickle)
    #  (Optional) Produce a FITS image showing the CNM_fraction
    decompose.produce_component_map(vel_range = [80,220], name_str = 'SMC')
    decompose.produce_component_map(vel_range = [-100,80], name_str = 'MW')

    decompose.produce_cnm_map(lw =7., vel_range=[-100,80], name_str = 'MW')
    decompose.produce_cnm_map(lw =7., vel_range=[80,220], name_str = 'SMC')

    decompose.produce_cnm_map(lw =12., vel_range=[-100,80], name_str = 'MW')
    decompose.produce_cnm_map(lw =12., vel_range=[80,220], name_str = 'SMC')

    decompose.produce_nhi_map(vel_range=[-100,80], name_str = 'MW')
    decompose.produce_nhi_map(vel_range=[80,220], name_str = 'SMC')
    decompose.produce_nhi_map(name_str = 'all')
