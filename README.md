Setup Virtual Environment
=========================

```
git clone https://github.com/jk0/api_demo.git

cd api_demo

virtualenv venv
. venv/bin/activate
```

Run Unit Tests
==============

```
python setup.py flake8
python setup.py test
```

Run Integration Tests
=====================

```
python setup.py develop

api --help
api

./integration_tests.sh

```
