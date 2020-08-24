import random

# ------------------------- Dad, begin copying this code -------------------------
import azure.cognitiveservices.speech as speechsdk

# Azure subscription setup
speech_key = "4a4f2a0b23ff40d8bdafa2aa0b116849"
service_region = "eastus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Creates a speech synthesizer using the default speaker as audio output.
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

# Helper function. Usage:
#
#   speak_neural(voice, style, rate, text)
#
# Voices (https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#neural-voices):
#   en-US-GuyNeural
#   en-US-AriaNeural
#
# Styles (Aria only?)
#   newscast-formal     A formal, confident and authoritative tone for news delivery
#   newscast-casual	    A versatile and casual tone for general news delivery
#   customerservice     Expresses a friendly and helpful tone for customer support
#   chat	            Expresses a casual and relaxed tone
#   cheerful            Expresses a positive and happy tone
#   empathetic          Expresses a sense of caring and understanding
#
# Rate:
#   0.5 - 2.0           Maybe faster or slower, but not much use outside this range
def speak_neural(voice, style, rate, text):
    ssml_string = \
        "<speak version=\"1.0\" xmlns=\"http://www.w3.org/2001/10/synthesis\" xmlns:mstts=\"https://www.w3.org/2001/mstts\" xml:lang=\"en-US\">" + \
            "<voice name=\"" + voice + "\">" + \
                "<prosody rate=\"" + rate + "\">" + \
                    "<mstts:express-as style=\"" + style +"\">" + \
                        text + \
                    "</mstts:express-as>" + \
                "</prosody>" + \
            "</voice>" + \
        "</speak>"

    # Use to debug XML formatting issues.
    # print(ssml_string)

    result = speech_synthesizer.speak_ssml_async(ssml_string).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech successfully synthesized to speaker")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))

# ------------------------- End of code to copy -------------------------



# The program
if __name__ == '__main__':
    words = [ "apple", "bannana", "pear", "tomato", "cucumber", "steak" ]

    # List the known en-US voices.
    voices = [ "en-US-GuyNeural", "en-US-AriaNeural" ]
    for index, voice in enumerate(voices):
        print(f"#{index}: {voice}")

    # Ask the user which voice to use.
    voice_index = int(input("Which voice should I use? "))

    word = words[random.randint(0, len(words) - 1)]
    speak_neural(voices[voice_index], "chat", "0.9", f"The word is... {word}")

    user_heard = input("Which word did you hear? ")
    if user_heard == word:
        print("Correct!")
    else:
        print(f"Sorry, it was actually: '{word}'")