"""

A simple hack script that pulls language stats from *all* public repos
and tallies lines of code by language.

Warning: There is no rate limiting implemented!

Code Flow:

* Page through all the repositories using the github api with `GET /repositories`
* The resulting list will contain repo meta data such as
    * repo['id']: auto increment id associated with this repo
    * repo['full_name']: owner/repo name
    * repo['owner']['login']: owner's name
    * repo['languages_url']: url to query the language stats for the repo
* Pull language stats for the repo and increment global counters along with
  user specific counters

"""

import os
import json
import requests
from collections import defaultdict


try:
    BASE_URI = os.environ['GH_URI']
except:
    BASE_URI = 'https://api.github.com'

HEADERS = {'Authorization': 'token %s' % os.environ['GH_TOKEN']}


def repo_iter(repo_list):
    """ helper method for looping through repos """
    for repo in repo_list:
        yield repo['id'], repo['full_name'], repo['owner']['login'], repo['languages_url']


def get_languages(uri):
    """ Query the language stats for a repo """
    r = requests.get(uri, headers=HEADERS)
    for lang, lines in r.json().iteritems():
        yield lang, lines


def get_repos(r_id=None):
    """ Get the next page of repos """
    if r_id is None:
        r_id = 0
    payload = {'since': r_id}
    r = requests.get(os.path.join(BASE_URI, 'repositories'),
                     params=payload, headers=HEADERS)
    return r.json()


def main():
    """ Get language stats """
    org_tallies = lambda: defaultdict(int)
    tallies = defaultdict(org_tallies)

    start_id = None
    while True:
        for r_id, full_name, owner, lang_uri in repo_iter(get_repos(start_id)):
            print('repo_id', r_id)
            for lang, lines in get_languages(lang_uri):
                tallies['all'][lang] += lines
                tallies[owner][lang] += lines
        if r_id == start_id:
            break
        start_id = r_id

    for owner, tal in tallies.iteritems():
        print(owner, tal)

    return 0


if __name__ == '__main__':
    exit(main())