# visualCaptcha-python

[![Build Status](http://img.shields.io/travis/emotionLoop/visualCaptcha-python.svg)](http://travis-ci.org/emotionLoop/visualCaptcha-python)
[![Coverage Status](https://coveralls.io/repos/emotionLoop/visualCaptcha-python/badge.png)](https://coveralls.io/r/emotionLoop/visualCaptcha-python)

Python package for visualCaptcha's backend service


## Installation with PIP

You need Python installed with pip.
```
pip install visualcaptcha
```

## Run tests

Run next command to run unit tests:
```
python test.py
```

## Usage

### Initialization

On initialization visualCaptcha function requires a `Session` session object as first argument:

```python
from visualcaptcha import Session, Captcha
visualCaptcha = Captcha( Session(session) )
# Optional arguments: visualCaptcha = Captcha( Session(session, namespace), assetsPath, defaultImages, defaultAudios )
```

Where:

- `session` is a required shared session object, where correct and option values are stored for later verification in the backend
- `namespace` is an optional argument. Defaults to `'visualcaptcha'` and  you can use it to use more than one visualCaptcha in the same page
- `assetsPath` is an optional argument. Defaults to the full path of `'./assets'`.
- `defaultImages` is an optional parameter. Defaults to the array inside of `./assets/images.json`. The `path` key is relative to `./assets/images/`
- `defaultAudios` is an optional parameter. Defaults to the array inside of `./assets/audios.json`. The `path` key is relative to `./assets/audios/`

### visualCaptcha.Captcha attributes

- `session`, `Session` object — An object that will have a reference for the session object.
It will have the following keys inside `visualCaptcha` key: `images`, `audios`, `validImageOption`, and `validAudioOption`.

- `imageOptions`, list — All the image options.
These can be easily overwritten with `defaultImages` when initializing `Captcha`.
By default, they're populated using the `./assets/images.json` file.

- `audioOptions`, list — All the audio options.
These can be easily overwritten with `defaultAudios` when initializing `Captcha`.
By default, they're populated using the `./assets/audios.json` file.

### visualCaptcha.Captcha methods

- `generate: ( self, numberOfOptions = 5 )` — Generate a new valid visualCaptcha front-end data. `numberOfOptions` — is an optional parameter for the number of generated images, defaults to `5`.
- `getFrontendData: ( self )` — Get data to be used by the frontend.
- `getValidImageOption: ( self )` — Get the current validImageOption.
- `getValidAudioOption: ( self )` — Get the current validAudioOption.
- `validateImage: ( self, sentOption )` — Validate the sent image value (sentOption) with the validImageOption.
- `validateAudio: ( self, sentOption )` — Validate the sent audio value (sentOption) with the validAudioOption.
- `getImageOptions: ( self )` — Return generated image options.
- `getImageOptionAtIndex: ( self, index )` — Return generated image option at given index.
- `getAudioOption: ( self ) ` — Alias for getValidAudioOption.
- `getAllImageOptions: ( self )` — Return all the image options.
- `getAllAudioOptions: ( self )` — Return all the audio options.
- `streamAudio: ( self, headers, fileType = 'mp3' )` — Stream audio file. Parameters:
  - `headers` is a list with the HTTP headers to be set;
  - `fileType` is the audio filetype, defaults to `'mp3'`, and it can also be `'ogg'`.
- `streamImage: ( self, headers, index, isRetina = False )` — Stream image file at given index for generated options. Parameters:
  - `headers` is a list with the HTTP headers to be set;
  - `index` is index of the image in the session images list to receive;
  - `isRetina`, boolean, deciding if the normal or retina image should be streamed, defaults to `False`.

## Pushing to PyPi

`$ python setup.py sdist upload`