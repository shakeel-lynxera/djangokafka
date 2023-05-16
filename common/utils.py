import json
import pytz
import sendgrid as sendgrid

from sendgrid.helpers.mail import Email, To, Content, Mail
from django.template.loader import render_to_string
from django.http import HttpResponse
from common.baselayer.basemodel import StatusChoices
from jobs.models import JobStatusChoices
from lang.locale_utils import get_message
from rest_framework.utils.serializer_helpers import ReturnList
import requests
from datetime import datetime
from django.utils import timezone
from pytz import timezone as pytime


def required(message):
    """Checks if the message is required to be processed in kafka event stream."""
    event = json.loads(message.value)
    return True, event
    # source = event.get("source", None)
    # ALLOW_SERVICES = ["fleet-management-system", "users"]
    # if source in ALLOW_SERVICES:
    #     return True, event
    # return False, None


def create_message(data=dict(), status_code=1, message=None):
    """Create message utility for creating responses

    Args:
        data ([list]): [List of objects]
        status ([int], mandatory): [Internal system status code for the
                                    response defined in module locale]
                                    Defaults to None.

    Returns:
        [dict]: [Dict with status, message and data keys for client]
    """

    return {
        # internal system codes
        "status": status_code,
        # locale message in the system codes
        "message": get_message(status_code)
        if message is None
        else error_message(message),
        "data": data,
    }


def create_response(
    response_body, http_status=None, header_dict=dict(), mime="application/json"
):
    """Create response utility for creating a generic response

    IMPORTANT : EXPECTS response_body param to be created and passed by
                create_message method.

    Args:
        response_body ([list]): [List of objects]
        http_status (int, optional): [The response HTTP Status code].
        header_dict (dict, optional): [Header data]. Defaults to {}.
        mime (str, optional): [Data type]. Defaults to 'application/json'.

    Returns:
        [HTTPResponse]: [The HTTP response]
    """

    if http_status is None:
        raise ValueError("No http status code provided")
    resp = HttpResponse(
        json.dumps(response_body), status=http_status, content_type=mime
    )
    for name, value in header_dict.items():
        resp[name] = value
    return resp


def error_message(errors, default=1):
    if isinstance(errors, str):
        return errors
    if not errors:
        return get_message(default)
    try:
        serialized_error_dict = errors
        # ReturnList of serialized_errors when many=True on serializer
        if isinstance(errors, ReturnList):
            serialized_error_dict = errors[0]

        serialized_errors_keys = list(serialized_error_dict.keys())
        # getting first error message from serializer errors
        try:
            message = serialized_error_dict[serialized_errors_keys[0]][0].replace(
                "This", serialized_errors_keys[0]
            )
            return message.replace("_", " ").capitalize()
        except Exception as e:
            print(e)
            return (
                serialized_error_dict[serialized_errors_keys[0]][0]
                .replace("_", " ")
                .capitalize()
            )

    except Exception as e:
        print(f"Error parsing serializer errors:{e}")
        return get_message(default)


def split_full_name(full_name):
    """Splits full name into first and last name"""
    if not full_name:
        return None, None
    names = full_name.split(" ")
    if len(names) == 1:
        return names[0], None
    return names[0], " ".join(names[1:])


def get_default_query_param(request, key, default):
    """

    @param request: request object
    @type request: request
    @param key: key to get data from
    @type key: str
    @param default: default variable to return if key is empty or doesn't exist
    @type default: str/None
    @return: key
    @rtype: str/None
    """
    if key in request.query_params:
        key = request.query_params.get(key)
        if key:
            return key
    return default


def send_email(data):
    try:
        payload = json.dumps(data)
        headers = {
            "Content-Type": "application/json",
        }
        response = requests.request(
            "POST", EMAIL_SERVICE_URL, headers=headers, data=payload
        )
        print("Email Service Response:", response)
        if response.ok:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error sending email:{e}")
        return False
