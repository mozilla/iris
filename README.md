# iris-core

![Travis (.com)](https://img.shields.io/travis/com/mozilla/iris)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/moziris)
![GitHub](https://img.shields.io/github/license/mozilla/iris)
![GitHub repo size](https://img.shields.io/github/repo-size/mozilla/iris)
![GitHub issues](https://img.shields.io/github/issues/mozilla/iris)

Iris is a visual test suite which makes asserts based on pattern matching in images.


## Installation

### Mac instructions:

#### System Requirements

 - Python 3
 - git
 - [Firefox](https://www.mozilla.org/en-US/firefox/new/)

#### Setup

```
cd ~
git clone https://github.com/mozilla/iris_firefox
# Run the Mac bootstrap script.
cd iris
./bootstrap/bootstrap.sh
# Run this command to agree to xcode terms of service.
sudo xcodebuild -license accept
```
 - **Restart** your Mac in order for certain libraries to be recognized.
 - In System Preferences, go to Mission Control and change the keyboard shortcut for "Application Windows" to "-", or none.
 - Launch Iris.
```
cd ~/iris_firefox
pipenv install
pipenv shell
iris firefox
```

### Windows 7 / Windows 10 Professional instructions:

#### System Requirements

 - Python 3
 - git
 - [Firefox](https://www.mozilla.org/en-US/firefox/new/)
 - [Powershell 3](https://www.microsoft.com/en-us/download/details.aspx?id=34595)
 - [.NET framework version 4.5](https://www.microsoft.com/en-us/download/details.aspx?id=30653).

#### Setup

```
git clone https://github.com/mozilla/iris_firefox
cd iris_firefox
bootstrap\bootstrap.sh
# Install project requirements and activate the virtualenv.
pipenv install
pipenv shell
# Run Iris.
iris firefox
```

### Ubuntu Linux instructions:

#### System Requirements

 - Python 3
 - git
 - [Firefox](https://www.mozilla.org/en-US/firefox/new/)

- [Follow instructions below for disabling Keyring](https://github.com/mozilla/iris_firefox/wiki/Setup#disable-system-keyring)
- Open Settings > Displays > "Scale for Menu and Title bars:" and verify that it is set to 1.

#### Setup
```
cd ~
git clone https://github.com/mozilla/iris_firefox
cd iris_firefox
./bootstrap/bootstrap.sh
# Note: This will take around 10 minutes to download, compile, and install dependencies.
# Run the following commands to complete installation and launch Iris.
pipenv install
pipenv shell
iris firefox
```

## Usage
