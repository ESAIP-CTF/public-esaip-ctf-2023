// Setup app
const express = require("express");
const app  = express();
app.set("view engine", "ejs");


// Static files path
const path = require("path")
app.use("/static", express.static(path.join(__dirname, "static")))

// Logging
app.use((req, _, next) => {
    console.log(`[Chat] ${req.socket.remoteAddress} - ${req.url}`);
    next();
})

// Routes
app.get("/bot", (req, res) => {
    res.render("index");
})


// Start app
const port = 3001;
app.listen(port, () => {
    console.log(`[Chat] Listening on port ${port}`)
})