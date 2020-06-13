import pyttsx3
import random

engine = pyttsx3.init()
words = [ "apple", "bannana", "pear", "tomato", "cucumber", "steak" ]

# List all of the available local voices.
voices = engine.getProperty('voices')
for index, voice in enumerate(voices):
    print(f"#{index}: {voice.name}")

# Ask the user which voice to use and set the corresponding property.
voice_index = int(input("Which voice should I use? "))
engine.setProperty('voice', voices[voice_index].id)

# Set other available properties (optional).
engine.setProperty('rate', 80)      # Talk at 80% normal speed
engine.setProperty('volume', 1.0)   # Talk at 100% volume

# Now say a random word from the list.
word = words[random.randint(0, len(words) - 1)]
engine.say(f"The word is... {word}")

# Block, processing events until the engine is done. This has a slightly annoying 
# delay at the end that's probably not going to easy to work around.
engine.runAndWait()

user_heard = input("Which word did you hear? ")
if user_heard == word:
    print("Correct!")
else:
    print(f"Sorry, it was actually: '{word}'")