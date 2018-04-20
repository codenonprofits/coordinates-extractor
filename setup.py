from distutils.core import setup

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Topic :: Software Development',
]

setup(
    name='coordinates-extractor',
    version='0.0.4',
    author='CodeNonprofits - GreatNonprofits',
    author_email='support@greatnonprofits.org',
    packages=['coordinates_extractor'],
    url='https://github.com/codenonprofits/coordinates-extractor',
    license='BSD licence, see LICENCE.txt',
    description='Library consultation phone carriers around the world.',
    download_url="https://github.com/codenonprofits/coordinates-extractor/archive/master.zip",
    keywords=['coordinates', 'extractor', 'google maps', 'maps', 'python'],
    classifiers=CLASSIFIERS,
    install_requires=[
        'beautifulsoup4==4.6.0',
        'cffi>=1.10.0',
        'chardet==3.0.4',
        'idna==2.6',
        'pycparser==2.18',
        'requests[security]',
        'six>=1.10.0',
        'urllib3==1.22',
        'vobject==0.9.5'
    ]
)
