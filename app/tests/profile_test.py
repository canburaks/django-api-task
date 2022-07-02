from django.test import TestCase
import requests
import json
from app.models import Profile, Post
from graphql_relay import from_global_id
import unittest
from app.utils import request_query


class ProfileTest(unittest.TestCase):

    data = {}

    def test_create_profile(self):
        response = request_query(
            """mutation
            createProfile($username: String!, $password: String!) {
                createProfile(input:{data:{username:$username, password:$password}}){
                    profile{
                    id
                    username
                    firstName
                    lastName
                    }
                }
            }""",
            variables={
                "username": TEST_PROFILE1["username"],
                "password": TEST_PROFILE1["password"],
            },
        )
        self.assertEqual(
            response.get("data").get("createProfile").get("profile").get("username"),
            TEST_PROFILE1["username"],
        )

    def test_update_profile(self):
        response = request_query(
            """mutation
            updateProfile($username: String!, $firstName: String, $lastName:String) {
                updateProfile(input:{username:$username, data:{firstName:$firstName, lastName:$lastName}}){
                    profile{
                    id
                    username
                    firstName
                    lastName
                    }
                }
            }""",
            variables={
                "username": TEST_PROFILE1["username"],
                "firstName": TEST_PROFILE1["first_name"],
                "lastName": TEST_PROFILE1["last_name"],
            },
        )
        self.assertEqual(
            response.get("data").get("updateProfile").get("profile").get("firstName"),
            TEST_PROFILE1["first_name"],
        )

    def test_delete_profile(self):
        response = request_query(
            """mutation ($username: String!){
                deleteProfile(
                input:{username:$username}){
                    ok
                }
            }""",
            variables={"username": TEST_PROFILE1["username"]},
        )
        self.assertEqual(response["data"]["deleteProfile"]["ok"], True)


TEST_PROFILE1 = {
    "username": "test_profile",
    "password": "Test123456",
    "first_name": "Test",
    "last_name": "Profile",
}
TEST_PROFILE2 = {
    "username": "test_profile_2",
    "password": "Test123456",
    "first_name": "Test2",
    "last_name": "Profile2",
}

TEST_POST = {
    "create": {"title": "Test Post Title", "description": "This is a test post description."},
    "update": {
        "title": "Test Post Updated Title",
        "description": "This is a updated test post description.",
    },
}

if __name__ == "__main__":
    unittest.main()
