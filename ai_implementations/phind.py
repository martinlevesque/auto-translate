import re
from tenacity import retry, stop_after_attempt
from playwright.sync_api import sync_playwright

CHUNK_SIZE_LIMIT = 500


def extract_begin_whitespace(line):
    pattern = r'^[\s]+'

    match = re.match(pattern, line)

    if match:
        return match.group()

    return ""


@retry(stop=stop_after_attempt(3))
def resolve_chunk(chunk):
    current_chunk_result = ""

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        context = browser.new_context(
            extra_http_headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"
            }
        )
        page = context.new_page()
        page.goto('https://www.phind.com/')
        page.set_default_timeout(60 * 2 * 1000)
        page.get_by_role('checkbox', name="Use Best Model (slow)").click()
        input_query = f'''translate the following yml to french with no explanation, and make sure to not translate the variable names, but only the values, also only provide one code snippet:
    {chunk['content']}'''
        page.get_by_placeholder('Ask anything. Supports code blocks and urls.').fill(input_query)
        page.get_by_role("button", name="Search").click()
        page.wait_for_selector('.fe-thumbs-up')
        page.wait_for_selector('.fe-refresh-cw')
        tmp_current_chunk_result = page.locator(".language-yaml").text_content()

        index_line = 0

        for line in tmp_current_chunk_result.splitlines():
            if len(chunk['lines']) <= index_line:
                break

            original_line = chunk['lines'][index_line]

            cleaned_line = extract_begin_whitespace(original_line) + line.strip()
            current_chunk_result += cleaned_line + "\n"

            index_line += 1

        browser.close()

    return current_chunk_result

def translate(chunks, translating_format="yml", target_language=None):
    for chunk in chunks:
        current_resolved_chunk = resolve_chunk(chunk)
        print(current_resolved_chunk.rstrip())
