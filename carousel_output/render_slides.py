#!/usr/bin/env python3
"""Render all slide HTML files to PNG using Playwright."""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

OUT = Path('/home/user/linkedin_post_creation/carousel_output')

async def render():
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=['--no-sandbox', '--disable-setuid-sandbox'])
        for i in range(1, 10):
            html_path = OUT / f'slide_{i:02d}.html'
            png_path = OUT / f'slide_{i:02d}.png'
            page = await browser.new_page(viewport={'width': 1080, 'height': 1350})
            await page.goto(f'file://{html_path}')
            await page.wait_for_timeout(1200)  # allow fonts to load
            await page.screenshot(path=str(png_path), full_page=False, type='png')
            await page.close()
            print(f'Rendered slide_{i:02d}.png')
        await browser.close()

asyncio.run(render())
print("All slides rendered.")
