let {template} = require('./fhir_template.js');
const fhirClient = require("fhirclient");



let insertFHIR = async function(blob_name, callback){

    let blob_address = `https://${process.env.AZURE_STORAGE_ACCOUNT}.core.windows.net/${AZURE_BLOB_CONTAINER}/${blob_name}`

    let fhir_record = Object.assign({}, template)

    fhir_record.address=blob_address
    fhir_record.series.bodySite.display="HoloSynthAccess"
    fhir_record.series.modality="MRI/CT"


    try{
        const client = fhirClient(req, res).client({
            serverUrl: process.env.ACCESSOR_FHIR_UR
        });
       await client.request({
            url: "ImagingStudy",
            method: "POST",
            body: fhir_record
        })
        .then(response=>{
            return callback({status: 200, payload: {success: true, response:`${blob_name} FHIR Record insertion complete`}})
        })
    }catch(err){
        return callback({status: 200, payload: {success: true, response:`Error with FHIR insertion`}})
    }
    

}



module.exports = {insertFHIR}; 