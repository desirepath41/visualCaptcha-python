from distutils.core import setup

setup(
    name='visualcaptcha',
    packages=['visualcaptcha'],
    version='0.0.7',
    description='visualCaptcha backend package for python',
    author='Bruno Bernardino',
    author_email='me@brunobernardino.com',
    url='https://github.com/desirepath41/visualCaptcha-python',
    download_url='https://github.com/desirepath41/visualCaptcha-python/tarball/0.0.7',
    keywords=['captcha', 'visualcaptcha', 'security'],
    classifiers=[],
    package_data={
        'visualcaptcha': [
            'assets/*.json',
            'assets/images/*.png',
            'assets/audios/*.mp3',
            'assets/audios/*.ogg'
        ]
    }
)
