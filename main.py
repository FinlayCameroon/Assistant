import sys

def volumeUp():
    import volumeControl as vc
    vc.VolumeControl().changeVolume(0.0)
    print("Volume set to max")

def muteAudio():
    import volumeControl as vc
    vc.VolumeControl().changeVolume(-85.0)
    print("Audio fully muted")

def volumeDown():
    import volumeControl as vc
    vc.VolumeControl().changeVolume(-12.0)
    print("Volume lowered")

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

def connectionCheck():
    import socket
    try:
        socket.create_connection(('google.com', 80))
        return True
    except OSError:
        return False

def time(location):
    from requests_html import HTMLSession
    s = HTMLSession()

    if location[0] == "location":
        url = f'https://www.google.com/search?q=what+is+the+time+in+{location[1]}'
    else:
        url = f'https://www.google.com/search?q=what+is+the+time'
    r = s.get(url, headers={
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36 OPR/88.0.4412.75'})
    time = r.html.find('gsrt vk_bk FzvWSb YwPhnf',first=True).text
    if location[0] == "location":
        res = f"In {location[1]} it is {time}"
    else:
        res = f"It is {time}"
    print(res)

def weatherInfo(location):
    from requests_html import HTMLSession
    s = HTMLSession()

    if location[0] == "location":
        url = f'https://www.google.com/search?q=weather+in+{location[1]}'
    else:
        url = f'https://www.google.com/search?q=what+is+the+weather'
    r = s.get(url, headers={
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36 OPR/88.0.4412.75'})
    temp = r.html.find('span#wob_tm', first=True).text
    unit = r.html.find('div.vk_bk.wob-unit span.wob_t', first=True).text
    desc = r.html.find('div.VQF4g', first=True).find(
        'span#wob_dc', first=True).text
    if location[0] == "location":
        res = f"In {location[1]} it is {temp}{unit} and it's {desc}"
    else:
        res = f"It is {temp}{unit} and it's {desc}"
    print(res)
    
def googleSearch(query):
    from nltk import tokenize
    from googlesearch import search
    query = tokenize.word_tokenize(query)
    for x in range(len(query)):
        if query[x] == "keyword" or query[x] == "keywords":
            pos = x+1
    query = query[pos:]
    query = " ".join(query)
    searchResults = search(query, num_results=3, lang="en")
    print("These are some of the top results for your search:")
    for result in searchResults:
        print(result)    

def textSummarizer(textToBeSummarized):
    import requests
    API_TOKEN = 'your_own_api'
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    posOfText = (linearSearch(textToBeSummarized,":"))+1
    output = query({
        "inputs": f"{textToBeSummarized[posOfText:]}",
    })
    print(output[0]['summary_text'])  
    
def checkCustomTriggers(api_response):
    customTriggers = api_response['triggers']
    numOfActivatedTriggers = 0
    for trigger in customTriggers:
        numOfActivatedTriggers += 1
    arrayOfCustomTriggers = [str() for x in range(numOfActivatedTriggers)]
    loopCounter = 0
    for trigger in customTriggers:
        arrayOfCustomTriggers[loopCounter] = trigger['type']
        loopCounter += 1

    entitiesDetection = customTriggers[0]['entities']
    entityResult = ["Not Found"]
    if entitiesDetection != "[]":
        for entity in entitiesDetection:
            entityType = entity['label']
            entityWord = entity['word']
            entityResult = [entityType, entityWord]
    
    

    return arrayOfCustomTriggers, entityResult

def activeCustomTriggers(activatedTriggers, entityResult):
    for trigger in activatedTriggers:
        if trigger == "Volume-Up":
            volumeUp()
        elif trigger == "MuteAudio":
            muteAudio()
        elif trigger == "volumeDown":
            volumeDown()
        elif trigger == "Weather":
            weatherInfo(entityResult)
        elif trigger == "Time":
            time()
        elif trigger == "Search-Google":
            pass  # google search
        elif trigger == "Exit":
            sys.exit()
    else:
        pass



connection = connectionCheck()
if connection == True:
    print("Assistant is online and fully functional")
    assistantOnline = True
else:
    print("Assistant is offline \nPlease become online to use my services")
    assistantOnline = False

while assistantOnline:
    apiRequest = input(str("You: "))
    arrayOfActivatedTriggers, arrayOfDetectedEntities = checkCustomTriggers(apiRequest)
    assistantAnswer = activeCustomTriggers(assistantOnline, arrayOfActivatedTriggers, arrayOfDetectedEntities)
   
