import { useState } from 'react'
import Modal from '../Modal/modal'
import { FlaskApiClient } from '../Api/apicalls'
import type { PostData, AnkiData } from '../Api/apicalls';

interface ButtonsProps {
  inputValue: string;
  selectedAudio : string;
  setAudioList : React.Dispatch<React.SetStateAction<string[]>>;
  selectedChapter : string;
}

const Buttons = ({inputValue, selectedAudio, setAudioList, selectedChapter} : ButtonsProps) => {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const handleOpenModal = () => {
        // Si no hay un audio seleccionado, avisa al usuario y no hagas nada
        if (!selectedAudio) {
            alert("Por favor, busca y selecciona un audio primero.");
            return;
        }

        setIsModalOpen(true);
    };

    const handleCloseModal = () => setIsModalOpen(false);
    const apiClient = new FlaskApiClient("http://127.0.0.1:5005");

    const handleSearch = async () => {
      const Data: PostData = {
        "key": inputValue,
        "chapt": selectedChapter
      };
      const result = await apiClient.post<string[]>('/api/getaudio/', Data);
      setAudioList(result || [])
    };

    const handleLastNote = async () => {
      const Data: AnkiData = {
        "audiofile": selectedAudio,
        "note_id": "last"
      };
      const result = await apiClient.post<string[]>('/api/anki/', Data);
      console.log(result)
    };

    return (
      <div>
        <div className="button-group">
            <button onClick={handleSearch} className="btn btn-primary">Buscar</button>
            <button onClick={handleLastNote} className="btn">Añadir a última carta</button>
            <button onClick={handleOpenModal} className="btn" id="open-modal-btn">Añadir a carta por Id</button>
        </div>
        <Modal
          handleCloseModal = {handleCloseModal}
          isModalOpen = {isModalOpen}
          apiClient = {apiClient}
          selectedAudio = {selectedAudio}
        />
      </div>
    );
};

export default Buttons;