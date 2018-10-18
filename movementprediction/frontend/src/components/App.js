import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import MapInterface from "./MapInterface";

const App = () => (
  <DataProvider endpoint="api/point/" 
                render={data => <MapInterface data={data} />} />
);

const wrapper = document.getElementById("app");

wrapper ? ReactDOM.render(<App />, wrapper) : null;