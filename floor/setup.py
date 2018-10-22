from setuptools import setup, find_packages

setup(
    name='floor',
    version='0.2.0',
    description='Dance floor',
    packages=find_packages(),
    install_requires=[
        'flask',
        'pymidi',
        'pyserial',
        'SimpleWebSocketServer',
    ],
    test_suite='nose.collector',
    tests_require=[
        'freezegun',
        'mock',
        'nose',
    ],
    dependency_links=[
        "git+https://github.com/dpallot/simple-websocket-server.git#egg=SimpleWebSocketServer"
    ]
)
