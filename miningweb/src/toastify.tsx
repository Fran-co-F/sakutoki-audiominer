import Toastify from 'toastify-js'
import "toastify-js/src/toastify.css"

export function alertError(message : string) {
    Toastify({
        text: message,
        duration: 3000,
        gravity: "top", // `top` or `bottom`
        position: "left", // `left`, `center` or `right`
        style: {
            background: "linear-gradient(to right, #b00000ff, #090a3659)",
        },
    }).showToast();
}

export function alertSuccess(message : string) {
    Toastify({
        text: message,
        duration: 3000,
        gravity: "top", // `top` or `bottom`
        position: "left", // `left`, `center` or `right`
        style: {
            background: "linear-gradient(to right, #23b000ff, #090a3659)",
        },
    }).showToast();
}
