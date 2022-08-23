from setuptools import setup, find_packages
from glob import glob

setup(
    name="cartooff",
    version="1.0",
    author="shoalwave",
    url="https://github.com/7304sk/cartooff",
    license='MIT',
    description="Wrapper class of cartopy",
    install_requires=['numpy','pandas','matplotlib','shapely','pip','cartopy'],
    packages=find_packages(),
    package_data={'cartooff': glob('cartooff/data/*')},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)