from setuptools import find_packages, setup

setup(
    name='raposa-schemas',
    packages=find_packages(),
    version='0.0.1',
    description='Algo Dev',
    author='Christian Hubbs',
    license='Not licensed for re-use.',
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
