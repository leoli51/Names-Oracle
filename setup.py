from setuptools import setup, find_packages


setup(
    name='names-oracle',
    version='0.1',
    description='Provides information and statistics about names and last names.',
    license='MIT',
    author="Leonardo La Rocca",
    author_email='leo_la_rocca@yahoo.it',
    packages=find_packages('src'),
    package_dir={'database': 'src/database'},
    package_data={'database': ['data/*']},
    url='https://github.com/leoli51/Names-Oracle',
    keywords='names database',
)