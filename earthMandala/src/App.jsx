import "./App.css";
import { useEffect, useState, useRef } from "react";
import pauseIcon from "./assets/pause.png"
import playIcon from "./assets/play.png"

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
          setTimeout(updateImage, 500);
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
        <div className="side">
          <select onChange={(e) => setType(e.target.value)} value={type}>
            <option value="eights">Three Quadrisections</option>
            <option value="sixteens">Four Quadrisections</option>
            <option value="thirtytwos">Five Quadrisections</option>
          </select>
        </div>

        <div className="center">
          {imageSrc ? <img src={imageSrc} alt="Earth Mandala" />: <p>Loading image...</p> }
        </div>

        <div className="side">
          <button onClick={togglePause} className="icon-button">
            <img src={paused ? playIcon : pauseIcon} alt={paused ? "Resume" : "Pause"} />
          </button> 
        </div>
      </div>
    </>
  )
}

export default App
