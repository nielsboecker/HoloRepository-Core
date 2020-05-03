const app = require("express");
const router = app.Router();

const transmission_service = require('../services/transmission_service.js');

router.post('/', async function(req, res){
    data = req.body.downloadURL;
    await transmission_service.transmit(data, async function(result) {
        if (result.status === 200) {
            res.send(`Backend has received: ${data},  ${result.payload.response}`);
        }else{
            res.json(result.payload).status(500);
        }
    });
    
});


module.exports = router;