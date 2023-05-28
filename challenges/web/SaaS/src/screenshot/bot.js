// required packages
const puppeteer = require("puppeteer");

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
		executablePath: "/usr/bin/chromium-browser"
	});

	const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 720 });
	await page.setDefaultNavigationTimeout(5000);

	try {
	    await page.goto(url);
	} catch {}

    const img = await page.screenshot();
    console.log(img.toString("base64"))

    browser.close();
	return;
}


if (process.argv.length === 2) {
    console.error("No URL provided!");
    process.exit(1);
}

goto(process.argv[2]);
