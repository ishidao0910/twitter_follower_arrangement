import { StrictMode } from "react";
import React from "react";
import ReactDom from "react-dom";

// import App from "./App";

const App = () => {
  return (
  <React.Fragment>
    <h1> test h1 </h1>
    <p> test p tag </p>
  </React.Fragment>
  );
};

ReactDom.render(
  <StrictMode>
    <App />
  </StrictMode>
  , document.getElementById("root")
);