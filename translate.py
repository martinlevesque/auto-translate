#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)
    context = browser.new_context(
        extra_http_headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"
        }
    )
    page = browser.new_page()
    page.goto('https://www.phind.com/')
    page.get_by_role('checkbox', name="Use Best Model (slow)").click()
    input_query = '''Please translate the following yml to french, and make sure to not translate the variable names, but only the values:en:
  views:
    test: "Hello world"
    test2: "What is that?"
    more:
      deep: 23'''
    page.get_by_placeholder('Ask anything. Supports code blocks and urls.').fill(input_query)
    page.get_by_role("button", name="Search").click()
    time.sleep(30)
    contentt = page.locator(".language-yaml").text_content()
    print(f"content = {contentt}")
    browser.close()
