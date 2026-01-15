import json
import urllib.request
import os
import base64

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    # AnkiConnect usa 127.0.0.1:8765 por defecto en Linux y Windows
    try:
        response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))
    except Exception as e:
        raise Exception(f"No se pudo conectar con Anki. ¿Está abierto? Error: {e}")

    if len(response) != 2:
        print("ex1")
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        print("ex2")
        raise Exception('response is missing required error field')
    if 'result' not in response:
        print("ex3")
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        print("ex4")
        raise Exception(response['error'])
    return response['result']

def newestcrd():
    # Buscamos notas añadidas hoy (added:1) o recientemente
    todaycards = invoke("findCards", query="added:1")
    if not todaycards:
        # Si no hay hoy, podrías ampliar el rango o manejar el error
        return None
    
    result = invoke("cardsModTime", cards=todaycards)
    newestcard = result[0]
    for card in result:
        if card["mod"] > newestcard["mod"]:
            newestcard = card
    
    # Obtenemos el noteId (ID de la nota), no el cardId
    # updateNoteFields requiere el ID de la NOTA.
    card_info = invoke("cardsInfo", cards=[newestcard["cardId"]])
    return card_info[0]["note"]

def addaudio_generic(audiopath, note_id=None):
    '''
    Versión unificada que funciona en Linux/Windows.
    Si note_id es None, busca la última nota.
    '''
    if not os.path.exists(audiopath):
        raise FileNotFoundError(f"No existe el audio en: {audiopath}")

    filename = os.path.basename(audiopath)

    # Lectura binaria para base64
    with open(audiopath, "rb") as f:
        base64_content = base64.b64encode(f.read()).decode('utf-8')

    # 1. Almacenar el archivo en Anki (AnkiConnect lo pone en la carpeta correcta)
    invoke("storeMediaFile", filename=filename, data=base64_content)
    
    # 2. Identificar la nota
    final_note_id = note_id if note_id else newestcrd()
    
    if not final_note_id:
        raise Exception("No se encontró una nota reciente para actualizar.")

    # 3. Actualizar el campo
    anki_audio_tag = f"[sound:{filename}]"

    return invoke("updateNoteFields", note={
        "id": int(final_note_id),
        "fields": {
            "Audio2": anki_audio_tag,
        }
    })