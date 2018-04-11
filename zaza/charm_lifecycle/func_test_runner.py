import argparse
import asyncio
import datetime
import logging
import os
import sys

import zaza.charm_lifecycle.configure as configure
import zaza.charm_lifecycle.destroy as destroy
import zaza.charm_lifecycle.utils as utils
import zaza.charm_lifecycle.prepare as prepare
import zaza.charm_lifecycle.deploy as deploy
import zaza.charm_lifecycle.test as test


def generate_model_name(charm_name, bundle_name):
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '{}{}{}'.format(charm_name, bundle_name, timestamp)


def func_test_runner(keep_model=False):
    """Deploy the bundles and run the tests as defined by the charms tests.yaml

    :param keep_model: Whether to destroy model at end of run
    :type keep_model: boolean
    """
    test_config = utils.get_charm_config()
    for t in test_config['gate_bundles']:
        model_name = generate_model_name(test_config['charm_name'], t)
        # Prepare
        prepare.prepare(model_name)
        # Deploy
        deploy.deploy(
            os.path.join(utils.BUNDLE_DIR, '{}.yaml'.format(t)),
            model_name)
        # Configure
        configure.configure(model_name, test_config['configure'])
        # Test
        test.test(model_name, test_config['tests'])
        if not keep_model:
            # Destroy
            destroy.destroy(model_name)


def parse_args(args):
    """Parse command line arguments

    :param args: List of configure functions functions
    :type list: [str1, str2,...] List of command line arguments
    :returns: Parsed arguments
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--keep-model', dest='keep_model',
                        help='Keep model at the end of the run',
                        action='store_true')
    parser.set_defaults(keep_model=False)
    return parser.parse_args(args)


def main():
    logging.basicConfig(level=logging.INFO)
    args = parse_args(sys.argv[1:])
    func_test_runner(keep_model=args.keep_model)
    asyncio.get_event_loop().close()
