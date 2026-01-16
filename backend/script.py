import re
import os
import flet as ft
import json
from just_playback import Playback
from os import listdir
from os.path import join
from rapidfuzz import process, fuzz

playback = Playback()

import ankiconect 

# Ruta del archivo de configuración
SETTINGS_FILE = "settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {"script_path": "", "voice_path": ""}

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

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

def getfiles(path):
    mypath = path
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

def findaudiopath(name, basepath):
    namestruc = name.split('_')
    try:
        return os.path.join(basepath, "vo", namestruc[1], f"{name}.ogg")
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

    # --- OPCIONES ---
    settings = load_settings()

    lines_dict = {}

    def search_clicked(e):
        key = (txt_input.value, chapt_dropdown.value)
        results = lines_dict.get(key, [])
        results = [r for r in results if r != "NoVo"]
        audio_dropdown.options = [ft.dropdown.Option(a) for a in results]
        if results:
            audio_dropdown.value = results[0]
            #play_audio(e)
        else:
            show_msg("No se encontraron audios", ft.Colors.RED_400)
            playback = Playback()
            audio_dropdown.value = ""
        page.update()

# --- BÚSQUEDA DIFUSA ---

    def on_search_change(e):
        termino = txt_input.value.strip().lower()
        search_results_container.controls.clear()
        
        if len(termino) > 2: # tras 3 caracteres
            choices = [key[0] for key in lines_dict.keys()]
            
            # 10 mejores coincidencias
            matches = process.extract(
                termino, 
                choices, 
                scorer=fuzz.WRatio, 
                limit=10
            )

            for text_match, score, index in matches:
                if score > 50:
                    search_results_container.controls.append(
                        ft.ListTile(
                            title=ft.Text(text_match, size=14, max_lines=1),
                            subtitle=ft.Text(f"Similitud: {int(score)}%", size=11),
                            on_click=lambda _, t=text_match: select_suggestion(t)
                        )
                    )
        
        search_results_container.visible = len(search_results_container.controls) > 0
        page.update()

    def select_suggestion(selected_text):
        txt_input.value = selected_text
        search_results_container.visible = False
        search_results_container.controls.clear()
        # Se dispara la búsqueda de audios automáticamente
        search_clicked(None) 
        page.update()

    # --- UI COMPONENTS ACTUALIZADOS ---
    txt_input = ft.TextField(
        label="Escribe para buscar frase...", 
        expand=True,
        on_change=on_search_change,
        on_submit=search_clicked
    )

    search_results_container = ft.Column(
        visible=False,
        scroll=ft.ScrollMode.AUTO,
        height=200,
        spacing=0
    )

    def on_apply_savesettings():
        if voice_path_field:
            settings["voice_path"] = voice_path_field.value
            save_settings(settings)
        if script_path_field:
            settings["script_path"] = script_path_field.value
            save_settings(settings)
        page.pop_dialog()
        page.update()
        check_assets()

    async def handle_get_script_path(e: ft.Event[ft.Button]):
        script_path_field.value = await ft.FilePicker().get_directory_path()

    async def handle_get_voice_path(e: ft.Event[ft.Button]):
        voice_path_field.value = await ft.FilePicker().get_directory_path()

    script_path_field = ft.TextField(
        label="Carpeta de Scripts", 
        value=settings["script_path"], 
        read_only=True, 
        expand=True
    )
    
    voice_path_field = ft.TextField(
        label="Carpeta de Voces (sound/vo)", 
        value=settings["voice_path"], 
        read_only=True, 
        expand=True
    )

    settings_dialog = ft.AlertDialog(
        title=ft.Text("Configuración de Rutas"),
        content=ft.Column([
            ft.Text("Selecciona dónde están tus carpetas de trabajo:"),
            ft.Row([
                voice_path_field,
                ft.IconButton(ft.Icons.FOLDER_OPEN, on_click=handle_get_voice_path)
            ]),
            ft.Row([
                script_path_field,
                ft.IconButton(ft.Icons.FOLDER_OPEN, on_click=handle_get_script_path)
            ]),
        ], tight=True, spacing=20),
        actions=[
            ft.TextButton("Cerrar y Aplicar", on_click=on_apply_savesettings)
        ]
    )

    def launch(e):
        page.pop_dialog()
        page.show_dialog(settings_dialog)

    btn_settings = ft.IconButton(ft.Icons.SETTINGS, on_click=lambda e: launch(e))

    # --- --- ---

    def show_msg(text, color=ft.Colors.BLUE_400):
        page.show_dialog(ft.SnackBar(ft.Text(text), bgcolor=color))

    def play_audio(e):
        if audio_dropdown.value:
            path = findaudiopath(audio_dropdown.value, settings["voice_path"])
            if os.path.exists(path):
                playback.load_file(path)
                playback.play()
            else:
                show_msg("Archivo de audio no encontrado en disco", ft.Colors.RED_400)

    def add_to_anki(e, note_id):
        if not audio_dropdown.value:
            show_msg("Selecciona un audio")
            return
        path = findaudiopath(audio_dropdown.value, settings["voice_path"])
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


    error_dialog = ft.AlertDialog(
        title=ft.Text("¡Advertencia!"),
        content=ft.Text("Debe colocar las carpetas 'script' y 'sound' ripeadas del juego en el root de la aplicacion"),
        actions=[btn_settings],
    )

    def check_assets():
        scripts_ok = settings["script_path"] and os.path.exists(settings["script_path"])
        
        voices_path = settings["voice_path"]
        voices_ok = voices_path and os.path.exists(voices_path)
        
        # Comprobar específicamente si existe la carpeta "vo" dentro de voces
        if voices_ok:
            vo_folder = os.path.join(voices_path, "vo")
            if not os.path.isdir(vo_folder):
                voices_ok = False
                show_msg("La carpeta de voces debe contener una subcarpeta llamada 'vo'.", ft.Colors.RED_400)
        else:
            show_msg("La ruta de voces no existe", ft.Colors.RED_400)

        if not scripts_ok or not voices_ok:
            page.show_dialog(error_dialog)
        else:
            nuevos_datos = getfiles(settings["script_path"])
            lines_dict.clear() 
            lines_dict.update(nuevos_datos)

    def show_popup():
        if not audio_dropdown.value:
            show_msg("Selecciona un audio")
            return
        page.show_dialog(dlg_modal)

    check_assets()

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

    # Layout
    page.add(
        ft.Container(
            padding=20,
            bgcolor="#2d3748",
            border_radius=10,
            content=ft.Column([
                ft.Row([
                    ft.Text("Anki Audio Miner", size=20, weight="bold"),
                    ft.IconButton(ft.Icons.SETTINGS, on_click=lambda e: page.show_dialog(settings_dialog))
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                
                ft.Column([
                    txt_input,
                    ft.Container(
                        content=search_results_container,
                        bgcolor="#1a202c",
                        border_radius=5,
                        padding=5 if search_results_container.visible else 0
                    )
                ], spacing=0),

                ft.Row([
                    ft.Text("Cap:", size=12),
                    chapt_dropdown, 
                    audio_dropdown, 
                    ft.IconButton(ft.Icons.PLAY_ARROW, on_click=play_audio)
                ]),
                
                ft.Row([
                    ft.FilledButton(
                        "Buscar", on_click=search_clicked, expand=True),
                    ft.FilledButton("Añadir Última", on_click=lambda e: add_to_anki(e, ""), expand=True),
                    ft.FilledButton("Por ID", on_click=show_popup, expand=True),
                ], alignment=ft.MainAxisAlignment.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
        )
    )

if __name__ == "__main__":
    ft.run(main)