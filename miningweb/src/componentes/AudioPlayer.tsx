import React, { useEffect } from 'react';
import { FlaskApiClient } from './Api/apicalls';

export interface AudioPlayerProps {
  audioFileName: string | null;
  playbackTrigger: number; // Nuevo prop para disparar la reproducción
}

// Instancia la clase una sola vez
const API_BASE_URL = "http://localhost:5005";
const apiClient = new FlaskApiClient(API_BASE_URL);

const AudioPlayer: React.FC<AudioPlayerProps> = ({ audioFileName, playbackTrigger }) => {
  useEffect(() => {
    let audioUrl: string | null = null;
    
    // Función asíncrona interna para manejar la reproducción
    const playAudio = async () => {
      if (audioFileName) {
        audioUrl = await apiClient.playAudioFile(audioFileName);
      }
    };
    
    playAudio();

    // Función de limpieza
    return () => {
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
    };
  }, [audioFileName, playbackTrigger]); // Escucha los cambios en audioFileName y en el disparador

  return null;
};

export default AudioPlayer;