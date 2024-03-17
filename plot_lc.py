# author: Igor Andreoni <igor.andreoni@gmail.com>

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from matplotlib.ticker import MaxNLocator
from astropy.cosmology import Planck18 as cosmo
import astropy.cosmology as ac
import astropy.units as u


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
    # For each strategy make a plot
    strategy_names = list(strategies.keys())
    for i in range(len(strategy_names)):
        print(f"\n Strategy name: {strategy_names[i]}")
        # Epochs of the strategy in days
        days_strategy = np.array(strategies[strategy_names[i]]["cadence_hr"]
                                 ) / 24
        depths_strategy = np.array(strategies[strategy_names[i]]["depths"])
        filters_strategy = np.array(strategies[strategy_names[i]]["filters"])
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
            for day_strategy, filter_strategy, depth_strategy in zip(days_strategy, filters_strategy, depths_strategy):
                # Apply the delay between the event and the obs. window
                day_strategy += delay_hr/24  # from hours to days
                # Apply a delay between filters to show overlapping points
                day_strategy += offset_filt_hr_tot/24
                if not (filt.replace('lsst', '') in filter_strategy):
                    continue
                elif f(day_strategy) <= depth_strategy:
                    detections.append((filt.replace('lsst', ''),
                                       day_strategy, f(day_strategy)))
                    # Plot the detection
                    ax.plot(day_strategy, f(day_strategy), linestyle="none",
                            marker="o", markersize=8,
                            color=filters_color_dict[filt.replace("lsst", "")])
                else:
                    non_detections.append((filt.replace('lsst', ''),
                                           day_strategy, depth_strategy))
                    # Plot the non-detection
                    ax.plot(day_strategy, depth_strategy, linestyle="none",
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
