import "./App.css";
import { useEffect, useState, useRef, useCallback } from "react";
import pauseIcon from "./assets/pause.png"
import playIcon from "./assets/play.png"

function randomHex() {
  const r = Math.floor(Math.random() * 256).toString(16).padStart(2, "0");
  const g = Math.floor(Math.random() * 256).toString(16).padStart(2, "0");
  const b = Math.floor(Math.random() * 256).toString(16).padStart(2, "0");
  return `#${r}${g}${b}`;
}

function App() {
  const [imageSrc, setImageSrc] = useState(null);
  const [type, setType] = useState("sixteens");
  const [paused, setPaused] = useState(false);
  const [colorMode, setColorMode] = useState("random");
  const [colors, setColors] = useState([randomHex(), randomHex(), randomHex()]);
  const [colorDropdownOpen, setColorDropdownOpen] = useState(false);
  const intervalRef = useRef(null);
  const colorRefs = [useRef(null), useRef(null), useRef(null)];

  const fetchImage = useCallback((url) => {
    const img = new Image();
    img.onload = () => {
      setImageSrc(url);
    };
    img.onerror = () => {
      console.error("Image failed to load:", url);
    };
    img.src = url;
  }, []);

  // Random mode: generate on-demand, poll for new images
  useEffect(() => {
    if (colorMode !== "random" || paused) return;

    const updateImage = () => {
      const timestamp = new Date().getTime();
      const url = `https://earth-mandalate.onrender.com/generate?type=${type}&t=${timestamp}`;
      fetchImage(url);
    };

    updateImage();
    intervalRef.current = setInterval(updateImage, 5000);
    return () => clearInterval(intervalRef.current);
  }, [type, paused, colorMode, fetchImage]);

  // Custom mode: poll with fixed colors
  useEffect(() => {
    if (colorMode !== "custom" || paused) return;

    const colorParam = colors.map(c => c.replace("#", "")).join(",");
    const updateImage = () => {
      const timestamp = new Date().getTime();
      const url = `https://earth-mandalate.onrender.com/generate?type=${type}&colors=${colorParam}&t=${timestamp}`;
      fetchImage(url);
    };

    updateImage();
    intervalRef.current = setInterval(updateImage, 5000);
    return () => clearInterval(intervalRef.current);
  }, [type, colors, colorMode, paused, fetchImage]);

  const togglePause = () => {
    setPaused((prev) => !prev);
  };

  const handleColorChange = (index, value) => {
    setColors(prev => {
      const next = [...prev];
      next[index] = value;
      return next;
    });
  };

  return (
    <>
      <div className="container">
        <div className="side">
          <div className="controls">
            <select onChange={(e) => setType(e.target.value)} value={type}>
              <option value="eights">Three Quadrisections</option>
              <option value="sixteens">Four Quadrisections</option>
              <option value="thirtytwos">Five Quadrisections</option>
            </select>

            {colorMode === "random" ? (
              <div className="color-selector">
                <div
                  className="color-square color-square-random"
                  onClick={() => setColorDropdownOpen(prev => !prev)}
                >
                  Random
                </div>
                {colorDropdownOpen && (
                  <div className="color-dropdown">
                    <div
                      className="color-dropdown-item"
                      onClick={() => {
                        setColorMode("custom");
                        setColorDropdownOpen(false);
                      }}
                    >
                      Choose Colors
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="color-selector">
                <div
                  className="color-square color-square-back"
                  onClick={() => setColorMode("random")}
                >
                  Random
                </div>
                {colors.map((color, i) => (
                  <div
                    key={i}
                    className="color-square color-square-swatch"
                    style={{ backgroundColor: color }}
                    onClick={() => colorRefs[i].current?.click()}
                  >
                    <input
                      ref={colorRefs[i]}
                      type="color"
                      value={color}
                      onChange={(e) => handleColorChange(i, e.target.value)}
                      className="color-input-hidden"
                    />
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="center">
          {imageSrc ? (
            <img src={imageSrc} alt="Earth Mandala" />
          ) : (
            <p>Loading...</p>
          )}
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
