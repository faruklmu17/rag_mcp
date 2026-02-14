import { test } from '@playwright/test';
import fs from 'fs';
import path from 'path';

test('Snapshot accessibility tree for MCP', async ({ page }) => {
  await page.goto('http://127.0.0.1:5500/index.html');
  const snapshot = await page.accessibility.snapshot();
  const outputPath = path.join('snapshots', 'ui_snapshot.json');

  fs.mkdirSync('snapshots', { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(snapshot, null, 2));

  console.log(`✅ Saved accessibility snapshot to ${outputPath}`);
});
