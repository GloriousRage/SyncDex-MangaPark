from playwright.sync_api import sync_playwright
from urllib.parse import quote
import time

class MangaParkService:
    """
    SyncDex service plugin for MangaPark.net
    """
    NAME = "mangapark"

    def __init__(self, username: str, password: str, headless: bool = True):
        self.username = username
        self.password = password
        self.headless = headless
        self.browser = None
        self.page = None

    def login(self):
        p = sync_playwright().start()
        self.browser = p.chromium.launch(headless=self.headless)
        self.page = self.browser.new_page()

        # Navigate to login page
        self.page.goto("https://mangapark.net/login")
        self.page.fill("input[name='username']", self.username)
        self.page.fill("input[name='password']", self.password)
        self.page.click("button[type='submit']")
        self.page.wait_for_url("https://mangapark.net/")
        time.sleep(1)

    def follow_titles(self, titles: list[str]):
        if not self.page:
            self.login()

        for title in titles:
            # Search by title
            search_url = f"https://mangapark.net/search?title={quote(title)}"
            self.page.goto(search_url)

            # Click first result
            try:
                self.page.wait_for_selector(".tab-content .item .name a", timeout=5000)
                self.page.click(".tab-content .item .name a")
            except:
                print(f"Search result not found for: {title}")
                continue

            # Wait for follow button to appear
            try:
                self.page.wait_for_selector(".follow-btn", timeout=5000)
                btn = self.page.inner_text(".follow-btn")
                if btn.lower().strip() in ["follow", "❤ follow"]:
                    self.page.click(".follow-btn")
                    print(f"Followed: {title}")
                else:
                    print(f"Already following: {title}")
            except:
                print(f"Follow button missing for: {title}")

            # Throttle requests
