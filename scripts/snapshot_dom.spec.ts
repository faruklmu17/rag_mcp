import { test } from '@playwright/test';
import fs from 'fs';
import path from 'path';

test('Snapshot DOM HTML for MCP QA', async ({ page }) => {
  await page.goto('http://127.0.0.1:5500/index.html');

  const domHtml = await page.content(); // grab rendered HTML
  const outputPath = path.join('snapshots', 'ui_snapshot.html');

  fs.mkdirSync('snapshots', { recursive: true });
  fs.writeFileSync(outputPath, domHtml);

  console.log(`✅ Saved DOM snapshot to ${outputPath}`);
});
