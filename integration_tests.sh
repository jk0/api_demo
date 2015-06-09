#!/bin/sh

echo "Creating user..."
curl -i -H "Content-Type: application/json" -X POST -d '{"first_name": "John", "last_name": "Doe", "userid": "jdoe", "groups": ["foo"]}' http://127.0.0.1:5000/users

echo "Updating user..."
curl -i -H "Content-Type: application/json" -X PUT -d '{"first_name": "Jonathan", "last_name": "Doe", "userid": "jdoe", "groups": ["foo"]}' http://127.0.0.1:5000/users/jdoe

echo "Fetching user..."
curl -i http://127.0.0.1:5000/users/jdoe

echo "Fetching group..."
curl -i http://127.0.0.1:5000/groups/foo

echo "Creating group..."
curl -i -H "Content-Type: application/json" -X POST -d '{"name": "bar"}' http://127.0.0.1:5000/groups

echo "Updating group..."
curl -i -H "Content-Type: application/json" -X PUT -d '["jdoe"]' http://127.0.0.1:5000/groups/bar

echo "Fetching group..."
curl -i http://127.0.0.1:5000/groups/bar

echo "Deleting group..."
curl -i -H "Content-Type: application/json" -X DELETE http://127.0.0.1:5000/groups/foo

echo "Deleting group..."
curl -i -H "Content-Type: application/json" -X DELETE http://127.0.0.1:5000/groups/bar

echo "Deleting user..."
curl -i -H "Content-Type: application/json" -X DELETE http://127.0.0.1:5000/users/jdoe
