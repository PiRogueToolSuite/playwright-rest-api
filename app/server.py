import asyncio
import logging
import os
import shutil
import tempfile
from tempfile import NamedTemporaryFile
from zipfile import ZipFile
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from fastapi import FastAPI, HTTPException
from playwright.async_api import async_playwright
from pydantic import BaseModel
from starlette.responses import StreamingResponse


class URLRequest(BaseModel):
    url: str
    proxy_server: str = None
    proxy_username: str = None
    proxy_password: str = None


app = FastAPI()


def add_watermark(input_path, output_path, url):
    now = datetime.utcnow()
    input_image = Image.open(input_path)
    output_image = Image.new(input_image.mode, (input_image.width, input_image.height + 40), 'black')
    output_image.paste(input_image)
    draw = ImageDraw.Draw(output_image)
    # font = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 14)
    # draw.text((5, input_image.height + 5), f'URL: {url}', font=font, fill='white')
    # draw.text((5, input_image.height + 20), f'Captured on {now.isoformat()}', font=font, fill='white')
    draw.text((5, input_image.height + 5), f'URL: {url}')
    draw.text((5, input_image.height + 20), f'Captured on {now.isoformat()}')
    output_image.save(output_path)


async def __capture_url(url_request: URLRequest):
    proxy = None
    if url_request.proxy_server:
        proxy = {
            'server': url_request.proxy_server,
            'username': url_request.proxy_username,
            'password': url_request.proxy_password
        }
    output_dir = tempfile.mkdtemp()
    tmp_screenshot_file_path = f'{output_dir}/tmp_screenshot.png'
    screenshot_file_path = f'{output_dir}/screenshot.png'
    har_file_path = f'{output_dir}/capture.har'
    async with async_playwright() as p:
        try:
            browser = await p.firefox.launch()
            if proxy:
                context = await browser.new_context(proxy=proxy, record_har_path=har_file_path)
            else:
                context = await browser.new_context(record_har_path=har_file_path)
            page = await context.new_page()
            page.set_default_navigation_timeout(60000)  # Timeout 1 minute
            await page.goto(url_request.url)
            await asyncio.sleep(15)
            await page.screenshot(path=tmp_screenshot_file_path, full_page=True)
            await context.close()
            await browser.close()
            add_watermark(tmp_screenshot_file_path, screenshot_file_path, url_request.url)
        except Exception as e:
            logging.error(e)
            shutil.rmtree(output_dir, ignore_errors=True)
            return None
    with NamedTemporaryFile(suffix='.zip', delete=False) as output_file:
        with ZipFile(output_file, mode='w') as z:
            z.write(screenshot_file_path, arcname='screenshot.png')
            z.write(har_file_path, arcname='capture.har')
        output_file.seek(0)
        output_file.flush()
    shutil.rmtree(output_dir, ignore_errors=True)
    return output_file.name


def __get_zip_archive(output_file):
    try:
        with open(output_file, 'rb') as o:
            yield from o
    finally:
        os.unlink(output_file)


@app.post('/capture')
async def capture_url(url_request: URLRequest):
    logging.info(f'Browsing {url_request}')
    output_file = await __capture_url(url_request)
    if not output_file:
        raise HTTPException(status_code=500, detail=f'Unable to browse {url_request.url}')
    else:
        response = StreamingResponse(__get_zip_archive(output_file))
        return response
