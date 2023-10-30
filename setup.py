import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='python_restclient',
    version='0.0.1',
    description='Rest Client for Python',
    url='https://github.com/shivank0103/python-restclient-project',
    author='Shivank Yadav',
    author_email='shivank0103@gmail.com',
    license='unlicense',
    packages=['restclient'],
    long_description=README,
    long_description_content_type="text/markdown",
    install_requires=[
        'requests==2.28.0',
    ],
    zip_safe=False
)
