import {
  Battery0Icon,
  Battery100Icon,
  Battery50Icon,
} from "@heroicons/react/16/solid";
import ArmButton from "../../components/ArmButton";
import DroneJoystick from "../../components/DroneJoystick";
import fpvPlaceholder from "/fpv-placeholder.jpg";
import Throttle from "../../components/Throttle";

interface dashboardProps {
  batteryVoltage: number;
  roll: number;
  pitch: number;
  yaw: number;
  isArmed: boolean;
  tiltX: number;
  tiltY: number;
  tiltZ: number;
}

export default function Dashboard({
  batteryVoltage,
  roll,
  pitch,
  yaw,
  isArmed,
  tiltX,
  tiltY,
  tiltZ,
}: dashboardProps) {
  const MAX_BATTERY_VOLTAGE = 18.3;
  const MIN_BATTERY_VOLTAGE = 12;
  const BATTERY_CELLS_NUM = 4;

  const renderBatteryVoltage = () => {
    return (
      <div className="flex gap-2 items-center">
        {batteryVoltage >
          MIN_BATTERY_VOLTAGE +
            (2 * (MAX_BATTERY_VOLTAGE - MIN_BATTERY_VOLTAGE)) / 3 && (
          <Battery100Icon className="w-8" />
        )}
        {batteryVoltage <=
          MIN_BATTERY_VOLTAGE +
            (2 * (MAX_BATTERY_VOLTAGE - MIN_BATTERY_VOLTAGE)) / 3 &&
          batteryVoltage >=
            MIN_BATTERY_VOLTAGE +
              (MAX_BATTERY_VOLTAGE - MIN_BATTERY_VOLTAGE) / 3 && (
            <Battery50Icon className="w-8" />
          )}
        {batteryVoltage <
          MIN_BATTERY_VOLTAGE +
            (MAX_BATTERY_VOLTAGE - MIN_BATTERY_VOLTAGE) / 3 && (
          <Battery0Icon className="w-8" />
        )}

        <div className="flex items-center">
          <div className="flex items-center">
            <p className="text-xl font-bold">
              {(batteryVoltage / BATTERY_CELLS_NUM)?.toFixed(2)} V
            </p>
            <p className="text-sm self-end">{BATTERY_CELLS_NUM}S</p>
          </div>
        </div>
        <p className="text-md">({batteryVoltage?.toFixed(2)} V)</p>
      </div>
    );
  };

  return (
    <>
      <div className="block w-full text-center top-0 sticky p-2 mb-2 bg-base-200 border-b border-t border-accent">
        <ArmButton {...{ isArmed }} />
      </div>
      <div className="flex flex-col gap-4 w-full p-4 pt-0 h-full md:h-[80vh]">
        <div className="flex h-full gap-6 flex-col md:flex-row items-start justify-center">
          <div className="flex flex-col gap-6 w-full md:w-2/3 h-full items-center">
            <img
              src={`http://192.168.1.129:8002/stream.mjpg`}
              className="aspect-video border border-accent rounded-md h-fit md:h-[50vh] w-full md:w-fit"
            />
            <div className="w-full bg-neutral rounded-md p-2">
              {renderBatteryVoltage()}
              <p>
                roll: {roll?.toFixed(2)}, pitch: {pitch?.toFixed(2)}, yaw:{" "}
                {yaw?.toFixed(2)}
              </p>
              <p>
                tilt: {tiltX?.toFixed(2)}, {tiltY?.toFixed(2)},{" "}
                {tiltZ?.toFixed(2)}
              </p>
              <div className="flex flex-col gap-4 mt-2">
                <Throttle />
                <div className="flex w-full justify-between items-center">
                  <DroneJoystick joystickType="turn" />
                  <DroneJoystick joystickType="tilt" />
                </div>
              </div>
            </div>
          </div>
          <div className="w-full md:w-1/3 h-full bg-neutral rounded-md overflow-y-auto p-2">
            <p>4</p>
            <div className="w-full h-1/3 rounded-md mb-2">BLOCK</div>
            <div className="w-full h-1/3 rounded-md">BLOCK</div>
          </div>
        </div>
      </div>
    </>
  );
}
