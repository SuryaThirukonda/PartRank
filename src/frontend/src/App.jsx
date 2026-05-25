
import "./App.css";
import { useEffect, useState } from "react";

const APP_URL = "http://localhost:8000/gpus/"

function App() {
  const [gpus, setGpus] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData(){
      try{
        const response = await fetch(APP_URL);

        if (!response.ok){
          throw new Error (response.statusText);
        }
        const data = await response.json();

        setGpus(data);

      }
      catch (error){
        console.error("Error fetching data: ", error);
        setError(error.message);
      }

      finally{
        setLoading(false);
      }

    }
    fetchData();

  }, []);
  
  function renderContent(){
    if (loading){
      return <p>Loading...</p>;
    }

    if (error) {
      return <p className="error">Error: {error}</p>;
    }

    if (gpus.length === 0){
      return <p>No GPU data available.</p>;
    }

    return (
      <div className="card-list">
        {gpus.map((gpu) => (
          <div className="card" key={gpu.id}>
            <h2>{gpu.name}</h2>
            <p>Score: {gpu.score}</p>
          </div>
        ))}
      </div>
    );
  }


  return (
    <main className="Page">
      <h1>PartRank</h1>
      <p>This page displays GPU info.</p>
      {renderContent()}
    </main>
  )
}

export default App;