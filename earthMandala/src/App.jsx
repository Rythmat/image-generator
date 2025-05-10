import "./App.css";
import { useEffect, useState } from "react";

function App() {
  const [imageSrc, setImageSrc] = useState(null);
  const [nextImage, setNextImage] = useState(null);
  
  useEffect(() => {
    const updateImage = () => {
      const timestamp = new Date().getTime();
      const url = `https://earth-mandalate.onrender.com/generate?${timestamp}`;
      const img = new Image();

      img.onload = () => {
        setImageSrc(url);
      };

      img.src = url;
      setNextImageUrl(url);
    };

    updateImage();
    const interval = setInterval(updateImage, 10000);
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
