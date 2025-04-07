"""
micromind helper functions.

Authors:
    - Francesco Paissan, 2023
"""
import sys
from pathlib import Path
from typing import Dict, Union
from argparse import Namespace

import argparse


def override_conf(hparams: Dict):
    """Handles command line overrides. Takes as input a configuration
    and defines all the keys as arguments. If passed from command line,
    these arguments override the default configuration.

    Arguments
    ---------
    hparams : Dict
        Dictionary containing current configuration.

    Returns
    -------
    Configuration agumented with overrides. : Namespace

    """
    parser = argparse.ArgumentParser()
    for key, value in hparams.items():
        parser.add_argument(
            f"--{key}", type=str2bool if isinstance(value, bool) else type(value), default=value)

    args, extra_args = parser.parse_known_args()
    for key, value in vars(args).items():
        if value is not None:
            hparams[key] = value

    return Namespace(**hparams)


def parse_configuration(cfg: Union[str, Path]):
    """Parses default configuration and compares it with user defined.
    It processes a user-defined python file that creates the configuration.
    Additionally, it handles eventual overrides from command line.

    Arguments
    ---------
    cfg : Union[str, Path]
        Configuration file defined by the user

    Returns
    -------
    Configuration Namespace. : argparse.Namespace

    """
    with open(cfg, "r") as f:
        conf = f.read()

    local_vars = {}

    exec(conf, {}, local_vars)

    return override_conf(local_vars)


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_run_params(run_id: str, tracking_uri: str = None) -> Dict:
    """Retrieve run params using the run id. If `tracking_uri` 
    is specified, it will be set for mlflow.

    Arguments
    ---------
    run_id : str
        id of the run to retrive the params
    tracking_uri:
        from mlflow documentation:
            - An empty string, or a local file path, prefixed with ``file:/``. Data is stored
              locally at the provided file (or ``./mlruns`` if empty).
            - An HTTP URI like ``https://my-tracking-server:5000``.
            - A Databricks workspace, provided as the string "databricks" or, to use a Databricks
              CLI `profile <https://github.com/databricks/databricks-cli#installation>`_,
              "databricks://<profileName>".
            - A :py:class:`pathlib.Path` instance


    Returns
    -------
    Parameters dictionary. : Dict[str, Any]
    """
    import mlflow
    import mlflow.tracking

    if tracking_uri:
        mlflow.set_tracking_uri(tracking_uri)
    client = mlflow.tracking.MlflowClient(tracking_uri)
    run = client.get_run(run_id)
    run_params = run.data.params
    return run_params


def export_configuration(dictionary: Dict, file_path: str) -> None:
    """Write dictionary contents to a file with one key-value pair per line.

    Arguments
    ---------
    dictionary : Dict
        Dictionary to write to file
    file_path : str
        Path to output file

    Returns
    -------
    None
    """
    with open(file_path, 'w') as f:
        for key, value in dictionary.items():
            f.write(f"{key}={value}\n")


def parse_configuration_yaml(cfg: Union[str, Path]):
    import yaml
    """Parses a YAML configuration file.

    Arguments
    ---------
    cfg : Union[str, Path]
        Path to YAML configuration file

    Returns
    -------
    Configuration Namespace. : argparse.Namespace
    """

    with open(cfg, "r") as f:
        local_vars = yaml.safe_load(f)
    return override_conf(local_vars)
