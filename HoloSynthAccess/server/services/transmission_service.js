let {downloadStudy} = require("../api/study_retriever.js");
let{uploadStudy}= require("../api/blob_uploader.js");
let{insertFHIR}= require("../api/fhir_client.js");


let transmit = async function(url, callback){
    console.log("beginning download");
    await downloadStudy(url, async function(result){
        if(result==null || result.status==500){
            return callback({status: 500, payload: {success: true, response: result.payload.response}})
        }else{
            console.log("beginning upload to azure");
            await uploadStudy(async function(result){
                if(result==null || result.status==500){
                    return callback({status: 500, payload: {success: true, response: result.payload.response}})
                }else{
                    console.log("beginning FHIR record insertion");
                    await insertFHIR(result.payload.blob_name, async function(result){
                        if(result==null || result.status==500){
                            return callback({status: 500, payload: {success: true, response: result.payload.response}})
                        }else{
                            return callback({status: 200, payload: {success: true, response: result.payload.response}})
                        }
                    });
                }
            });
            
        }
    });

}



module.exports = {transmit}; 

