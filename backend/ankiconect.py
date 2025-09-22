import json
import urllib.request
import shutil
import os
import base64

ANKI_MEDIAFOLDER = "C:\\Users\\Franco\\AppData\\Roaming\\Anki2\\User 1\\collection.media"

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    print(requestJson)
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

def newestcrd():
    '''
    Searches for the newest card in all decks
    '''

    todaycards = invoke("findCards", query = "added:2")
    result = invoke("cardsModTime", cards = todaycards)
    newestcard = result[0]
    for card in result:
        if card["mod"] > newestcard["mod"]:
            newestcard = card
    return newestcard["cardId"]

def formatforanki(audiopath):
    '''
    Fromats the audio filename for anki reproduction
    [sound:<audiofilename>]
    '''

    name = audiopath.split('/')[-1]
    return "[sound:" + name + "]"

def addaudio(audiopath):
    '''
    Takes the audiofile and copies it to your anki media folder, then adds the reference to the corresponding last added note
    '''

    filename = os.path.basename(audiopath)

    try:
        with open(audiopath, "rb") as f: # "rb" for read binary
            file_content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {audiopath}")
        raise(FileNotFoundError)
        #exit()
    except Exception as e:
        print(f"Error reading file: {e}")
        raise(Exception)
        #exit()

    base64_encoded_content = base64.b64encode(file_content).decode('utf-8')

    result_store = invoke("storeMediaFile",
        filename = filename,
        data = base64_encoded_content
    )
    print(result_store)
     
    note_id = int(newestcrd())
    anki_audio = formatforanki(audiopath)

    result = invoke("updateNoteFields", note={
        "id": note_id,
        "fields": {
            "Audio2": anki_audio,
        }
    })

def addaudio_id(audiopath, note_id):
    '''
    Takes the audiofile and copies it to your anki media folder, then adds the reference to the corresponding note by id
    '''

    filename = os.path.basename(audiopath)

    try:
        with open(audiopath, "rb") as f: # "rb" for read binary
            file_content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {audiopath}")
        raise(FileNotFoundError)
        #exit()
    except Exception as e:
        print(f"Error reading file: {e}")
        raise(Exception)
        #exit()

    base64_encoded_content = base64.b64encode(file_content).decode('utf-8')

    result_store = invoke("storeMediaFile",
        filename = filename,
        data = base64_encoded_content
    )
    
    print(result_store)
    anki_audio = formatforanki(audiopath)

    print(note_id)
    result_mod = invoke("updateNoteFields", note={
        "id": int(note_id),
        "fields": {
            "Audio2": anki_audio,
        }
    })
    print(note_id)
