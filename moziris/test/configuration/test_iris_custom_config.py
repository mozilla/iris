import os
import sys
import pytest
import moziris
from unittest.mock import patch
from moziris.util import arg_parser


with patch.object(
    sys,
    "argv",
    [
        "iris",
        "sample",
        "-a",
        "-b",
        "-c",
        "-d=/iris/tests",
        "-e",
        "-i=DEBUG",
        "-k",
        "-l=en-GB",
        "-m=1",
        "-n",
        "-o",
        "-p=8888",
        "--code_root=/iris",
        "-t=testnamehere",
        "-w=testworkingdir",
        "-x=excludeme",
        "-z",
    ],
):

    test_config = arg_parser.get_core_args()
    from pprint import pprint

    print("\n\n\ntest args:\n")
    pprint(test_config.__dict__)


class TestIrisCustomConfiguration:
    # Check that values are set correctly

    def test_set_target(self):
        target = test_config.target
        assert target == "sample", "target = {}".format(target)

    def test_set_rerun(self):
        rerun = test_config.rerun
        assert rerun

    def test_set_highlight(self):
        highlight = test_config.highlight
        assert highlight

    def test_set_clear(self):
        clear = test_config.clear
        assert clear

    def test_set_test_directory(self):
        test_directory = test_config.directory
        assert test_directory == "/iris/tests", "directory = {}".format(test_directory)

    def test_set_email_report(self):
        email = test_config.email
        assert email

    def test_set_logging_level(self):
        level = test_config.level
        assert level == 10, "level = {}".format(level)

    def test_set_display_control_center(self):
        control = test_config.control
        assert control

    def test_set_locale(self):
        locale = test_config.locale
        assert locale == "en-GB"

    def test_set_max_tries(self):
        max_tries = test_config.max_tries
        assert max_tries == 1, "max_tries = {}".format(max_tries)

    def test_set_no_check(self):
        no_check = test_config.no_check
        assert no_check

    def test_set_override_disabled_tests(self):
        override = test_config.override
        assert override

    def test_set_port(self):
        port = test_config.port
        assert port == 8888, "port = {}".format(port)

    def test_set_code_root(self):
        code_root = test_config.code_root
        assert code_root == "/iris", "code_root = {}".format(code_root)

    def test_set_tests_to_run(self):
        test = test_config.test
        assert test == "testnamehere", "test = {}".format(test)

    @pytest.mark.xfail(reason="still working on file paths in travis")
    def test_set_working_directory(self):
        workdir = test_config.workdir
        assert workdir == "/testworkingdir", "workdir = {}".format(workdir)

    def test_set_excluded_files(self):
        exclude = test_config.exclude
        assert exclude == "excludeme", "exclude = {}".format(exclude)

    def test_set_resize(self):
        resize = test_config.resize
        assert resize
