import os
from codecs import open
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

os.chdir(here)

version_contents = {}
with open(os.path.join(here, "switcherlabs", "version.py"), encoding="utf-8") as f:
    exec(f.read(), version_contents)

readme = None
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    readme = f.read()

setup(
    name="switcherlabs",
    version=version_contents["VERSION"],
    description="Python SDK for SwitcherLabs",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="SwitcherLabs",
    author_email="support@switcherlabs.com",
    url="https://github.com/switcherlabs/switcherlabs-python",
    license="MIT",
    keywords="switcherslabs api feature-flags",
    packages=find_packages(exclude=["tests", "tests.*"]),
    zip_safe=False,
    install_requires=[
        'requests >= 2.20; python_version >= "3.0"',
        'requests[security] >= 2.20; python_version < "3.0"',
    ],
    python_requires="!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
)
