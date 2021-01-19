"""Setup script"""
import setuptools
import os
import re

HERE = os.path.abspath(os.path.dirname(__file__))
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')
TESTS_REQUIRE = [
    'coverage',
    'nose',
    'pytest'
]


def get_version():
    init = open(
        os.path.join(
            HERE,
            "aws_allowlister",
            "bin",
            "version.py"
        )
    ).read()
    return VERSION_RE.search(init).group(1)


def get_description():
    return open(
        os.path.join(os.path.abspath(HERE), "README.md"), encoding="utf-8"
    ).read()


setuptools.setup(
    name="aws-allowlister",
    include_package_data=True,
    version=get_version(),
    author="Kinnaird McQuade",
    author_email="kinnairdm@gmail.com",
    description="Generate AWS AllowList SCPs",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/salesforce/aws-allowlister",
    packages=setuptools.find_packages(exclude=['test*']),
    tests_require=TESTS_REQUIRE,
    install_requires=[
        'beautifulsoup4',
        'click',
        'requests',
        'policy_sentry',
        'SQLAlchemy',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": "aws-allowlister=aws_allowlister.bin.cli:main"},
    zip_safe=True,
    keywords='aws iam roles policy policies privileges security',
    python_requires='>=3.6',
)
