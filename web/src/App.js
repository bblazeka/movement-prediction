import React, { Component } from 'react';
import DataProvider from "./components/DataProvider";
import MapInterface from "./components/MapInterface";
import './App.css';

class App extends Component {

  render() {
    return (
      <div>
        <DataProvider endpoint="http://localhost:8000/api/point/" 
                render={data => <MapInterface data={data} />} />
      </div>
    );
  }
}

export default App;
