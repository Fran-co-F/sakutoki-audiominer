import { useState, useEffect } from 'react'
import AudioPlayer from '../AudioPlayer'

interface ComboProps {
  selectedChapter: string;
  setSelectedChapter: (value : string) => void
  selectedAudio : string;
  setSelectedAudio : (value : string) => void
  audioList : string[];
}

const ComboBox = ({selectedChapter, setSelectedChapter, audioList, selectedAudio, setSelectedAudio} : ComboProps) => {

    const chapters = ['01', '02', '03', '04', '05'];
    const [playbackTrigger, setPlaybackTrigger] = useState(0);

    const handleChapterChange = (event : React.ChangeEvent<HTMLSelectElement>) => {
        setSelectedChapter(event.target.value);
    };

    const handleAudioChange = (event : React.ChangeEvent<HTMLSelectElement>) => {
        setSelectedAudio(event.target.value);
    };

    // Función para reproducir/repetir el audio
    const handlePlayAudio = () => {
        // Si no hay un archivo de audio seleccionado, no hagas nada
        if (!selectedAudio) {
        alert("Selecciona un archivo de audio primero.");
        return;
        }
        // Incrementa el estado para disparar la reproducción
        setPlaybackTrigger(prev => prev + 1);
    };

    useEffect(() => {
        console.log(audioList[0] || "")
        setSelectedAudio(audioList[0] || "")
        console.log(selectedAudio)
    }, [audioList])

    return (
        <div className="form-group-inline">
            <select
              value={selectedChapter}
              onChange={handleChapterChange}
            >
              {chapters.map((chapter) => ( 
                <option key={chapter} value={chapter}>
                  {chapter}
                </option>
              ))}
            </select>

            <select
              value={selectedAudio}
              onChange={handleAudioChange}
            >
              {audioList.map((audio) => ( 
                <option key={audio} value={audio}>
                  {audio}
                </option>
              ))}
            </select>

            <button className='button-group btn' onClick={handlePlayAudio}>
            <i className="fa-solid fa-rotate-right"></i>
            </button>

            <AudioPlayer 
            audioFileName={selectedAudio}
            playbackTrigger={playbackTrigger} />
        </div>
    );
};

export default ComboBox;