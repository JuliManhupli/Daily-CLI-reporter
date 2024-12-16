import os

import requests
from dotenv import load_dotenv


def load_env_vars():
    """Load environment variables from a .env file and validate them."""
    load_dotenv()

    API_KEY = os.getenv('API_KEY')
    if not API_KEY:
        raise ValueError("Please make sure API_KEY is set in the .env file")

    WORKSPACE_ID = os.getenv('WORKSPACE_ID')
    if not WORKSPACE_ID:
        raise ValueError("Please make sure WORKSPACE_ID is set in the .env file")

    USER_ID = os.getenv('USER_ID')
    if not USER_ID:
        raise ValueError("Please make sure USER_ID is set in the .env file")

    return {
        'API_KEY': API_KEY,
        'WORKSPACE_ID': WORKSPACE_ID,
        'USER_ID': USER_ID
    }


def get_time_entries(api_key, workspace_id, user_id):
    """Fetch time entries from the Clockify API."""
    url = f'https://api.clockify.me/api/v1/workspaces/{workspace_id}/user/{user_id}/time-entries'
    headers = {'X-Api-Key': api_key}
    response = requests.get(url, headers=headers)
    return response


def main():
    env_vars = load_env_vars()
    response = get_time_entries(env_vars['API_KEY'], env_vars['WORKSPACE_ID'], env_vars['USER_ID'])

    if response.status_code == 200:
        time_entries = response.json()
        for idx, entry in enumerate(time_entries, start=1):
            print(f"Task {idx}: {entry['description']}")
    else:
        print('Failed to fetch time entries', response.status_code)


if __name__ == '__main__':
    main()
