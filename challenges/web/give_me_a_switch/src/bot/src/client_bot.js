// Required packages
const puppeteer = require("puppeteer-extra");
const stealthP = require("puppeteer-extra-plugin-stealth");
puppeteer.use(stealthP());
const bot_email = process.env.EMAIL;
const bot_pass  = process.env.PASS;

// Sleep
const delay = (time) => {
    return new Promise(resolve => setTimeout(resolve, time));
}

// Readline
function rlSync() {
    return new Promise((resolve, _) => {
        process.stdin.resume();
        process.stdin.on("data", (d) => {
            process.stdin.pause();
            resolve(d.toString().slice(0,-1));
        });
    });
}

const google_login = async (page) => {
	console.log("[LOG] Setup bot's google account...");
	await page.goto("https://accounts.google.com/ServiceLogin");

	// Login 1st part
	const email = await page.waitForSelector("#identifierId");
	email.focus();
	await page.keyboard.type(bot_email, { delay: 500 });
	await page.keyboard.press("Enter");
	await page.waitForNavigation();

	// Login 2st part
	await delay(3000);
	await page.keyboard.type(bot_pass, { delay: 500 });
	await page.keyboard.press("Enter");
	await page.waitForNavigation();

	return;
}

// Navigate
const browser = async (url) => {
	const browser = await puppeteer.launch({
		ignoreHTTPSErrors: true,
		headless: "new",
		args: ["--no-sandbox", "--ignore-certificate-errors"],
		executablePath: "/usr/bin/chromium-browser"
	});

	console.log(`[LOG] Starting bot with ${url}...`)
	const page = await browser.newPage();
	page.on("dialog", async dialog => {
        await dialog.dismiss();
    });

	/* ** Login to Google ** */
	await google_login(page);

	/* ** Go to provided URL ** */
	console.log("[LOG] Accessing exploit page...");
	try {
	    await page.goto(url);
	} catch {}

	console.log("[LOG] Wait 10s...");
    await delay(10000);

	console.log("[LOG] Leaving...");
    browser.close();
	return;
}

// Main
const main = async () => {
	console.log("[QUESTION] Which URL do you want to send to the victim?");
	const url = await rlSync();
    await browser(url);
}

main()