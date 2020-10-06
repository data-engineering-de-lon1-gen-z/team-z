# Get started

1. Clone the repo: `git clone https://github.com/data-engineering-de-lon1-gen-z/team-z.git`
2. Change your working directory: `cd team-z/`
3. (optional) Setup your venv: `python3 -m venv .venv`
4. Install the requirements: `pip install -r requirements.txt`
5. (optional) Install pylint and black: `pip install pylint black`

    See more on black python formatter in VSCode: https://dev.to/adamlombard/how-to-use-the-black-python-code-formatter-in-vscode-3lo0

6. Set up the docker containers: `docker-compose up -d` & Cross your fingers 🤞

Adminer should now be running in the browser on `localhost:8081` and mysql database at `root:password@localhost:33066`
