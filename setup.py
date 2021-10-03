import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyeasyremote",
    version="1.0",
    author="Jeroen Tas",
    author_email = 'hi@j45.nl',
    url = 'https://github.com/Jeroen-45/pyeasyremote',
    description="Control Easy Remote supporting DMX lighting control software using python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["pyeasyremote"],
    install_requires=[]
)