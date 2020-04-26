import React, {Component} from "react";
import { MDBBtn, MDBDataTable, } from 'mdbreact';
import { headers } from './data/headers.js';
import { postHeaders } from './data/postHeaders.js';
import { usePromiseTracker, trackPromise } from "react-promise-tracker";
import Loader from 'react-loader-spinner';
import axios from 'axios';

const downloadBaseURL = process.env.REACT_APP_CIA_DOWNLOAD_URL;
const apiBaseURL = process.env.REACT_APP_CIA_BASE_URL;
const backendURL=`${process.env.REACT_APP_BACKEND_HOST}:${process.env.REACT_APP_BACKEND_PORT}`
const postArray=['kidney','abdomen', 'lung','brain','bone'];
var dataHeader;
var postSwitch=false;

const LoadingIndicator = props => {
   const { promiseInProgress } = usePromiseTracker();
   return (
     promiseInProgress &&
     <div
       style={{
         width: "100%",
         height: "100%",
         display: "flex",
         justifyContent: "center",
         alignItems: "center"
       }}
     >
       <Loader type="ThreeDots" color="#2BAD60" height={100} width={100} />
     </div>
  );
 }


class DataTable extends Component {

  constructor(props) {
    super(props);

    this.state = {
      tableData: {},
      loadingData: true
    };
  }

  send(downloadURL){
    const data={"downloadURL": downloadURL};
    trackPromise(
      axios
      .post(`${backendURL}/send`, data)
      .then((response)=> {
        if(response.status==200){
          console.log(response.data)
          console.log("Sent to HoloRepository!")
          alert("Sent to HoloRepository")
        }
        else{
          console.log("Error with transmission to HoloRepository!")
          alert("Error with transmission to HoloRepository!")
        }
      })
      .catch(err => {
        alert("Error with transmission to HoloRepository!")
        console.error(err);
      })
      );
  }

  dataFetch(){
    var file = (this.props.bodyPart).toLowerCase();
    if(file){
      if(this.props.local){
        var apiURL = `data/${file}.json`;
      }else{
        var searchBodyPart = (this.props.bodyPart).toUpperCase();
        var apiURL = `${apiBaseURL}${searchBodyPart}`;
      }

    if(postArray.includes(file)){
      dataHeader=postHeaders;
      postSwitch=true;
    }else{
      dataHeader=headers;
      postSwitch=false;
    }

    trackPromise(
      fetch(apiURL)
        .then(response => response.json())
        .then(json => {

          var dataLength = json.length;
          if(dataLength!=0){
            for (var i = 0; i < dataLength; i++) {
              var downloadURL = downloadBaseURL + json[i].SeriesInstanceUID;
              if(postSwitch==true){
                json[i].send =  <MDBBtn  value={downloadURL} onClick={e => this.send(e.target.value)}  color="blue" size="sm">Send</MDBBtn>;
              }
              json[i].download =  <MDBBtn href= {downloadURL}  color="purple" size="sm">Download</MDBBtn>;
            }

            this.setState({
                tableData: {
                  columns: dataHeader,
                  rows: json
                },
                loadingData: false
              });
          }else{
            alert("Not a valid body part");
          }

        })
        .catch((error) => {
          alert("Not a valid body part");
        }));
    }
  }

  componentDidMount(){
    this.dataFetch();
  }

  componentDidUpdate(prevProps) {
    if (this.props.bodyPart !== prevProps.bodyPart) {
      this.dataFetch();
    }
  }


  render(){

    return (
      <div>
        <LoadingIndicator/>
        <MDBDataTable
        bordered
        small
        data={this.state.tableData}
        striped
        />
      </div>

    );

  }
}

export default DataTable;
