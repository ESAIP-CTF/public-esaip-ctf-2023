class ChatBot {
    constructor() {
        this.session_start = false;
        this.caller = "";
        this.messages = {
            "What is the status of my order?": `You can find this information on the <a href="https://www.nintendo.com/orders/">order status</a> page.`,
            "How long will it take to receive my order?": `Please see <a href="https://en-americas-support.nintendo.com/app/answers/detail/a_id/5910">Shipping & Processing</a> for detailed information.`,
            "How do I obtain a refund or return an item I purchased from Nintendo?": `Please see <a href="https://en-americas-support.nintendo.com/app/answers/detail/a_id/15576">Returns and Exchanges</a> for detailed information.`,
            "What is the condition of Authentic Nintendo Refurbished Products?": `Authentic Nintendo Refurbished Products may have minor cosmetic defects, such as small scratches or dents. However, they are held to the same functional specifications as our new systems and come with the same one-year warranty as our new systems.`
        };
    }

    init(caller) {
        this.caller = caller;
        this.session_start = true;
    }

    ask(question) {
        if (this.session_start) {
            return this.messages[question] ? this.messages[question] : `I don't understand your question.`;
        } else {
            return "Session not started!";
        }
    }
}

const regex = /<|>/g

var user_msg = (msg, date) => {
    const user_template = `
    <div class="d-flex flex-row justify-content-end mb-4 pt-1">
        <div>
            <p class="small p-2 me-3 mb-1 text-white rounded-3" style="background-color: #FF393A;">{{message}}</p>
            <p class="small me-3 mb-3 rounded-3 text-muted d-flex justify-content-end">{{date}}</p>
        </div>
        <img src="/static/img/toad.png" alt="avatar 1" style="width: 45px; height: 100%;">
    </div>`;

    let content;
    var output  = document.createElement("div");
    if (regex.test(msg)) {
        content = user_template
            .replace("{{message}}", "Attack detected!")
            .replace("{{date}}", date);
    } else {
        content = user_template
            .replace("{{message}}", msg)
            .replace("{{date}}", date);
    }
    output.innerHTML = content;
    chat.appendChild(output);
}

var bot_msg = (msg, date) => {
    const bot_template = `
    <div class="d-flex flex-row justify-content-start">
        <img src="/static/img/toadette.png" alt="avatar 1" style="width: 45px; height: 100%;">
        <div>
            <p class="small p-2 ms-3 mb-1 rounded-3" style="background-color: #f5f6f7;">{{message}}</p>
            <p class="small ms-3 mb-3 rounded-3 text-muted">{{date}}</p>
        </div>
    </div>`;

    var output  = document.createElement("div");
    var content = bot_template
        .replace("{{message}}", msg)
        .replace("{{date}}", date);
    output.innerHTML = content;
    chat.appendChild(output);
}

window.onload = () => {
    var bot = new ChatBot();

    onmessage = e => {
        if (!(e.source === parent)) { return }

        if (e.data.action === "init") {
            bot.init(e.data.caller);

        } else if (e.data.action === "ask") {
            var d = new Date();
            d = d.getHours() + ':' + d.getMinutes();

            user_msg(e.data.question, d);
            bot_msg(bot.ask(e.data.question), d);
            scrollTo(0, document.body.scrollHeight);
        }
    }
}
