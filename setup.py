from setuptools import setup, find_packages

with open('LICENSE') as f:
    license = f.read()

setup(
    name="expkit",
    version="0.0.1",
    description="early stage, machine learning quick-experiment toolkit",
    author="Jonathan Gingras",
    author_email="jonathan.gingras.1@gmail.com",
    url="https://github.com/jonathangingras/expkit",
    license=license,
    packages=find_packages(exclude=('docs', 'tests', 'tests.*')),
    package_data={'expkit.resources': '*.mk'}
)
