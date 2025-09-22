import re
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin
from os import listdir
from os.path import isfile, join
from ankiconect import addaudio, addaudio_id

app = Flask(__name__)
CORS(app)
global linesdict

def parsefile(FILE):
    '''
    Parses the script file, first by blocks and then takes the text between quotation marks,
    returns an ordered list
    '''

    i = 0
    lines = FILE.read()
    y = re.findall("text = {.*?line", lines, re.S)
    list = []
    for block in y:
        z = re.findall("\".+?\"", block, re.S)
        for i in range(len(z)):
            z[i] =  z[i][1:-1]
        list.append(z)
    return list
            
def processline(list):
    '''
    Takes a list from parsefile then, takes the information necesary, 
    this being the dialog line and the correspondign audio
    If theres is no audio it stores "NoVo"
    '''

    cleanlist = []
    for sublist in list:
        cleansublist = []
        if sublist[0] == "vo":
            cleansublist.append(sublist[1])
        else:
            cleansublist.append("NoVo")

        truestring = ""
        for i in range(len(sublist)):
            if sublist[i] == "rt2" or sublist[i] == "ruby":
                truestring = truestring + sublist[i-1]
                ##print(truestring)
                ##truestring = truestring[1:-1]
        cleansublist.append(truestring)
        cleanlist.append(cleansublist)
    return cleanlist
                
def makedicc(list, dicc, chapt):
    '''
    Takes a list from processline then stores the data in the diccionary, 
    with the dialog being the key and a list of audionames the value
    '''

    for sublist in list:
        if sublist[1] not in dicc:
            dicc[(sublist[1], chapt)] = [sublist[0]]
        else:
            dicc[(sublist[1], chapt)] += [sublist[0]]

def getfiles():

    mypath = "script/"
    dicc = {}
    onlyfiles = [f for f in listdir(mypath)]
    ##onlyfiles = listdir(mypath)
    for filename in onlyfiles:
        chapt = filename[0:2]
        list = processline(parsefile(open(mypath + filename, "r", encoding="utf8")))
        makedicc(list, dicc, chapt)
    return dicc

""" @app.route('/api/getaudio/')
def getaudio(key, chapt):
    global linesdict
    print(f"dict key:{key} \n dict value {linesdict[(key, chapt)]}")
    return linesdict[(key, chapt)] """

@app.route('/api/getaudio/', methods=['POST'])
@cross_origin()
def getaudio():
    global linesdict
    # Obtener los datos del JSON enviado en el cuerpo de la solicitud
    try:
        data = request.get_json()
        if not data:
            return {"error": "No JSON data received"}, 400
        
        key = data.get('key')
        chapt = data.get('chapt')

        if not key or not chapt:
            return {"error": "Missing 'key' or 'chapt' in JSON data"}, 401

        print(f"dict key:{key} \n dict value {linesdict.get((key, chapt))}")
        
        # Usamos .get() para evitar un error si la clave no existe
        result = linesdict.get((key, chapt))
        if result is None:
            print(linesdict)
            return {"error": "Audio not found for the given key and chapter"}, 404
        
        return result
    
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/api/playaudio/<audiofile>', methods=['POST'])
@cross_origin()
def playaudiofile(audiofile):
    '''
    given a selected audioname, and a boolean to decide if it will be reproduced, 
    returns the filepath of the selected audio
    '''
    try:
        namestruc = audiofile.split('_')
        try:
            audiopath = "sound/vo/" + namestruc[1] + "/" + audiofile + ".ogg"
            return send_file(audiopath, mimetype="audio/ogg")
        except IndexError:
            return ""
    
    except IndexError:
        return {"error": "Invalid audio file format"}, 400
    except FileNotFoundError:
        return {"error": "Audio file not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500

def findaudiopath(name):
    '''
    given a selected audioname, and a boolean to decide if it will be reproduced, 
    returns the filepath of the selected audio
    '''

    namestruc = name.split('_')
    try:
        audiopath = "sound/vo/" + namestruc[1] + "/" + name + ".ogg"
        return audiopath
    except IndexError:
        return ""

@app.route('/test', methods=['GET'])
def testconn():
    return "Hello World!"

@app.route('/api/ankilast/<audiofile>', methods=['POST'])
@cross_origin()
def addaudioF(audiofile):
    try:
        addaudio(audiofile)
    except FileNotFoundError:
        return {"error": "Audio file not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/api/anki/', methods=['POST'])
@cross_origin()
def addaudio_idF():
    try:
        data = request.get_json()
        if not data:
            return {"error": "No JSON data received"}, 400
        
        audiofile = data.get('audiofile')
        note_id = data.get('note_id')

        if not audiofile or not note_id:
            return {"error": "Missing 'audiofile' or 'note_id' in JSON data"}, 400

        if note_id == "last":
            addaudio(findaudiopath(audiofile))
            return {"success": "audio ingresado en ultima note creada"}, 200

        addaudio_id(findaudiopath(audiofile), note_id)
        return {"success": f"audio ingresado en note: {note_id}"}, 200

    except FileNotFoundError:
        return {"error": "Audio file not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == '__main__':
    global linesdict
    linesdict = getfiles()
    app.run(debug=True, port=5005)

##getfiles("「なぜ！\u3000なぜ渡さないの！\u3000あれは私との友情の証でしょ！」", "")
