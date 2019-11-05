import sys
import pytest
from unittest.mock import patch
from moziris.util import arg_parser

with patch.object(sys, "argv", ["iris", "sample", "-n"]):
    default_config = arg_parser.get_core_args()


class TestIrisConfigDefault:
    def test_default_target(self):
        target = default_config.target
        assert target == "sample", "target = {}".format(target)

    def test_default_rerun(self):
        rerun = default_config.rerun
        assert rerun is False

    def test_default_highlight(self):
        highlight = default_config.highlight
        assert highlight is False

    def test_default_clear(self):
        clear = default_config.clear
        assert clear is False

    def test_default_test_directory(self):
        test_directory = default_config.directory
        assert test_directory == "", "directory = {}".format(test_directory)

    def test_default_email_report(self):
        email = default_config.email
        assert email is False

    def test_default_logging_level(self):
        level = default_config.level
        assert level == 20, "level = {}".format(level)

    def test_default_display_control_center(self):
        control = default_config.control
        assert control is False

    def test_default_locale(self):
        locale = default_config.locale
        assert locale == "en-US"

    def test_default_max_tries(self):
        max_tries = default_config.max_tries
        assert max_tries == 3, "max_tries = {}".format(max_tries)

    def test_default_no_check(self):
        no_check = default_config.no_check
        assert no_check is True

    def test_default_override_disabled_tests(self):
        override = default_config.override
        assert override is False

    def test_default_port(self):
        port = default_config.port
        assert port == 2000, "port = {}".format(port)

    def test_default_code_root(self):
        code_root = default_config.code_root
        assert code_root is None, "code_root = {}".format(code_root)

    def test_default_tests_to_run(self):
        test = default_config.test
        assert test == "", "test = {}".format(test)

    def test_default_excluded_files(self):
        exclude = default_config.exclude
        assert exclude == "", "exclude = {}".format(exclude)

    def test_default_resize(self):
        resize = default_config.resize
        assert resize is False

    def test_default_virtual_keyboard(self):
        virtual_keyboard = default_config.virtual_keyboard
        assert virtual_keyboard is False
