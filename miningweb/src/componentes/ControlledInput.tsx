import { useEffect } from 'react'

interface InputProps {
  setInputValue: React.Dispatch<React.SetStateAction<string>>;
  inputValue : string;
}

const ControlledInput = ({setInputValue, inputValue} : InputProps) => {

    useEffect(() => {
            setInputValue("「」")
    }, []);

/*     useEffect(() => {
        const handlePaste = (event: ClipboardEvent) => {
            event.preventDefault();
            const clipboardText = event.clipboardData?.getData('text/plain');
            
            if (clipboardText) {
                // Actualiza directamente el estado del padre
                setInputValue(clipboardText);
                console.log("Texto capturado y actualizado: ", clipboardText);
            }
        };

        // Añade el event listener al documento. Esto se hace una sola vez.
        document.addEventListener('paste', handlePaste);
        
        // Función de limpieza: elimina el event listener cuando el componente se desmonta.
        return () => {
            document.removeEventListener('paste', handlePaste);
        };
    }, []); // La dependencia asegura que el listener se recrea si InputValue cambia */
    
    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setInputValue(event.target.value);
    };

    return (
        <div className="form-group">
              <label htmlFor="searchText" className="">Texto a buscar</label>
              <input
                type="text"
                id="searchText"
                value={inputValue}
                onChange={handleInputChange}
              />
        </div>
    );
};

export default ControlledInput;