import React from "react";
export default function Throttle() {
  const [throttle, setThrottle] = React.useState(0);
  return (
    <>
      <div className="w-full flex gap-2">
        <input
          type="range"
          min={0}
          max="100"
          value={throttle}
          className="range"
          onChange={(e) => setThrottle(Number(e.target.value))}
        />
        <p className="font-bold">{throttle}%</p>
      </div>
    </>
  );
}
