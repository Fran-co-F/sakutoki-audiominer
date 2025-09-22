import { useState } from 'react'
import Buttons from './componentes/Buttons/index'
import ComboBox from './componentes/ComboBox/index'
import ControlledInput from './componentes/ControlledInput'
import './App.css'

function App() {
  const [inputValue, setInputValue] = useState('');
  const [selectedAudio, setSelectedAudio] = useState<string>('');
  const [selectedChapter, setSelectedChapter] = useState('01');
  const [audioList, setAudioList] = useState<string[]>([]);;
  //const [isAudioEnabled, setIsAudioEnabled] = useState<boolean>(true);;

  return (
    <>
    <div className="container">
        <header>
            <h1>Anki Audio Inserter</h1>
        </header>
        <main id="main">
            <ControlledInput
              setInputValue={setInputValue}
              inputValue={inputValue}
            />
            <ComboBox
              selectedChapter = {selectedChapter}
              setSelectedChapter = {setSelectedChapter}
              audioList = {audioList}
              setSelectedAudio = {setSelectedAudio}
              selectedAudio = {selectedAudio}
            />
            {/*
            <AudioPlayerSwitch
              isAudioEnabled={isAudioEnabled}
              setIsAudioEnabled={setIsAudioEnabled}
            />
            */}
            <Buttons
              inputValue = {inputValue}
              selectedAudio = {selectedAudio}
              setAudioList = {setAudioList}
              selectedChapter = {selectedChapter}
            />
        </main>
    </div>
    </>
  )
}

export default App
