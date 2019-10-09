import sys

import pytest

from moziris.base.testcase import BaseTest
from moziris.api import *


class Test(BaseTest):
    @pytest.mark.details(
        meta="Sample Test experiment",
        locale=["en-US", "es-ES", "ro"],
        description="Working with debug images.",
        custom_value="ojo",
    )
    def run(self):
        result = exists(Pattern("eyes.png"))
        assert result, "Eyes found"
