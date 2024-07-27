import React from "react";

export default function ArmButton() {
  const [armed, setArmed] = React.useState(false);
  const [isLoading, setIsLoading] = React.useState(false);

  function toggleArm() {
    setIsLoading(true);
    setTimeout(() => {
      setArmed((val) => !val);
      setIsLoading(false);
    }, 1000);
  }

  return (
    <button
      className={`btn btn-bordered rounded-md min-w-40 min-h-10 font-bold text-2xl uppercase ${
        isLoading
          ? "disabled"
          : armed
          ? "bg-green-600 hover:bg-green-800"
          : "bg-red-500 hover:bg-red-800"
      } text-white`}
      onClick={toggleArm}
    >
      {isLoading ? (
        <span className="loading loading-spinner loading-sm text-white" />
      ) : armed ? (
        "Armed"
      ) : (
        "Disarmed"
      )}
    </button>
  );
}
