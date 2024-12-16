# Daily-CLI-reporter

This Python project interacts with the Clockify API to fetch user information, workspaces, and time entries.

## Prerequisites

Before using this script, ensure you have the following:

- [Python](https://www.python.org/downloads/) 3.7 or later
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management
- A Clockify account and API key

## Steps

**1. Clone the Repository**

Open a terminal and navigate to your desired project directory. Then, clone the repository using the following command:

```bash
git clone https://github.com/JuliManhupli/Daily-CLI-reporter
cd Daily-CLI-reporter
```

**2. Install dependencies**

Make sure you have Poetry installed. Then, run the following command to install the project dependencies:

```bash
poetry install
```

**3. Set up environment variables**

Create an .env file in the root directory of your project and include the following environment variables (you can use 
env.ini as a template):

```bash
API_KEY=your_clockify_api_key
WORKSPACE_ID=your_workspace_id
USER_ID=your_user_id
```

You can obtain your API key by logging into your Clockify account and visiting
the [API settings page](https://docs.clockify.me/). 
You can use the `fetch_ids.py` script to retrieve the workspace_id and user_id.

**4. Run the script**

To run the script and fetch time entries from the Clockify API, use:

```bash
python clockify_fetch.py
```
