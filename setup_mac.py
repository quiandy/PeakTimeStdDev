import ez_setup
ez_setup.use_setuptools()

import sys
from setuptools import setup

setup(
    app=["PeakTimeStdDev.py"],
    setup_requires=["py2app"],
)