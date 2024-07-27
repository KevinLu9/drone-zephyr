import { useState } from "react";
import "./App.css";

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <button
        className="btn btn-secondary"
        onClick={() => setCount((val) => val + 1)}
      >
        TEST
      </button>
      <h1 className="text-3xl font-bold underline text-red-500">
        Count: {count}
      </h1>
    </>
  );
}

export default App;
