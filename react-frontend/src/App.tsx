import { useState, useEffect } from 'react'

function App() { 

  interface Data {
    members: string[];
  }
  
  const [data, setData] = useState<Data | null>(null);

  useEffect(() => {
    fetch('http://localhost:5000/members').then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, [])

  return (
    <div>
      {data === null ? (
        <p>Loading... Make sure server.py is running.</p>
      ) : (
        data.members.map((member, i) => (
          <p key={i}>{member}</p>
        ))
      )}
    </div>
  );
  

}

export default App