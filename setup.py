import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='logger',
    version='0.0.2',
    author='Arthur Moraux',
    author_email='arthur.moraux@gmail.com',
    description='A logger utility for tracking metrics values during training of pyTorch models.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ArthMx/Logger',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
