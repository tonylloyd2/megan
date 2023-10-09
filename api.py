import speech_recognition as sr
from gtts import gTTS
import winsound
from pydub import AudioSegment
import pyautogui
import webbrowser
import requests
from urllib.parse import quote


def listen_for_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for commands...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return None
    except sr.RequestError:
        print("Unable to access the Google Speech Recognition API.")
        return None

def respond(response_text):
    print(response_text)
    tts = gTTS(text=response_text, lang='en')
    tts.save("response.mp3")
    sound = AudioSegment.from_mp3("response.mp3")
    sound.export("response.wav", format="wav")
    winsound.PlaySound("response.wav", winsound.SND_FILENAME)
    # os.system("afplay response.mp3") for non-windows

# tasks = []
listeningToTask = False

def main():
    # global tasks
    # global listeningToTask
    # respond("Hello, lloyd. I hope you're having a nice day today.")
    while True:
        command = listen_for_command()

        triggerKeyword = "megan"

        
        if command and (triggerKeyword in command or listeningToTask):
            if listeningToTask:
                x = requests.get('https://script.google.com/macros/s/<scriptId>/exec?text=' + quote(command))
                listeningToTask = False
                respond("Adding " + command + " to your task list.")
            elif "add a task" in command:
                listeningToTask = True
                respond("Sure, what is the task?")
            elif "list tasks" in command:
                x = requests.get('https://script.google.com/macros/s/<scriptId>/exec?q=list')
                json = x.json()
                tasks = json['tasks']
                respond("Sure. Your tasks are:")
                for task in tasks:
                    respond(task)
            elif "take a screenshot" in command:
                pyautogui.screenshot("screenshot.png")
                respond("I took a screenshot for you.")
            elif "open chrome" in command:
                respond("Opening Chrome.")
                webbrowser.open("http://www.youtube.com")
            elif "exit" in command:
                respond("Goodbye!")
                break
            else:
                respond("Sorry, I'm not sure how to handle that command.")

if __name__ == "__main__":
    # print(quote("bologna pet the dog"))
    main()
    # x = requests.get('https://script.google.com/macros/s/<scriptId>/exec?text=Like%20the%20video!')
    # print(x)
    # print(x.json())
	