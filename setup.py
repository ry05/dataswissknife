import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dataswissknife",
    version="0.0.1",
    author="Ramshankar Yadhunath, Srivenkata Srikanth, Arvind Sudheer",
    author_email="yadramshankar@gmail.com",
    description="A Handy Little Tool to aid your Data Science Project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ry05/dataswissknife",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
