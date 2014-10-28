from distutils.core import setup

with open('README.md') as file:
    long_description = file.read()

setup(
    name = 'visualcaptcha',
    packages = ['visualcaptcha'],
    version = '0.0.1',
    description = 'visualCaptcha backend package for python',
    long_description = long_description,
    author = 'Bruno Bernardino',
    author_email = 'me@brunobernardino.com',
    url = 'https://github.com/emotionLoop/visualCaptcha-python',
    download_url = 'https://github.com/emotionLoop/visualCaptcha-python/tarball/0.0.1',
    keywords = ['captcha', 'visualcaptcha', 'security'],
    classifiers = [],
)