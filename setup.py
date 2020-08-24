from setuptools import setup, find_packages

setup(
    name="sim-pack",
    version="0.0.1",
    py_modules=find_packages(),
    include_package_data=True,
    install_requires=[
        "azure-cli==2.10.1",
    ],
    entry_points={
        'console_scripts': ['sim-pack=sim_packager:main'],
    }
)
