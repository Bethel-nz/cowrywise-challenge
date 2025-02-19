from setuptools import setup, find_packages

setup(
    name="admin",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'psycopg2-binary',
        'redis',
        'requests',
        'pytest',
        'python-dotenv'
    ],
) 