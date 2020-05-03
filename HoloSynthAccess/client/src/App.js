import React from 'react';
import './style/App.css';
import SearchTable from './searchTable.js'
require('dotenv').config()

const App = () => {

    return (
      <div className="canvas">
        <div className="header-container">HoloSynthAccess</div>
        <div className="main-container">
          <SearchTable />
        </div>
      </div>
    );
}

export default App;