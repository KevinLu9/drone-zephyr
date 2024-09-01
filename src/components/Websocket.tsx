import React from "react";

interface websocketProps {
  batteryVoltage: number;
  setBatteryVoltage: React.Dispatch<React.SetStateAction<number>>;
  roll: number;
  setRoll: React.Dispatch<React.SetStateAction<number>>;
  pitch: number;
  setPitch: React.Dispatch<React.SetStateAction<number>>;
  yaw: number;
  setYaw: React.Dispatch<React.SetStateAction<number>>;
  isArmed: boolean;
  setIsArmed: React.Dispatch<React.SetStateAction<number>>;
  tiltX: number;
  setTiltX: React.Dispatch<React.SetStateAction<number>>;
  tiltY: number;
  setTiltY: React.Dispatch<React.SetStateAction<number>>;
  tiltZ: number;
  setTiltZ: React.Dispatch<React.SetStateAction<number>>;
}

const Websocket = React.memo(
  function Websocket({
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
  }: websocketProps) {
    // Create WebSocket connection.
    let count = 0;
    // const websocketURI = `ws://${location.hostname}:8001`;
    const websocketURI = `ws://192.168.1.129:8001`;
    const socket = new WebSocket(websocketURI);
    // Connection opened
    socket.addEventListener("open", () => {
      console.log(`[LOG] Successfully connected to:\n ${websocketURI}`);
      setInterval(() => {
        socket.send(`PERIODIC PACKET: ${count}`);
        count++;
      }, 4000);
    });

    socket.addEventListener("message", (event) => {
      const liveData = JSON.parse(event.data);
      // console.log({ liveData: JSON.parse(event.data) });

      if (batteryVoltage != liveData?.battery_voltage)
        setBatteryVoltage(liveData?.battery_voltage);
      if (roll != liveData?.roll) setRoll(liveData?.roll);
      if (pitch != liveData?.pitch) setPitch(liveData?.pitch);
      if (yaw != liveData?.yaw) setYaw(liveData?.yaw);
      if (isArmed != liveData?.is_armed) setIsArmed(liveData?.is_armed);
      if (tiltX != liveData?.tilt_x) setTiltX(liveData?.tilt_x);
      if (tiltY != liveData?.tilt_y) setTiltY(liveData?.tilt_y);
      if (tiltZ != liveData?.tilt_z) setTiltZ(liveData?.tilt_z);
    });
    return <></>;
  },
  () => true // Memo with arePropsEqual function true to prevent this component from rerendering
);

export default Websocket;
