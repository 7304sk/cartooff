import setuptools

setuptools.setup(
    name="cartooff",
    version="1.0",
    author="shoalwave",
    url="https://github.com/7304sk/cartooff",
    license='MIT',
    description="Wrapper class of cartopy",
    packages=setuptools.find_packages(),
    install_requires=['numpy','pandas','matplotlib','cartopy','mpl_toolkits','shapely','pip'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)