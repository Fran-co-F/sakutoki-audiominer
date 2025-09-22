// Obtener los elementos del DOM
const openModalBtn = document.getElementById('open-modal-btn');
const modal = document.getElementById('id-modal');
const closeBtn = document.querySelector('.close-btn');
const cancelBtn = document.getElementById('cancel-btn');
const confirmBtn = document.getElementById('confirm-btn');
const cardIdInput = document.getElementById('card-id-input');

console.log(versions.node())

// Función para abrir el modal
function openModal() {
    modal.style.display = 'flex';
}

// Función para cerrar el modal
function closeModal() {
    modal.style.display = 'none';
    cardIdInput.value = ''; // Limpia el input al cerrar
}

// Evento para abrir el modal al hacer clic en el botón "Añadir a carta por Id"
openModalBtn.addEventListener('click', openModal);

// Evento para cerrar el modal al hacer clic en la "x"
closeBtn.addEventListener('click', closeModal);

// Evento para cerrar el modal al hacer clic en el botón "Cancelar"
cancelBtn.addEventListener('click', closeModal);

// Evento para manejar el clic en "Aceptar"
confirmBtn.addEventListener('click', () => {
    const cardId = cardIdInput.value;
    if (cardId.trim() !== '') {
        alertInfo('Se ha solicitado añadir audio a la carta con el ID: ' + cardId)
        // alert('Se ha solicitado añadir audio a la carta con el ID: ' + cardId);
        // Aquí iría la lógica para enviar el ID a tu función real
        // Por ejemplo: insertAudioToCard(cardId);
        closeModal();
    } else {
        alertError('Por favor, ingresa un ID válido.')
    }
});

// Cerrar el modal si el usuario hace clic fuera de él
window.addEventListener('click', (event) => {
    if (event.target == modal) {
        closeModal();
    }
});

function alertError(message) {
    Toastify.toast({
        text: message,
        duration : 5000,
        close: false,
        gravity: "top",
        position: "right",
        style: {
            background: 'red',
            color:'white',
            textAlign:'center'
        }
    })
} 

function alertSuccess(message) {
    Toastify.toast({
        text: message,
        duration : 5000,
        gravity: "top",
        position: "right",
        close: false,
        style: {
            background: 'green',
            color:'white',
            textAlign:'center'
        }
    })
} 

function alertInfo(message) {
    Toastify.toast({
        text: message,
        duration : 10,
        gravity: "top",
        position: "right",
        close: false,
        style: {
            background: 'blue',
            color:'white',
            textAlign:'center'
        }
    })
} 