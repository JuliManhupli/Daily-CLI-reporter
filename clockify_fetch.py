import os
from datetime import datetime
from collections import defaultdict

import pytz
import requests
from dotenv import load_dotenv

ukraine_tz = pytz.timezone('Europe/Kyiv')

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


def display_time_entries(time_entries):
    """Display each time entry."""
    for entry in time_entries:
        description = entry.get('description', 'No description')
        start_time = entry['timeInterval']['start']
        end_time = entry['timeInterval']['end']
        duration = entry['timeInterval'].get('duration', 'No duration')

        start_time = datetime.fromisoformat(start_time[:-1]).replace(tzinfo=pytz.UTC)
        end_time = datetime.fromisoformat(end_time[:-1]).replace(tzinfo=pytz.UTC) if end_time else None

        start_time_ukraine = start_time.astimezone(ukraine_tz).replace(tzinfo=None)
        end_time_ukraine = end_time.astimezone(ukraine_tz).replace(tzinfo=None) if end_time else "Ongoing"

        print(f"Task: {description}")
        print(f"  Start Time: {start_time_ukraine}")
        print(f"  End Time: {end_time_ukraine}")
        print(f"  Duration: {duration}")
        print()


def group_by_date_and_task(time_entries):
    """Group time entries by date and task, and calculate total time spent."""
    grouped_data = defaultdict(lambda: defaultdict(lambda: {'total_time': 0, 'entries': []}))

    for entry in time_entries:
        description = entry.get('description', 'No description')
        start_time = entry['timeInterval']['start']
        end_time = entry['timeInterval']['end']
        duration = entry['timeInterval'].get('duration', None)

        start_time = datetime.fromisoformat(start_time[:-1]).replace(tzinfo=pytz.UTC)
        end_time = datetime.fromisoformat(end_time[:-1]).replace(tzinfo=pytz.UTC) if end_time else datetime.now()

        start_time_ukraine = start_time.astimezone(ukraine_tz).replace(tzinfo=None)
        end_time_ukraine = end_time.astimezone(ukraine_tz).replace(tzinfo=None)

        date_key = start_time.date()

        if duration is not None:
            try:
                duration_seconds = int(duration)
            except ValueError:
                duration_seconds = (end_time_ukraine - start_time_ukraine).total_seconds()
        else:
            duration_seconds = (end_time_ukraine - start_time_ukraine).total_seconds()

        # Group by date and task description
        grouped_data[date_key][description]['total_time'] += duration_seconds
        grouped_data[date_key][description]['entries'].append({
            'start_time': start_time_ukraine,
            'end_time': end_time_ukraine,
            'duration': duration_seconds
        })

    return grouped_data


def display_report(grouped_data):
    """Display the grouped report."""
    for date, tasks in grouped_data.items():
        print('-' * 50)
        print(f"\nDate: {date}")
        for task, data in tasks.items():
            print(f"\n\tTask: {task}")
            print(f"\t\tTotal Time: {data['total_time'] / 3600:.2f} hours")
            for entry in data['entries']:
                print(f"\t\t- Start: {entry['start_time']} End: {entry['end_time']} Duration: {entry['duration'] / 3600:.2f} hours")
        print('-' * 50)


def main():
    env_vars = load_env_vars()
    response = get_time_entries(env_vars['API_KEY'], env_vars['WORKSPACE_ID'], env_vars['USER_ID'])

    if response.status_code == 200:
        time_entries = response.json()
        if time_entries:
            display_time_entries(time_entries)
            grouped_data = group_by_date_and_task(time_entries)
            display_report(grouped_data)
        else:
            print("No time entries found.")
    else:
        print('Failed to fetch time entries', response.status_code)


if __name__ == '__main__':
    main()
