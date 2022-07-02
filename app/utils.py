from django.contrib.auth.models import User
from graphql import GraphQLError
from importlib import import_module
from django.conf import settings
from django.contrib.sessions.models import Session
import requests
import json


def get_user_id_from_session(info):
    session_key = info.context.session.get("_SessionBase__session_key")
    session = Session.objects.filter(session_key=session_key).first()
    if session:
        return session.get_decoded().get("_auth_user_id")
    return None


def get_user_id_from_header(info):
    if info.context.META.get("HTTP_AUTHORIZATION"):
        return info.context.META.get("HTTP_AUTHORIZATION")
    return None


def get_user_id(info):
    session_user_id = get_user_id_from_session(info)
    if session_user_id is None:
        auth_user_id = get_user_id_from_header(info)
        if auth_user_id is None:
            if info.context.user.is_authenticated is False:
                return None
            else:
                return info.context.user.id
        else:
            return auth_user_id
    else:
        return session_user_id


def request_query(query, variables={}):
    try:
        url = "http://localhost:8000/graphql"
        r = requests.post(url, json={"query": query, "variables": variables})
        json_data = json.loads(r.text)
        if json_data.get("errors"):
            print(json_data.get("errors")[0].get("message"), "\n")
            return None
        return json_data
    except Exception as e:
        print("Exception ", e)
