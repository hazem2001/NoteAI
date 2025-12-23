import { useState, useEffect } from 'react'
import api from './services/api'

function SlideBar(currentNote) {
  const [notes, setNotes] = useState([]);
  const [search, setSearch] = useState("");
  useEffect( () => {

    const temp = async () => { 
        try {
            const res = await api.get('/notes');
            setNotes(res.data);
        } catch(error) {
            console.error("Api error", error);
        }
    };

    temp();
  }, []);

  const handleSearch = (event) => {
    setSearch(event.target.value);
  };

  return (
    <div className="h-full hidden md:block md:w-64 bg-gray-100 border-r border-gray-200">
        <input className='rounded-2xl m-2 p-2 focus:outline-none'
        type='text' 
        value={search}
        onChange={handleSearch} 
        placeholder='Search ...'></input>

        { notes.map(note => (
            <div key={note.id} className={`hover:bg-gray-200 
            rounded-lg mx-2 p-2 text-[16px] ${ currentNote.id == note.id && 'bg-gray-200'}`}>  
                {note.title} 
            </div>
        ) )}
    </div>
  );
}

export default SlideBar