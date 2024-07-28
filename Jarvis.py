import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import wikipediaapi
import pywhatkit
import os 
import tkinter as tk
from PIL import Image, ImageTk

# Function to update the GIF frame
def update(ind):
    frame = frames[ind]
    ind += 1
    if ind == frame_count:
        ind = 0
    response_label.configure(image=frame)
    window.after(100, update, ind)

# Initialize the Speech Recognizer
r = sr.Recognizer()

# Define the wake word or phrase
WAKE_WORD = "jarvis"

def listen_for_wake_word():
    with sr.Microphone() as source:
        print("Listening for wake word...")
        while True:
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio).lower()
                if WAKE_WORD in text:
                    print("Wake word detected!")
                    text_to_speech("Jarvis at your service , Hi! Tony!!..." )
                     # Replace with your assistant activation function
                return text.lower()
            except sr.UnknownValueError:
                listen_for_wake_word() # Ignore if the recognizer does not understand
            except sr.RequestError as e:
                print(f"Service error: {e}")

def speech_to_text():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        text_to_speech("How can i help you Tony?")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            text_to_speech(text)
            execution(text)
            return text.lower()
        except sr.UnknownValueError:
            text_to_speech("Sorry, could not understand Tony.")
            return 0
        except sr.RequestError as e:
            text_to_speech("Could not request results from Google Speech Recognition service; {0}".format(e))
            return 0

# Create the tkinter window
#window=threading.Thread(target=listen_for_wake_word).start()
window = tk.Tk()
window.title("Jarvis")

# Load the GIF frames
image = Image.open("listening1.gif")
frames = [ImageTk.PhotoImage(image.copy().convert('RGBA')) for i in range(image.n_frames)]
frame_count = len(frames)

# Add a label with the first frame of the GIF
response_label = tk.Label(window, width=400, height=400)
response_label.pack()

# Add a button to start listening and animation
listen_button = tk.Button(window, text="Start Listening", command=speech_to_text)
listen_button.pack()

# Start updating the GIF frames
window.after(0, update, 0)

def text_to_speech(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Set properties (optional)
    voice_id = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
    # You can set properties like the rate (speed) and volume
    engine.setProperty('voice', voice_id)
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)

    # Convert the text to speech
    engine.say(text)

    # Wait for the speech to finish
    engine.runAndWait()

def execution(text):

    command=text
    
    while True:
        
         if command==0:  
            continue  

         elif 'exit' in command or 'close' in command:

            text_to_speech(" Bye tony!! see you soon !!")
            window.destroy()
            break
        
         elif 'date' in command or 'time' in command:
             data_time(command)
             break
         elif "who are you" in command:
            text_to_speech("I'm JARVIS your personal assistant.")
            break
            
         elif "how are you" in command:
            text_to_speech("I'm fine Tony, What about you?")
            break
            
         elif "fine" in command:
            text_to_speech("Glad to hear that Tony!!")
            break
            
         elif "good" in command:
            text_to_speech("Glad to hear that Tony!!")
            break
        
         elif 'who is' in command or 'what is' in command:
            get_wikipedia_summary(command)
            break

         elif 'open' in command:
            if not (check_sysApps(command)):
                open_website(command)
            break

         elif 'play' in command:
            command = remove(command)
            play(command)
            break


         elif 'search' in command:
            command = remove(command)
            pywhatkit.search(command)
            break
        
         else:
            text_to_speech('Access Denied')
            break

def remove(command):
    element = ['what is','who is','open','.com','please','play','can','you','website','for me','search','for', ' ']
    for x in element:
        if x in command:
            command = command.replace(x, '')

    return command


def data_time(command):
    if 'time' in command:
        current_time = datetime.datetime.now().time()
        time = current_time.strftime("%#I %#M %p")
        text_to_speech("current time is"+time)

    if 'date' in command:
        current_date = datetime.date.today()
        date= current_date.strftime("%A, %#d  %B %Y")
        text_to_speech(date)


def get_wikipedia_summary(query, lang='english'):
    
    query = remove(query)
    wiki_wiki = wikipediaapi.Wikipedia(lang)
    page_py = wiki_wiki.page(query)

    if not page_py.exists():
        text_to_speech(f"Page '{query}' does not exist on Wikipedia.")
        pywhatkit.search(query)

    text = page_py.summary[:500]
    text_to_speech(text)

def check_sysApps(command):
    applications = ['notepad.exe', 'calc.exe', 'explorer.exe', 'control.exe', 'taskmgr.exe', 'cmd.exe', 
              'powershell.exe', 'regedit.exe', 'devmgmt.msc', 'services.msc', 'compmgmt.msc', 
              'diskmgmt.msc', 'mspaint.exe', 'wordpad.exe', 'msconfig.exe', 'notepad++.exe', 
              'chrome.exe', 'iexplore.exe', 'outlook.exe', 'winword.exe', 'excel.exe', 'powerpnt.exe',
                'code.exe',  'skype.exe' ,  'zoom.exe', 'teams.exe', ]

    app_names=['notepad', 'calculator', 'fileexplorer', 'controlpanel', 'taskmanager', 'commandpromptcmd',
            'powershell', 'registryeditor', 'devicemanager', 'services', 'computermanagement', 
            'diskmanagement', 'mspaint', 'wordpad', 'systemconfiguration', 'notepad++', 'chrome',
            'internetexplorer', 'microsoftoutlook(msoutkook)', 'word', 'excel', 
            'powerpoint', 'visualstudiocodevscode', 'skype', 'zoom', 'teams', ]
    command = remove(command)
    print(command)
    for x in range(len(app_names)):
        
        if command in app_names[x] or app_names[x] in command:
            if command =='':
                text_to_speech(" tell the application name to be open Tony")
                return True
            print("validated",app_names[x],' ',applications[x])
            open_application(applications[x])
            return True
        
    return False


def open_application(application_path):
    try:
        # Using os.system to open the application
        text_to_speech("Opening Your Application",application_path)
        os.system('start '+application_path)

    except FileNotFoundError:
        text_to_speech(f"Error: Application not found at {application_path}")
    except Exception as e:
        text_to_speech(f"unexpected error occurred: {e}")
        

            
def open_website(command):
    command = remove(command)
    url = 'www.'+command+'.com'
    url= url.replace(' ', '')
    print(url)
    webbrowser.open(url)

def play(command):
    try:
        pywhatkit.playonyt(command)
        text_to_speech("Playing..."+command)

    except:
        text_to_speech("Network Error  try again...")


if __name__ == '__main__':
    txt=listen_for_wake_word()
    if WAKE_WORD==txt:
        window.mainloop()
    
    