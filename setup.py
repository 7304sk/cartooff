from setuptools import setup, find_packages
import os

def file_walk_relative(top, remove=''):
    top = top.replace('/', os.path.sep)
    remove = remove.replace('/', os.path.sep)
    for root, dirs, files in os.walk(top):
        for file in files:
            yield os.path.join(root, file).replace(remove, '')

setup(
    name="cartooff",
    version="1.0",
    author="shoalwave",
    url="https://github.com/7304sk/cartooff",
    license='MIT',
    description="Wrapper class of cartopy",
    install_requires=['numpy','pandas','matplotlib','shapely','pip','cartopy'],
    packages=['cartooff'],
    package_data={'cartooff': list(file_walk_relative('cartooff/data/', remove='cartooff/'))},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)