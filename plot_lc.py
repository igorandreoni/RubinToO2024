# author: Igor Andreoni <igor.andreoni@gmail.com>

import os
import glob

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from matplotlib.ticker import MaxNLocator
from astropy.cosmology import Planck18 as cosmo
import astropy.cosmology as ac
import astropy.units as u


def get_kne_filename(inj_params_list=None, datadir='models/'):
    """Given kilonova parameters, get the filename from the grid of models
    developed by M. Bulla

    Parameters
    ----------
    inj_params_list : `list` [`dict`]
        parameters for the kilonova model such as
        mass of the dynamical ejecta (mej_dyn), mass of the disk wind ejecta
        (mej_wind), semi opening angle of the cylindrically-symmetric ejecta
        fan ('phi'), and viewing angle ('theta'). For example
        inj_params_list = [{'mej_dyn': 0.005,
              'mej_wind': 0.050,
              'phi': 30,
              'theta': 25.8}]
    """
    # Get files, model grid developed by M. Bulla
    file_list = glob.glob(os.path.join(datadir, "*.dat"))

    # If no specific parameters passed - return everything.
    if inj_params_list is None or len(inj_params_list) == 0:
        return file_list

    # Otherwise find the parameters for each file and
    # then find the relevant matches.
    params = {}
    matched_files = []
    for filename in file_list:
        key = filename.replace(".dat", "").split("/")[-1]
        params[key] = {}
        params[key]["filename"] = filename
        key_split = key.split("_")
        # Binary neutron star merger models
        # FIXME reinstate difference nsns and bns
        # if key_split[0] == "nsns":
        if True:
            mejdyn = float(key_split[2].replace("mejdyn", ""))
            mejwind = float(key_split[3].replace("mejwind", ""))
            phi0 = float(key_split[4].replace("phi", ""))
            theta = float(key_split[5])
            dist_Mpc = float(key_split[6].replace("dMpc", ""))
            params[key]["mej_dyn"] = mejdyn
            params[key]["mej_wind"] = mejwind
            params[key]["phi"] = phi0
            params[key]["theta"] = theta
            params[key]["dMpc"] = dist_Mpc
        # Neutron star--black hole merger models
        #elif key_split[0] == "nsbh":
        #    mej_dyn = float(key_split[2].replace("mejdyn", ""))
        #    mej_wind = float(key_split[3].replace("mejwind", ""))
        #    phi = float(key_split[4].replace("phi", ""))
        #    theta = float(key_split[5])
        #    params[key]["mej_dyn"] = mej_dyn
        #    params[key]["mej_wind"] = mej_wind
        #    params[key]["phi"] = phi
        #    params[key]["theta"] = theta
    for key in params.keys():
        for inj_params in inj_params_list:
            match = all([np.isclose(params[key][var], inj_params[var])
                        for var in inj_params.keys()])
            if match:
                matched_files.append(params[key]["filename"])
                print(f"Found match for {inj_params}")
    print(
        f"Found matches for {len(matched_files)}/{len(inj_params_list)} \
          sets of parameters"
    )

    return matched_files


def getRawPotential(rate, area, time_window, maglim, M):
    """
    How many kilonovae shall we expect given an intrinsic
    BNS merger rate, an area, a time window, given our magnitude
    limit and the peak magnitude of the kilonova?

    Parameters
    ----------
    rate float
        in events/Gpc3/y
    area float
        in deg2
    time_window float
        in days
    maglim float
        magnitude limit (AB)
    Magpeak float
        peak absolute magnitude

    Returns
    -------
    n float
        number of expected events
    """
    # Find the redshift
    z = ac.z_at_value(cosmo.distmod, (maglim - M)*u.mag)
    vol = cosmo.comoving_volume(z).to("Gpc3")
    n = rate * (time_window / 365.) * vol.value * area / 41253

    return n


def doPlotLc(strategies, t, delay_hr, xlim=[0, 7], ylim=[28, 18],
             doShow=True, doSave=True, n_interp=120,
             offset_filt_hr=0,
             outfile_base="plot_lc", outfile_format='pdf',
             event_name="merger",
             filters_color_dict={'u': 'b', 'g': 'g', 'r': 'r', 'i': 'yellow',
                                 'z': 'k', 'y': 'orange'},
             linestyle="-"):
    # Make sure the time starts from zero in the model
    if t["t[days]"][0] == 0:
        pass
    else:
        # Add one row at the top
        t.add_row([0.] + [99. for x in np.arange(len(t.colnames) - 1)])
        # Re-sort
        t.sort("t[days]")
    # For each strategy make a plot
    strategy_names = list(strategies.keys())
    for i in range(len(strategy_names)):
        print(f"\n Strategy name: {strategy_names[i]}")
        # Epochs of the strategy in days
        days_strategy = np.array(strategies[strategy_names[i]]["cadence_hr"]
                                 ) / 24
        depths_strategy = strategies[strategy_names[i]]["depths"]
        filters_strategy = strategies[strategy_names[i]]["filters"]
        # Initialize detections and non-detections
        detections = []
        non_detections = []
        # Initialize the possible time offset by filter
        offset_filt_hr_tot = 0

        # Initialize the figure
        fig, ax = plt.subplots()
        # Blank plot for the detections and non-detections
        ax.plot([], [], label="Det.", color="k",
                marker="o", linestyle="none", markersize=8)
        ax.plot([], [], label="UL", color="k",
                marker="v", linestyle="none", markersize=8)
        for filt in t.colnames:
            # Ignore anything not LSST
            if filt[0] != "l":
                continue
            # Ignore time column
            if filt == "t[days]":
                continue
            # Add the offset by filter
            offset_filt_hr_tot += offset_filt_hr
            # Interpolate to reduce noise
            idx = [i for i in np.arange(len(t)) if
                   np.isnan(t[filt][i]) == False]
            idx = [i for i in idx if not t[filt][i] == np.inf]
            xnew = np.linspace(t["t[days]"][idx].min(),
                               t["t[days]"][idx].max(), n_interp)
            f = interpolate.interp1d(t["t[days]"][idx], t[filt][idx])
            if filt[0] == "l":
                label = f"{filt.replace('lsst', '')}"
            else:
                label = f"Roman {filt.replace('f', 'F')}"
            # Plot the model
            ax.plot(xnew, f(xnew), linestyle=linestyle, label=label,
                    color=filters_color_dict[filt.replace("lsst", "")])
            # for each epoch, check if there is the given filter
            for day_strategy, filter_strategy, depth_strategy_epoch in zip(days_strategy, filters_strategy, depths_strategy):
                # Apply the delay between the event and the obs. window
                day_strategy += delay_hr/24  # from hours to days
                # Apply a delay between filters to show overlapping points
                day_strategy += offset_filt_hr_tot/24
                if not (filt.replace('lsst', '') in filter_strategy):
                    continue
                else:
                    # Find depth for the given filter
                    idx = filter_strategy.index(filt.replace('lsst', ''))
                    depth = depth_strategy_epoch[idx]
                # Detection or non-detection?
                if f(day_strategy) <= depth:
                    detections.append((filt.replace('lsst', ''),
                                       day_strategy, f(day_strategy)))
                    # Plot the detection
                    ax.plot(day_strategy, f(day_strategy), linestyle="none",
                            marker="o", markersize=8,
                            color=filters_color_dict[filt.replace("lsst", "")])
                else:
                    non_detections.append((filt.replace('lsst', ''),
                                           day_strategy, depth))
                    # Plot the non-detection
                    ax.plot(day_strategy, depth, linestyle="none",
                            marker="v", markersize=8,
                            color=filters_color_dict[filt.replace("lsst", "")])

        # Set plot parameters
        plt.rcParams['xtick.labelsize'] = 11
        ax.legend(fontsize=11, loc='center left', bbox_to_anchor=(1, 0.5))
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_xlabel(f"Time from {event_name} (days)", fontsize=13)
        ax.set_ylabel("AB Magnitude", fontsize=13)
        ax.set_title(strategy_names[i], fontsize=13)
        ax.tick_params(axis='both', labelsize=13)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        # Save to file
        if doSave is True:
            out_filename = f"{outfile_base}_{strategy_names[i]}.\
{outfile_format}"
            plt.savefig(out_filename.replace(" ", "_"), bbox_inches='tight')
        if doShow is True:
            plt.show()
        plt.close()
