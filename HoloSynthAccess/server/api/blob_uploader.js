const { BlobServiceClient, StorageSharedKeyCredential } = require('@azure/storage-blob');
const fs = require('fs')
const sharedKeyCredential = new StorageSharedKeyCredential(process.env.AZURE_STORAGE_ACCOUNT, process.env.AZURE_STORAGE_ACCESS_KEY);
const blobServiceClient = new BlobServiceClient(
    `https://${process.env.AZURE_STORAGE_ACCOUNT}.blob.core.windows.net`,
    sharedKeyCredential
);



let uploadStudy = async function(callback){
    let name=Date.now().toString() + 'imaging_study'

    const containerClient = blobServiceClient.getContainerClient(process.env.AZURE_BLOB_CONTAINER);
    const blockBlobClient = containerClient.getBlockBlobClient(name + ".zip");

    

    try {
        let fileStream= fs.createReadStream("./file/temp.zip");
        await blockBlobClient.uploadStream(fileStream,
          uploadOptions.bufferSize, uploadOptions.maxBuffers,
          { blobHTTPHeaders: { blobContentType: "application/zip" } });
          return callback({status: 200, payload: {success: true, blob_name:name, response:`${name} uploaded to Azure blob storage`}})
      } catch (err) {
        return callback({status: 500, payload: {success: true, response:` Error with upload to Azure blob storage`}})
      }
}




module.exports = {uploadStudy}; 