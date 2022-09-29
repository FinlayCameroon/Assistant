import sys

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
    API_KEY = "0sww17AF6iXk8lbmRtx25dYWceuY6kf1"
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


def time():
    import datetime
    now = datetime.datetime.now()
    print(now.strftime("%H:%M"))


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
    print("Assistant is online")
    assistantOnline = True
    apiRes = API_REQUEST("What is the weather")
    arrayOfActivatedTriggers, arrayOfDetectedEntities = checkCustomTriggers(
        apiRes)

    assistantAnswer = activeCustomTriggers(assistantOnline, arrayOfActivatedTriggers, arrayOfDetectedEntities)


elif connectionCheck == False:
    print("Assistant is offline \nPlease become online to use my services")
    assistantOnline = False


connection = connectionCheck()
if connection == True:
    print("Assistant is online and fully functional")
    assistantOnline = True
else:
    print("Assistant is offline \nPlease become online to use my services")
    assistantOnline = False

while assistantOnline:
    apiRequest = input(str("You: "))
    arrayOfActivatedTriggers, arrayOfDetectedEntities = checkCustomTriggers(apiRes)
    assistantAnswer = activeCustomTriggers(assistantOnline, arrayOfActivatedTriggers, arrayOfDetectedEntities)
