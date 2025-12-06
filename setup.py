from setuptools import setup, find_packages

setup(
    name="crawler_scrapper",
    version="0.1.0",
    description="Modular crawler and scraper system for integration with auto builder, foundation, taxonomy, gateway and other systems",
    author="InfinityXOneSystems",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "urllib3>=2.0.0",
        "pyyaml>=6.0.0",
        "jsonschema>=4.19.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
