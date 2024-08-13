// import React from "react";
import "./App.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import ErrorBoundary from "./components/ErrorBoundary.tsx";
import Dashboard from "./pages/Dashboard/Dashboard.tsx";
import Websocket from "./components/Websocket.tsx";

function App() {
  // const [liveData, setLiveData] = React.useState({});

  const router = createBrowserRouter([
    {
      path: "/",
      element: <Dashboard />,
      errorElement: <ErrorBoundary />,
    },
  ]);

  return (
    <>
      <Websocket />
      {/* <Websocket liveData={liveData} setLiveData={setLiveData} /> */}
      <RouterProvider router={router} />
    </>
  );
}

export default App;
