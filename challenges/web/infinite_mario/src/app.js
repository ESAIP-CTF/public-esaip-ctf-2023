// Setup log config
const process = require('process');
const fs = require("fs");
process.chdir("logs/");
var merge = (src, dst) => {
    for (const [key, value] of Object.entries(src)) {
        if (`${value}`.includes("object")) {
            dst[key] = merge(value, typeof dst[key] === "object" ? dst[key] : {});
        } else {
            dst[key] = value || dst[key] || "";
        }
    }
    return dst;
};


// Setup express server
const cookieParser = require("cookie-parser");
const mongodb = require("mongodb");
const express = require("express");
const path    = require("path");
const app     = express();
const port    = 3000;


// Middleware
app.use("/static", express.static(path.join(__dirname, "static")));
app.use(cookieParser());
app.use((req, res) => {
    var config = merge({
        path: req.cookies.log,
        data: [req.url, req.method, req.headers["user-agent"]]
    },{
        path: "all_users.txt",
        data: []
    });

    if (!config.path.includes("/")) {
        fs.writeFile(config.path, config.data.join(" | "), (e) => {
            if (e) {
                fs.mkdir(config.path, { recursive: true }, (e) => {
                    if (e) {
                        throw new Error(e);
                    }
                });
            } else {
                console.log(`[LOG] Log saved into: ${config.path}.`);
            }
        })
    }

    req.next();
})


// Routes
app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "main.html"));
})


// Start app
app.listen(port, () => {
    console.log(`[LOG] App listening on port ${port}.`);
})
