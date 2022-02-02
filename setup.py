from setuptools import find_packages, setup
from pathlib import Path
import os
import sys

sys.path.insert(0, os.path.join(Path(os.getcwd()), 'schemas'))
from schemas.version import VERSION

setup(
    name='raposa-schemas',
    version=VERSION,
    description='Provides schemas for a consistent interface between UI and ' \
        + 'back-end API.',
    author='Christian Hubbs, Connor Valentine, Owais Sarwar',
    license='Not licensed for re-use.',
    url='https://github.com/hubbs5/raposa-schemas',
    packages = find_packages(),
    install_requires=[
        'pydantic',
        'typing-extensions'
    ],
    python_requires='>=3.7',
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
	]
)
