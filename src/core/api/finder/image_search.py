# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import datetime
import logging

import cv2
import numpy as np

try:
    import Image
except ImportError:
    from PIL import Image

from src.core.api.finder.pattern import Pattern
from src.core.api.settings import Settings
from src.core.api.location import Location
from src.core.api.errors import ScreenshotError
from src.core.api.rectangle import Rectangle
from src.core.api.screen.screenshot_image import ScreenshotImage
from src.core.api.enums import MatchTemplateType
from src.core.api.screen.display import DisplayCollection

from src.core.api.save_debug_image.save_image import save_debug_image

logger = logging.getLogger(__name__)

FIND_METHOD = cv2.TM_CCOEFF_NORMED


def is_pattern_size_correct(pattern, region):
    """validates that the pattern is inside the region."""
    p_width, p_height = pattern.get_size()
    r_width = region.width
    r_height = region.height
    is_correct = True

    if p_width > r_width:
        logger.warning('Pattern Width (%s) greater than Region/Screenshot Width (%s)' % (p_width, r_width))
        is_correct = False
    if p_height > r_height:
        logger.warning('Pattern Height (%s) greater than Region/Screenshot Height (%s)' % (p_height, r_height))
        is_correct = False
    return is_correct


def match_template(pattern: Pattern, region: Rectangle = None,
                   match_type: MatchTemplateType = MatchTemplateType.SINGLE):
    """Find a pattern in a Region or full screen

    :param Pattern pattern: Image details
    :param Region region: Region object.
    :param MatchTemplateType match_type: Type of match_template (single or multiple)
    :return: Location.
    """
    if region is None:
        region = DisplayCollection[0].bounds

    locations_list = []
    save_img_location_list = []
    logger.debug('Searching for pattern: %s' % pattern.get_filename())
    if not isinstance(match_type, MatchTemplateType):
        logger.warning('%s should be an instance of `%s`' % (match_type, MatchTemplateType))
        return []
    try:
        stack_image = ScreenshotImage(region=region)
        precision = pattern.similarity

        needle = pattern.get_color_image() if precision == 0.99 else pattern.get_gray_image()
        haystack = stack_image.get_color_image() if precision == 0.99 else stack_image.get_gray_image()

        res = cv2.matchTemplate(np.array(haystack), np.array(needle), FIND_METHOD)
        if match_type is MatchTemplateType.SINGLE:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if max_val >= precision:
                locations_list.append(Location(max_loc[0] + region.x, max_loc[1] + region.y))
                save_img_location_list.append(Location(max_loc[0], max_loc[1]))
        elif match_type is MatchTemplateType.MULTIPLE:
            loc = np.where(res >= precision)
            for pt in zip(*loc[::-1]):
                save_img_location = Location(pt[0], pt[1])
                location = Location(pt[0] + region.x, pt[1] + region.y)
                save_img_location_list.append(save_img_location)
                locations_list.append(location)

        save_debug_image(pattern, stack_image, save_img_location_list)

    except ScreenshotError:
        logger.warning('Screenshot failed.')
        return []

    return locations_list


def image_find(pattern, timeout = None, region = None):
    """ Search for an image in a Region or full screen.

    :param Pattern pattern: Name of the searched image.
    :param timeout: Number as maximum waiting time in seconds.
    :param Region region: Region object.
    :return: Location.
    """
    # if not is_pattern_size_correct(pattern, region):
    #     return None

    if timeout is None:
        timeout = Settings.auto_wait_timeout

    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds=timeout)

    while start_time < end_time:
        time_remaining = end_time - start_time
        logger.debug("Searching for image %s - %s seconds remaining" % (pattern.get_filename(), time_remaining))
        pos = match_template(pattern, region, MatchTemplateType.SINGLE)
        start_time = datetime.datetime.now()

        if len(pos) == 1:
            return pos[0]
    return None


def image_vanish(pattern: Pattern, timeout: float = None, region: Rectangle = None) -> None or bool:
    """ Search if an image is NOT in a Region or full screen.

    :param Pattern pattern: Name of the searched image.
    :param timeout: Number as maximum waiting time in seconds.
    :param Region region: Region object.
    :return: Location.
    """
    if not is_pattern_size_correct(pattern, region):
        return None

    pattern_found = True

    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds=timeout)

    while pattern_found is True and start_time < end_time:
        image_found = match_template(pattern, region, MatchTemplateType.SINGLE)
        if len(image_found) == 0:
            pattern_found = True
        else:
            pattern_found = False
        start_time = datetime.datetime.now()

    return None if pattern_found else True
