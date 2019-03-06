import React, { Component } from 'react';
import MapInterface from "./components/MapInterface";
import ErrorBoundary from './ErrorBoundary';
import './App.css';

class App extends Component {

  render() {
    return (
      <div>
        <ErrorBoundary>
          <MapInterface />
        </ErrorBoundary>
      </div>
    );
  }
}

export default App;
