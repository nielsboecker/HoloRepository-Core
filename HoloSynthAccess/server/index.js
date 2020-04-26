const express = require('express')
const app = express()
const logger = require('morgan');  
const cors = require('cors');
require('dotenv').config();
const bodyParser = require('body-parser');

const port= process.env.PORT || 3006;

let transmission_router = require("./routes/transmission_router.js");

app.use(cors({credentials: true}));

app.use(logger('dev'));
app.use(bodyParser.urlencoded({ extended: false }));

// parse application/json
app.use(bodyParser.json())
 

app.get('/', (req, res) => res.send('HoloSynthAcess backend is working as intended'))

app.use('/send', transmission_router);

app.listen(port, () => console.log(`HoloSynthAccess backend listening at http://localhost:${port}`))