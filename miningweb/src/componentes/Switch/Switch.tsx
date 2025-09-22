import './switch.css'

interface SwitchProps {
  isAudioEnabled: boolean | undefined;
  setIsAudioEnabled: React.Dispatch<React.SetStateAction<boolean>>
}

const AudioPlayerSwitch = ({isAudioEnabled, setIsAudioEnabled} : SwitchProps) => {

    const handleSwitchChange = () => {
        // 2. Cambia el estado cada vez que se hace clic
        setIsAudioEnabled(!isAudioEnabled);
    };

    return (
        <div className="switch-container">
            <input 
                type="checkbox" 
                id="miSwitch" 
                className="switch-checkbox" 
                checked={isAudioEnabled} 
                onChange={handleSwitchChange}/>
            <label htmlFor="miSwitch" className="switch-label">
                <span className="switch-inner"></span>
                <span className="switch-toggle"></span>
            </label>
            <span className="switch-text">Reproducir audio</span>
        </div>
    );
};
export default AudioPlayerSwitch;
