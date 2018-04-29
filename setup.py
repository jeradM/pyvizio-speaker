from setuptools import setup

setup(
    name='pyvizio_speaker',
    packages=['pyvizio_speaker'],
    version='0.0.1',
    description='Python library for controlling Vizio SmartCast Speakers',
    author='Jerad Meisner',
    author_email='jerad.meisner@gmail.com',
    url='https://github.com/jeradM/pyvizio_speaker',
    download_url='https://github.com/jeradM/pyvizio_speaker/archive/0.0.1.tar.gz',
    keywords=['Vizio', 'SmartCast', 'Soundbar', 'Speaker'],
    install_requires=[
        'aiohttp'
    ],
    classifiers=[]
)
