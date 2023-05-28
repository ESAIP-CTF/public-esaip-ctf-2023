var Oiram = Oiram || {};
const free_play = false;
let game_running = false;
let game_stop = false;
let game = document.getElementById("game");
let f = document.getElementById("msg-end");
let player = document.getElementById("player");
let player_sprite = document.getElementById("player-sprite");
let timer = document.getElementById("msg-timer");
let col_obj = false;
let col_fin = false;
var car_radians;
var audio = new Audio();
let sprites = ["donkeykong", "luigi", "peach", "toad", "wario", "yoshi"];
let sounds = ["07 3 Circuts.ogg", "13 Sky Garden.ogg", "21 SNES Mario Circuit.ogg", "08 Shy Guy Beach & Cheep-Cheep Island.ogg", "15 Snow Land.ogg", "22 SNES Donut Plains.ogg", "10 Bowser Castle.ogg", "17 Yoshi Desert.ogg", "25 SNES Choco Island.ogg", "12 Cheese Land.ogg", "20 Rainbow Road.ogg", "26 SNES Koopa Beach.ogg"]
var Engine = Matter.Engine,
    Render = Matter.Render,
    Bodies = Matter.Bodies,
    Composite = Matter.Composite;
var engine,
    render;
var int_game;

function menu_click_listener() {
    if(free_play && !game_running) {
        game_running = true
        start_game();
    }
}

function play_coin() {
    let audio_tmp = new Audio("/assets/sound/coins.ogg");
    audio.volume = 0.7;
    audio.loop = false;
    audio_tmp.play();
}

Oiram.game = function() {
    audio.play();
    let sprite = sprites[Math.floor(Math.random() * sprites.length)];
    player_sprite.src = "/assets/img/sprites_" + sprite + ".png";
    game.style.display = "block";

    const date = new Date(new Date().getTime() + 60000);

    Oiram.forward = false;
    Oiram.backward = false;
    Oiram.left = false;
    Oiram.right = false;

    car_radians = 0;

    engine = Engine.create();
    engine.gravity.y = 0;

    render = Render.create({
        element: game,
        engine: engine,
        options: {
            width: 800,
            height: 600,
            wireframes: false
        }
    });

    var player_car = Bodies.rectangle(185, 660, 60, 40, { render: { opacity: 0 }});
    player_car.frictionAir = 0.1;
    player_car.friction = 0.05;
    var bot1 = Bodies.rectangle(120, 600, 64, 76, {
        render: {
            sprite: {
                texture: "/assets/img/oiram_kart.png",
                xScale: 0.9,
                yScale: 0.9
            },
        }
    });
    bot1.frictionAir = 0.1;
    bot1.friction = 0.05;

    var collisions = [];
    collisions.push(Bodies.rectangle(1024, 16, 2048, 32, { isStatic: true }));
    collisions.push(Bodies.rectangle(992, 2048 - 16, 800, 32, { isStatic: true }));
    collisions.push(Bodies.rectangle(992, 2048 - 16, 800, 32, { isStatic: true }));
    collisions.push(Bodies.rectangle(609, 2048 - 192, 32, 384, { isStatic: true }));
    collisions.push(Bodies.rectangle(1376, 2048 - 192, 32, 354, { isStatic: true }));
    collisions.push(Bodies.rectangle(314, 2048 - 368, 560, 32, { isStatic: true }));
    collisions.push(Bodies.rectangle(1700, 2048 - 353, 660, 32, { isStatic: true }));
    collisions.push(Bodies.rectangle(16, 848, 32, 1696, { isStatic: true }));
    collisions.push(Bodies.rectangle(127, 1000 - 1280, 32, 32, { isStatic: true }));
    collisions.push(Bodies.rectangle(1080, 480, 240, 288, { isStatic: true }));
    collisions.push(Bodies.rectangle(1080, 480, 240, 288, { isStatic: true }));  
    collisions.push(Bodies.rectangle(840, 608, 270, 32, { isStatic: true }));  
    collisions.push(Bodies.rectangle(1184, 992, 32, 800, { isStatic: true }));  
    collisions.push(Bodies.rectangle(504, 352, 462, 32, { isStatic: true }));  
    collisions.push(Bodies.rectangle(288, 672, 32, 640, { isStatic: true }));  
    collisions.push(Bodies.rectangle(568, 976, 590, 32, { isStatic: true }));  
    collisions.push(Bodies.rectangle(1056, 1376, 1058, 32, { isStatic: true }));  
    collisions.push(Bodies.rectangle(992, 1537, 32, 350, { isStatic: true }));
    collisions.push(Bodies.rectangle(1454, 352, 550, 32, { isStatic: true }));
    collisions.push(Bodies.rectangle(2048 - 16, 350, 32, 640, { isStatic: true }));
    collisions.push(Bodies.rectangle(1856, 672, 384, 32, { isStatic: true }));
    collisions.push(Bodies.rectangle(1680, 722, 32, 130, { isStatic: true }));
    collisions.push(Bodies.rectangle(1680, 932, 32, 150, { isStatic: true }));
    collisions.push(Bodies.rectangle(1856, 992, 384, 32, { isStatic: true }));
    collisions.push(Bodies.rectangle(2048 - 16, 1350, 32, 722, { isStatic: true }));
    for (let col in collisions) {
        collisions[col].render.opacity = 0;
    }
    Composite.add(engine.world, collisions);

    var mapBackground = Bodies.rectangle(1034, 1014, 2324, 2324, {
        isStatic: true,
        isSensor: true,
        render: {
            sprite: {
                texture: "/assets/img/map.png",
                xScale: 2,
                yScale: 2
            }
        }
    });

    Composite.add(engine.world, [player_car, mapBackground, bot1]);

    Render.run(render);

    var player_angle = 0;

    int_game = setInterval(function() {

        if(Oiram.forward) {
            x = 0;
            y = -0.006;
            Matter.Body.applyForce(player_car, player_car.position, Matter.Vector.create(x * Math.cos(car_radians) - y * Math.sin(car_radians), x * Math.sin(car_radians) + y * Math.cos(car_radians)));
        }
        if(Oiram.backward) {
            x = 0;
            y = 0.003;
            Matter.Body.applyForce(player_car, player_car.position, Matter.Vector.create(x * Math.cos(car_radians) - y * Math.sin(car_radians), x * Math.sin(car_radians) + y * Math.cos(car_radians)));
        }
        if(Oiram.left) {
            if(Oiram.forward || Oiram.backward) {
                car_radians-= 0.06;
            }
        }
        if(Oiram.right) {
            if(Oiram.forward || Oiram.backward) {
                car_radians+= 0.06;
            }
        }
        
        player_angle = (car_radians * (180/Math.PI))  % 360;
        if(player_angle < 0) {
            player_angle+= 360;
        }

        if(player_angle > -22.5 && player_angle < 22.5) {
            player_sprite.removeAttribute("class");
            player_sprite.classList.add("to-top");
        }
        if(player_angle > 22.5 && player_angle < 67.5) {
            player_sprite.removeAttribute("class");
            player_sprite.classList.add("to-top-right");
        }
        if(player_angle > 67.5 && player_angle < 112.5) {
            player_sprite.removeAttribute("class");
            player_sprite.classList.add("to-right");
        }
        if(player_angle > 112.5 && player_angle < 157.5) {
            player_sprite.removeAttribute("class");
            player_sprite.classList.add("to-bottom-right");
        }
        if(player_angle > 157.5 && player_angle < 202.5) {
            player_sprite.removeAttribute("class");
            player_sprite.classList.add("to-bottom");
        }
        if(player_angle > 202.5 && player_angle < 247.5) {
            player_sprite.removeAttribute("class");
            player_sprite.classList.add("to-bottom-left");
        }
        if(player_angle > 247.5 && player_angle < 292.5) {
            player_sprite.removeAttribute("class");
            player_sprite.classList.add("to-left");
        }
        if(player_angle > 292.5 && player_angle < 337.5) {
            player_sprite.removeAttribute("class");
            player_sprite.classList.add("to-top-left");
        }

        Matter.Body.setAngularVelocity(player_car, 0);
        Matter.Body.setAngularVelocity(bot1, 0);
        Matter.Render.lookAt(render, player_car, Matter.Vector.create(270, 270))

        if(Matter.Collision.collides(player_car, collisions[8])) {
            if(!col_obj) {
                play_coin();
                col_obj = true;
                Matter.Body.setPosition(bot1, Matter.Vector.create(400, 1350))
            }
        }

        if(Matter.Collision.collides(player_car, bot1) && col_obj == true) {
            if(!col_fin) {
                play_coin();
                col_fin = true;
                bot1.render.sprite.texture = "/assets/img/oiram_kart_gold.png"
                f.style.display = "inline-block";
            }
        }

        let diff = date - new Date();
        diff = (diff / 1000).toString().slice(0, 5).padEnd(5, "0");
        if(diff > 0) {
            timer.innerHTML = diff;
        } else {
            if(!game_stop) {
                game_stop = true;
                timer.innerHTML = "TIME OUT";
                setTimeout(() => {
                    reset_g();
                }, 1000);
            }
        }

        Engine.update(engine, 1000 / 60);
    }, 1000 / 60);

    document.addEventListener("keydown", keydowngame)
    document.addEventListener("keyup", keyupgame)
};

function keydowngame(event) {
    if(event.code == "ArrowUp") {
        Oiram.forward = true;
    }
    if(event.code == "ArrowDown") {
        Oiram.backward = true;
    }
    if(event.code == "ArrowLeft") {
        Oiram.left = true;
    }
    if(event.code == "ArrowRight") {
        Oiram.right = true;
    }
};

function keyupgame(event) {
    if(event.code == "ArrowUp") {
        Oiram.forward = false;
    }
    if(event.code == "ArrowDown") {
        Oiram.backward = false;
    }
    if(event.code == "ArrowLeft") {
        Oiram.left = false;
    }
    if(event.code == "ArrowRight") {
        Oiram.right = false;
    }
};

/* document.getElementById("btn_start").onclick = (event) => {
    if(!game_running) {
        game_running = true
        start_game();
    }
} */

function reset_g() {
    document.removeEventListener("keydown", keydowngame)
    document.removeEventListener("keyup", keyupgame)
    clearInterval(int_game);
    setTimeout(() => {
        Engine.clear(engine);
        Render.stop(render);
        try { render.canvas.remove(); }
        catch {}
        render.canvas = null;
        render.context = null;
        render.textures = {};
        audio.pause();
        f.style.display = "none";
        col_obj = false;
        col_fin = false;
        game.style.display = "none";
        game_stop = false;
        game_running = false;
    }, 1000);
    audio.volume = 0.4;
    console.log('Cleared!');
    document.body.style.top = "0";
}

function start_game() {
    console.log("Starting game...");
    setTimeout(() => {
        document.body.style.top = "-100vh";
        Oiram.game();
    }, 500);

    audio.pause();
    let s = sounds[Math.floor(Math.random() * sounds.length)];
    audio = new Audio("/assets/sound/" + s);
    audio.loop = true;
    audio.volume = 1;
    audio.load();
}
