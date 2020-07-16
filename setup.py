from setuptools import setup, find_packages
from glob import glob


long_description = """
* Marbas is a reformed tokenizer from pynori
* Original pynori repo: https://github.com/gritmind/python-nori
"""



setup(
    name = 'marbas',
    version = '0.1.0',
	
    url = 'https://github.com/MJ-Jang/Marbas.git',
    author = 'MJ Jang',
    author_email = 'mj.jang@sktair.com',
	
    description = 'Lucene Nori, Korean Mopological Analyzer, in Python', 
    #long_description=open('README.md', encoding='utf-8').read(), 
    long_description = long_description,
	long_description_content_type = 'text/markdown', 
	
	license='Apache 2.0',
	
    install_requires = ['cython'],
    zip_safe = False,
	
	
	# See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
	
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
	
		# Specify the Python versions you support
        'Programming Language :: Python :: 3.7',
		
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',
    ],
	
    # What does your project relate to?
    #keywords='',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
	packages = find_packages(exclude=['tests']), 

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
	package_data={
        '': ['marbas/resources/*',
             'marbas/config.ini',
             'marbas/resources/mecab-ko-dic-2.1.1-20180720/*']
	},
	include_package_data=True,
	
    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[],


)





