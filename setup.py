from setuptools import find_packages, setup

setup(
    name="gk6",
    version="2.0.0",
    description="Convert Postman collections into k6 load testing scripts",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="you@example.com",
    url="https://github.com/gopikrishna4595/gk6",
    packages=find_packages(),
    install_requires=["typer[all]"],
    entry_points={"console_scripts": ["gk6 = gk6.cli:app"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)
