from setuptools import setup, find_packages
# Sacado de https://stackoverflow.com/questions/1471994/what-is-setup-py
setup(
    name="biblioteca",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "sqlmodel"
    ],
    entry_points={
        "console_scripts": [
            "biblioteca=biblioteca.app:main",
        ],
    },
    author="Rodrigo Tapiador Cano",
    description="Un sistema de gestión de biblioteca con base de datos n-n",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rasitoo/biblioteca",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)