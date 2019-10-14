# moziris

![Travis (.com)](https://img.shields.io/travis/com/mozilla/iris)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/moziris)
![GitHub](https://img.shields.io/github/license/mozilla/iris)
![GitHub repo size](https://img.shields.io/github/repo-size/mozilla/iris)
![GitHub issues](https://img.shields.io/github/issues/mozilla/iris)

Mozilla Iris is a tool that uses on-screen pattern and text matching, while manipulating a machine's mouse and keyboard, to test visual and interactive states of an application.
For more detailed information and troubleshooting tips, please [view our wiki](https://github.com/mozilla/iris/wiki).

## Installation

### System Requirements

 - [Firefox](https://www.mozilla.org/en-US/firefox/new/)
 - [Docker](https://docs.docker.com/v17.12/install/)

### Setup

You can either clone as a git repository or download as a zip file:

```
# After cloning repo or extracting archive
cd iris
# Build the project and tag as "iris"
docker build . -t iris
```

## Usage

The Iris project is meant to be used with your own "target" and tests. A target is basically a pytest plugin invoked by Iris, which will then gather data during the run to present in a web-based interface known as the Iris Control Center.

Iris is available as a PyPI library named `moziris`. It requires system dependencies that are installed using the bootstrap script from this repo.

Once your system is configured, and the setup instructions have been followed, you can test some of Iris' functionality.

To invoke the "sample" target - which is just a placeholder project for demonstration purposes:
```
docker run -it iris /bin/bash
iris sample
```

To open the Control Center, which is the web-based UI for managing local Iris runs:
```
docker run -it iris /bin/bash
iris -k
```

To verify that the Iris API itself exists, without running tests, this command will move your mouse on screen:
```
docker run -it iris /bin/bash
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

```
pip install pre-commit
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
