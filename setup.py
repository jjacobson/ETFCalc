from setuptools import setup

setup(
    name='etfcalc',
    packages=['etfcalc'],
    include_package_data=True,
    install_requires=[
        'flask',
        'pandas_datareader',
        'pyquery',
        'requests_cache',
        'pandas',
        'requests',
        'FinanceScraper'
    ],
)
