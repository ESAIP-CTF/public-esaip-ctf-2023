const express = require("express");
const axios = require("axios");
const uri = require("uri-js");
app = express();

app.set("trust proxy", 1);

app.get("/flag", (req, res) => {
    if (req.ip === "127.0.0.1") {
        res.send("ECTF{UrL_RfCsss<3}");
    } else {
        res.send("Permission denied!");
    }
})

app.use((req, res) => {
    const url = uri.parse(`${req.protocol}://${req.hostname}${req.path}`)

    if (url.host !== "www.supermarioplomberie.fr") {
        res.status(403);
        res.send("Only www.supermarioplomberie.fr is authorized!");
    } else {
        axios.get(`${req.protocol}://${req.hostname}${req.path}`).then(response => {
            res.contentType(response.headers["content-type"]);
            res.send(response.data);
        }).catch(e => {
            res.status(404);
            res.send("Page not found!");
        });
    }
})

app.listen(3000, () => {});
