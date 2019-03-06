# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from distutils.dir_util import copy_tree
import importlib
import logging
from mozrunner import FirefoxRunner, errors
import os
import pytest
import shutil

from src.core.api.keyboard.keyboard_api import check_keyboard_state
from src.core.util import cleanup
from src.core.util.app_loader import get_app_test_directory
from src.core.util.arg_parser import parse_args
from src.core.util.json_utils import create_target_json
from src.core.util.local_web_server import LocalWebServer
from src.core.util.logger_manager import initialize_logger
from src.core.util.path_manager import PathManager
from src.core.util.system import check_7zip, fix_terminal_encoding, init_tesseract_path, reset_terminal_encoding
from src.core.util.test_loader import sorted_walk

logger = logging.getLogger(__name__)


def main():
    args = parse_args()
    initialize_logger()
    if verify_config(args):
        target_plugin = get_target(args.application)
        pytest_args = get_test_params(args.application)
        initialize_platform(args)
        setup_control_center()
        if args.control:
            launch_control_center()
        pytest.main(pytest_args, plugins=[target_plugin])
    else:
        logger.error('Failed platform verification.')
        exit(1)


def get_target(target_name):
    logger.info('Desired target: %s' % target_name)
    try:
        my_module = importlib.import_module('targets.%s.app' % target_name)
        try:
            target_plugin = my_module.Target()
            logger.info('Found target named %s' % target_plugin.target_name)
            return target_plugin
        except NameError:
            logger.error('Can\'t find default Target class.')
            exit(1)
    except ModuleNotFoundError:
        logger.error('Problems importing module.')
        exit(1)


def initialize_platform(args):
    cleanup.init()
    fix_terminal_encoding()
    PathManager.create_working_directory(args.workdir)
    PathManager.create_run_directory()


def get_test_params(target):
    tests_to_execute = get_app_test_directory(target)
    pytest_args = []

    if tests_to_execute['running']:
        for running in tests_to_execute['running']:
            pytest_args.append(running)

    if tests_to_execute['excluded']:
        for excluded in tests_to_execute['excluded']:
            pytest_args.append('--ignore={}'.format(excluded))

    pytest_args.append('-vs')
    pytest_args.append('-r ')
    pytest_args.append('-s')
    return pytest_args


def verify_config(args):
    """Checks keyboard state is correct, and that Tesseract and 7zip are installed."""
    try:
        if not all([check_keyboard_state(args.no_check), init_tesseract_path(), check_7zip()]):
            exit(1)
    except KeyboardInterrupt:
        exit(1)
    return True


def setup_control_center():
    copy_tree(os.path.join(PathManager.get_module_dir(), 'src', 'control_center', 'assets'), parse_args().workdir)
    targets_dir = os.path.join(PathManager.get_module_dir(), 'targets')

    exclude_dirs = {'__pycache__'}
    for path, dirs, files in sorted_walk(targets_dir):
        [dirs.remove(d) for d in list(dirs) if d in exclude_dirs]
        for target in dirs:
            src = os.path.join(targets_dir, target, 'icon.png')
            dest = os.path.join(parse_args().workdir, 'images', '%s.png' % target)
            try:
                shutil.copyfile(src, dest)
            except FileNotFoundError:
                logger.warning('Could not find icon file for target: %s' % target)
        break
    create_target_json()


def launch_control_center():
    profile_path = os.path.join(parse_args().workdir, 'cc_profile')
    fx_path = PathManager.get_local_firefox_path()
    if fx_path is None:
        logger.error('Can\'t find local Firefox installation, aborting Iris run.')
        return False, None

    args = []
    args.append('-new-tab')
    args.append('http://127.0.0.1:%s' % parse_args().port)
    process_args = {'stream': None}
    fx_runner = FirefoxRunner(binary=fx_path, profile=profile_path,
                           cmdargs=args, process_args=process_args)
    fx_runner.start()
    server = LocalWebServer(parse_args().workdir, parse_args().port)

    # TODO: implement auto-quit detection
    # TODO: pass parameters from Control Center to active target
    #quit_firefox()
    #status = fx_runner.process_handler.wait(Settings.FIREFOX_TIMEOUT)
    #if status is None:
    #    logger.debug('Firefox did not quit. Executing force quit.')
    #    fx_runner.stop()


class ShutdownTasks(cleanup.CleanUp):
    """Class for restoring system state when Iris has been quit.
    """
    @staticmethod
    def at_exit():
        reset_terminal_encoding()
        # TBD:
        # terminate subprocesses
        # remove temp folder(s)
