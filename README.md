# moziris

![Travis (.com)](https://img.shields.io/travis/com/mozilla/iris)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/moziris)
![GitHub](https://img.shields.io/github/license/mozilla/iris)
![GitHub repo size](https://img.shields.io/github/repo-size/mozilla/iris)
![GitHub issues](https://img.shields.io/github/issues/mozilla/iris)

Mozilla Iris is a tool that uses on-screen pattern and text matching, while manipulating a machine's mouse and keyboard, to test visual and interactive states of an application.
For more detailed information and troubleshooting tips, please [view our wiki](https://github.com/mozilla/iris/wiki).

## Installation

### Mac instructions:

#### System Requirements

 - Python 3
 - git
 - [Firefox](https://www.mozilla.org/en-US/firefox/new/)

#### Setup

```
git clone https://github.com/mozilla/iris
# Run the Mac bootstrap script
cd iris
./bootstrap/bootstrap.sh
# Run this command to agree to xcode terms of service
sudo xcodebuild -license accept
```
 - **Restart** your Mac in order for certain libraries to be recognized
 - In System Preferences, go to Mission Control and change the keyboard shortcut for "Application Windows" to "-", or none
 - Launch Iris
```
cd iris
pipenv install
pipenv shell
iris sample
```

### Windows 7 / Windows 10 Professional instructions:

#### System Requirements

 - Python 3
 - git
 - [Firefox](https://www.mozilla.org/en-US/firefox/new/)
 - [Powershell 3](https://www.microsoft.com/en-us/download/details.aspx?id=34595)
 - [.NET framework version 4.5](https://www.microsoft.com/en-us/download/details.aspx?id=30653)

#### Setup

```
git clone https://github.com/mozilla/iris
cd iris
bootstrap\bootstrap.sh
# Install project requirements and activate the virtualenv
pipenv install
pipenv shell
# Run Iris
iris sample
```

### Ubuntu Linux 16.04 instructions:

#### System Requirements

 - Python 3
 - git
 - [Firefox](https://www.mozilla.org/en-US/firefox/new/)
 - [Follow instructions below for disabling Keyring](https://github.com/mozilla/iris/wiki/Setup#disable-system-keyring)
 - Open Settings > Displays > "Scale for Menu and Title bars:" and verify that it is set to 1

#### Setup
```
git clone https://github.com/mozilla/iris
cd iris
./bootstrap/bootstrap.sh
# Note: This will take around 10 minutes to download, compile, and install dependencies
# Run the following commands to complete installation and launch Iris
pipenv install
pipenv shell
iris sample
```

## Usage

The Iris project is meant to be used with your own "target" and tests. A target is basically a pytest plugin invoked by Iris, which will then gather data during the run to present in a web-based interface known as the Iris Control Center.

Iris is available as a PyPI library named `moziris`. It requires system dependencies that are installed using the bootstrap script from this repo.

Once your system is configured, and the setup instructions have been followed, you can test some of Iris' functionality.

To invoke the "sample" target - which is just a placeholder project for demonstration purposes:
```
iris sample
```

To open the Control Center, which is the web-based UI for managing local Iris runs:
```
iris -k
```

To verify that the Iris API itself exists, without running tests, this command will move your mouse on screen:
```
api-test
```

A complete list of command-line options is available when invoking the `-h` flag.

For more detailed examples, see the [project wiki](https://github.com/mozilla/iris/wiki/Command-line-examples).


## Contributing

See our [project wiki](https://github.com/mozilla/iris/wiki/Developer-Workflow) for more information on contributing to Iris.

### Enable Pre-Commit Hooks

Iris has pre-commit hooks for flake8 linting and [black code formatting](https://pypi.org/project/black/). These hooks will run black and flake8 *prior to* committing your changes.

This means that black will format all python files in-place, and flake8 will lint your code for any errors.
If there are flake8 violations, *your changes will not be committed*. The list of ignored rules is documented in the
`tox.ini` file. There should be a compelling reason to do so before adding to this list.

*If you already have Iris installed on your system prior to this patch, you will need to run `pipenv install` again to install the pre-commit module.*

```
# Install dependencies, including pre-commit
pipenv install
# Install pre-commit hooks defined in .pre-commit-config.yaml
pre-commit install
```

That's it! Here's an example of how it works:
```
# make some changes
git add -A
git commit -m 'detailed commit message'
[WARNING] Unstaged files detected.
[INFO] Stashing unstaged files to /Users/ksereduck/.cache/pre-commit/patch1570121459.
black....................................................................Passed
Flake8...................................................................Failed
hookid: flake8

targets/firefox/bug_manager.py:11:1: E402 module level import not at top of file
targets/firefox/bug_manager.py:12:1: E402 module level import not at top of file
targets/firefox/bug_manager.py:14:1: E402 module level import not at top of file
targets/firefox/bug_manager.py:15:1: E402 module level import not at top of file
targets/firefox/bug_manager.py:16:1: E402 module level import not at top of file

[INFO] Restored changes from /Users/ksereduck/.cache/pre-commit/patch1570121459.
```
