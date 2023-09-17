from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cicd-pipeline-framework",
    version="0.3.1",
    author="Mario Perez",
    author_email="perezmario303@gmail.com",
    description="Dynamic CI/CD pipeline generation with integrated security scanning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marioperez/cicd-pipeline-framework",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pyyaml>=6.0",
        "click>=8.0.0",
        "jinja2>=3.0.0",
        "requests>=2.28.0",
        "gitpython>=3.1.0",
        "python-dotenv>=0.19.0",
        "colorama>=0.4.4",
        "tabulate>=0.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "pytest-mock>=3.6.0",
            "flake8>=4.0.0",
            "black>=22.0.0",
        ],
        "web": [
            "flask>=2.0.0",
            "flask-cors>=3.0.10",
        ],
    },
    entry_points={
        "console_scripts": [
            "pipeline-gen=src.cli:main",
        ],
    },
)
