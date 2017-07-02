const git = require("simple-git");
let Client = require("node-rest-client").Client;
const path = require('path');

const argv = require("minimist")(process.argv.slice(2));
const HASS = "_hass_";
const config = JSON.parse(require('fs').readFileSync(argv.config || "/data/options.json", "UTF-8"));
const watchingTargets = {};
const baseDir = config.base_dir || "/config";

let addons = [];

addToWatchList = function (addon, folder) {
    if (!watchingTargets.hasOwnProperty(folder)) {
        watchingTargets[folder] = [];
    }

    if (watchingTargets[folder].indexOf(addon) === -1) {
        watchingTargets[folder].push(addon);
    }
};

let ii;
for (ii = 0; ii < config.hass_watch.length; ii++) {
    addToWatchList(HASS, config.hass_watch[ii]);
}

for (ii = 0; ii < config.addons.length; ii++) {
    addToWatchList(config.addons[ii].name, config.addons[ii].watch);
}

isChildOf = (child, parent) => (child !== parent) && parent.split("/").every((t, i) => child.split("/")[i] === t);
const isHassNotify = config.notify || true;
const hassioHost = config.hassio_host || "http://172.17.0.2";
const hassHost = config.hass_host || "http://172.17.0.1:8123";
const checkDelay = config.check_delay || 1;

const restClient = new Client({
    connection: {
        rejectUnauthorized: false
    }
});

notify = function (message) {
    if (!isHassNotify) {
        return;
    }

    restClient.post(hassHost + "/api/services/notify/" + config.notify_entity,
        {
            data: JSON.stringify({"message": message}),
            method: "POST",
            headers: {
                "x-ha-access": config.hass_key,
                "Content-Type": "application/json",
            }
        },
        function (data, response) {
        })
        .on('error', function (error) {
            console.error("Failed to call service " + error);
        });
};

const restartHass = function () {
    restClient.post(hassioHost + "/homeassistant/restart",
        {
            data: {},
            method: "POST",
        },
        function (data, response) {
        })
        .on('error', function (error) {
            console.error("Failed to restart hass " + error);
        });
};

const restartAddon = function (name) {
    for (let jj = 0; jj < addons.length; jj++) {
        if (addons[jj].name === name) {
            restClient.post(hassioHost + "/addons/" + addons[jj].slug + "/restart",
                {
                    data: {},
                    method: "POST",
                },
                function (data, response) {
                })
                .on('error', function (error) {
                    console.error("Failed to restart  addon " + name + " " + error);
                });
        }
    }
};

getAddons = function () {
    restClient.get(hassioHost + "/supervisor/info",
        function (data) {
            if (typeof  data !== "object") {
                console.error("Failed to fetch addons");
                process.exit(1);
            }
            addons = data.data.addons;
        })
        .on('error', function (error) {
            console.error("Failed to get addons " + error);
        });
};

const doPull = function () {
    git(baseDir).pull(function (err, update) {
        if (err) {
            console.error("Error while pulling from git: %s", err.message);
            return;
        }

        if (update && update.summary.changes) {
            let addonsToUpdate = [];
            for (ii = 0; ii < update.files.length; ii++) {
                let folder = path.dirname(update.files[ii]);
                for (let key in watchingTargets) {
                    if (isChildOf(folder, key) || update.files[ii] === key) {
                        for (let jj = 0; jj < watchingTargets[key].length; jj++) {
                            if (addonsToUpdate.indexOf(watchingTargets[key][jj]) === -1) {
                                addonsToUpdate.push(watchingTargets[key][jj]);
                            }
                        }
                    }
                }
            }

            if (addonsToUpdate.length === 0) {
                console.log("No restart required");
                return;
            }

            let updateString = "[ConfigWatcher] Going to restart following add-ons";

            for (ii = 0; ii < addonsToUpdate.length; ii++) {
                updateString += " " + addonsToUpdate[ii];
            }

            console.log(updateString);
            notify(updateString);

            // Two times because hass might be one of the targets for restarting
            for (ii = 0; ii < addonsToUpdate.length; ii++) {
                if (addonsToUpdate[ii] === HASS) {
                    restartHass();
                } else {
                    restartAddon(addonsToUpdate[ii]);
                }
            }

        } else {
            console.log("No changes");
        }
    });


    setInterval(doPull, (checkDelay) * 60 * 1000);
};

getAddons();
doPull();