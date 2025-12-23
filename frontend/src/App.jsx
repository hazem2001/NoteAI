import { useState } from 'react'
import SlideBar from './SlideBar'
import NoteEditor from './NoteEditor'

function App() {
  const [currentNote, setCount] = useState(null)

  return (
    <div className="h-full flex">
        <SlideBar currentNote={currentNote}/>
        <NoteEditor currentNote={currentNote}/>
    </div>
  )
}

export default App
