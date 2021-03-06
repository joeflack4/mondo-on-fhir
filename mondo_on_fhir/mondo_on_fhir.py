"""Mondo on FHIR
"""
import os
import subprocess
from argparse import ArgumentParser
from typing import Dict

import requests
import pandas as pd


# Vars
PKG_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(PKG_DIR, '..')
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
DEFAULTS = {
    'out-dir': PROJECT_DIR,
    'mondo_path': os.path.join(DATA_DIR, 'mondo.owl'),
    'fhir_owl_path': os.path.join(DATA_DIR, 'fhir-owl.jar'),
}


# Functions
# TODO: Add version to download name
def download_dependencies(
    mondo_url='https://github.com/monarch-initiative/mondo/releases/download/v2022-07-01/mondo.owl',
    fhir_owl_url='https://github.com/aehrc/fhir-owl/releases/download/v1.1/fhir-owl-v1.1.jar',
    fhir_owl_path=DEFAULTS['fhir_owl_path'], mondo_path=DEFAULTS['mondo_path']
):
    """Download"""
    if not os.path.exists(mondo_path):
        with open(mondo_path, 'wb') as f:
            resp = requests.get(mondo_url, verify=False)
            f.write(resp.content)
    if not os.path.exists(fhir_owl_path):
        with open(fhir_owl_path, 'wb') as f:
            resp = requests.get(fhir_owl_url, verify=False)
            f.write(resp.content)


# TODO: Utilize args: https://github.com/aehrc/fhir-owl
def run(out_dir) -> Dict[str, pd.DataFrame]:
    """Run
    https://github.com/aehrc/fhir-owl"""
    download_dependencies()
    # TODO: Add version to outfile
    outpath = os.path.join(out_dir, 'mondo.json')
    args = f'java -jar {DEFAULTS["fhir_owl_path"]} -i {DEFAULTS["mondo_path"]} -o {outpath}'
    subprocess.run(args.split(' '))

    return {
        'mondo': pd.DataFrame()  # TODO
    }


def cli_get_parser() -> ArgumentParser:
    """Add required fields to parser."""
    package_description = \
        'Mondo on FHIR'
    parser = ArgumentParser(description=package_description)

    parser.add_argument(
        '-o', '--out-dir',
        default=DEFAULTS['out-dir'],
        help='The directory where results should be saved.')

    return parser


def cli_validate(d: Dict) -> Dict:
    """Validate CLI args. Also updates these args if/as necessary"""
    return d


def cli() -> Dict[str, pd.DataFrame]:
    """Command line interface."""
    parser = cli_get_parser()
    kwargs = parser.parse_args()
    kwargs_dict: Dict = vars(kwargs)
    kwargs_dict = cli_validate(kwargs_dict)
    return run(**kwargs_dict)


# Execution
if __name__ == '__main__':
    cli()
