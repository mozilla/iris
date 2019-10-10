# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import inspect
import logging
import os
import subprocess
import sys
import tempfile

from moziris.api.enums import Color
from moziris.api.os_helpers import OSHelper

logger = logging.getLogger(__name__)


def _create_tempdir():
    """Creates the temporary directory.
    Writes to the global variable tmp_dir
    :return:
         Path of temporary directory.
    """
    temp_dir = tempfile.mkdtemp(prefix="iris_")
    logger.debug('Created temp dir "%s"' % temp_dir)
    return temp_dir


class _Settings:
    """Class that holds general Iris settings.

    wait_scan_rate              -   The number of times actual pattern search operations are performed per second.
                                    (default - 3)
    type_delay                  -   The number of seconds between each keyboard press. (default - 0)
    move_mouse_delay            -   duration of mouse movement from current location to target location. (default - 0.5
                                    or value selected from Control Center)
    click_delay                 -   The number of seconds a click event is executed after the mouse moves to the target
                                    location. (default - 0)
    min_similarity              -   The default minimum similarity of find operations. While using a Region.find()
                                    operation. Iris searches the region using a default minimum similarity of 0.8.
    auto_wait_timeout           -   The maximum waiting time for all subsequent find operations. (default - 3)
    delay_before_mouse_down     -   Delay before the mouse is put in a held down state.
    delay_before_drag           -   Delay before the drag operation takes place.
    delay_before_drop           -   Delay before the drop operation takes place.
    slow_motion_delay           -   Controls the duration of the visual effect (seconds).
    observe_scan_rate           -   The number of times actual search operations are performed per second while waiting
                                    for a pattern to appear or vanish.
    observe_min_changed_pixels  -   The minimum size in pixels of a change to trigger a change event.
    highlight_duration          -   The duration of the highlight effect.
    highlight_color             -   The rectangle/circle border color for the highlight effect.
    highlight_thickness         -   The rectangle/circle border thickness for the highlight effect.
    mouse_scroll_step           -   The number of pixels for a vertical/horizontal scroll event.
    """

    DEFAULT_MIN_SIMILARITY = 0.8
    DEFAULT_SLOW_MOTION_DELAY = 2
    DEFAULT_OBSERVE_MIN_CHANGED_PIXELS = 50
    DEFAULT_TYPE_DELAY = 0
    DEFAULT_MOVE_MOUSE_DELAY = 0.5
    DEFAULT_CLICK_DELAY = 0
    DEFAULT_WAIT_SCAN_RATE = 3
    DEFAULT_OBSERVE_SCAN_RATE = 3
    DEFAULT_AUTO_WAIT_TIMEOUT = 3
    DEFAULT_DELAY_BEFORE_MOUSE_DOWN = 0.3
    DEFAULT_DELAY_BEFORE_DRAG = 0.3
    DEFAULT_DELAY_BEFORE_DROP = 0.3
    DEFAULT_HIGHLIGHT_DURATION = 2
    DEFAULT_HIGHLIGHT_COLOR = Color.RED
    DEFAULT_HIGHLIGHT_THICKNESS = 2
    DEFAULT_MOUSE_SCROLL_STEP = 100
    DEFAULT_SITE_LOAD_TIMEOUT = 30
    DEFAULT_HEAVY_SITE_LOAD_TIMEOUT = 90
    DEFAULT_KEY_SHORTCUT_DELAY = 0.1
    DEFAULT_UI_DELAY = 1
    DEFAULT_UI_DELAY_SHORT = 0.5
    DEFAULT_UI_DELAY_LONG = 2.5
    DEFAULT_SYSTEM_DELAY = 5
    PACKAGE_ROOT = os.path.realpath(os.path.split(__file__)[0] + "/../..")

    def __init__(
        self,
        wait_scan_rate=DEFAULT_WAIT_SCAN_RATE,
        type_delay=DEFAULT_TYPE_DELAY,
        move_mouse_delay=DEFAULT_MOVE_MOUSE_DELAY,
        click_delay=DEFAULT_CLICK_DELAY,
        min_similarity=DEFAULT_MIN_SIMILARITY,
        auto_wait_timeout=DEFAULT_AUTO_WAIT_TIMEOUT,
        delay_before_mouse_down=DEFAULT_DELAY_BEFORE_MOUSE_DOWN,
        delay_before_drag=DEFAULT_DELAY_BEFORE_DRAG,
        delay_before_drop=DEFAULT_DELAY_BEFORE_DROP,
        slow_motion_delay=DEFAULT_SLOW_MOTION_DELAY,
        observe_scan_rate=DEFAULT_OBSERVE_SCAN_RATE,
        observe_min_changed_pixels=DEFAULT_OBSERVE_MIN_CHANGED_PIXELS,
        system_delay=DEFAULT_SYSTEM_DELAY,
        highlight_duration=DEFAULT_HIGHLIGHT_DURATION,
        highlight_color=DEFAULT_HIGHLIGHT_COLOR,
        highlight_thickness=DEFAULT_HIGHLIGHT_THICKNESS,
        mouse_scroll_step=DEFAULT_MOUSE_SCROLL_STEP,
        key_shortcut_delay=DEFAULT_KEY_SHORTCUT_DELAY,
        site_load_timeout=DEFAULT_SITE_LOAD_TIMEOUT,
    ):

        self.wait_scan_rate = wait_scan_rate
        self._type_delay = type_delay
        self.move_mouse_delay = move_mouse_delay
        self._click_delay = click_delay
        self._min_similarity = min_similarity
        self.auto_wait_timeout = auto_wait_timeout
        self.delay_before_mouse_down = delay_before_mouse_down
        self.delay_before_drag = delay_before_drag
        self.delay_before_drop = delay_before_drop
        self.slow_motion_delay = slow_motion_delay
        self.system_delay = system_delay
        self.observe_scan_rate = observe_scan_rate
        self.observe_min_changed_pixels = observe_min_changed_pixels
        self.highlight_duration = highlight_duration
        self.highlight_color = highlight_color.value
        self.highlight_thickness = highlight_thickness
        self.mouse_scroll_step = mouse_scroll_step
        self.key_shortcut_delay = key_shortcut_delay
        self.site_load_timeout = site_load_timeout
        self.locale = ""
        self.highlight = False
        self.virtual_keyboard = False
        self.debug_image = False
        self.debug_image_path = _create_tempdir()
        self._code_root = trim_path(get_active_root())
        sys.path.append(self._code_root)

    @property
    def click_delay(self):
        return self._click_delay

    @click_delay.setter
    def click_delay(self, value):
        if value > 1:
            self._click_delay = 1
        else:
            self._click_delay = value

    @property
    def debug_image(self):
        return self._debug_image

    @debug_image.setter
    def debug_image(self, value: bool):
        self._debug_image = value

    @property
    def debug_image_path(self):
        return self._debug_image_path

    @debug_image_path.setter
    def debug_image_path(self, value):
        self._debug_image_path = value

    @property
    def highlight(self):
        return self._highlight

    @highlight.setter
    def highlight(self, value: bool):
        self._highlight = value

    @property
    def locale(self):
        return self._locale

    @locale.setter
    def locale(self, value):
        self._locale = value

    @property
    def min_similarity(self):
        return self._min_similarity

    @min_similarity.setter
    def min_similarity(self, value):
        if value > 1:
            self._min_similarity = 1
        else:
            self._min_similarity = value

    @property
    def SITE_LOAD_TIMEOUT(self):
        return self.site_load_timeout

    @property
    def SYSTEM_DELAY(self):
        return self.system_delay

    @property
    def type_delay(self):
        return self._type_delay

    @type_delay.setter
    def type_delay(self, value):
        if value > 1:
            self._type_delay = 1
        else:
            self._type_delay = value

    @property
    def virtual_keyboard(self):
        return self._virtual_keyboard

    @virtual_keyboard.setter
    def virtual_keyboard(self, value):
        self._virtual_keyboard = value

    @property
    def code_root(self):
        return self._code_root

    @code_root.setter
    def code_root(self, value):
        self._code_root = value
        sys.path.append(self._code_root)

    @staticmethod
    def set_code_root_from_caller():
        caller = inspect.stack()[1][1]
        Settings.code_root = os.path.split(caller)[0]


def get_active_root():
    """
    Determine location of targets/tests dynamically, using this priority:
    1. Set by user via environment variable.
    2. Using the Pipfile to locate active project.
    3. If neither of the above, default to package root.
    """
    try:
        path = os.environ["IRIS_CODE_ROOT"]
        if path is not None:
            if os.path.exists(path):
                return path
    except KeyError:
        logger.debug(
            "No code root found in environment variables, trying other methods."
        )

    cmd = subprocess.run(
        "pipenv --where", shell=True, stdout=subprocess.PIPE, timeout=5
    )
    path = cmd.stdout.decode("utf-8").strip()
    if os.path.exists(path):
        return path
    else:
        path_warning()
        return os.path.realpath(os.path.dirname(__file__) + "/../..")


def trim_path(path):
    if path[-1] == "/" or path[-1] == "\\":
        return path[:-1]
    else:
        return path


def path_warning():
    logger.critical("Problems were encountered finding the project code root.")
    logger.critical("If they persist, try setting these environment variables:")
    if OSHelper.is_windows():
        logger.critical("\tset IRIS_CODE_ROOT=%CD%")
        logger.critical("\tset PYTHONPATH=%CD%")
        logger.critical("\nYou must restart your terminal for this to take effect.\n")
    else:
        logger.critical("\texport IRIS_CODE_ROOT=$PWD")
        logger.critical("\texport PYTHONPATH=$PWD")


Settings = _Settings()
