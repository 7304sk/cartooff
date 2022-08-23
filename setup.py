from setuptools import setup, find_packages

setup(
    name="cartooff",
    version="1.0",
    author="shoalwave",
    url="https://github.com/7304sk/cartooff",
    license='MIT',
    description="Wrapper class of cartopy",
    packages=find_packages(),
    install_requires=['numpy','pandas','matplotlib','shapely','pip','cartopy'],
    package_data={'cartooff': ['cartooff/data']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)