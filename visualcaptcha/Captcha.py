import os
import re
import json
import random
import mimetypes


class Captcha(object):

    # @param session is the default session object
    # @param Assets path. By default, it will be ./assets
    # @param defaultImages is optional. Defaults to the array inside ./images.json. The path is relative to ./assets/images/
    # @param defaultAudios is optional. Defaults to the array inside ./audios.json. The path is relative to ./assets/audios/
    def __init__(self, session={}, assetsPath='', defaultImages=[], defaultAudios=[]):
        # Attach the session object reference to visualCaptcha
        self.session = session

        # If no assetsPath is specified, set the default
        if (not assetsPath or assetsPath == ''):
            self.assetsPath = os.path.dirname(os.path.realpath(__file__)) + '/assets'
        else:
            self.assetsPath = assetsPath

        # If there are no defaultImages, get them from ./images.json
        if (not defaultImages or len(defaultImages) == 0):
            defaultImages = self.utilReadJSON(self.assetsPath + '/images.json')

        # If there are no defaultAudios, get them from ./audios.json
        if (not defaultAudios or len(defaultAudios) == 0):
            defaultAudios = self.utilReadJSON(self.assetsPath + '/audios.json')

        # Attach the images object reference to visualCaptcha
        self.imageOptions = defaultImages

        # Attach the audios object reference to visualCaptcha
        self.audioOptions = defaultAudios

    # Generate a new valid option
    # @param numberOfOptions is optional. Defaults to 5
    def generate(self, numberOfOptions=5):
        imageValues = []

        # Save previous image & audio options from session
        oldImageOption = self.getValidImageOption()
        oldAudioOption = self.getValidAudioOption()

        # Reset the session data
        self.session.clear()

        # Avoid the next IF failing if a string with a number is sent
        numberOfOptions = int(numberOfOptions)

        # Set the minimum numberOfOptions to two
        if (numberOfOptions < 2):
            numberOfOptions = 2

        # Shuffle all imageOptions
        random.shuffle(self.imageOptions)

        # Get a random sample of X images
        images = random.sample(self.imageOptions, numberOfOptions)

        # Set a random value for each of the images, to be used in the frontend
        for image in images:
            randomValue = self.utilRandomHex(10)
            imageValues.append(randomValue)

            image['value'] = randomValue

        self.session.set('images', images)

        # Select a random image option, pluck current valid image option
        condition = True
        while condition:
            newImageOption = random.sample(self.getImageOptions(), 1)[0]

            condition = (oldImageOption and oldImageOption['path'] == newImageOption['path'])

        self.session.set('validImageOption', newImageOption)

        # Select a random audio option, pluck current valid audio option
        condition = True
        while condition:
            newAudioOption = random.sample(self.audioOptions, 1)[0]

            condition = (oldAudioOption and oldAudioOption['path'] == newAudioOption['path'])

        self.session.set('validAudioOption', newAudioOption)

        # Set random hashes for audio and image field names, and add it in the frontend data object
        validImageOption = self.getValidImageOption()

        self.session.set('frontendData', {
            'values': imageValues,
            'imageName': validImageOption['name'],
            'imageFieldName': self.utilRandomHex(10),
            'audioFieldName': self.utilRandomHex(10)
        })

    # Stream audio file
    # @param headers object. used to store http headers for streaming
    # @param fileType defaults to 'mp3', can also be 'ogg'
    def streamAudio(self, headers, fileType='mp3'):
        audioOption = self.getValidAudioOption()
        # If there's no audioOption, we set the file name as empty
        audioFileName = audioOption['path'] if audioOption else ''

        audioFilePath = self.assetsPath + '/audios/' + audioFileName

        # If the file name is empty, we skip any work and return a 404 response
        if (audioFileName != ''):
            # We need to replace '.mp3' with '.ogg' if the fileType == 'ogg'
            if (fileType == 'ogg'):
                audioFilePath = re.sub(r'(?i)\.mp3', '.ogg', audioFilePath)
            else:
                # This isn't doing anything, really, but I feel better with it
                fileType = 'mp3'

            return self.utilStreamFile(headers, audioFilePath)

        return False

    # Stream image file given an index in the session visualCaptcha images array
    # @param headers object. used to store http headers for streaming
    # @param index of the image in the session images array to send
    # @param isRetina boolean. Defaults to false
    def streamImage(self, headers, index, isRetina=False):
        imageOption = self.getImageOptionAtIndex(index)
        # If there's no imageOption, we set the file name as empty
        imageFileName = imageOption['path'] if imageOption else ''
        imageFilePath = self.assetsPath + '/images/' + imageFileName

        # Force boolean for isRetina
        if isRetina:
            isRetina = 1
        else:
            isRetina = 0

        isRetina = int(isRetina) >= 1

        # If retina is requested, change the file name
        if (isRetina):
            imageFileName = re.sub(r'(?i)\.png', '@2x.png', imageFileName)
            imageFilePath = re.sub(r'/(?i)\.png', '@2x.png', imageFilePath)

        # If the index is non-existent, the file name will be empty, same as if the options weren't generated
        if (imageFileName != ''):
            return self.utilStreamFile(headers, imageFilePath)

        return False

    # Get data to be used by the frontend
    def getFrontendData(self):
        return self.session.get('frontendData')

    # Get the current validImageOption
    def getValidImageOption(self):
        return self.session.get('validImageOption')

    # Get the current validAudioOption
    def getValidAudioOption(self):
        return self.session.get('validAudioOption')

    # Validate the sent image value with the validImageOption
    def validateImage(self, sentOption):
        validImageOption = self.getValidImageOption()

        return (sentOption == validImageOption['value'])

    # Validate the sent audio value with the validAudioOption
    def validateAudio(self, sentOption):
        validAudioOption = self.getValidAudioOption()

        return (sentOption == validAudioOption['value'])

    # Return generated image options
    def getImageOptions(self):
        return self.session.get('images')

    # Return generated image option at index
    def getImageOptionAtIndex(self, index):
        index = int(index)
        imageOptions = self.getImageOptions()

        return imageOptions[index] if ((len(imageOptions) > (index - 1)) and imageOptions[index]) else None

    # Alias for getValidAudioOption
    def getAudioOption(self):
        return self.getValidAudioOption()

    # Return all the image options
    def getAllImageOptions(self):
        return self.imageOptions

    # Return all the audio options
    def getAllAudioOptions(self):
        return self.audioOptions

    # Create a hex string from random bytes
    def utilRandomHex(self, count):
        return os.urandom(count).encode('hex')

    # Read input file as JSON
    def utilReadJSON(self, filePath):
        if (not os.path.isfile(filePath)):
            return None

        json_data = open(filePath)
        data = json.load(json_data)
        json_data.close()

        return data

    # Stream file from path
    def utilStreamFile(self, headers, filePath):
        if (not os.path.isfile(filePath)):
            return False

        mimeType = self.getMimeType(filePath)

        # Set the appropriate mime type
        headers['Content-Type'] = mimeType

        # Make sure this is not cached
        headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        headers['Pragma'] = 'no-cache'
        headers['Expires'] = 0

        f = open(filePath)
        content = f.read()
        f.close()

        return content

    # Get File's mime type
    def getMimeType(self, filePath):
        return mimetypes.guess_type(filePath)[0]
