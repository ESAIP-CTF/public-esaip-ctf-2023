const cookieParser = require("cookie-parser");
const session = require("express-session");
const express = require("express");
const axios = require("axios");
const path = require("path");


// Setup app
const app  = express();
app.set("view engine", "ejs");


// Middlewares
app.use("/static", express.static(path.join(__dirname, "static")));
app.use(cookieParser());
app.use(session({
    secret: require("crypto").randomBytes(32).toString("hex"),
    saveUninitialized:true,
    cookie: {
        path: "/",
        httpOnly: true,
        maxAge: 1000 * 60 * 60 * 24
    },
    resave: false 
}));

// Logging
app.use((req, _, next) => {
    console.log(`[App]  ${req.socket.remoteAddress} - ${req.url}`);
    next();
})

// Routes
app.get("/", (req, res) => {
    res.render("index");
})

app.get("/buy", (req, res) => {
    // responses
    const allowed = `<script>
        alert("${process.env.FLAG}");
        document.location.href = "http://www.nintendo.com/switch/";
    </script>`
    const not_allowed = `<script>
        alert("Not allowed!");
        document.location.href = "/";
    </script>`

    const access_token = req.session.access_token;
    if (access_token) {
        axios.get(`https://www.googleapis.com/oauth2/v2/userinfo?fields=email&access_token=${access_token}`).then(response => {
            const email = response.data.email;
            if (email === process.env.EMAIL) {
                res.send(allowed);
            } else {
                res.status(403);
                res.send(not_allowed);
            }
        }).catch(error => {
            res.status(403);
            res.send(not_allowed);
        });
    } else {
        res.status(403);
        res.send(not_allowed);
    }
})


// OAuth
const client_id     = process.env.CLIENT_ID;
const client_secret = process.env.SECRET
const redirect_uri  = process.env.REDIRECT_URI;
const response_type = "code";
const scope         = "email";

app.get("/auth", (req, res) => {
    var state = require("crypto").randomBytes(32).toString("hex");
    req.session.state = state;
    return res.redirect(`https://accounts.google.com/o/oauth2/v2/auth?response_type=${response_type}&redirect_uri=${redirect_uri}&scope=${scope}&client_id=${client_id}&state=${state}`);
});

app.get("/auth/callback", (req, res) => {
    const state = req.query.state;
    if (req.session.state == undefined || state !== req.session.state) {
        return res.redirect("/?error=1");
    }

    const code = req.query.code;
    if (!code) {
        return res.redirect("/auth");
    }

    axios.post("https://accounts.google.com/o/oauth2/token", {
        grant_type: "authorization_code",
        redirect_uri: redirect_uri,
        client_id: client_id,
        client_secret: client_secret,
        code: code
    },{
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    }).then(response => {
        var access_token = response.data.access_token;

        if (access_token) {
            req.session.access_token = access_token;
            return res.redirect("/buy");
        } else {
            return res.redirect("/");
        }
    }).catch(error => {
        return res.redirect("/");
    });
});


// Start app
const port = 3000;
app.listen(port, () => {
    console.log(`[App] Listening on port ${port}`)
})
