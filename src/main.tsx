import ReactDOM from "react-dom/client";
import "./index.css";
import Navbar from "./components/Navbar.tsx";
// import { Provider } from "react-redux";
// import store from "./store";
import App from "./App.tsx";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <>
    {/* <Provider store={store}> */}
    <Navbar />
    <App />
    {/* </Provider> */}
  </>
);
