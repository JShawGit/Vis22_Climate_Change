import argparse
import json


def get_config():
    """ Gets the configuration of the program. """
    parser = argparse.ArgumentParser(description='Get the configuration input.')
    parser.add_argument(
        '--config', '-c',
        type=str,
        nargs='?',
        required=False,
        help='Load settings from a JSON file.',
        default='../config/configuration.json'
    )
    file = parser.parse_args().config
    with open(file) as fp:
        config = json.load(fp)
    return config
