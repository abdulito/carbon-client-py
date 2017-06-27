from setuptools import setup, find_packages

setup(
    name='carbonio_client',
    version='0.2.3',
    packages=find_packages(),
    install_requires=[
        'requests==2.11.1',
        'requests-toolbelt>=0.8.0'
    ]


)

