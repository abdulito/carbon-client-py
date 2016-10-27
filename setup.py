from setuptools import setup, find_packages

setup(
    name='carbonio_client',
    version='0.1.5',
    packages=find_packages(),
    install_requires=[
        'httplib2>=0.9',
        'requests==2.11.1'
    ]


)

