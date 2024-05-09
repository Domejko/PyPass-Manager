import webbrowser
import os
from typing import Union, List

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By

from src.tools import check_os


browser_name = webbrowser.get(using=None).name

PROXY_HOST = "12.12.12.123"
PROXY_PORT = "1234"


class Browser:
    browser_type = None
    
    def __init__(self, browser_type: str):
        self.browser_type = browser_type
        self.driver = None

    def chrome(self):
        from selenium.webdriver.chrome.service import Service as ChromeService
        from webdriver_manager.chrome import ChromeDriverManager

        options = webdriver.ChromeOptions()
        options = self.setup_driver(options)
        options.add_experimental_option('detach', True)

        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    def firefox(self):
        from selenium.webdriver.firefox.service import Service as FirefoxService

        if check_os() == 'Windows':
            from webdriver_manager.firefox import GeckoDriverManager
            from selenium.webdriver.firefox.options import Options

            options = Options()
            profile = webdriver.FirefoxProfile()
            profile = self.setup_driver(profile=profile)
            options.profile = profile
            desired = webdriver.DesiredCapabilities.FIREFOX

            self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        else:
            install_dir = "/snap/firefox/current/usr/lib/firefox"
            driver_loc = os.path.join(install_dir, "geckodriver")
            binary_loc = os.path.join(install_dir, "firefox")

            service = FirefoxService(driver_loc)
            options = webdriver.FirefoxOptions()

            options.binary_location = binary_loc
            firefox_capabilities = DesiredCapabilities.FIREFOX
            firefox_capabilities['marionette'] = True

            self.driver = webdriver.Firefox(service=service, options=options)

    def opera(self):
        from selenium.webdriver.chrome import service
        from webdriver_manager.opera import OperaDriverManager

        webdriver_service = service.Service(OperaDriverManager().install())
        webdriver_service.start()

        options = webdriver.ChromeOptions()
        options.add_experimental_option('w3c', True)
        options = self.setup_driver(options)

        self.driver = webdriver.Remote(webdriver_service.service_url, options=options)

    def chromium(self):
        from selenium.webdriver.chrome.service import Service as ChromiumService
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.core.os_manager import ChromeType

        options = webdriver.ChromeOptions()
        options = self.setup_driver(options)

        self.driver = webdriver.Chrome(
            service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)

    def edge(self):
        from selenium.webdriver.edge.service import Service as EdgeService
        from webdriver_manager.microsoft import EdgeChromiumDriverManager

        options = webdriver.EdgeOptions()
        options = self.setup_driver(options)

        self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

    def get_webdriver(self):
        if self.browser_type == 'chrome' or self.browser_type == 'google-chrome':
            self.chrome()
        elif self.browser_type == 'firefox' or self.browser_type == 'mozilla':
            self.firefox()
        elif self.browser_type == 'opera':
            self.opera()
        elif self.browser_type == 'chromium' or self.browser_type == 'chromium-browser':
            self.chromium()
        elif self.browser_type == 'windows-default':
            self.edge()

    def setup_driver(self, options):
        if self.browser_type != 'firefox':
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

            return options
        else:
            options.set_preference("network.proxy.type", 1)
            options.set_preference("network.proxy.http", PROXY_HOST)
            options.set_preference("network.proxy.http_port", PROXY_PORT)

            options.set_preference("webdriver_enable_native_events", False)
            options.set_preference("webdriver_accept_untrusted_certs", True)
            options.set_preference("webdriver_assume_untrusted_issuer", True)
            options.set_preference("dom.webdriver.enabled", False)
            options.add_argument("--disable-blink-features=AutomationControlled")

            return options

    def open_page(self, url: str):
        self.get_webdriver()
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.get(url)

    def add_credentials(self, by: By, value: str, text: str):
        pass


browser = Browser(browser_name)
browser.open_page("https://nowsecure.nl/")
