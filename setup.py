from setuptools import setup

setup(
    name='CertPathway',
    version='0.1.0',
    packages=['CertPathway'],
    include_package_data=True,
    install_requires=[
        'arrow',
        'bs4',
        'Flask',
        'html5validator',
        'requests',
        'selenium',
    ],
    python_requires='>=3.8',
)
