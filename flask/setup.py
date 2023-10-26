from setuptools import setup

setup(
    name="flask_blog",
    version="0.1.0",
    packages=["blog"],
    author="Luan Louzada",
    install_requires=[
        "flask",
        "flask_pymongo",
        "dynaconf",
        "unidecode",
        "flask-bootstrap",
        "mistune",
    ],
)
