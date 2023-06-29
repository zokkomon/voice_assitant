import speech_recognition as sr
import pyttsx3
import openai  
from gtts import gTTS
import pywhatkit
import datetime
import wikipedia
import pyjokes
import sys
import os
import webbrowser
from playsound import playsound

#set your openai key
openai.api_key="OpenAI api key"

#intailize speech to text
engine = pyttsx3.init()

def assistant(filename):
    listener = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        voice = listener.record(source)
        listener.pause_threshold = 2
    try:
        return listener.recognize_google(voice,language='en-IN')
    except:
        print('unknown error')
     
def run_guru(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]

def talk(text):
    engine.say(text)
    engine.runAndWait()

#intailize text to speech
def main():
    while True:
        #wait for user to say guru
        print("Say guru")
        talk('say guru')
        with sr.Microphone() as source:
            listener = sr.Recognizer()
            listener.pause_threshold = 2
            voice = listener.listen(source)
            try:
                transcription = listener.recognize_google(voice,language='en-IN')
                if transcription.lower() == "guru":
                    #Record audio
                    print("Hukum Aakaa...")
                    talk("hukum aakaa...")
                    with sr.Microphone() as source:
                        listener = sr.Recognizer()
                        source.pause_threshold = 1
                        voice = listener.listen(source, phrase_time_limit=None, timeout=None,)
                        with open('path to save input.wav', "wb") as f:
                            f.write(voice.get_wav_data())

                    #transcribe audio to speech
                    text = assistant(filename)
                    if 'goodbye' in text.lower() or 'exit' in text.lower():
                        talk('Goodbye!')
                        sys.exit()

                    elif 'query' in text:
                        print(f"You said: {text}")
                        fn = "gpt.wav"
                        print("Say your Query...")
                        with sr.Microphone() as source:
                            listener = sr.Recognizer()
                            voice = listener.listen(source, phrase_time_limit=None, timeout=None)
                            with open(fn, "wb") as f:
                                f.write(voice.get_wav_data())

                            with sr.AudioFile('path to save gpt.wav') as source:
                                audio_data = listener.record(source)
 
                                # Convert speech to text
                                audio = listener.recognize_google(audio_data)

                                # Print the text
                                print(audio)
                        
                        #Generate response with GPT_3
                        response = run_guru(audio)
                        print(f"GPT-3 says: {response}")
                        #record audio with gtts for video
                        tts = gTTS(text=response, lang= 'en')
                        tts.save("path to save sample.mp3")

                        playsound('sample.mp3')
                        #Read resposne using tts:
                        # talk(response)

                    elif 'search' in text:
                        kw = text.replace('search', '')
                        pywhatkit.search(kw)
                        talk("Searching..." + kw)
                         
                    elif 'play' in text:
                        song = text.replace('play', '')
                        pywhatkit.playonyt(song)
                        talk('playing' + song)

                    elif 'send message' in text:
                        pywhatkit.sendwhatmsg_instantly("Phone Number","hey",10,True,2)
                        talk("message sended!")

                        '''pywhatkit.sendwhatmsg_to_group_instantly("WhatsApp Group Name", "Hey All!",15,14)
                        talk("Successfully Sent!")'''

                    elif 'send image' in text:
                        pywhatkit.sendwhats_image("+918511346537", "path of ypur local image")
                        talk('image sended')
                        
                    elif 'time' in text:
                        time = datetime.datetime.now().strftime('%I:%M %p')
                        talk('Current time is ' + time)

                    elif 'who is' in text:
                        person = text.replace('who is', '')
                        info = wikipedia.summary(person, 1)
                        print(info)
                        talk(info)

                    elif 'open files' in text:
                        webbrowser. open('path')

                    elif 'date' in text:
                        talk('sorry, I have a headache')

                    elif 'are you single' in text:
                        talk('I am in a relationship with wifi')

                    elif 'joke' in text:
                        talk(pyjokes.get_joke())

                    else:
                        talk('Please say the text again.')

            
            except Exception as e:
                print("An error occurred: {}".format(e))

while True:
    main()





                    
                        
                                    
                



