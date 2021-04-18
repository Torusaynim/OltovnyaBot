import setuptools

# Load the long_description from README.md
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OltovnyaBot",
    version="0.1.0",
    author="Torusaynim & Shamhal3228",
    author_email="PerlovIvan@yandex.ru",
    description="Bot for Discord app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Torusaynim/.OltovnyaBot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)