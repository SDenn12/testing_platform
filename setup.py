from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Testing platform'
LONG_DESCRIPTION = 'A basic testing platform, can post and get tests.'

# Setting up
setup(
    name="testing_platform",
    version=VERSION,
    author="Samuel Dennis",
    author_email="samuel.dennis3141@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas', 'pymongo', 'flask'],
    keywords=['python', 'test', 'login'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)