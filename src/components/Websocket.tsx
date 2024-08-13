// import React from "react";

// interface websocketProps {
//   liveData: object;
//   setLiveData: React.Dispatch<React.SetStateAction<object>>;
// }

// Create WebSocket connection.
let count = 0;
const websocketURI = `ws://${location.hostname}:8001`;
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
  console.log({ liveData: JSON.parse(event.data) });
  // setLiveData(JSON.parse(event.data));
});

export default function Websocket() {
  return <></>;
}
// export default function Websocket({ liveData, setLiveData }: websocketProps) {}
