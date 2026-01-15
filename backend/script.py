import re
import os
import flet as ft
from just_playback import Playback
from os import listdir
from os.path import join

playback = Playback()

import ankiconect 

def parsefile(FILE_PATH):
    with open(FILE_PATH, "r", encoding="utf8") as f:
        lines = f.read()
    y = re.findall("text = {.*?line", lines, re.S)
    result_list = []
    for block in y:
        z = re.findall("\".+?\"", block, re.S)
        z = [item[1:-1] for item in z]
        result_list.append(z)
    return result_list

def processline(raw_list):
    cleanlist = []
    for sublist in raw_list:
        cleansublist = []
        cleansublist.append(sublist[1] if sublist[0] == "vo" else "NoVo")
        
        truestring = ""
        for i in range(len(sublist)):
            if sublist[i] in ["rt2", "ruby"]:
                truestring += sublist[i-1]
        cleansublist.append(truestring)
        cleanlist.append(cleansublist)
    return cleanlist

def makedicc(processed_list, dicc, chapt):
    for sublist in processed_list:
        key = (sublist[1], chapt)
        if key not in dicc:
            dicc[key] = [sublist[0]]
        else:
            dicc[key] += [sublist[0]]

def getfiles():
    mypath = "assets/script/"
    dicc = {}
    if not os.path.exists(mypath):
        return dicc
    onlyfiles = [f for f in listdir(mypath)]
    for filename in onlyfiles:
        chapt = filename[0:2]
        raw = parsefile(join(mypath, filename))
        processed = processline(raw)
        makedicc(processed, dicc, chapt)
    return dicc

def findaudiopath(name):
    namestruc = name.split('_')
    try:
        return f"assets/sound/vo/{namestruc[1]}/{name}.ogg"
    except IndexError:
        return ""

def main(page: ft.Page):
  
    page.title = "Anki Audio Inserter"
    page.window.width = 350 
    page.window.height = 100
    page.bgcolor = "#232937" 
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    lines_dict = getfiles()

    # Componentes de UI
    txt_input = ft.TextField(value="「」" ,label="Texto a buscar", expand=True)
    chapt_dropdown = ft.Dropdown(
        width=100,
        options=[ft.dropdown.Option(str(i).zfill(2)) for i in range(1, 6)] + [ft.dropdown.Option("ge")],
        value="05"
    )
    audio_dropdown = ft.Dropdown(label="Audios encontrados", expand=True)
    note_id_input = ft.TextField(label="Note ID", width=150, visible=False)

    id_input_dialog = ft.TextField(
        label="Escribe el ID de la nota", 
        autofocus=True,
        on_submit=lambda e: confirm_id_action(e) # Permitir 'Enter' para confirmar
    )

    def show_msg(text, color=ft.Colors.BLUE_400):
        page.show_dialog(ft.SnackBar(ft.Text(text), bgcolor=color))

    def search_clicked(e):
        key = (txt_input.value, chapt_dropdown.value)
        results = lines_dict.get(key, [])
        results = [r for r in results if r != "NoVo"]
        audio_dropdown.options = [ft.dropdown.Option(a) for a in results]
        if results:
            audio_dropdown.value = results[0]
            play_audio(e)
        else:
            show_msg("No se encontraron audios", ft.Colors.RED_400)
            playback = Playback()
            audio_dropdown.value = ""
        page.update()
        

    def play_audio(e):
        if audio_dropdown.value:
            path = findaudiopath(audio_dropdown.value)
            if os.path.exists(path):
                playback.load_file(path)
                playback.play()
            else:
                show_msg("Archivo de audio no encontrado en disco", ft.colors.RED_400)

    def add_to_anki(e, note_id):
        print(audio_dropdown.value)
        if not audio_dropdown.value:
            show_msg("Selecciona un audio")
            return
        path = findaudiopath(audio_dropdown.value)
        try:
            if note_id == "":
                ankiconect.addaudio_generic(path)
                show_msg("Añadido correctamente", ft.Colors.GREEN_700)
            else:
                print(f"entro a la funcion con {note_id} y {path}")
                ankiconect.addaudio_generic(path, note_id)
                show_msg(f"Añadido correctamente a note: {note_id}", ft.Colors.GREEN_700)
        except Exception as ex:
            show_msg(f"Error: {str(ex)}", ft.Colors.RED_400)

    def close_dlg(e):
        id_input_dialog.value=""
        page.pop_dialog()

    def confirm_id_action(e):
        note_id = id_input_dialog.value
        
        if note_id:
            # Llamamos a tu lógica de Anki pasándole el ID del popup
            page.pop_dialog()
            add_to_anki(None, note_id) 
            #id_input_dialog.value = "" # Limpiamos para la próxima vez
        else:
            show_msg("Por favor, ingresa un ID válido", ft.Colors.ORANGE_400)
        id_input_dialog.value=""

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar ID de Nota"),
        content=id_input_dialog,
        actions=[
            ft.TextButton("Cancelar", on_click=close_dlg),
            ft.TextButton("Confirmar", on_click=confirm_id_action),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def show_popup():
        if not audio_dropdown.value:
            show_msg("Selecciona un audio")
            return
        page.show_dialog(dlg_modal)

    # Layout
    page.add(
        ft.Container(
            padding=30,
            bgcolor="#2d3748",
            border_radius=10,
            content=ft.Column([
                ft.Text("Anki Audio Inserter", size=20, weight="bold"),
                txt_input,
                ft.Row([
                    chapt_dropdown, 
                    audio_dropdown, 
                    ft.IconButton(ft.Icons.REFRESH, on_click=playback.play)
                ]),
                ft.Row([
                    ft.FilledButton(
                        "Buscar", 
                        on_click=search_clicked, 
                        style=ft.ButtonStyle(bgcolor="#5a82a6", shape=ft.RoundedRectangleBorder(radius=5))
                    ),
                    ft.FilledButton(
                        "Añadir Última", 
                        on_click=lambda e: add_to_anki(e, ""), 
                        style=ft.ButtonStyle(bgcolor="#5a82a6", shape=ft.RoundedRectangleBorder(radius=5))
                    ),
                    ft.FilledButton(
                        "Por ID", 
                        on_click=show_popup, # Abre el popup
                        style=ft.ButtonStyle(bgcolor="#5a82a6", shape=ft.RoundedRectangleBorder(radius=5))
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
    )

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")