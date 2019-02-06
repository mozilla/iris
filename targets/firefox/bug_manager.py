# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import logging

import bugzilla
from github import Github

from src.configuration.config_parser import get_config_property
from targets.firefox.errors import BugManagerError
from src.core.api.os_helpers import OSHelper

logger = logging.getLogger(__name__)

bugzilla_api_key = get_config_property('Bugzilla', 'api_key')
base_url = get_config_property('Bugzilla', 'bugzilla_url')
github_api_key = Github(get_config_property('GitHub', 'github_key'))

bugzilla_os = {'win': 'Windows 10', 'win7': 'Windows 7', 'linux': 'Linux', 'mac': 'macOS'}


def get_github_issue(id):
    """Get Github issues details."""
    try:
        repo = [x for x in github_api_key.get_user().get_repos() if x.name == 'iris2']
        return repo[0].get_issue(id)
    except Exception as e:
        raise BugManagerError('Github API call failed: {}'.format(str(e)))


def get_bugzilla_bug(id):
    """Get Bugzilla bug details."""
    try:
        b = bugzilla.Bugzilla(url=base_url, api_key=bugzilla_api_key)
        return b.get_bug(id)
    except Exception as e:
        raise BugManagerError('Bugzilla API call failed: {}'.format(str(e)))


def is_blocked(id):
    """Checks if a Github issue/Bugzilla bug is blocked or not."""
    try:
        if 'issue_' in id:
            bug = get_github_issue(id).state
            if bug.state == 'closed':
                return False
            else:
                if OSHelper.get_os() in bug.title:
                    return True
                return False
        else:
            bug = get_bugzilla_bug(id)
            print(bug.status, bug.platform)
            if bug.status in ['CLOSED', 'RESOLVED']:
                return False
            else:
                if bugzilla_os[OSHelper.get_os()] == bug.platform or bug.platform in ['All', 'Unspecified']:
                    return True
                return False
    except BugManagerError as e:
        logger.error(str(e))
        return True
