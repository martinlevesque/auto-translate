import re
import sys
import time
from tenacity import retry, stop_after_attempt
from playwright.sync_api import sync_playwright
from translating_formats.constants import TERMS_SEPARATOR

CHUNK_SIZE_LIMIT = 1000


def extract_begin_whitespace(line):
    pattern = r"^[\s]+"

    match = re.match(pattern, line)

    if match:
        return match.group()

    return ""


@retry(stop=stop_after_attempt(3))
def resolve_chunk(chunk, target_language=None):
    result_lines = []

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        context = browser.new_context(
            extra_http_headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"
            }
        )
        page = context.new_page()
        page.goto("https://www.deepl.com/translator")
        page.get_by_role(
            "button", name="Detect language"
        ).click()
        page.get_by_placeholder("Search languages").fill('English')
        page.get_by_role(
            "button", name="English"
        ).click()

        time.sleep(10)

        browser.close()

    return result_lines


def translate(chunks, target_language=None):
    resulting_chunks = []

    for chunk in chunks:
        resolved_lines = resolve_chunk(chunk, target_language=target_language)
        translated_chunk = chunk
        translated_chunk["resolved_lines"] = resolved_lines
        resulting_chunks.append(translated_chunk)

    return resulting_chunks
