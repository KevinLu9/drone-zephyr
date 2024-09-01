import React from "react";
import { Joystick } from "react-joystick-component";
import { JoystickShape } from "react-joystick-component";

interface IJoystickProps {
  size?: number;
  stickSize?: number;
  baseColor?: string;
  stickColor?: string;
  disabled?: boolean;
  throttle?: number;
  sticky?: boolean;
  stickImage?: string;
  baseImage?: string;
  followCursor?: boolean;
  move?: (event: IJoystickUpdateEvent) => void;
  stop?: (event: IJoystickUpdateEvent) => void;
  start?: (event: IJoystickUpdateEvent) => void;
  baseShape?: JoystickShape;
  stickShape?: JoystickShape;
  controlPlaneShape?: JoystickShape;
  minDistance?: number;
  pos: { x: number; y: number };
}

type JoystickDirection = "FORWARD" | "RIGHT" | "LEFT" | "BACKWARD";

export interface IJoystickUpdateEvent {
  type: "move" | "stop" | "start";
  x: number | null;
  y: number | null;
  direction: JoystickDirection | null;
  distance: number; // Percentile 0-100% of joystick
}

export default function DroneJoystick({
  joystickType,
}: {
  joystickType: string;
}) {
  const [joystickPos, setJoystickPos] = React.useState({ x: 0, y: 0 });

  const handleStart = (e) => {
    navigator.vibrate(200);
  };
  const handleMove = (e) => {
    console.log("MOVE", e);
    setJoystickPos({ x: e.x, y: e.y });
    // navigator.vibrate(200);
  };
  const handleStop = (e) => {
    console.log("STOP", e);
    setJoystickPos({ x: 0, y: 0 });
    navigator.vibrate([200, 100]);
  };
  return (
    <>
      <Joystick
        size={100}
        controlPlaneShape={
          joystickType == "turn" ? JoystickShape.AxisX : JoystickShape.Circle
        }
        start={handleStart}
        move={handleMove}
        stop={handleStop}
        pos={joystickPos}
        // sticky={true}
        // baseColor="red"
        // stickColor="blue"
        // disabled={true}
      ></Joystick>
    </>
  );
}
