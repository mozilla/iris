# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
import ctypes
import logging
import re
import subprocess

import pyautogui
import pyperclip

from moziris.api.keyboard.key import Key
from moziris.api.os_helpers import OSHelper

logger = logging.getLogger(__name__)
DEFAULT_KEY_SHORTCUT_DELAY = 0.1
pyautogui.FAILSAFE = False


def get_clipboard():
    """Return the content copied to clipboard."""
    return pyperclip.paste()


def shutdown_process(process_name: str):
    """Checks if the process name exists in the process list and close it ."""

    if OSHelper.is_windows():
        command_str = "taskkill /IM " + process_name + ".exe"
        try:
            subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            logger.error('Command  failed: "%s"' % command_str)
            raise Exception("Unable to run Command.")
    elif OSHelper.is_mac() or OSHelper.is_linux():
        command_str = "pkill " + process_name
        try:
            subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            logger.error('Command  failed: "%s"' % command_str)
            raise Exception("Unable to run Command.")


def is_lock_on(key):
    """Determines if a keyboard key(CAPS LOCK, NUM LOCK or SCROLL LOCK) is ON.

    :param key: Keyboard key(CAPS LOCK, NUM LOCK or SCROLL LOCK).
    :return: TRUE if keyboard_key state is ON or FALSE if keyboard_key state is OFF.
    """
    if OSHelper.is_windows():
        hll_dll = ctypes.WinDLL("User32.dll")
        keyboard_code = 0
        if key == Key.CAPS_LOCK:
            keyboard_code = 0x14
        elif key == Key.NUM_LOCK:
            keyboard_code = 0x90
        elif key == Key.SCROLL_LOCK:
            keyboard_code = 0x91
        try:
            key_state = hll_dll.GetKeyState(keyboard_code) & 1
        except Exception:
            raise Exception("Unable to run Command.")
        if key_state == 1:
            return True
        return False

    elif OSHelper.is_linux() or OSHelper.is_mac():
        try:
            cmd = subprocess.run(
                "xset q", shell=True, stdout=subprocess.PIPE, timeout=20
            )
            shutdown_process("Xquartz")
        except subprocess.CalledProcessError as e:
            logger.error("Command  failed: %s" % repr(e.cmd))
            raise Exception("Unable to run Command.")
        else:
            processed_lock_key = key.value.label
            if "caps" in processed_lock_key:
                processed_lock_key = "Caps"
            elif "num" in processed_lock_key:
                processed_lock_key = "Num"
            elif "scroll" in processed_lock_key:
                processed_lock_key = "Scroll"
            stdout = cmd.stdout.decode("utf-8").split("\n")
            for line in stdout:
                if processed_lock_key in line:
                    values = re.findall(r"\d*\D+", " ".join(line.split()))
                    for val in values:
                        if processed_lock_key in val and "off" in val:
                            return False
        return True


def check_keyboard_state(disable=False):
    """Check Keyboard state.

    Iris cannot run in case Key.CAPS_LOCK, Key.NUM_LOCK or Key.SCROLL_LOCK are pressed.
    """
    if disable:
        return True

    key_on = False
    keyboard_keys = [Key.CAPS_LOCK, Key.NUM_LOCK, Key.SCROLL_LOCK]
    for key in keyboard_keys:
        try:
            if is_lock_on(key):
                logger.error(
                    "Cannot run Iris because %s is on. Please turn it off to continue."
                    % key.value.label.upper()
                )
                key_on = True
                break
        except subprocess.TimeoutExpired:
            logger.error("Unable to invoke xset command.")
            logger.error(
                "Please fix xset on your machine, or turn off keyboard checking with -n flag."
            )
            key_on = True
            break
    return not key_on


def get_active_modifiers(key):
    """Gets all the active modifiers depending on the used OS.

    :param key: Key modifier.
    :return: Returns an array with all the active modifiers.
    """
    all_modifiers = [Key.SHIFT, Key.CTRL]
    if OSHelper.is_mac():
        all_modifiers.append(Key.CMD)
    elif OSHelper.is_windows():
        all_modifiers.append(Key.WIN)
    else:
        all_modifiers.append(Key.META)

    all_modifiers.append(Key.ALT)

    active_modifiers = []
    for item in all_modifiers:
        try:
            for key_value in key:

                if item == key_value.value:
                    active_modifiers.append(item)
        except TypeError:
            if item == key.value:
                active_modifiers.append(item)

    return active_modifiers


def is_shift_character(character):
    """
    Returns True if the key character is uppercase or shifted.
    """
    return character.isupper() or character in '~!@#$%^&*()_+{}|:"<>?'
