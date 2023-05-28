// required packages
const puppeteer = require("puppeteer");

// variables
const host = "127.0.0.1:5000";

// sleep
const delay = (time) => {
    return new Promise(resolve => setTimeout(resolve, time));
}

// navigate
async function goto(url) {
	const browser = await puppeteer.launch({
		headless: true,
		ignoreHTTPSErrors: true,
		args: ["--no-sandbox", "--ignore-certificate-errors" ],
		executablePath: "/usr/bin/chromium"
	});

	const page = await browser.newPage();
    await page.setCookie({
		"name" : "flag",
		"value" : "ECTF{T4k3_c4R3_0f_Server_S1d3_HTML_S4nitizeR_C0nteXt}",
		"domain" : host,
		"httpOnly": false
	});
	await page.setDefaultNavigationTimeout(5000);

    // Go to provided URL
	try {
	    await page.goto(url);
	} catch {}

    await delay(1000);

    browser.close();
	return;
}

if (process.argv.length === 2) {
    console.error("No URL provided!");
    process.exit(1);
}

goto(process.argv[2]);