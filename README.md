# delty

## Local Installation

### Requirements

1. Complete the numan-development
   [quick-start](https://github.com/BeaNuman/numan-development#quickstart) guide, until
   the docker provision.
2. Install [pyenv](https://github.com/pyenv/pyenv-installer) to manage python versions
   on your local machine.

### Setup

These commands will install python, a virtual environment for the monolith app, install
all dependencies and ensure poetry loads environment variables from .env files.

```console
$ pyenv install 3.10.5
$ pyenv local 3.10.5
$ pip install poetry
$ poetry install
$ poetry self add poetry-dotenv-plugin
```

### Release plan
1st version

1. The user logs in
2. The user enters a URL
3. The app re-renders the form with an iframe that renders the URL the user entered
4. The user now selects the set of elements that needs to be observed
5. The app now observes the elements and logs the changes to the console
6. Set a finite lifespan to cron jobs
