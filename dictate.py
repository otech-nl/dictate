import speech_recognition as sr
import pyttsx
from sys import stderr, stdout, argv

tts = pyttsx.init('sapi5')   # Windows specific
tts.setProperty('rate', 150)
recognizer = sr.Recognizer()

print(sr.Microphone.list_microphone_names())


def log(msg):
    stderr.write(msg)


def error(msg):
    log('\n%s\n' % msg)


OUT = None
if len(argv) > 1:
    fname = argv[1]
    log('Saving to "%s".\n' % fname)
    OUT = open(fname, 'w')


def say(text, intro=''):
    tts.say(text)
    tts.runAndWait()


def i_heard(text):
    text = text.capitalize()+'.\n'
    stdout.write(text)
    if OUT:
        OUT.write(text)


text = ''
while text != 'stop':
    stderr.write('?')   # prompt
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        with open('audio.wav', 'wb') as wav:
            wav.write(audio.get_wav_data())

    stderr.write('> ')  # working...
    try:
        text = recognizer.recognize_sphinx(audio)
        # text = recognizer.recognize_google(audio)
        i_heard(text)
    except sr.UnknownValueError as e:
        error('Could not understand audio: %s' % e)
    except sr.RequestError as e:
        error('Recognition error: %s' % e)
