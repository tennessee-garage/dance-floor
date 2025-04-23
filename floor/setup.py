from setuptools import find_packages, setup

setup(
    name="floor",
    version="0.2.0",
    description="Dance floor",
    packages=find_packages(),
    test_suite="nose.collector",
    install_requires=["gevent"],
)
