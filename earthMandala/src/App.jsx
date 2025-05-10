import "./App.css";
import { useEffect, useState } from "react";

function App() {
  const [imageSrc, setImageSrc] = useState(null);
  
  useEffect(() => {
    const updateImage = () => {
      const timestamp = new Date().getTime();
      const url = `https://earth-mandalate.onrender.com/generate?${timestamp}`;
      const img = new Image();

      img.onload = () => {
        setImageSrc(url);
      };

      img.onerror = () => {
        console.error("Image failed to load:", url);
      };

      img.src = url;
    };

    updateImage();
    const interval = setInterval(updateImage, 5000);
    return () => clearInterval(interval);
  }, []);


  return (
    <>
      <div className="container">
      {imageSrc && <img src={imageSrc} alt="Earth Mandala"/>}
    </div>
    </>
  )
}

export default App
