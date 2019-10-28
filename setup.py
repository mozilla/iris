# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import platform
from setuptools import setup, find_packages

PACKAGE_NAME = "moziris"
PACKAGE_VERSION = "0.8"

INSTALL_REQUIRES = [
    "bugzilla==1.0.0",
    "coloredlogs==10.0",
    "image==1.5.27",
    "flaky==3.6.1",
    "funcy==1.13",
    "gitpython==3.0.2",
    "more-itertools==7.2.0",
    "mozdownload==1.26",
    "mozinfo==1.1.0",
    "mozinstall==2.0.0",
    "mozrunner==7.7",
    "mozversion==2.2.0",
    "mss==4.0.3",
    "numpy==1.17.2",
    "opencv-python==4.1.1.26",
    "packaging==19.1",
    "psutil==5.6.3",
    "pyautogui==0.9.47",
    "pygithub==1.43.8",
    "pynput==1.4.2",
    "pyperclip==1.7.0",
    "pytesseract==0.3.0",
    "pytest==5.1.2",
    "python-dateutil==2.8.0",
]

if platform.system() == "Linux":
    INSTALL_REQUIRES.append("xlib")

TESTS_REQUIRE = []

DEV_REQUIRES = []

setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    description="Automation tool for visual testing",
    classifiers=[
        "Environment :: Console",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: Microsoft :: Windows :: Windows 8",
        "Operating System :: Microsoft :: Windows :: Windows 8.1",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
    keywords=["automation", "testing"],
    author="Mozilla",
    author_email="mwobensmith@mozilla.com",
    url="https://github.com/mozilla/iris",
    download_url="https://github.com/mozilla/iris/latest.tar.gz",
    license="MPL2",
    packages=find_packages(),
    python_requires=">=3.7.3",
    include_package_data=True,  # See MANIFEST.in
    zip_safe=False,
    use_2to3=False,
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    extras_require={"dev": DEV_REQUIRES},  # For `pip install -e .[dev]`
    entry_points={
        "console_scripts": [
            "iris = moziris.scripts.main:main",
            "api-test = moziris.scripts.test:api_test",
        ]
    },
)
