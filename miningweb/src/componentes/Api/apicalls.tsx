import { alertSuccess, alertError } from '../../toastify';

export interface PostData {
  key: string;
  chapt: string;
}

export interface AnkiData {
  audiofile: string;
  note_id: string;
}

// Interfaz para el componente que usará la clase
export interface AudioPlayerProps {
  audioFileName: string | null; // El nombre del archivo a reproducir
}


export class FlaskApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  /**
   * Realiza una solicitud POST a un endpoint de la API y retorna una Promesa con los datos.
   * @param endpoint El camino del endpoint (ej. '/api/endpoint').
   * @param data Los datos a enviar en el cuerpo de la solicitud.
   * @returns Una Promesa que se resuelve con la lista de strings o null si hay un error.
   */
  public async post<T>(endpoint: string, data: PostData | AnkiData): Promise<T | null> {
    const url = `${this.baseUrl}${endpoint}`;
    try {

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorData = await response.json();
        switch (response.status) {
          case 400:
            //console.error('Error 400: Bad Request', errorData.message);
            throw new Error(`${errorData.error}`);
            // Handle specific 400 error logic
            break;
          case 404:
            //console.error('Error 404: Not Found', errorData.message);
            throw new Error(`${errorData.error}`);
            // Handle specific 404 error logic
            break;
          case 500:
            //console.error('Error 500: Internal Server Error', errorData.message);
            throw new Error(`${errorData.error}`);
            // Handle specific 500 error logic (e.g., display a generic error message)
            break;
          default:
            //console.error(`Error ${response.status}: An unexpected error occurred`, errorData.message);
            throw new Error(`${errorData.error}`);
            // Handle other error codes
        }
        //throw new Error(`Error de red: ${response.status}`);
        return null
      }
      alertSuccess("String found")
      const result = await response.json() as T;
      return result;

    } catch (error) {
      alertError(error as string)
      console.error(error);
      return null;
    }
  }

  /**
   * Obtiene un archivo de audio por su nombre y lo reproduce.
   * @param audiofileName El nombre del archivo de audio (ej. '01_00_00').
   * @returns La URL temporal del Blob para que pueda ser revocada.
   */
  public async playAudioFile(audiofileName: string): Promise<string | null> {
    const url = `${this.baseUrl}/api/playaudio/${audiofileName}`;
    
    try {
      // Como el endpoint usa un POST pero los datos van en la URL,
      // el body puede ser un objeto vacío.
      const response = await fetch(url, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }
      
      const audioBlob = await response.blob();
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.play();

      return audioUrl;

    } catch (error) {
      alertError(`No se pudo reproducir el archivo de audio: ${error}`)
      console.error("No se pudo reproducir el archivo de audio:", error);
      return null;
    }
  }
}
