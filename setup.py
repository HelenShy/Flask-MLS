from setuptools import setup

setup(
    name='MLS-CLI',
    version='1.0',
    py_modules=['cli', 'cli.commands'],
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points="""
        [console_scripts]
        mls=cli.cli:cli
    """,
)
