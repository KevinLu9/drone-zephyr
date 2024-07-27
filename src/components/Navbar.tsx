import zephyr from "/zephyr.svg";

export default function Navbar() {
  return (
    <>
      <div className="navbar bg-base-100 w-full hideen md:flex items-center justify-center bg-gradient-to-r from-secondary to-70% to-base-100">
        <img src={zephyr} alt="" className="h-10 w-10" />
        <button className="btn btn-ghost text-2xl font-bold text-primary">
          Zephyr
        </button>
      </div>
    </>
  );
}
