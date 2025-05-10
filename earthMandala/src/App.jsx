import "./App.css";
import { useEffect, useState } from "react";

function App() {
  const [imageSrc, setImageSrc] = useState(null);
  
  useEffect(() => {
    const updateImage = () => {
      const timestamp = new Date().getTime();
      setImageSrc(`http://localhost:5000/generate?${timestamp}`)
    };

    updateImage();
    const interval = setInterval(updateImage, 10000);
    return () => clearInterval(interval);
  }, []);


  return (
    <>
      <div style={{ height: "100vh", display: "flex", justifyContent: "center", alignItems: "center" }}>
      {imageSrc && <img src={imageSrc} alt="Earth Mandala"/>}
    </div>
    </>
  )
}

export default App
