from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="LLMExchange - A Tool calling GenAI Application",
    description="A GenAI application that uses LLMs to classify and process currency conversion requests.",
    version="0.1",
    author="Maesak Delbar",
    author_email="maesak.delbar@gmail.com",
    packages=find_packages(include=['src', 'src.*']),
    install_requires = requirements,
)