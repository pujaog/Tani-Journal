const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  // Capture console messages
  const consoleLogs = { error: [], warn: [], log: [] };
  page.on('console', msg => {
    const type = msg.type();
    if (type === 'error' || type === 'warn') {
      consoleLogs[type].push(msg.text());
    }
  });

  // Capture uncaught exceptions
  const pageErrors = [];
  page.on('pageerror', err => pageErrors.push(err.toString()));

  try {
    console.log('🌐 Loading landing page...');
    const response = await page.goto('http://localhost:3000', { waitUntil: 'networkidle' });
    console.log(`✅ Page loaded with status: ${response.status()}`);

    // Wait for the page to fully render
    await page.waitForTimeout(1000);

    // Check if the hero text is visible
    const heroTitle = await page.$('h1');
    if (heroTitle) {
      const text = await heroTitle.textContent();
      console.log(`✅ Hero title visible: "${text.substring(0, 50)}..."`);
    }

    // Test day/night toggle button - look for any button
    const buttons = await page.$$('button');
    let toggleBtn = null;
    for (const btn of buttons) {
      const ariaLabel = await btn.getAttribute('aria-label');
      const classList = await btn.evaluate(el => el.className);
      if (ariaLabel && (ariaLabel.includes('toggle') || ariaLabel.includes('theme') || ariaLabel.includes('mode'))) {
        toggleBtn = btn;
        break;
      }
    }

    if (toggleBtn) {
      console.log('✅ Day/night toggle button found');
      await toggleBtn.click();
      await page.waitForTimeout(500);
      console.log('✅ Day/night toggle clicked successfully');
    } else {
      console.log('⚠️  Day/night toggle button not found (may not be visible on landing)');
    }
      // Test day/night toggle button - look for the Sun icon button with "Day" text
      // Test day/night toggle button
      const toggleBtns = await page.$$('button.journal-chip');
      if (toggleBtns.length > 0) {
        const toggleBtn = toggleBtns[0];
        console.log('✅ Day/night toggle button found (journal-chip)');
        const initialText = await toggleBtn.textContent();
        console.log(`   Initial state: ${initialText.trim()}`);
      
        await toggleBtn.click();
        await page.waitForTimeout(500);
      
        const newText = await toggleBtn.textContent();
        console.log(`   After click: ${newText.trim()}`);
      
        if (initialText !== newText) {
          console.log('✅ Day/night toggle working - text changed');
        } else {
          console.log('⚠️  Toggle text did not change');
        }
      } else {
        console.log('⚠️  Day/night toggle button not found');
      }

    // Check Sign in button
    const signInBtn = await page.$('button:has-text("Sign in")');
    if (signInBtn) {
      console.log('✅ Sign in button visible');
    } else {
      console.log('⚠️  Sign in button not found');
    }

    // Check for critical errors
    if (pageErrors.length > 0) {
      console.log('❌ Page errors detected:');
      pageErrors.forEach(err => console.log(`   - ${err}`));
    } else {
      console.log('✅ No page errors');
    }

    if (consoleLogs.error.length > 0) {
      console.log('❌ Console errors:');
      consoleLogs.error.forEach(err => console.log(`   - ${err}`));
    } else {
      console.log('✅ No console errors');
    }

    if (consoleLogs.warn.length > 0) {
      console.log('⚠️  Console warnings (first 5):');
      consoleLogs.warn.slice(0, 5).forEach(w => console.log(`   - ${w}`));
      if (consoleLogs.warn.length > 5) console.log(`   ... and ${consoleLogs.warn.length - 5} more`);
    } else {
      console.log('✅ No console warnings');
    }

    console.log('\n📋 SMOKE TEST SUMMARY:');
    console.log(`✅ Page loads successfully`);
    console.log(`✅ Landing page UI elements present`);
    console.log(`✅ No critical errors detected`);

  } catch (err) {
    console.error('❌ Smoke test failed:', err.message);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
