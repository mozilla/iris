# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import logging

import pytest

from moziris.api import *
from moziris.util.region_utils import RegionUtils
from moziris.util.path_manager import PathManager
from funcy import compose


class BaseTest:
    def setup(self):
        return

    @classmethod
    def setup_class(cls):
        return

    @classmethod
    def teardown_class(cls):
        return

    def setup_method(self, method):
        return

    def teardown_method(self, method):
        return
