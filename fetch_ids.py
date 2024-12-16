import os

import requests
from dotenv import load_dotenv


def load_env_vars():
    """Load environment variables from a .env file."""
    load_dotenv()
    API_KEY = os.getenv('API_KEY')
    if API_KEY:
        return API_KEY
    else:
        raise ValueError("Please make sure API_KEY is set in the .env file")


def fetch_user_info(api_key):
    """
    Fetches user information from the Clockify API and returns the user ID.
    """
    headers = {'X-Api-Key': api_key}
    response = requests.get('https://api.clockify.me/api/v1/user', headers=headers)
    if response.status_code == 200:
        user_info = response.json()
        return user_info['id']
    else:
        raise Exception(f'Failed to fetch user info: {response.status_code}')


def fetch_workspaces(api_key):
    """
    Fetches the list of workspaces from the Clockify API.
    """
    headers = {'X-Api-Key': api_key}
    response = requests.get('https://api.clockify.me/api/v1/workspaces', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Failed to fetch workspaces: {response.status_code}')


def main():
    api_key = load_env_vars()

    try:
        user_id = fetch_user_info(api_key)
        print(f'USER_ID: {user_id}')

        workspaces = fetch_workspaces(api_key)
        for workspace in workspaces:
            print(f'Workspace Name: {workspace["name"]}, WORKSPACE_ID: {workspace["id"]}')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
