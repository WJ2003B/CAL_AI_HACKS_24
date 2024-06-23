import time
import azure.cognitiveservices.speech as speechsdk

def configure_speech_recognition():
    speech_config = speechsdk.SpeechConfig(subscription="a8f58060ddcf4eeebdb3db9a07ca670f", region="eastus")
    
    speech_config.speech_recognition_language = "en-US"
    audio_in_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    audio_out_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_in_config
    )
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_out_config
    )

    return speech_recognizer, speech_synthesizer

speech_recognizer, speech_synthesizer = configure_speech_recognition()
def speech_recognize_keyword_from_microphone():
    """Performs keyword-triggered speech recognition with input from the microphone"""
    speech_config = speechsdk.SpeechConfig(subscription="a8f58060ddcf4eeebdb3db9a07ca670f", region="eastus")

    # Creates an instance of a keyword recognition model. Update this to
    # point to the location of your keyword recognition model.
    speech_config.speech_recognition_language = "en-US"

    model = speechsdk.KeywordRecognitionModel("assistant.table")

    # The phrase your keyword recognition model triggers on.
    keyword = "assistant"

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    done = False

    def stop_cb(evt):
        """Callback that signals to stop continuous recognition upon receiving an event `evt`"""
        nonlocal done
        done = True

    def recognizing_cb(evt):
        """Callback for recognizing event"""
        if evt.result.reason == speechsdk.ResultReason.RecognizingKeyword:
            pass
        elif evt.result.reason == speechsdk.ResultReason.RecognizingSpeech:
            pass

    def recognized_cb(evt):
        """Callback for recognized event"""
        if evt.result.reason == speechsdk.ResultReason.RecognizedKeyword:
            pass
        elif evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print('RECOGNIZED: {}'.format(evt.result.text))
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print('NOMATCH: {}'.format(evt))

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(recognizing_cb)
    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

    # Stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start keyword recognition
    speech_recognizer.start_keyword_recognition(model)
    print('Say something starting with "{}" followed by whatever you want...'.format(keyword))
    while not done:
        time.sleep(0.5)

    speech_recognizer.stop_keyword_recognition()

    return True

def recognize_speech():
    """Function to recognize speech after keyword detection"""
    speech_config = speechsdk.SpeechConfig(subscription="a8f58060ddcf4eeebdb3db9a07ca670f", region="eastus")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    wake = False
    print("Speak into your microphone:")
    while not wake:
        wake = speech_recognize_keyword_from_microphone()
        if wake:
            break

    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    recognized_text = None  # Variable to capture the recognized speech

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        recognized_text = speech_recognition_result.text
        print(f"Recognized: {recognized_text}")

    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print(f"No speech could be recognized: {speech_recognition_result.no_match_details}")

    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))

        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")

    return recognized_text

###Text to speech###

def speak_text(speech_synthesizer, output_text):
    # if use_speech set to False do not render speech
    use_speech = True
    if use_speech:
        speech_synthesis_result = speech_synthesizer.speak_text_async(output_text).get()

        if (
            speech_synthesis_result.reason
            == speechsdk.ResultReason.SynthesizingAudioCompleted
        ):
            # successful conversion to speech
            # print(f"Speech synthesized for text [{output_text}]")
            pass

        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))

            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print(
                        "Error details: {}".format(cancellation_details.error_details)
                    )
                    print("Did you set the speech resource key and region values?")

        return speech_synthesis_result
    else:
        return ""

# Run the recognize_speech function and capture the output into a variable
recognized_speech = recognize_speech()


