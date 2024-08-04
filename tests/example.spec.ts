import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
  await page.goto('https://meet.google.com/eai-pgsj-wdj');
w
  // Expect a title "to contain" a substring.
  await expect(page).toHaveTitle(/Playwright/);
});
