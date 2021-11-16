from setuptools import setup, find_packages


setup(
    name='names-oracle',
    version='0.2',
    description='Provides information and statistics about names and last names.',
    license='MIT',
    author="Leonardo La Rocca",
    author_email='leo_la_rocca@yahoo.it',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['data/*']},
    url='https://github.com/leoli51/Names-Oracle',
    keywords='names database',
)