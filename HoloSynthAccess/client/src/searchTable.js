import React, { Component } from "react";
import DataTable from './dataTable.js';
import './style/searchTable.css';
import '../node_modules/react-widgets/dist/css/react-widgets.css';
import { DropdownList } from 'react-widgets'
import { bodyParts } from './data/bodyparts.js';


class SearchTable extends Component {
  constructor(props) {
    super(props);

    this.state = {
      bodyPart: '',
      local: false
    };
    this.mySubmitHandler = this.mySubmitHandler.bind(this);
    this.myAPISubmitHandler = this.myAPISubmitHandler.bind(this);
  }

  mySubmitHandler = (event) => {
    event.preventDefault();
    this.setState({
      bodyPart: this.element.value,
      local: true
    });

  }

  myAPISubmitHandler = (event) => {
    event.preventDefault();
    this.setState({
      bodyPart: this.elementm.value,
      local: false
    });


  }

  render() {
    let paramsPass = {
      bodyPart:this.state.bodyPart,
      local:this.state.local
    };

    return (
      <div className="grid-container">

      <div className="searchLocalContainer">
        <p>Search a body part locally:</p>
        <form onSubmit={this.mySubmitHandler}>
          <label>
            <input type="text" ref={el => this.element = el} />
          </label>
          <input type="submit" value="Submit" />
        </form>
      </div>

        <div className="searchAPIContainer">
          <p>Select a body part:</p>
          <DropdownList
            data={bodyParts}
            value={this.state.value}
            onChange={value => this.setState({ 
              bodyPart: value,
              local: false 
            })}
          />
        </div>


        <div className="table">
          <DataTable {...paramsPass}/>
        </div>


      </div>
    );
  }
}

export default SearchTable;
