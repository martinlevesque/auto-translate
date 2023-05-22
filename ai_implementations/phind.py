import copy
import re
import json
from tenacity import retry, stop_after_attempt
from playwright.sync_api import sync_playwright
from translating_formats.constants import TERMS_SEPARATOR

CHUNK_SIZE_LIMIT = 500


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
        page.goto("https://www.phind.com/")
        page.set_default_timeout(60 * 2 * 1000)
        page.get_by_role(
            "checkbox", name="Use Best Model (slow)"
        ).click()  # TERMS_SEPARATOR
        input_query = f"""translate the following text into {target_language}. only provide a single code block containing the translations separated by {TERMS_SEPARATOR} with no other text. Again just one code block with the translations only:
{chunk['content']}"""
        page.get_by_placeholder("Ask anything. Supports code blocks and urls.").fill(
            input_query
        )
        page.get_by_role("button", name="Search").click()
        page.wait_for_selector(".fe-thumbs-up")
        page.wait_for_selector(".fe-refresh-cw")
        tmp_current_chunk_result = page.locator("pre").text_content()

        result_lines = [
            l.strip()
            for l in tmp_current_chunk_result.split(TERMS_SEPARATOR)
            if l.strip() != ""
        ]

        browser.close()

    return result_lines


def translate(chunks, translating_format="yml", target_language=None):
    resulting_chunks = []

    for chunk in chunks:
        resolved_lines = resolve_chunk(chunk, target_language=target_language)
        translated_chunk = copy.deepcopy(chunk)
        translated_chunk["resolved_lines"] = resolved_lines
        resulting_chunks.append(translated_chunk)

    return resulting_chunks
