// src/GoogleMeetBot.ts
import { chromium } from 'playwright-extra';
import StealthPlugin from 'puppeteer-extra-plugin-stealth';
import fs from 'fs-extra';
import { JoinParams, SendChatMessageParams, AbstractMeetBot } from './AbstractMeetBot';

const stealthPlugin = StealthPlugin();
stealthPlugin.enabledEvasions.delete('iframe.contentWindow');
stealthPlugin.enabledEvasions.delete('media.codecs');
chromium.use(stealthPlugin);

export class GoogleMeetBot extends AbstractMeetBot {
  private page: any;

  async join({ url, fullName, fakeVideoPath }: JoinParams): Promise<void> {
    console.log('Launching browser...');

    const browserArgs = ['--use-fake-device-for-media-stream'];
    if (fakeVideoPath && await fs.pathExists(fakeVideoPath)) {
      browserArgs.push(`--use-file-for-fake-video-capture=${fakeVideoPath}`);
    }

    const browser = await chromium.launch({
      headless: false,
      args: browserArgs,
    });

    const context = await browser.newContext({
      permissions: ['camera', 'microphone'],
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
      viewport: { width: 1280, height: 720 }
    });

    this.page = await context.newPage();

    console.log('Navigating to Google Meet URL...');
    await this.page.goto(url, { waitUntil: 'networkidle' });

    console.log('Waiting for the input field to be visible...');
    await this.page.waitForSelector('input[type="text"][aria-label="Your name"]');
    
    console.log('Waiting for 10 seconds...');
    await this.page.waitForTimeout(10000);

    console.log('Filling the input field with the name...');
    await this.page.fill('input[type="text"][aria-label="Your name"]', fullName);

    console.log('Waiting for the "Ask to join" button...');
    await this.page.waitForSelector('//button[.//span[text()="Ask to join"]]', { timeout: 60000 });

    console.log('Clicking the "Ask to join" button...');
    await this.page.click('//button[.//span[text()="Ask to join"]]');
  }

  async sendChatMessage({ message, pin }: SendChatMessageParams): Promise<void> {
    console.log('Waiting for the "Chat with everyone" button...');
    await this.page.waitForSelector('button[aria-label="Chat with everyone"]', { timeout: 60000 });

    console.log('Clicking the "Chat with everyone" button...');
    await this.page.click('button[aria-label="Chat with everyone"]');

    console.log('Waiting for 5 seconds...');
    await this.page.waitForTimeout(5000);

    console.log('Waiting for the "Send a message" textarea to be visible...');
    await this.page.waitForSelector('textarea[aria-label="Send a message"]', { timeout: 60000 });

    console.log('Filling the "Send a message" textarea...');
    await this.page.fill('textarea[aria-label="Send a message"]', message);

    console.log('Waiting for the "Send a message" button to become enabled...');
    const sendMessageButtonSelector = 'button[aria-label="Send a message"]';
    await this.page.waitForFunction((selector: string) => {
      const button = document.querySelector(selector);
      return button && !button.hasAttribute('disabled');
    }, sendMessageButtonSelector);

    console.log('Clicking the "Send a message" button...');
    await this.page.click(sendMessageButtonSelector);

    console.log('Waiting for the message text to appear...');
    await this.page.waitForSelector(`//div[contains(text(), "${message}")]`, { timeout: 60000 });

    if (pin) {
      console.log('Hovering over the message container...');
      await this.page.hover(`//div[contains(text(), "${message}")]/ancestor::div[contains(@class, "jO4O1 chmVPb")]`);

      console.log('Waiting for the "Pin message" button...');
      const pinMessageButtonSelector = '//button[@aria-label="Pin message"]';
      await this.page.waitForSelector(pinMessageButtonSelector, { timeout: 60000 });

      console.log('Clicking the "Pin message" button...');
      await this.page.click(pinMessageButtonSelector);

      console.log('Waiting for the "Pin this message" confirmation button...');
      await this.page.waitForSelector('//button[.//span[text()="Pin this message"]]', { timeout: 60000 });

      console.log('Clicking the "Pin this message" confirmation button...');
      await this.page.click('//button[.//span[text()="Pin this message"]]');
    }

    console.log('Waiting for an hour...');
    await this.page.waitForTimeout(3600000);

    console.log('Closing the browser...');
    await this.page.context().browser().close();

    console.log('All done, check the screenshot. ✨');
  }
}
