import {
  useNavigate,
  useRouteError,
  isRouteErrorResponse,
} from "react-router-dom";

export default function ErrorBoundary() {
  const error = useRouteError();
  const navigate = useNavigate();
  let errorStatus: string | number = "";
  let errorStatusText: string | number = "";

  if (isRouteErrorResponse(error)) {
    // error is type `ErrorResponse`
    errorStatus = error.status;
    errorStatusText = error.statusText;
  } else if (error instanceof Error) {
    errorStatusText = error.message;
  } else if (typeof error === "string") {
    errorStatusText = error;
  } else {
    errorStatusText = "Unknown error";
  }

  return (
    <div className="w-full flex flex-col items-center justify-center gap-2 p-10">
      <p className="text-6xl text-gray-400 font-bold">{errorStatus}</p>
      <p className="text-3xl text-blue-600 font-semibold">{errorStatusText}</p>
      <button
        className="underline"
        onClick={() => {
          navigate("/");
        }}
      >
        Return Home
      </button>
    </div>
  );
}
