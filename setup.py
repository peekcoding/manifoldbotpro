from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mikhailtal-trader",
    version="0.1.0",
    author="Your Name",
    description="Trading bot for MikhailTal's Manifold Markets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mikhailtal-trader",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "openai>=1.0.0",
        "anthropic>=0.18.0",
        "pydantic>=2.0.0",
        "python-dateutil>=2.8.2",
    ],
)
