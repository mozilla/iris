# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import inspect
import logging
import os

import cv2
import numpy as np

from moziris.api.errors import APIHelperError, FindError
from moziris.api.location import Location
from moziris.api.os_helpers import OSHelper
from moziris.api.settings import Settings

try:
    import Image
except ImportError:
    from PIL import Image

logger = logging.getLogger(__name__)


class Pattern:
    """A Pattern represents a file on disk that will be used in an on-screen find operation.

    Iris searches a given region using the Pattern, with a default minimum similarity of 0.8.
    This default value can be changed in Settings.min_similarity. Using similar() you can
    change this minimum value on an instance basis when this Pattern object is searched.
    """

    def __init__(self, image_name: str, from_path: str = None):
        self.caller = inspect.stack()[1][1]
        self.temp_name = image_name
        self.similarity = Settings.min_similarity
        self.loaded = False
        if from_path is not None:
            self.load_pattern(path=from_path)

    def load_pattern(self, path=None):
        if self.loaded:
            return

        if path is None:
            path = _get_image_path(self.caller, self.temp_name)

        name, scale = _parse_name(os.path.split(path)[1])
        image = cv2.imread(path, cv2.IMREAD_COLOR)

        self.image_name = name
        self.image_path = path
        self.scale_factor = scale
        self._target_offset = None
        self._size = _get_pattern_size(image, scale)
        self.rgb_array = _get_array_from_image(image)
        self.color_image = _get_image_from_array(scale, self.rgb_array)
        self.gray_image = _get_gray_image(self.color_image)
        self.gray_array = _get_array_from_image(self.gray_image)
        self.loaded = True

    def __str__(self):
        self.load_pattern()
        return "(%s, %s, %s, %s)" % (
            self.image_name,
            self.image_path,
            self.scale_factor,
            self.similarity,
        )

    def __repr__(self):
        self.load_pattern()
        return "%s(%r, %r, %r, %r)" % (
            self.__class__.__name__,
            self.image_name,
            self.image_path,
            self.scale_factor,
            self.similarity,
        )

    def target_offset(self, dx: int, dy: int):
        """Add offset to Pattern from top left.

        :param int dx: x offset from center.
        :param int dy: y offset from center.
        :return: A new pattern object.
        """
        self.load_pattern()
        new_pattern = Pattern(self.image_name, from_path=self.image_path)
        new_pattern._target_offset = Location(dx, dy)
        return new_pattern

    def get_filename(self):
        """Getter for the image_name property."""
        self.load_pattern()
        return self.image_name

    def get_file_path(self):
        """Getter for the image_path property."""
        self.load_pattern()
        return self.image_path

    def get_target_offset(self):
        """Getter for the target_offset property."""
        self.load_pattern()
        return self._target_offset

    def get_scale_factor(self):
        """Getter for the scale_factor property."""
        self.load_pattern()
        return self.scale_factor

    def get_rgb_array(self):
        """Getter for the RGB array of image."""
        self.load_pattern()
        return self.rgb_array

    def get_color_image(self):
        """Getter for the color_image property."""
        self.load_pattern()
        return self.color_image

    def get_gray_image(self):
        """Getter for the gray_image property."""
        self.load_pattern()
        return self.gray_image

    def get_gray_array(self):
        """Getter for the gray_array property."""
        self.load_pattern()
        return self.gray_array

    def similar(self, value: float):
        """Set the minimum similarity of the given Pattern object to the specified value."""
        if value > 0.99:
            self.similarity = 0.99
        elif 0.0 <= value and value <= 0.99:
            self.similarity = value
        else:
            self.similarity = Settings.min_similarity
        return self

    def exact(self):
        """Set the minimum similarity of the given Pattern object to 0.99, which means exact match is required."""
        self.similarity = 0.99
        return self

    def get_size(self):
        """Getter for the _size property."""
        self.load_pattern()
        return self._size

    def get_color_array(self):
        """Encode color image to BGR2RGB """
        self.load_pattern()
        return cv2.cvtColor(np.array(self.color_image), cv2.COLOR_BGR2RGB)


def _parse_name(full_name: str) -> (str, int):
    """Detects the scale factor in image name.

    :param str full_name: Image full name. Valid format name@[scale_factor]x.png.
    Examples: google_search@2x.png, amazon_logo@2.5x.png

    :return: Pair of image name and scale factor.
    """
    start_symbol = "@"
    end_symbol = "x."
    if start_symbol not in full_name:
        return full_name, 1
    else:
        try:
            start_index = full_name.index(start_symbol)
            end_index = full_name.index(end_symbol, start_index)
            scale_factor = float(full_name[start_index + 1 : end_index])
            image_name = (
                full_name[0:start_index] + full_name[end_index + 1 : len(full_name)]
            )
            return image_name, scale_factor
        except ValueError:
            logger.warning('Invalid file name format: "%s".' % full_name)
            return full_name, 1


def _apply_scale(scale: int, rgb_array):
    """Resize the image for HD images.

    :param scale: Scale of image.
    :param rgb_array: RGB array of image.
    :return: Scaled image.
    """
    if scale > 1:
        temp_h, temp_w, not_needed = rgb_array.shape
        new_w, new_h = int(temp_w / scale), int(temp_h / scale)
        return cv2.resize(rgb_array, (new_w, new_h), interpolation=cv2.INTER_AREA)
    else:
        return rgb_array


def _get_array_from_image(image: Image):
    """Returns np array from an Image."""
    if image is None:
        return None
    return np.array(image)


def _get_pattern_size(image: Image, scale: float) -> (int, int):
    """Returns a tuple with values for image width and height"""
    if image is None or scale is None:
        return None
    height, width, channel = image.shape
    return int(width / scale), int(height / scale)


def _get_image_from_array(scale: int, array) -> Image:
    """Converts a scaled array into Image."""
    if scale is None or array is None:
        return None
    return Image.fromarray(_apply_scale(scale, array))


def _get_gray_image(colored_image: Image) -> Image:
    """Converts colored image to gray image."""
    if colored_image is None:
        return None
    return colored_image.convert("L")


def _get_image_path(caller, image: str) -> str:
    """Enforce proper location for all Pattern creation.

    :param caller: Path of calling Python module.
    :param image: String filename of image.
    :return: Full path to image on disk.

    We will look at all possible paths relative to the calling file, with this priority:

    - current platform locale folder
    - common locale folder
    - current platform root
    - common root

    Each directory is scanned for four possible file names, depending on resolution.
    If we find nothing, we will raise an exception.
    """

    module = os.path.split(caller)[1]
    module_directory = os.path.split(caller)[0]
    file_name = image.split(".")[0]
    names = [image, "%s@2x.png" % file_name]

    if OSHelper.get_os_version() == "win7":
        os_version = "win7"
    else:
        os_version = OSHelper.get_os().value
    paths = []

    current_locale = Settings.locale
    platform_directory = os.path.join(module_directory, "images", os_version)

    if current_locale != "":
        platform_locale_directory = os.path.join(platform_directory, current_locale)
        for name in names:
            paths.append(os.path.join(platform_locale_directory, name))

    common_directory = os.path.join(module_directory, "images", "common")

    if current_locale != "":
        common_locale_directory = os.path.join(common_directory, current_locale)
        for name in names:
            paths.append(os.path.join(common_locale_directory, name))

    for name in names:
        paths.append(os.path.join(platform_directory, name))

    for name in names:
        paths.append(os.path.join(common_directory, name))

    found = False
    image_path = None
    for path in paths:
        if os.path.exists(path):
            found = True
            image_path = path
            break

    logger.debug("Module %s requests image %s" % (module, image))
    if found:
        logger.debug("Found %s" % image_path)
        return image_path
    else:
        raise APIHelperError("Image not found")
