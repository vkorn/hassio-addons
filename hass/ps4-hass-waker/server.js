#!/usr/bin/env node

const express = require("express");
const app = express();

const router = express.Router();

const {Device} = require("ps4-waker");
const OK = {status: "success"};
const HTTP_400 = 400;
const HTTP_404 = 404;

const argv = require('minimist')(process.argv.slice(2));

if (!argv.credentials) {
    console.error("Please spesify --credentials");
    process.exit(1);
}

const get_options = function (ip) {
    return {
        address: ip,
        credentials: argv.credentials,
        timeout: argv.timeout || 5000
    }
};

router.route("/:device_ip/info")
    .get(function (req, res) {
        let ps4 = new Device(get_options(req.params.device_ip));
        ps4.getDeviceStatus().then(function (info) {
            res.json(info);
            ps4.close();
        }).catch(function (err) {
            res.status(HTTP_404);
            res.json({status: err.message});
        })
    });

router.route("/:device_ip/on")
    .get(function (req, res) {
        let ps4 = new Device(get_options(req.params.device_ip));
        ps4.turnOn().then(function () {
            res.json(OK);
            ps4.close();
        }).catch(
            function (err) {
                res.status(HTTP_400);
                res.json({status: err.message})
            }
        );
    });

router.route("/:device_ip/off")
    .get(function (req, res) {
        let ps4 = new Device(get_options(req.params.device_ip));
        ps4.turnOff().then(function () {
            res.json(OK);
            ps4.close();
        }).catch(
            function (err) {
                res.status(HTTP_400);
                res.json({status: err.message})
            }
        );
    });

router.route("/:device_ip/start/:title")
    .get(function (req, res) {
        let ps4 = new Device(get_options(req.params.device_ip));
        ps4.startTitle(req.params.title).then(function () {
            res.json(OK);
            ps4.close();
        }).catch(
            function (err) {
                res.status(HTTP_400);
                res.json({status: err.message})
            }
        );
    });

router.route("/:device_ip/key/:key")
    .get(function (req, res) {
        let ps4 = new Device(get_options(req.params.device_ip));
        ps4.sendKeys([req.params.key]).then(function () {
            res.json(OK);
            ps4.close();
        }).catch(
            function (err) {
                res.status(HTTP_400);
                res.json({status: err.message})
            }
        );
    });


app.use("/ps4", router);
const port = argv.port || 3000;
const ip = argv.host || "0.0.0.0";
app.listen(port, ip, function () {
    console.log("Listening on " + ip + ":" + port);
});
