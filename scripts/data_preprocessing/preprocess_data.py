from termcolor import colored
import data_processor as dp
import pandas as pd
import numpy as np
import read_data
import os

import xarray as xr
#import pymodis

# https://appliedsciences.nasa.gov/sites/default/files/D2P4E_MODISPython.pdf


def find_time_limits(files):
    """
        Find the maximum min times and minimum max times of all the data.
        :param files: The input types and their files as a dictionary.
        :return: The max-min (start) and min-max (end) times.
    """

    def compare_timings(times_dict, min_time, max_time):
        if times_dict["begin"] is None: times_dict["begin"] = min_time
        else: times_dict["begin"] = max(min_time, times_dict["begin"])
        if times_dict["end"] is None: times_dict["end"] = max_time
        else: times_dict["end"] = min(max_time, times_dict["end"])
        return times_dict

    # Search data for the best overlapping timeframes from the total timings
    time_limits = {"begin": None, "end": None}
    for key in list(files.keys()):

        # Make sure the dataset exists
        print(colored(f"\nAttempting to get time limits for {key}...", 'blue'))
        if not files[key]:
            print(colored(f"Error: {key} has no dataset-files.\n", 'red'))
            exit(1)

        # If MODIS data, it has a special case
        if key == 'land':
            print(colored(f"\rProgress: {round((0 / 1) * 100, 2)}%", 'yellow'), end='')
            time_limits = compare_timings(
                time_limits,
                pd.to_datetime({'year': [2001], 'month': [1], 'day': [1]})[0],
                pd.to_datetime({'year': [2020], 'month': [12], 'day': [31]})[0]
            )
            print(colored(f"\rProgress: {round((1 / 1) * 100, 2)}%", 'yellow'), end='')

        # Find the min/max times for ALL items
        else:
            local_times = {
                "begin": pd.to_datetime({'year': [2050], 'month': [1], 'day': [1]})[0],
                "end": pd.to_datetime({'year': [1900], 'month': [1], 'day': [1]})[0]
            }
            n_files = len(files[key])
            i_file = 1
            for file in files[key]:

                # Print Progress
                print(colored(f"\rProgress: {round((float(i_file) / float(n_files)) * 100, 2)}%", 'yellow'), end='')

                # Read in the dataset
                dataset = read_data.read_netcdf(file)

                # Process the min/max values
                times = dataset.time.values
                local_times['begin'] = min(times.min(), local_times['begin'])
                local_times['end'] = max(times.max(), local_times['end'])
                i_file += 1

            # Add the key's min/max times to the total range
            time_limits = compare_timings(time_limits, local_times["begin"], local_times["end"])

        # Print Progress
        print(colored(f"\nSuccessfully got timings for {key}.", 'green'))

    # Return the min/max values
    return time_limits


def split_data_files_by_time(time_limits, data_location, files):
    # Create new directory for new data
    new_folder = os.path.join(data_location, "_data_1_time_split")
    if not os.path.exists(new_folder): os.makedirs(new_folder)

    # Copy data with only valid times to another folder
    for key in list(files.keys()):

        if key == 'land':
            continue

        # Make sure the dataset exists
        print(colored(f"Attempting to split the timings for {key}...", 'blue'))
        if not files[key]:
            print(colored(f"Warning: {key} gives no dataset-files.\n", 'yellow'))
            continue

        # Find the min/max times for ALL items
        n_files = len(files[key])
        i_file = 1
        for file in files[key]:
            print(colored(f"\rProgress: {round((float(i_file) / float(n_files)) * 100, 2)}%", 'yellow'), end='')

            # Remove out-of-bounds entries in the dataframe
            dataset = read_data.read_netcdf(file)
            dataset = dataset.where(
                (dataset.time <= time_limits["end"]) & (dataset.time >= time_limits["begin"]),
                drop=True
            )

            # If not empty, write to file
            new_file = os.path.abspath(os.path.join(new_folder, file.split('/')[-2], file.split('/')[-1]))
            new_split = os.path.split(new_file)[0]
            if not os.path.exists(new_split): os.makedirs(new_split)
            try:
                dataset.to_netcdf(new_file)
            except:
                print(colored(f"\nWarning: Dataset skipped for {key}: {file}.", 'yellow'))
            i_file += 1

        # Print Progress
        print(colored(f"\nSuccessfully split the timings for {key}.\n", 'green'))


def split_data_files_by_location(location_limits, data_location, files):
    # Create new directory for new data
    new_folder = os.path.join(data_location, "_data_2_loc_split")
    if not os.path.exists(new_folder): os.makedirs(new_folder)

    # Copy data with only valid times to another folder
    for key in list(files.keys()):

        if key == 'land':
            continue

        # Make sure the dataset exists
        print(colored(f"Attempting to split locations for {key}...", 'blue'))
        if not files[key]:
            print(colored(f"Warning: {key} gives no dataset-files.\n", 'yellow'))
            continue

        # Find the min/max times for ALL items
        n_files = len(files[key])
        i_file = 1
        for file in files[key]:
            print(colored(f"\rProgress: {round((float(i_file) / float(n_files)) * 100, 2)}%", 'yellow'), end='')

            # Remove out-of-bounds entries in the dataframe
            dataset = read_data.read_netcdf(file)
            if key == 'precip':
                dataset = dataset.where((dataset.lon >= location_limits["longitude"]["min"]), drop=True)
                dataset = dataset.where((dataset.lon <= location_limits["longitude"]["max"]), drop=True)
                dataset = dataset.where((dataset.lat >= location_limits["latitude"]["min"]), drop=True)
                dataset = dataset.where((dataset.lat <= location_limits["latitude"]["max"]), drop=True)
            else:
                dataset = dataset.where((dataset.longitude >= location_limits["longitude"]["min"]), drop=True)
                dataset = dataset.where((dataset.longitude <= location_limits["longitude"]["max"]), drop=True)
                dataset = dataset.where((dataset.latitude >= location_limits["latitude"]["min"]), drop=True)
                dataset = dataset.where((dataset.latitude <= location_limits["latitude"]["max"]), drop=True)

            # If not empty, write to file
            new_file = os.path.abspath(os.path.join(new_folder, file.split('/')[-2], file.split('/')[-1]))
            new_split = os.path.split(new_file)[0]
            if not os.path.exists(new_split): os.makedirs(new_split)
            try:
                dataset.to_netcdf(new_file)
            except:
                print(colored(f"\nWarning: Dataset skipped for {key}: {file}.", 'yellow'))
            i_file += 1

        # Print Progress
        print(colored(f"\nSuccessfully split locations for {key}.\n", 'green'))


def preprocess(data_types, data_locations, coordinate_ranges):
    """
        Preprocesses the data to have matching variable
        values. Writes the results to file.
        :param data_types: The types of data read in.
        :param data_locations: The filepaths of all the data.
        :param coordinate_ranges: The valid coordinates of the data.
        :return: None.
    """
    # Get the input data file paths
    file_paths = {}
    for data_type in data_types:
        data_location = os.path.abspath(os.path.join(data_locations["preprocessed"], data_types[data_type]))
        print(colored(data_location, 'cyan'))
        file_paths[data_type] = read_data.get_directory_files(data_location)
    print(colored(f"----------------------------------------\n", 'blue'))

    # Get the time range of the data
    # time_limits = find_time_limits(file_paths)
    # print(colored(f"----------------------------------------\n", 'blue'))
    time_limits = {
        'begin': np.datetime64('2009-04-20T00:24:57.832712704'),
        'end': np.datetime64('2019-12-31T23:12:47.823288064')
    }
    print(colored(time_limits, 'red'))

    # Write datasets, filtered by time
    """split_data_files_by_time(
        time_limits,
        data_locations["processed_temp"],
        file_paths
    )
    print(colored(f"----------------------------------------\n", 'blue'))"""

    # Get files of the filtered-time datasets
    file_paths = {}
    for data_type in data_types:
        if data_type == 'land': continue
        data_location = os.path.abspath(os.path.join(
            data_locations["processed_temp"], "_data_1_time_split",
            data_types[data_type]
        ))
        print(colored(data_location, 'cyan'))
        file_paths[data_type] = read_data.get_directory_files(data_location)
    print(colored(f"----------------------------------------\n", 'blue'))

    # Filter the datasets by location
    split_data_files_by_location(
        coordinate_ranges,
        data_locations["processed_temp"],
        file_paths
    )
    print(colored(f"----------------------------------------\n", 'blue'))
