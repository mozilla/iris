# import pytest
# import sys
# from unittest.mock import patch
#
# from pprint import pprint
#
#
# @pytest.fixture(scope="class")
# def default_config():
#     with patch.object(sys, "argv", ["iris", "sample", "-n"]):
#         default = arg_parser.get_core_args()
#         print("\n\n\default args:\n")
#         pprint(default.__dict__)
#     yield default
#
#     sys.argv = [sys.argv[0]]
#
#         # return arg_parser.get_core_args()
#
#
# @pytest.fixture(scope="class")
# def custom_config():
#     with patch.object(
#         sys,
#         "argv",
#         [
#             "iris",
#             "sample",
#             "-a",
#             "-b",
#             "-c",
#             "-d=/iris/tests",
#             "-e",
#             "-i=DEBUG",
#             "-k",
#             "-l=en-GB",
#             "-m=1",
#             "-n",
#             "-o",
#             "-p=8888",
#             "--code_root=/iris",
#             "-t=testnamehere",
#             "-w=testworkingdir",
#             "-x=excludeme",
#             "-z",
#         ],
#     ):
#
#         test = arg_parser.get_core_args()
#         print("\n\n\test args:\n")
#         pprint(test.__dict__)
#         yield test
#
#         sys.argv = [sys.argv[0]]
#
#         # return arg_parser.get_core_args()
