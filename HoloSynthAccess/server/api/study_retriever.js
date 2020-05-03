const axios = require('axios');

const Fs = require('fs')  
const Path = require('path')  


let downloadStudy = async function(url, callback) {
    //Modified section of code from https://stackoverflow.com/questions/55374755/node-js-axios-download-file-and-writefile
   
    console.log(url);
    const path = Path.resolve(__dirname, 'file', 'temp.zip')
    const writer = Fs.createWriteStream(path);
  
    return axios({
      method: 'get',
      url: url,
      responseType: 'stream',
    }).then(response => {
  
      return new Promise((resolve, reject) => {
        response.data.pipe(writer);
        let error = null;
        writer.on('error', err => {
          error = err;
          writer.close();
          reject(err);
          return callback({status: 500, payload: {success: false, response: "There was an error with fetching the imaging study"}})
        });
        writer.on('close', () => {
          if (!error) {
            resolve(true);
            console.log("file downloaded")
            return callback({status: 200, payload: {success: true, response: "Study fetched correctly"}})
          }
        });
      });
    })
    .catch(err=>{
        console.error(err);
    });

}
    module.exports = {downloadStudy};