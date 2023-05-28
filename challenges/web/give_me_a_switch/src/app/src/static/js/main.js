window.onload = () => {
    scroll = () => {};
    setTimeout(() => { bot.contentWindow.postMessage({"action": "init", "caller": document.location.href}, '*') }, 500);
}