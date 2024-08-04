import { chromium } from 'playwright-extra';
import StealthPlugin from 'puppeteer-extra-plugin-stealth';
import path from 'path';
import { JoinGoogleMeetParams } from './types';

const stealthPlugin = StealthPlugin();
stealthPlugin.enabledEvasions.delete('iframe.contentWindow');
stealthPlugin.enabledEvasions.delete('media.codecs');
chromium.use(stealthPlugin);

export async function joinGoogleMeet({ url, fullName, message }: JoinGoogleMeetParams) {
  const videoPath = path.resolve(__dirname, '../assets/videos/standup.y4m');

  console.log('Launching browser...');
  const browser = await chromium.launch({
    headless: false,
    args: [
      '--use-fake-device-for-media-stream',
      `--use-file-for-fake-video-capture=${videoPath}`
    ]
  });

  const context = await browser.newContext({
    permissions: ['camera', 'microphone'],
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    viewport: { width: 1280, height: 720 }
  });

  const page = await context.newPage();

  console.log('Navigating to Google Meet URL...');
  await page.goto(url, { waitUntil: 'networkidle' });

  console.log('Waiting for the input field to be visible...');
  await page.waitForSelector('input[type="text"][aria-label="Your name"]');
  
  console.log('Waiting for 10 seconds...');
  await page.waitForTimeout(10000);

  console.log('Filling the input field with the name...');
  await page.fill('input[type="text"][aria-label="Your name"]', fullName);

  console.log('Waiting for the "Ask to join" button...');
  await page.waitForSelector('//button[.//span[text()="Ask to join"]]', { timeout: 60000 });

  console.log('Clicking the "Ask to join" button...');
  await page.click('//button[.//span[text()="Ask to join"]]');

  console.log('Waiting for the "Chat with everyone" button...');
  await page.waitForSelector('button[aria-label="Chat with everyone"]', { timeout: 60000 });

  console.log('Clicking the "Chat with everyone" button...');
  await page.click('button[aria-label="Chat with everyone"]');

  console.log('Waiting for 5 seconds...');
  await page.waitForTimeout(5000);

  console.log('Waiting for the "Send a message" textarea to be visible...');
  await page.waitForSelector('textarea[aria-label="Send a message"]', { timeout: 60000 });

  console.log('Filling the "Send a message" textarea...');
  await page.fill('textarea[aria-label="Send a message"]', message);

  console.log('Waiting for the "Send a message" button to become enabled...');
  const sendMessageButtonSelector = 'button[aria-label="Send a message"]';
  await page.waitForFunction((selector) => {
    const button = document.querySelector(selector);
    return button && !button.hasAttribute('disabled');
  }, sendMessageButtonSelector);

  console.log('Clicking the "Send a message" button...');
  await page.click(sendMessageButtonSelector);

  console.log('Waiting for the message text to appear...');
  await page.waitForSelector(`//div[contains(text(), "${message}")]`, { timeout: 60000 });

  console.log('Hovering over the message container...');
  await page.hover(`//div[contains(text(), "${message}")]/ancestor::div[contains(@class, "jO4O1 chmVPb")]`);

  console.log('Waiting for the "Pin message" button...');
  const pinMessageButtonSelector = '//button[@aria-label="Pin message"]';
  await page.waitForSelector(pinMessageButtonSelector, { timeout: 60000 });

  console.log('Clicking the "Pin message" button...');
  await page.click(pinMessageButtonSelector);

  console.log('Waiting for the "Pin this message" confirmation button...');
  await page.waitForSelector('//button[.//span[text()="Pin this message"]]', { timeout: 60000 });

  console.log('Clicking the "Pin this message" confirmation button...');
  await page.click('//button[.//span[text()="Pin this message"]]');

  console.log('Waiting for an hour...');
  await page.waitForTimeout(3600000);

  console.log('Closing the browser...');
  await browser.close();
  
  console.log('All done, check the screenshot. ✨');
}
