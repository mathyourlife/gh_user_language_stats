# Github language stats

A simple hack script that pulls language stats from *all* public repos
and tallies lines of code by language.

Warning: There is no rate limiting implemented!

Code Flow:

* Page through all the repositories using the github api with `GET /repositories`
* The resulting list will contain repo meta data such as
    * `repo['id']`: auto increment id associated with this repo
    * `repo['full_name']`: owner/repo name
    * `repo['owner']['login']`: owner's name
    * `repo['languages_url']`: url to query the language stats for the repo
* Pull language stats for the repo and increment global counters along with
  user specific counters

## Usage

```bash
export GH_TOKEN=[your auth token]
export GH_URI=https://api.github.com   # Alter for private GHE
python main.py
```
