try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Twitter Exploration - Web App',
    'author': 'Alexandre Combessie',
    'url': 'To be added',
    'download_url': 'Where to download it.',
    'author_email': 'alex.combessie@gmail.com',
    'version': '0.1',
    'install_requires': ['numpy', 'nltk', 'pattern', 'tweepy', 'pymongo', 'scikit-learn', 'scipy', 'nose'],
    'packages': ['twitterapp'],
    'scripts': ['background_collection-clustering.py'],
    'name': 'twitter-exploration-webapp'
}

setup(**config)
