from setuptools import setup, find_packages

setup(
    name='saybot',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'openai',
        'emoji',
        'python-dotenv',
        'telegram',
        'datetime',
        'python-telegram-bot'

    ],
)
