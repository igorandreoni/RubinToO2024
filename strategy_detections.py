import pandas as pd
import numpy as np
from scipy import interpolate

def detections_non_detections(strategies, t, delay_hr, offset_filt_hr=0):
    """Prints the detections and non-detections for each strategy in a structured table format."""

    # For each strategy, create a structured table (DataFrame) for detections and non-detections
    strategy_names = list(strategies.keys())

    for i in range(len(strategy_names)):
        print(f"\nStrategy name: {strategy_names[i]}")

        # Epochs of the strategy in days
        days_strategy = np.array(strategies[strategy_names[i]]["cadence_hr"]) / 24
        depths_strategy = strategies[strategy_names[i]]["depths"]
        filters_strategy = strategies[strategy_names[i]]["filters"]

        # Initialize detections and non-detections as lists to populate the DataFrame later
        detection_data = []
        non_detection_data = []

        # Initialize the possible time offset by filter
        offset_filt_hr_tot = 0

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
            idx = [i for i in np.arange(len(t)) if not np.isnan(t[filt][i])]
            idx = [i for i in idx if not t[filt][i] == np.inf]
            f = interpolate.interp1d(t["t[days]"][idx], t[filt][idx])

            # For each epoch, check if there is the given filter
            for day_strategy, filter_strategy, depth_strategy_epoch in zip(days_strategy, filters_strategy, depths_strategy):
                # Apply the delay between the event and the obs. window
                day_strategy += delay_hr / 24  # from hours to days
                # Apply a delay between filters to show overlapping points
                day_strategy += offset_filt_hr_tot / 24
                if not (filt.replace('lsst', '') in filter_strategy):
                    continue
                else:
                    # Find depth for the given filter
                    idx = filter_strategy.index(filt.replace('lsst', ''))
                    depth = depth_strategy_epoch[idx]

                # Detection or non-detection?
                if f(day_strategy) <= depth:
                    detection_data.append({
                        'Filter': filt.replace('lsst', ''),
                        'Day': day_strategy,
                        'Magnitude': f(day_strategy)
                    })
                else:
                    non_detection_data.append({
                        'Filter': filt.replace('lsst', ''),
                        'Day': day_strategy,
                        'Limiting Magnitude': depth
                    })

        # Convert detections and non-detections to DataFrames
        detections_df = pd.DataFrame(detection_data)
        non_detections_df = pd.DataFrame(non_detection_data)

        # Print the results in a structured DataFrame format
        print("\nDetections:")
        if not detections_df.empty:
            print(detections_df.to_string(index=False))
        else:
            print("No detections.")

        print("\nNon-Detections:")
        if not non_detections_df.empty:
            print(non_detections_df.to_string(index=False))
        else:
            print("No non-detections.")
