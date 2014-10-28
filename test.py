import os
import sys
import unittest
from visualcaptcha import *

assetsFullPath = os.path.dirname( os.path.realpath(__file__) ) + '/visualcaptcha/assets'
visualCaptcha = None
sessionMock = {}

# Runs before each test
def globalSetup():
    global visualCaptcha, sessionMock

    # Set a new "session" every time
    sessionMock = Session({})

    # Start visualCaptcha with that new session
    visualCaptcha = Captcha( sessionMock )

# Helper function to check if an object exists in an array
def containsObject( theObject, array ):
    for element in array:
        if theObject == element:
            return True

    return False

# Test Setup exceptions
class SetupTest( unittest.TestCase ):

    # Runs before each test in this group
    def setUp( self ):
        globalSetup()

    # Should return nothing if nothing is set
    def test_session_nothing_set( self ):
        session = Session()
        self.assertIsNone( session.get('test') )

    # Should return something if something is set
    def test_session_set( self ):
        session = Session()
        session.set( 'test', 'awesome' )
        self.assertEqual( session.get('test'), 'awesome' )

    # Should allow an array of dicts to be used instead of the default images for options
    def test_image_array( self ):
        global sessionMock

        imageOptions = [{
            'name': 'Test',
            'path': 'test.png'
        }]

        visualCaptcha = Captcha( sessionMock, False, imageOptions )

        obtainedImages = visualCaptcha.getAllImageOptions()

        self.assertIsNotNone( obtainedImages )

        self.assertEqual( len(obtainedImages), 1 )

        # Check the obtained image is the same we sent over
        self.assertIsNotNone( obtainedImages[0]['name'] )
        self.assertIsNotNone( obtainedImages[0]['path'] )

        self.assertEqual( obtainedImages[0]['name'], 'Test' )
        self.assertEqual( obtainedImages[0]['path'], 'test.png' )

    # Should allow an array of dicts to be used instead of the default audios for options
    def test_audio_array( self ):
        global sessionMock

        audioOptions = [{
            'path': 'test.mp3',
            'value': 'test'
        }]

        visualCaptcha = Captcha( sessionMock, False, False, audioOptions )

        obtainedAudios = visualCaptcha.getAllAudioOptions()

        self.assertIsNotNone( obtainedAudios )

        self.assertEqual( len(obtainedAudios), 1 )

        # Check the obtained audio is the same we sent over
        self.assertIsNotNone( obtainedAudios[0]['path'] )
        self.assertIsNotNone( obtainedAudios[0]['value'] )

        self.assertEqual( obtainedAudios[0]['path'], 'test.mp3' )
        self.assertEqual( obtainedAudios[0]['value'], 'test' )

# Test getAllImageOptions
class ImageOptionsTest( unittest.TestCase ):

    # Runs before each test in this group
    def setUp( self ):
        globalSetup()

    # Should return the list with all the possible image options
    def test_all_image_options( self ):
        global visualCaptcha

        imageOptions = visualCaptcha.getAllImageOptions()

        self.assertIsNotNone( imageOptions )

        # We should have at least 20 image options, so probability plays a role
        self.assertTrue( len(imageOptions) > 19 )

        # Images need to have a name
        self.assertIsNotNone( imageOptions[0]['name'] )

        # Images need to have a path
        self.assertIsNotNone( imageOptions[0]['path'] )

    # Should find all the files for all the images, and their retina versions, making sure they're not empty
    def test_find_all_images_and_retina( self ):
        global visualCaptcha, assetsFullPath

        imageOptions = visualCaptcha.getAllImageOptions()
        
        for imageOption in imageOptions:
            currentImagePath = assetsFullPath + '/images/' + imageOption[ 'path' ]

            # Check the image file exists and is a file
            self.assertTrue( os.path.isfile(currentImagePath) )

            # Check the image file is not empty
            currentImageStat = os.stat( currentImagePath )
            self.assertTrue( currentImageStat.st_size > 0 )

            # Check the retina image file exists and is a file
            currentImagePath = currentImagePath.replace( '.png', '@2x.png' )
            self.assertTrue( os.path.isfile(currentImagePath) )

            # Check the retina image file is not empty
            currentImageStat = os.stat( currentImagePath )
            self.assertTrue( currentImageStat.st_size > 0 )

# Test getAllAudioOptions
class AudioOptionsTest( unittest.TestCase ):

    # Runs before each test in this group
    def setUp( self ):
        globalSetup()

    # Should return the list with all the possible audio options
    def test_all_audio_options( self ):
        global visualCaptcha

        audioOptions = visualCaptcha.getAllAudioOptions()

        self.assertIsNotNone( audioOptions )

        # We should have at least 20 audio options, so probability plays a role
        self.assertTrue( len(audioOptions) > 19 )

        # Audios need to have a path
        self.assertIsNotNone( audioOptions[0]['path'] )

        # Audios need to have a value
        self.assertIsNotNone( audioOptions[0]['value'] )

    # Should find all the files for all the audios, and their .ogg versions, making sure they're not empty
    def test_find_all_audios_and_ogg( self ):
        global visualCaptcha, assetsFullPath

        audioOptions = visualCaptcha.getAllAudioOptions()
        
        for audioOption in audioOptions:
            currentAudioPath = assetsFullPath + '/audios/' + audioOption[ 'path' ]

            # Check the audio file exists and is a file
            self.assertTrue( os.path.isfile(currentAudioPath) )

            # Check the audio file is not empty
            currentAudioStat = os.stat( currentAudioPath )
            self.assertTrue( currentAudioStat.st_size > 0 )

            # Check the ogg file exists and is a file
            currentAudioPath = currentAudioPath.replace( '.mp3', '.ogg' )
            self.assertTrue( os.path.isfile(currentAudioPath) )

            # Check the ogg audio file is not empty
            currentAudioStat = os.stat( currentAudioPath )
            self.assertTrue( currentAudioStat.st_size > 0 )

# Test generate
class GenerateTest( unittest.TestCase ):

    # Runs before each test in this group
    def setUp( self ):
        globalSetup()

    # Should generate a new valid image option each time it's called
    def test_generate_new_image( self ):
        global visualCaptcha

        # Generate first values
        visualCaptcha.generate()

        firstValue = visualCaptcha.getValidImageOption()[ 'value' ]

        # Generate second values
        visualCaptcha.generate()

        secondValue = visualCaptcha.getValidImageOption()[ 'value' ]

        # Check both values don't match
        self.assertNotEqual( firstValue, secondValue )

    # Should generate a new valid audio option each time it's called
    def test_generate_new_audio( self ):
        global visualCaptcha

        # Generate first values
        visualCaptcha.generate()

        firstValue = visualCaptcha.getValidAudioOption()[ 'value' ]

        # Generate second values
        visualCaptcha.generate()

        secondValue = visualCaptcha.getValidAudioOption()[ 'value' ]

        # Check both values don't match
        self.assertNotEqual( firstValue, secondValue )

    # Should generate new field names each time it's called
    def test_generate_new_field_name( self ):
        global visualCaptcha

        # Generate first values
        visualCaptcha.generate()

        firstImageValue = visualCaptcha.getFrontendData()[ 'imageFieldName' ]
        firstAudioValue = visualCaptcha.getFrontendData()[ 'audioFieldName' ]

        # Generate second values
        visualCaptcha.generate()

        secondImageValue = visualCaptcha.getFrontendData()[ 'imageFieldName' ]
        secondAudioValue = visualCaptcha.getFrontendData()[ 'audioFieldName' ]

        # Check both values don't match
        self.assertNotEqual( firstImageValue, secondImageValue )
        self.assertNotEqual( firstAudioValue, secondAudioValue )

    # Should generate frontend data
    def test_generate_frontend_data( self ):
        global visualCaptcha

        # Generate values
        visualCaptcha.generate()

        frontendData = visualCaptcha.getFrontendData()

        self.assertIsNotNone( frontendData['values'] )
        self.assertIsNotNone( frontendData['imageName'] )
        self.assertIsNotNone( frontendData['imageFieldName'] )
        self.assertIsNotNone( frontendData['audioFieldName'] )

        self.assertIsInstance( frontendData['values'], list )
        self.assertTrue( len(frontendData['imageName']) > 0 )
        self.assertTrue( len(frontendData['imageFieldName']) > 0 )
        self.assertTrue( len(frontendData['audioFieldName']) > 0 )

    # Should generate new frontend data each time it's called
    def test_generate_new_frontend_data( self ):
        global visualCaptcha

        # Generate first values
        visualCaptcha.generate()

        firstValue = visualCaptcha.getFrontendData()

        # Generate second values
        visualCaptcha.generate()

        secondValue = visualCaptcha.getFrontendData()

        # Check both values don't match
        self.assertNotEqual( firstValue, secondValue )

# Test validateImage
class ValidateImageTest( unittest.TestCase ):

    # Runs before each test in this group
    def setUp( self ):
        globalSetup()

    # Should return true if the chosen image option is the valid one
    def test_return_true_image( self ):
        global visualCaptcha

        # Generate option values
        visualCaptcha.generate()

        optionValue = visualCaptcha.getValidImageOption()[ 'value' ]

        # Validate, sending the right optionValue, expecting a "true" to be returned
        self.assertTrue( visualCaptcha.validateImage(optionValue) )

    # Should return false if the chosen image option is not the valid one
    def test_return_false_image( self ):
        global visualCaptcha

        # Will never match the optionValue
        optionValue = random.random()

        # Generate option values
        visualCaptcha.generate()

        # Validate, sending the right optionValue, expecting a "false" to be returned
        self.assertFalse( visualCaptcha.validateImage(optionValue) )

# Test validateAudio
class ValidateAudioTest( unittest.TestCase ):

    # Runs before each test in this group
    def setUp( self ):
        globalSetup()

    # Should return true if the chosen audio option is the valid one
    def test_return_true_audio( self ):
        global visualCaptcha

        # Generate option values
        visualCaptcha.generate()

        optionValue = visualCaptcha.getValidAudioOption()[ 'value' ]

        # Validate, sending the right optionValue, expecting a "true" to be returned
        self.assertTrue( visualCaptcha.validateAudio(optionValue) )

    # Should return false if the chosen audio option is not the valid one
    def test_return_false_audio( self ):
        global visualCaptcha

        # Will never match the optionValue
        optionValue = random.random()

        # Generate option values
        visualCaptcha.generate()

        # Validate, sending the right optionValue, expecting a "false" to be returned
        self.assertFalse( visualCaptcha.validateAudio(optionValue) )

# Test getImageOptions
class GetImageOptionsTest( unittest.TestCase ):

    # Runs before each test in this group
    def setUp( self ):
        globalSetup()

    # Should return a list with possible image options and the valid image option included
    def test_return_list_images( self ):
        global visualCaptcha

        foundValidOptions = 0
        numberOfOptions = 4

        # Generate option values ( 4 )
        visualCaptcha.generate( numberOfOptions )

        # Get the options list
        options = visualCaptcha.getImageOptions()

        optionsLength = len( options )

        self.assertEqual( optionsLength, numberOfOptions )

        # Loop through all options, and count each time an image was successfully validated
        for option in options:
            validationResult = visualCaptcha.validateImage( option['value'] )

            if ( validationResult ):
                foundValidOptions += 1

        # We should only find 1 valid option
        self.assertEqual( foundValidOptions, 1 )

    # Should return a list with all possible image options different
    def test_return_unique_list( self ):
        global visualCaptcha

        foundSimilarOptions = 0
        numberOfOptions = 4

        # Generate option values ( 4 )
        visualCaptcha.generate( numberOfOptions )

        # Get the options list
        options = visualCaptcha.getImageOptions()

        optionsLength = len( options )

        self.assertEqual( optionsLength, numberOfOptions )

        # Loop through all options, and count each time a duplicate value exists in the array
        for i in xrange( 0, optionsLength, 1 ):
            for j in xrange( 0, optionsLength, 1 ):
                if ( i != j and options[i]['value'] == options[j]['value'] ):
                    foundSimilarOptions += 1

        # We should find no equal options
        self.assertEqual( foundSimilarOptions, 0 )

    # Should return the same current image options list, if we don't generate a new valid value
    def test_return_same_list( self ):
        global visualCaptcha

        numberOfOptions = 4

        # Generate option values ( 4 )
        visualCaptcha.generate( numberOfOptions )

        # Get the first options list
        firstOptions = visualCaptcha.getImageOptions()

        # Get the second options list
        secondOptions = visualCaptcha.getImageOptions()

        # Get the third options list
        thirdOptions = visualCaptcha.getImageOptions()

        # Loop through all options, and test each time that the same object exists in both the other arrays
        for i in xrange( 0, numberOfOptions, 1 ):
            # Check if all the values match
            self.assertEqual( firstOptions[i]['value'], secondOptions[i]['value'] )
            self.assertEqual( firstOptions[i]['value'], thirdOptions[i]['value'] )

# Test getAudioOption
class GetAudioOptionTest( unittest.TestCase ):

    # Runs before each test in this group
    def setUp( self ):
        globalSetup()

    # Should return the current audio option, which should be the valid audio option
    def test_return_valid_audio( self ):
        global visualCaptcha

        # Generate option values
        visualCaptcha.generate()

        # Get the option
        option = visualCaptcha.getAudioOption()

        # Check if the audio was successfully validated
        self.assertTrue( visualCaptcha.validateAudio(option['value']) )

    # Should return the same audio option, if we don't generate a new valid value
    def test_return_same_audio( self ):
        global visualCaptcha

        # Generate option values
        visualCaptcha.generate()

        # Get the first option
        firstOption = visualCaptcha.getAudioOption()

        # Get the second option
        secondOption = visualCaptcha.getAudioOption()

        # Get the third option
        thirdOption = visualCaptcha.getAudioOption()

        # Check if all the values match
        self.assertEqual( firstOption['value'], secondOption['value'] )
        self.assertEqual( firstOption['value'], thirdOption['value'] )

# Test streamImage
class StreamImageTest( unittest.TestCase ):

    # Runs before each test in this group
    def setUp( self ):
        globalSetup()

    # Should find and stream an image file
    def test_stream_image( self ):
        global visualCaptcha

        # Generate option values
        visualCaptcha.generate()

        # Stream the image
        fileReturn = visualCaptcha.streamImage( {}, 0 )

        # Check if the image was successfully streamed
        self.assertTrue( fileReturn )

    # Should find and stream a retina image file
    def test_stream_retina( self ):
        global visualCaptcha

        # Generate option values
        visualCaptcha.generate()

        # Stream the retina image
        fileReturn = visualCaptcha.streamImage( {}, 0, True )

        # Check if the image was successfully streamed
        self.assertTrue( fileReturn )

    # Should fail to find an image file
    def test_stream_undefined_index( self ):
        global visualCaptcha

        # Generate option values
        visualCaptcha.generate()

        # Stream the image
        fileReturn = visualCaptcha.streamImage( {}, 100 )

        # Check if the image failed streaming
        self.assertFalse( fileReturn )

# Test streamAudio
class StreamAudioTest( unittest.TestCase ):

    # Runs before each test in this group
    def setUp( self ):
        globalSetup()

    # Should find and stream an audio file - mp3
    def test_stream_mp3( self ):
        global visualCaptcha

        # Generate option values
        visualCaptcha.generate()

        # Stream the mp3 audio file
        fileReturn = visualCaptcha.streamAudio( {} )

        # Check if the audio file was successfully streamed
        self.assertTrue( fileReturn )

    # Should find and stream an audio file - ogg
    def test_stream_ogg( self ):
        global visualCaptcha

        # Generate option values
        visualCaptcha.generate()

        # Stream the ogg audio file
        fileReturn = visualCaptcha.streamAudio( {}, 'ogg' )

        # Check if the audio file was successfully streamed
        self.assertTrue( fileReturn )

    # Should fail to find an audio file
    def test_stream_ungenerated_audio( self ):
        global visualCaptcha

        # Stream the audio file (we didn't generate options, so it should fail)
        fileReturn = visualCaptcha.streamAudio( {} )

        # Check if the audio failed streaming
        self.assertFalse( fileReturn )

if __name__ == '__main__':
    print "Running unit tests"
    unittest.main()
