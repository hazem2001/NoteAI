import { useState } from 'react'

function NoteEditor(currentNote) {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  const handleTitle = (event) => {
    setTitle(event.target.value);
  };

  const handleContent = (event) => {
    setContent(event.target.value);
  };

  return (
    <div className='h-full flex-1 font-sans'>
        <div className='h-full flex flex-col items-center mt-36'>
            <textarea className='rounded-2xl p-2 focus:outline-none text-5xl w-1/2 font-bold'
            type='text' 
            value={title}
            onChange={handleTitle} 
            placeholder='Title'></textarea>

            <textarea className='rounded-2xl p-2 focus:outline-none text-3xl w-1/2'
            type='text' 
            value={content}
            onChange={handleContent} 
            placeholder='Content...'></textarea>
        </div>
    </div>
  );
}

export default NoteEditor