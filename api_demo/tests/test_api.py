#   Copyright 2015 Josh Kearney
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""API Unit Tests"""

import json
import unittest

from api_demo import api
from api_demo import version


USER = {
    "first_name": "Joe",
    "last_name": "Smith",
    "userid": "jsmith",
    "groups": []
}

GROUP = {
    "name": "foo",
    "users": []
}


class TestApi(unittest.TestCase):
    def setUp(self):
        self.app = api.APP.test_client()

    def test_index(self):
        response = self.app.get("/")
        self.assertEqual(response.data, version.version_string())
        self.assertEqual(response.status_code, 200)

    def test_000_create_user(self):
        response = self.app.post("/users", data=json.dumps(USER),
                                 content_type="application/json")
        self.assertEqual(json.loads(response.data), USER)
        self.assertEqual(response.status_code, 201)

    def test_001_create_user_dup(self):
        response = self.app.post("/users", data=json.dumps(USER),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 409)

    def test_002_create_user_invalid(self):
        invalid_request = {"foo": "bar"}
        response = self.app.post("/users", data=json.dumps(invalid_request),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 422)

    def test_003_get_user(self):
        response = self.app.get("/users/jsmith")
        self.assertEqual(json.loads(response.data), USER)
        self.assertEqual(response.status_code, 200)

    def test_004_get_user_nonexistent(self):
        response = self.app.get("/users/jdoe")
        self.assertEqual(response.status_code, 404)

    def test_005_update_user(self):
        USER["first_name"] = "Joseph"
        response = self.app.put("/users/jsmith", data=json.dumps(USER),
                                content_type="application/json")
        self.assertEqual(json.loads(response.data), USER)
        self.assertEqual(response.status_code, 200)

    def test_006_update_user_nonexistent(self):
        USER["first_name"] = "Joseph"
        response = self.app.put("/users/jdoe", data=json.dumps(USER),
                                content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_007_update_user_invalid(self):
        invalid_request = {"foo": "bar"}
        response = self.app.put("/users/jsmith",
                                data=json.dumps(invalid_request),
                                content_type="application/json")
        self.assertEqual(response.status_code, 422)

    def test_008_delete_user_nonexistent(self):
        response = self.app.delete("/users/jdoe")
        self.assertEqual(response.status_code, 404)

    def test_009_delete_user(self):
        response = self.app.delete("/users/jsmith")
        self.assertEqual(response.status_code, 204)

    def test_100_create_group(self):
        response = self.app.post("/groups", data=json.dumps(GROUP),
                                 content_type="application/json")
        self.assertEqual(json.loads(response.data), {"users": []})
        self.assertEqual(response.status_code, 201)

    def test_101_create_group_dup(self):
        response = self.app.post("/groups", data=json.dumps(GROUP),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 409)

    def test_102_create_group_invalid(self):
        invalid_request = {"foo": "bar"}
        response = self.app.post("/groups", data=json.dumps(invalid_request),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 422)

    def test_103_get_group(self):
        response = self.app.get("/groups/foo")
        self.assertEqual(json.loads(response.data), {"users": []})
        self.assertEqual(response.status_code, 200)

    def test_104_get_group_nonexistent(self):
        response = self.app.get("/groups/bar")
        self.assertEqual(response.status_code, 404)

    def test_105_update_group(self):
        users = ["jsmith"]
        group = {"users": ["jsmith"]}
        response = self.app.put("/groups/foo", data=json.dumps(users),
                                content_type="application/json")
        self.assertEqual(json.loads(response.data), group)
        self.assertEqual(response.status_code, 200)

    def test_106_update_group_nonexistent(self):
        GROUP["users"].append("jsmith")
        response = self.app.put("/groups/bar", data=json.dumps(GROUP),
                                content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_107_update_group_invalid(self):
        invalid_request = {"foo": "bar"}
        response = self.app.put("/groups/foo",
                                data=json.dumps(invalid_request),
                                content_type="application/json")
        self.assertEqual(response.status_code, 422)

    def test_108_delete_group_nonexistent(self):
        response = self.app.delete("/groups/bar")
        self.assertEqual(response.status_code, 404)

    def test_108_delete_group(self):
        response = self.app.delete("/groups/foo")
        self.assertEqual(response.status_code, 204)
