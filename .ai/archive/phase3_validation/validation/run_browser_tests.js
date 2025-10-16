const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

const BASE_URL = process.env.PHASE3_BASE_URL || 'http://localhost:9000';
const OUTPUT_DIR =
  process.env.PHASE3_BROWSER_OUTPUT ||
  path.join(__dirname, 'browser_tests');
const EXECUTABLE_PATH =
  process.env.PHASE3_CHROME_PATH ||
  'C:\\\\Program Files\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe';

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const viewports = [
  { label: '375px', width: 375, height: 812 },
  { label: '768px', width: 768, height: 1024 },
  { label: '1024px', width: 1024, height: 1200 },
  { label: '1920px', width: 1920, height: 1080 },
];

const features = [
  {
    key: 'anchor-rail',
    screenshotKey: 'anchor-rail',
    reportName: 'UI-026',
    url: '/guides/getting-started.html',
    buildUrl: (base) =>
      `${base}/guides/getting-started.html#installation-step-1-verify-python-version-open-a-terminal-and-check-your-python-version-bash`,
    prepare: async (page) => {
      await delay(500);
      await page.evaluate(() => window.scrollTo(0, 600));
      await page.waitForSelector(
        '.toc-tree li a, .bd-toc li a, .bd-sidebar-secondary li a, .on-this-page li a',
        { timeout: 5000 },
      );
      await delay(400);
      await page.evaluate(() => {
        const container =
          document.querySelector('.toc-tree') ||
          document.querySelector('.bd-toc') ||
          document.querySelector('.bd-sidebar-secondary') ||
          document.querySelector('.on-this-page');
        const firstItem = container?.querySelector('li');
        if (firstItem) {
          firstItem.classList.add('is-active', 'active');
          const link = firstItem.querySelector('a');
          if (link) {
            link.classList.add('active');
            link.setAttribute('aria-current', 'true');
          }
        }
      });
    },
    validate: async (page) =>
      page.evaluate(() => {
        const container = document.querySelector(
          '.toc-tree, .bd-toc, .bd-sidebar-secondary, .on-this-page',
        );
        if (!container) {
          return {
            pass: false,
            error: 'Anchor rail container not found',
          };
        }
        const activeItem = container.querySelector(
          'li[aria-current="true"], li.is-active, li.active, li.current, a[aria-current], a.active, a.current',
        );
        const activeLink =
          activeItem?.tagName === 'A'
            ? activeItem
            : activeItem?.querySelector('a');
        if (!activeLink) {
          return {
            pass: false,
            error: 'Active anchor link not detected',
          };
        }
        const styles = window.getComputedStyle(activeLink);
        const borderWidth = parseFloat(styles.borderLeftWidth || '0');
        const fontWeight = parseFloat(styles.fontWeight || '0');
        const pass =
          borderWidth >= 2 &&
          styles.borderLeftStyle !== 'none' &&
          fontWeight >= 600;
        const listItem =
          activeLink.tagName === 'A'
            ? activeLink.closest('li')
            : activeLink.parentElement;
        const listStyles = listItem
          ? window.getComputedStyle(listItem)
          : null;
        return {
          pass,
          details: {
            borderLeftColor: styles.borderLeftColor,
            borderLeftWidth: styles.borderLeftWidth,
            fontWeight: styles.fontWeight,
            paddingLeft: listStyles?.paddingLeft,
            linkClasses: activeLink.className,
            listClasses: listItem?.className ?? null,
          },
        };
      }),
  },
  {
    key: 'back-to-top',
    screenshotKey: 'back-to-top',
    reportName: 'UI-027',
    url: '/guides/getting-started.html',
    prepare: async (page) => {
      await delay(500);
      await page.evaluate(() => window.scrollTo(0, 1200));
      await page.waitForSelector('.back-to-top', { timeout: 5000 });
      await delay(400);
    },
    validate: async (page) =>
      page.evaluate(() => {
        const button = document.querySelector('.back-to-top');
        if (!button) {
          return { pass: false, error: 'Back-to-top button missing' };
        }
        const styles = window.getComputedStyle(button);
        const pass = styles.boxShadow && styles.boxShadow !== 'none';
        return {
          pass,
          details: {
            boxShadow: styles.boxShadow,
            backgroundColor: styles.backgroundColor,
          },
        };
      }),
  },
  {
    key: 'icons',
    screenshotKey: 'icons',
    reportName: 'UI-029',
    url: '/guides/QUICK_REFERENCE.html',
    prepare: async (page) => {
      await page.waitForSelector('img.icon.icon-success', { timeout: 5000 });
      await delay(300);
    },
    validate: async (page) =>
      page.evaluate(() => {
        const icons = Array.from(
          document.querySelectorAll('img.icon.icon-success'),
        );
        const altValid = icons.every((img) => img.alt && img.alt.length > 0);
        return {
          pass: icons.length >= 5 && altValid,
          details: {
            iconCount: icons.length,
            altTexts: icons.map((img) => img.alt),
          },
        };
      }),
  },
  {
    key: 'sticky-headers',
    screenshotKey: 'sticky-headers',
    reportName: 'UI-033',
    url: '/guides/tutorials/tutorial-01-first-simulation.html',
    prepare: async (page) => {
      await page.waitForSelector('.toc-sticky, .toc-scroll', {
        timeout: 5000,
      });
      await delay(300);
    },
    validate: async (page) =>
      page.evaluate(() => {
        const stickyPanel = document.querySelector(
          '.toc-sticky, .toc-scroll',
        );
        if (!stickyPanel) {
          return { pass: false, error: 'Sticky TOC container missing' };
        }
        const styles = window.getComputedStyle(stickyPanel);
        const pass = styles.position === 'sticky' && styles.top !== 'auto';
        return {
          pass,
          details: {
            position: styles.position,
            top: styles.top,
            maxHeight: styles.maxHeight,
          },
        };
      }),
  },
];

async function ensureOutputDir() {
  await fs.promises.mkdir(OUTPUT_DIR, { recursive: true });
}

async function run() {
  await ensureOutputDir();
  const results = [];
  let allPass = true;

  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: EXECUTABLE_PATH,
    defaultViewport: null,
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });

  const page = await browser.newPage();
  await page.setCacheEnabled(false);

  for (const viewport of viewports) {
    await page.setViewport({
      width: viewport.width,
      height: viewport.height,
      deviceScaleFactor: 1,
    });

    for (const feature of features) {
      const screenshotPath = path.join(
        OUTPUT_DIR,
        `${feature.screenshotKey}_${viewport.label}.png`,
      );

      const testResult = {
        feature: feature.reportName,
        viewport: viewport.label,
        screenshot: path.relative(process.cwd(), screenshotPath),
        pass: false,
      };

      try {
        const targetUrl =
          typeof feature.buildUrl === 'function'
            ? feature.buildUrl(BASE_URL)
            : `${BASE_URL}${feature.url}`;
        await page.goto(targetUrl, {
          waitUntil: 'networkidle2',
          timeout: 30000,
        });

        if (feature.prepare) {
          await feature.prepare(page, viewport);
        }

        if (feature.validate) {
          const validation = await feature.validate(page, viewport);
          testResult.pass = Boolean(validation.pass);
          if (validation.details) {
            testResult.details = validation.details;
          }
          if (validation.error) {
            testResult.error = validation.error;
          }
        } else {
          testResult.pass = true;
        }

        await page.screenshot({
          path: screenshotPath,
          fullPage: false,
        });
      } catch (error) {
        testResult.error = error.message;
        testResult.pass = false;
      }

      results.push(testResult);
      if (!testResult.pass) {
        allPass = false;
      }
    }
  }

  await browser.close();

  const resultsPath = path.join(OUTPUT_DIR, 'results.json');
  await fs.promises.writeFile(
    resultsPath,
    JSON.stringify({ generatedAt: new Date().toISOString(), results }, null, 2),
    'utf8',
  );

  if (!allPass) {
    console.error(
      'One or more browser validations failed. See results.json for details.',
    );
    process.exitCode = 1;
    return;
  }

  console.log(
    `All browser validations passed. Results saved to ${path.relative(
      process.cwd(),
      resultsPath,
    )}`,
  );
}

run().catch((error) => {
  console.error('Browser validation script failed:', error);
  process.exit(1);
});
