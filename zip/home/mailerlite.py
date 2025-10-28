import traceback

import requests
from django.conf import settings


def api_request(method, endpoint, data):
    api_key = settings.MAILERLITE_API_KEY
    if not api_key:
        return {"message": "MailerLite API key is not configured"}, None

    base_url = settings.MAILERLITE_BASE_URL
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
        "X-Version": "2025-10-28",
    }

    url = f"{base_url}/{endpoint}"
    try:
        response = requests.request(method, url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        json = response.json()
        return None, json
    except requests.Timeout:
        return {"message": "Request timed out"}, None
    except requests.RequestException as e:
        if e.response is not None:
            try:
                error_json = e.response.json()
                return error_json, None
            except requests.JSONDecodeError:
                return {"message": e.response.text}, None
        print(f"Request failed:")
        traceback.print_exception(e)
        return {"message": "Request failed"}, None
    except Exception as e:
        print(f"Unexpected error:")
        traceback.print_exception(e)
        return {"message": "Unexpected error"}, None


def add_subscriber(email, group_input_names=None):
    if group_input_names is None:
        group_input_names = []

    groups = [
        settings.MAILERLITE_GROUPS[name]["id"]
        for name in group_input_names
        if name in settings.MAILERLITE_GROUPS
    ]

    error, response = api_request(
        "POST",
        "subscribers",
        {
            "email": email,
            "groups": groups,
        },
    )

    return error, response
