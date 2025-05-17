import "./App.css";
import { useEffect, useState } from "react";

function App() {
  const [imageSrc, setImageSrc] = useState(null);
  const [type, setType] = useState("sixteens");
  const [paused, setPaused] = useState(false)
  const intervalRef = useRef(null);
  
  useEffect(() => {
    const updateImage = () => {
      const timestamp = new Date().getTime();
      const url = `https://earth-mandalate.onrender.com/generate?type=${type}&t=${timestamp}`;
      const img = new Image();

      img.onload = () => {
        setImageSrc(url);
      };

      img.onerror = () => {
        console.error("Image failed to load:", url);
        if (!paused) {
          setTimeout(updateImage, 2000);
        }
      };

      img.src = url;
    };
    if(!paused){
      updateImage();
      intervalRef.current = setInterval(updateImage, 5000);
    }
    
    return () => clearInterval(intervalRef.current);
  }, [type, paused]);


  const togglePause = () => {
    setPaused((prev) => !prev);
  };

  return (
    <>
      <div className="container">
        <select onChange={(e) => setType(e.target.value)} value={type}>
          <option value="eigths">Three Quadrisections</option>
          <option value="sixteens">Four Quadrisections</option>
          <option value="thirtytwos">Five Quadrisections</option>
        </select>

        <button onClick={togglePause}>
          {paused ? "Resume" : "Pause"}
        </button>

        {imageSrc && <img src={imageSrc} alt="Earth Mandala"/>}
      </div>
    </>
  )
}

export default App
