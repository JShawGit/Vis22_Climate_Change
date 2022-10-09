from termcolor import colored
import data_processor
import pandas as pd
import numpy as np
import read_data
import netCDF4
import shutil
import sys
import os

# R utils
"""
os.environ["R_HOME"] = r"..\R-4.2.1"
import rpy2.robjects.packages as rpackages
utils = rpackages.importr('utils')
utils.chooseCRANmirror(ind=1)
utils.install_packages("MODIStsp")
MODIS = rpackages.importr('MODIStsp')
"""


def metadata_from_modis_files(data_location):
    """
        Gets useful information from MODIS data filenames.
        :param data_location: Location of all the modis files
        :return: A dictionary of filenames and their metadata.
    """
    filepaths = read_data.get_directory_files(data_location)
    metadata = {}
    for filepath in filepaths:
        file = filepath.split('/')[-1]
        metadata[file] = {
            'satellite': file[:3],
            'start_time': pd.Timestamp(year=int(file[9:13]), month=1, day=1),
            'end_time': pd.Timestamp(year=int(file[28:32]), month=12, day=31),
            'horiz': file[18:20],
            'vert': file[21:23]
        }
    return metadata


def find_time_limits(files):
    """
        Find the maximum min times and minimum max times of all the data.
        :param files: The input types and their files as a dictionary.
        :return: The max-min (start) and min-max (end) times.
    """
    # Search data for the best overlapping timeframes from the total timings
    time_limits = {"start": None, "end": None}
    for key in list(files.keys()):

        if key == 'land':
            continue

        # Make sure the dataset exists
        print(colored(f"Attempting to get timings for {key}...", 'blue'))
        if not files[key]:
            print(colored(f"Warning: {key} gives no dataset-files.\n", 'yellow'))
            continue

        # Check if MODIS data
        if key == 'land':
            continue
            metadata = files['key'][list(files['key'].keys())[0]]
            time_min = metadata['start_time']
            if time_limits["start"] is None or time_min > time_limits["start"]:
                time_limits["start"] = time_min
            time_max = metadata['end_time']
            if time_limits["end"] is None or time_max < time_limits["end"]:
                time_limits["end"] = time_max

        # Find the min/max times for ALL items
        n_files = len(files[key])
        i_file = 1
        for file in files[key]:

            # Print Progress
            print(colored(f"\rProgress: {round((float(i_file)/float(n_files))*100, 2)}%", 'yellow'), end='')

            # Read in the dataset
            dataset = read_data.read_netcdf(file, False)

            time_min = dataset['time'].min()
            if time_limits["start"] is None or time_min > time_limits["start"]:
                time_limits["start"] = time_min
            time_max = dataset['time'].max()
            if time_limits["end"] is None or time_max < time_limits["end"]:
                time_limits["end"] = time_max
            i_file += 1

        # Print Progress
        print(colored(f"\nSuccessfully got timings for {key}.\n", 'green'))

    # Return the min/max values
    return time_limits


def split_data_files_by_time_and_location(time_limits, location_limits, data_location, files):

    # Create new directory for new data
    new_folder = os.path.join(data_location, "_data_split")
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
            print(colored(f"\rProgress: {round((float(i_file)/float(n_files))*100, 2)}%", 'yellow'), end='')

            # Remove out-of-bounds entries in the dataframe
            latitude = 'latitude'
            longitude = 'longitude'
            if key == 'precip':
                latitude = 'lat'
                longitude = 'lon'
            dataset = read_data.read_netcdf(file, False)
            dataset = dataset[
                (dataset['time'] <= time_limits["start"]) &
                (dataset['time'] >= time_limits["end"]) &
                (dataset[latitude] <= location_limits['latitude']['max']) &
                (location_limits['latitude']['min'] <= dataset[latitude]) &
                (dataset[longitude] <= location_limits['longitude']['max']) &
                (location_limits['longitude']['min'] <= dataset[longitude])
            ]

            # If not empty, write to file
            if not dataset.empty:
                new_file_name = file.split('/')[-1].split('.')[0] + '.csv'
                new_file = os.path.join(new_folder, file.split('/')[-2], new_file_name)
                new_split = os.path.split(new_file)[0]
                if not os.path.exists(new_split): os.makedirs(new_split)
                dataset.to_csv(new_file)
            else:
                print(colored(f"\nWarning: Dataset skipped for {key}.", 'red'))
            i_file += 1

        # Print Progress
        print(colored(f"\nSuccessfully split the timings for {key}.\n", 'green'))
    print(colored(f"----------------------------------------\n", 'blue'))


def preprocess(data_types, data_locations, location_limits):
    """
        Preprocesses the data to have matching variable
        values. Writes the results to file.
        :param data: The input types and their files as a dictionary.
        :return: None.
    """
    # Get the data files
    files = {}
    for data_type in data_types:
        data_location = os.path.join(data_locations["preprocessed"], data_types[data_type])
        if data_type == 'land':
            files[data_type] = metadata_from_modis_files(data_location)
        path = os.path.join(data_location)
        files[data_type] = read_data.get_directory_files(path)

    # Find the proper time minimums and maximums
    # time_limits = find_time_limits(files)
    time_limits = {
        'start': pd.Timestamp('2019-12-31 00:00:03.385014784'),
        'end': pd.Timestamp('2009-04-20 23:35:46.631379456')
    }

    print(colored(time_limits, 'red'))

    # Copy the datasets that are within the correct timeframe to a specific folder
    split_data_files_by_time_and_location(
        time_limits,
        location_limits,
        data_locations["processed_temp"],
        files
    )
