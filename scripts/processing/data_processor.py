from processing import read_data
import urllib.request
import pandas as pd
import xarray as xr
import os


def download_data(start_year=2007, end_year=2022):
    """ Downloads data to be used in the program. """

    # Make dirs
    if not os.path.exists('../data/preprocessed/precip/'): os.makedirs('../data/preprocessed/precip/')
    if not os.path.exists('../data/preprocessed/temp/'): os.makedirs('../data/preprocessed/temp/')

    # Global precipitation
    print("Downloading precipitation data...")
    for year in range(start_year, end_year):
        url = f'https://downloads.psl.noaa.gov/Datasets/cpc_us_precip/RT/precip.V1.0.{year}.nc'
        savename = '../data/preprocessed/precip/' + url.split('/')[-1]
        urllib.request.urlretrieve(url, savename)

    # Global temperatures
    print("Downloading temperature data...")
    for year in range(start_year, end_year):
        url = f'https://www.northwestknowledge.net/metdata/data/tmmn_{year}.nc'
        savename = '../data/preprocessed/temp/' + url.split('/')[-1]
        urllib.request.urlretrieve(url, savename)


def get_data(preprocessed='../data/preprocessed_data/', to_get={'precip': 'precip/precip.V1.0.*.nc', 'temp': 'temp/tmmn_*.nc'}):
    preprocessed = '../data/preprocessed/'
    def open_dataset(filename, concat_dim=None, combine='by_coords'):
        print(filename)
        if '*' in filename:
            return xr.open_mfdataset(filename, concat_dim=concat_dim, combine=combine)
        return xr.open_dataset(filename)
    return {item: open_dataset(os.path.abspath(preprocessed + path)) for item, path in to_get.items()}


def filter_netcdf(variables, ranges):
    """
        Filters a netCDF dataset by a list of variables and their ranges.
        https://stackoverflow.com/questions/61990409/how-to-filter-data-by-dimension-in-a-netcdf-file
        :param variables: dict with key: var name, value: netCDF variable
        :param ranges: dict with key: dim name, value: 2-tuple of (start, stop) indices
        :return: variables subsetted according to the supplied ranges, in same format as the input variables dictionary
    """
    subsets = {}
    for varname, v in variables.items():
        subset_args = []
        if v.shape:
            for size, dim in zip(v.shape, v.dimensions):
                if dim in ranges:
                    subset_args.append(slice(*ranges[dim]))
                else:
                    subset_args.append(slice(0, size))
            print(subset_args)
            subsets[varname] = v.__getitem__(subset_args)
        else:
            # scalar
            subsets[varname] = v
    return subsets


def get_variable_values(dataset, variable):
    """
        Return the min and max values of some variable.
        :param dataset: A netCDF dataset.
        :param variable: A netCDF variable name.
        :return: An array of values.
    """
    return dataset.variables[variable][:]


def get_variable_min(dataset, variable):
    """
        Return the min and max values of some variable.
        :param dataset: A netCDF dataset.
        :param variable: A netCDF variable name.
        :return: The minimum value of the variable.
    """
    return dataset.variables[variable][:].min()


def get_variable_max(dataset, variable):
    """
        Return the min and max values of some variable.
        :param dataset: A netCDF dataset.
        :param variable: A netCDF variable name.
        :return: The maximum value of the variable.
    """
    return dataset.variables[variable][:].max()


def get_variable_range(dataset, variable, min_val, max_val):
    """
        Return the min and max values of some variable.
        :param dataset: A netCDF dataset.
        :param variable: A netCDF variable name.
        :param min_val: The minimum range.
        :param max_val: The max range.
        :return: A list of values within range.
    """
    return dataset.variables[variable][(dataset >= min_val) & (dataset <= max_val)]


def get_times(dataset, variable='time'):
    """
        Return the min and max values of some variable.
        :param dataset: A netCDF dataset.
        :param variable: A netCDF variable name.
        :return: Times converted to a pandas datetime format.
    """
    return pd.to_datetime(dataset.variables[variable][:], unit='s')


def get_variable_metadata(dataset, variable, metadata_type=None):
    """
        Return the min and max values of some variable.
        :param dataset: A netCDF dataset.
        :param variable: A netCDF variable name.
        :param metadata_type: The type of metadata to retrieve (optional).
        :return: Times converted to a pandas datetime format.
    """
    data = dataset.variables[variable].__dict__
    if metadata_type is not None:
        data = data[metadata_type]
    return data
