import re
import sys
import json
from tenacity import retry, stop_after_attempt
from playwright.sync_api import sync_playwright
from translating_formats.constants import TERMS_SEPARATOR
from implementations.base import Base

CHUNK_SIZE_LIMIT = 1000


def wait_for_result(page):
    page.wait_for_selector(".fe-thumbs-up")
    page.wait_for_selector(".fe-refresh-cw")


class Phind(Base):

    def translate(self, chunks):
        resulting_chunks = []

        for chunk in chunks:
            resolved_lines = self.resolve_chunk(chunk)
            translated_chunk = chunk
            translated_chunk["resolved_lines"] = resolved_lines
            resulting_chunks.append(translated_chunk)

        return resulting_chunks

    @staticmethod
    def extract_begin_whitespace(line):
        pattern = r"^[\s]+"

        match = re.match(pattern, line)

        if match:
            return match.group()

        return ""

    @retry(stop=stop_after_attempt(3))
    def resolve_chunk(self, chunk):
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
            ).click()
            input_query = (
                f"translate the following text into {self.target_language}. Only provide a single code block containing "
                f"the translations separated by {TERMS_SEPARATOR} with no other text:\n"
                f"{chunk['content']}"
            )
            page.get_by_placeholder("Ask anything. Supports code blocks and urls.").fill(
                input_query
            )
            page.get_by_role("button", name="Search").click()
            wait_for_result(page)

            content_looks_complete = False
            max_attempts = 10

            while not content_looks_complete and max_attempts > 0:
                locator = page.locator('pre')

                tag_exists = locator.is_visible()

                if not tag_exists:
                    page.get_by_placeholder("Ask a followup question").fill(
                        'you forgot to format it as a code block'
                    )
                    page.keyboard.press("Enter")

                max_attempts -= 1

            tmp_current_chunk_result = page.locator("pre").text_content()

            result_lines = [
                l.strip()
                for l in tmp_current_chunk_result.split(TERMS_SEPARATOR)
                if l.strip() != ""
            ]

            if len(result_lines) != len(chunk["lines"]):
                print(
                    f"ERROR: lines mismatch in translated chunk: {json.dumps(chunk, indent=4)}"
                    f"\n\nInput query: {input_query}"
                    f"\n\nReturned result: {tmp_current_chunk_result}"
                    f"\nResult lines: {json.dumps(result_lines, indent=4)}"
                    f"\nChunk lines: {json.dumps(chunk['lines'], indent=4)}",
                    file=sys.stderr,
                )

                raise Exception(
                    f"Number of lines in result ({len(result_lines)}) does not match number "
                    f"of lines in chunk ({len(chunk['lines'])})"
                )

            browser.close()

        return result_lines

Klass = Phind