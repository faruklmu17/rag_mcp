import { test, expect } from '@playwright/test';

const APP_URL = 'http://127.0.0.1:5500/index.html';

test.describe('Agile Storyboard Column Layout', () => {

  test('should have exactly 4 status columns initially', async ({ page }) => {
    await page.goto(APP_URL);

    const columns = page.locator('.column');
    await expect(columns).toHaveCount(4);

    const expectedStatuses = ['Developing', 'Under Review', 'Testing', 'Done'];
    for (const status of expectedStatuses) {
      await expect(page.locator(`.column h3:has-text("${status}")`)).toBeVisible();
    }
  });

  test('should only display the 4 known status columns', async ({ page }) => {
    await page.goto(APP_URL);
  
    const expectedStatuses = ['Developing', 'Under Review', 'Testing', 'Done'];
    const columns = await page.locator('.column h3').allTextContents();
  
    // Check that we only have the expected columns (no extras)
    expect(columns.sort()).toEqual(expectedStatuses.sort());
  });
  

});
