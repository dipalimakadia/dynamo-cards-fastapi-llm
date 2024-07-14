import { useState } from "react";
import axios from "axios";
import Flashcard from "./Flashcard.jsx";
import "./Flashcard.css";

function App() {
  const [youtubeLink, setYoutubeLink] = useState("");
  const [keyConcepts, setKeyConcepts] = useState([]);

  const handleLinkChange = (event) => {
    setYoutubeLink(event.target.value);
  };
  const sendLink = async () => {
    try {
      const response = await axios.post("http://localhost:8000/analyze_video", {
        youtube_link: youtubeLink,
      });

      const data = response.data;
      if (data.key_concepts && Array.isArray(data.key_concepts)) {
        const transformedConcepts = data.key_concepts.map((concept) => {
          const term = Object.keys(concept)[0];
          const definition = concept[term];
          return { term, definition };
        });
        setKeyConcepts(transformedConcepts);
      } else {
        console.error("Data doesn't contain key concepts: ", data);
      }
    } catch (error) {
      console.log(error);
      setKeyConcepts([]);
    }
  };

  const discardFlashcard = (index) => {
    setKeyConcepts((currentConcepts) =>
      currentConcepts.filter((_, i) => i !== index)
    );
  };

  return (
    <>
      <div className="App">
        <h1>You tube Link</h1>
        <div className="inputContainer">
          <input
            type="text"
            placeholder="Paste Youtube Link"
            value={youtubeLink}
            onChange={handleLinkChange}
            className="inputField"
          />
          <button onClick={sendLink}>Generate Flashcard</button>
        </div>
        <div className="flashcardsContainer">
          {keyConcepts.map((concept, index) => (
            <Flashcard
              key={index}
              term={concept.term}
              definition={concept.definition}
              onDiscard={() => discardFlashcard(index)}
            />
            //   <h2>Response Data: </h2>
            //   <p>{JSON.stringify(responseData, null, 2)}</p>
            // </div>
          ))}
        </div>
      </div>
    </>
  );
}

export default App;
