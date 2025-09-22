import { useState } from 'react'
import { FlaskApiClient } from '../Api/apicalls'
import type { AnkiData } from '../Api/apicalls'

interface ModalProps {
  handleCloseModal : () => void;
  isModalOpen: boolean;
  selectedAudio : string;
  apiClient : FlaskApiClient;
}

const Modal = ({handleCloseModal, isModalOpen, selectedAudio, apiClient} : ModalProps) => {
    const [cardId, setCardId] = useState('');

    const fetchData = async (Data : AnkiData) => {
        console.log(Data);
        const result = await apiClient.post('/api/anki/', Data);
        console.log(result);
        
        alert(`Se ha solicitado añadir audio a la carta con el ID: ${cardId}`);
    };

    // Función para reproducir/repetir el audio
    const handleAddById = () => {
        // Incrementa el estado para disparar la reproducción
        const Data: AnkiData = {
            "audiofile": selectedAudio,
            "note_id": cardId
        };
        fetchData(Data)
        handleCloseModal();
    };

    return (
        <div>
            {isModalOpen && (    
                <div id="id-modal" className="modal">
                    <div className="modal-content">
                        <span className="close-btn">&times;</span>
                        <h2>Añadir a carta por Id</h2>
                        <div className="form-group">
                            <label htmlFor="cardIdInput">ID de la carta</label>
                            <input
                            type="text"
                            id="cardIdInput"
                            placeholder="Escribe el ID aquí"
                            value={cardId}
                            onChange={(e) => setCardId(e.target.value)}
                            className="card-id-input"
                            />
                        </div>
                        <div className="modal-buttons">
                            <button onClick={handleCloseModal} className="btn btn-primary">
                            Cancelar
                            </button>
                            <button onClick={handleAddById} className="btn">
                            Aceptar
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Modal