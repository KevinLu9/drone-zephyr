import ArmButton from "../../components/ArmButton";
import fpvPlaceholder from "/fpv-placeholder.jpg";

export default function Dashboard() {
  return (
    <>
      <div className="block w-full text-center top-0 sticky p-2 mb-2 bg-base-200 border-b border-t border-accent">
        <ArmButton />
      </div>
      <div className="flex flex-col gap-4 w-full p-4 pt-0 h-full md:h-[80vh]">
        <div className="flex h-full gap-6 flex-col md:flex-row items-start justify-center">
          <div className="flex flex-col gap-6 w-full md:w-2/3 h-full">
            <img
              src={fpvPlaceholder}
              className="aspect-video border border-accent rounded-md h-[50vh] w-fit"
            />
            <div className="w-full bg-neutral rounded-md h-1/3 p-2">1</div>
            <div className="w-full bg-neutral rounded-md h-1/3 p-2">2</div>
            <div className="w-full bg-neutral rounded-md h-1/3 p-2">3</div>
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
