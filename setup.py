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

import setuptools

from api_demo import version


setuptools.setup(
    name="api_demo",
    version=version.version_hash(),
    author="Josh Kearney",
    author_email="josh@jk0.org",
    description="Flask API demo.",
    license="Apache License, Version 2.0",
    packages=[
        "api_demo",
    ],
    install_requires=[
        "flask"
    ],
    setup_requires=[
        "flake8",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    entry_points={
        "console_scripts": ["api = api_demo.api:main"]
    },
    test_suite="api_demo.tests"
)
