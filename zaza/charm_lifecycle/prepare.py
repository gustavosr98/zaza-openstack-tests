"""Run prepare phase."""
import argparse
import copy
import logging
import os
import sys

import zaza.controller

MODEL_DEFAULTS = {
    # Model defaults from charm-test-infra
    #   https://jujucharms.com/docs/2.1/models-config
    'agent-stream': 'proposed',
    'default-series': 'xenial',
    'image-stream': 'daily',
    'test-mode': 'true',
    'transmit-vendor-metrics': 'false',
    # https://bugs.launchpad.net/juju/+bug/1685351
    # enable-os-refresh-update: false
    'enable-os-upgrade': 'false',
    'automatically-retry-hooks': 'false',
    'use-default-secgroup': 'true',
}


def get_model_settings():
    """Construct settings for model from defaults and env variables.

    :returns: Settings to usee for model
    :rtype: Dict
    """
    model_settings = copy.deepcopy(MODEL_DEFAULTS)
    for setting in os.environ.get('MODEL_SETTINGS', '').split(';'):
        if not setting:
            continue
        key, value = setting.split('=')
        model_settings[key.strip()] = value.strip()
    return model_settings


def prepare(model_name):
    """Run all steps to prepare the environment before a functional test run.

    :param model: Name of model to add
    :type bundle: str
    """
    zaza.controller.add_model(model_name, config=get_model_settings())


def parse_args(args):
    """Parse command line arguments.

    :param args: List of configure functions functions
    :type list: [str1, str2,...] List of command line arguments
    :returns: Parsed arguments
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model-name', help='Name of model to add',
                        required=True)
    return parser.parse_args(args)


def main():
    """Add a new model."""
    logging.basicConfig(level=logging.INFO)
    args = parse_args(sys.argv[1:])
    prepare(args.model_name)
