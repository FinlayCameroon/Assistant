import sys
import webbrowser
import io
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import tempfile
import os


temp_dir = tempfile.mkdtemp()
save_path = os.path.join(temp_dir, "temp.wav")


def volumeUp():
    import volumeControl as vc
    vc.VolumeControl().changeVolume(0.0)


def muteAudio():
    import volumeControl as vc
    vc.VolumeControl().changeVolume(-85.0)


def volumeDown():
    import volumeControl as vc
    vc.VolumeControl().changeVolume(-12.0)


def API_REQUEST(text):
    import requests
    API_KEY = "your own api key"
    r = requests.post('https://api.carterapi.com/v0/chat', json={
        'api_key': f'{API_KEY}',
        'query': f'{text}',
        'uuid': "user-id-123",
    })
    agent_response = r.json()
    return agent_response


def linearSearch(data, target):
    for x in range(len(data)):
        if data[x] == target:
            return x
            break


def audioToText(audioFile):
    model = whisper.load_model("large", in_memory=True) # change model size from large to medium if computer is lower end
    result = model.transcribe(audioFile)
    print(result["text"])


def openTwitter():
    webbrowser.open_new_tab("https://twitter.com")


def openYoutube():
    webbrowser.open_new_tab("https://www.youtube.com")


def connectionCheck():
    import socket
    try:
        socket.create_connection(('google.com', 80))
        print("Everything is fully connected")
        return True
    except OSError:
        print("Connection is not available")
        return False
        


def time(rawInput):
    from requests_html import HTMLSession
    s = HTMLSession()
    from nltk import tokenize
    pos = 0
    place = tokenize.word_tokenize(rawInput)
    for x in range(len(place)):
        if place[x] == "in" or place[x] == "at" or place[x] == "In" or place[x] == "At":
            pos = x+1
    place = place[pos:]
    place = " ".join(place)
    url = f'https://www.google.com/search?q=time+in+{place}'
    r = s.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36 OPR/88.0.4412.75'})
    time = r.html.find('div.wDYxhc', first=True).text
    time = time.replace("Feedback", "")
    time = time.replace("Local Time", "")
    time = tokenize.word_tokenize(time)
    time = f"The time in {place} is {time[0]}"
    print(time)


def weatherInformation(rawInput):
    from requests_html import HTMLSession
    from nltk import tokenize
    s = HTMLSession()
    pos = 0
    place = tokenize.word_tokenize(rawInput)
    for x in range(len(place)):
        if place[x] == "in" or place[x] == "at" or place[x] == "In" or place[x] == "At":
            pos = x+1
    place = rawInput[pos:]
    url = f'https://www.google.com/search?q=what+is+the+weather+in+{place}'
    r = s.get(url, headers={
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36 OPR/88.0.4412.75'})
    temp = r.html.find('span#wob_tm', first=True).text
    unit = r.html.find('div.vk_bk.wob-unit span.wob_t', first=True).text
    desc = r.html.find('div.VQF4g', first=True).find(
        'span#wob_dc', first=True).text
    place = r.html.find('div.wob_loc', first=True).text
    res = f"It is {temp}{unit} and it's {desc} in {place}"
    print(res)


def textSummarizer(textToBeSummarized):
    import requests
    API_TOKEN = 'your own api key'
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query({
        "inputs": f"{textToBeSummarized}", "options": {"use_gpu": True} # turn "use_gpu" to False if you dont have HuggingFace Pro subscription
    })
    print(output[0]['summary_text'])


def newsRequest():
    print("Not yet implemented")
    # will use webscraping to gather data from twitter, bbc, ect


def websiteFinder(query):
    from nltk import tokenize
    from googlesearch import search

    query = tokenize.word_tokenize(query)
    for x in range(len(query)):
        if query[x] == "keyword" or query[x] == "keywords":
            pos = x+1
    query = query[pos:]
    query = " ".join(query)
    searchResults = search(query, num_results=10, lang="en")
    print("These are some of the top results for your search:")
    for result in searchResults:
        print(result)
        webbrowser.open_new_tab(result)


def bigSearch(query):
    import BigQuery
    from nltk import tokenize
    query = tokenize.word_tokenize(query)
    pos = 0
    for x in range(len(query)):
        if query[x] == "keyword" or query[x] == "keywords":
            pos = x+1
    query = query[pos:]
    query = " ".join(query)
    searchEngine = BigQuery.BigQuery(query)
    wikipediaResult = searchEngine.wikiSearch()
    googleScientificResult, googleScientificFact, googleGeneralInformationResult = searchEngine.googleSearch()
    wolframalphaResult = searchEngine.wolframalphaSearch()
    result = f"{wikipediaResult}\n{googleScientificResult}\n{googleScientificFact}\n{googleGeneralInformationResult}\n{wolframalphaResult}"
    textSummarizer(result)


def checkCustomTriggers(api_response):
    customTriggers = api_response["triggers"]
    numOfActivatedTriggers = 0
    for trigger in customTriggers:
        numOfActivatedTriggers += 1
    arrayOfCustomTriggers = [str() for x in range(numOfActivatedTriggers)]
    loopCounter = 0
    for trigger in customTriggers:
        arrayOfCustomTriggers[loopCounter] = trigger['type']
        loopCounter += 1

    return arrayOfCustomTriggers


def activeCustomTriggers(activatedTriggers, rawInput):
    for trigger in activatedTriggers:
        if trigger == "Volume-Up":
            volumeUp()
        elif trigger == "MuteAudio":
            muteAudio()
        elif trigger == "volumeDown":
            volumeDown()
        elif trigger == "Weather-Information":
            weatherInformation()
        elif trigger == "Time":
            time(rawInput)
        elif trigger == "Search-Google":
            bigSearch(rawInput)
        elif trigger == "Exit":
            sys.exit()
        elif trigger == "Transcribe-Audio":
            audioFilePath = input("Enter the path to the audio file: ")
            audioToText(audioFilePath)
        elif trigger == "Text-Summarizer":
            textToBeSummarized = input(
                "Enter the text you want to summarize: ")
            textSummarizer(textToBeSummarized=textToBeSummarized)
        elif trigger == "Open-Twitter":
            openTwitter()
        elif trigger == "Open-Youtube":
            openYoutube()
        elif trigger == "Website-Finder":
            websiteFinder(rawInput)
        elif trigger == "News-Request":
            newsRequest()
        elif trigger == "Connection-Check":
            connectionCheck()

    else:
        pass


def main(model="base", english=True, energy=500, dynamic_energy=True, verbose=False, pause=0.8):
    if model != "large" and english:
        model = model + ".en"
    audio_model = whisper.load_model(model, in_memory=True)

    r = sr.Recognizer()
    r.energy_threshold = energy
    r.pause_threshold = pause
    r.dynamic_energy_threshold = dynamic_energy

    assistantOnline = connectionCheck()

    if assistantOnline == True:
        with sr.Microphone(sample_rate=16000) as source:
            print("Say something!")
            while assistantOnline:
                print("Listening...")
                # get and save audio to wav file
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                data = io.BytesIO(audio.get_wav_data())
                audio_clip = AudioSegment.from_file(data)
                audio_clip.export(save_path, format="wav")
                try:
                    if english:
                        print("Transcribing...")
                        result = audio_model.transcribe(
                            save_path, language='english')
                    else:
                        print("Transcribing...")
                        result = audio_model.transcribe(save_path)

                    if not verbose:
                        predicted_text = result["text"]
                        print(f"You said: {predicted_text}")
                    else:
                        print(result)
                except:
                    print("Error: Could not transcribe audio")
                if len(predicted_text) > 2:
                    apiAns = API_REQUEST(predicted_text)
                    arrayOfActivatedTriggers = checkCustomTriggers(apiAns)
                    activeCustomTriggers(
                        arrayOfActivatedTriggers, predicted_text)
                assistantOnline = connectionCheck()


main(model="tiny", english=True, energy=450,
     dynamic_energy=True, verbose=False, pause=0.8) # if you want more accurate speech recognition change tiny to base but the bigger the model longer it will take
