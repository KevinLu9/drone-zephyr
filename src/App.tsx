import React from "react";
import "./App.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import ErrorBoundary from "./components/ErrorBoundary.tsx";
import Dashboard from "./pages/Dashboard/Dashboard.tsx";
import Websocket from "./components/Websocket.tsx";

function App() {
  const [batteryVoltage, setBatteryVoltage] = React.useState(0);
  const [roll, setRoll] = React.useState(0);
  const [pitch, setPitch] = React.useState(0);
  const [yaw, setYaw] = React.useState(0);
  const [isArmed, setIsArmed] = React.useState(false);
  const [tiltX, setTiltX] = React.useState(0);
  const [tiltY, setTiltY] = React.useState(0);
  const [tiltZ, setTiltZ] = React.useState(0);

  const router = createBrowserRouter([
    {
      path: "/",
      element: (
        <Dashboard
          {...{
            batteryVoltage,
            roll,
            pitch,
            yaw,
            isArmed,
            tiltX,
            tiltY,
            tiltZ,
          }}
        />
      ),
      errorElement: <ErrorBoundary />,
    },
  ]);

  return (
    <>
      <Websocket
        {...{
          batteryVoltage,
          setBatteryVoltage,
          roll,
          setRoll,
          pitch,
          setPitch,
          yaw,
          setYaw,
          isArmed,
          setIsArmed,
          tiltX,
          setTiltX,
          tiltY,
          setTiltY,
          tiltZ,
          setTiltZ,
        }}
      />
      <RouterProvider router={router} />
    </>
  );
}

export default App;
