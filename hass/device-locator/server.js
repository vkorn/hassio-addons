#!/usr/bin/env node

const express = require("express");
const app = express();

const router = express.Router();
const argv = require('minimist')(process.argv.slice(2));
const devices = {};
if (argv.config) {
    data = JSON.parse(require('fs').readFileSync(argv.config, "UTF-8"));
    if (data.hosts) {
        data = data.hosts;
        for (let ii = 0; ii < data.length; ii++) {
            devices[data[ii].ip] = data[ii].name;
        }
        console.log("Got " + data.length + " entries from config");
    }
}

router.route("")
    .get(function (req, res) {
        let ip = req.ip;
        let name = "";
        if (devices.hasOwnProperty(ip)) {
            name = devices[ip];
        }

        res.json({
            "ip": ip,
            "name": name
        });
    });

app.enable('trust proxy');
app.use("/", router);
const port = argv.port || 3000;
const ip = argv.host || "0.0.0.0";
app.listen(port, ip, function () {
    console.log("Listening on " + ip + ":" + port);
});