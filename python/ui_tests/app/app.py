"""
-----------
Application
-----------
"""

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import tempfile
import urlparse

import pom
from pom import ui
from pom.base import camel2snake
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import RemoteConnection
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from ui_tests import config
from ui_tests.app import pages

__all__ = [
    'Application',
]

ui.UI.timeout = config.UI_TIMEOUT
RemoteConnection.set_timeout(config.PAGE_TIMEOUT)


@pom.register_pages(pages.pages)
class Application(pom.App):
    """Application to launch in browser."""

    def __init__(self, url, browser, *args, **kwgs):
        """Constructor."""
        profile_dir = tempfile.mkdtemp()

        if browser == 'chrome':
            webdriver_path = ChromeDriverManager().install()
            options = webdriver.ChromeOptions()
            options.add_argument("user-data-dir=" + profile_dir)
            kwgs['chrome_options'] = options

        if browser == 'firefox':
            webdriver_path = GeckoDriverManager().install()
            profile = webdriver.FirefoxProfile(profile_dir)
            kwgs['firefox_profile'] = profile

        # FIXME: POM bug workaround
        browser = 'Chrome' if browser == 'chrome' else browser

        self._url = url
        self._webdriver_path = webdriver_path
        self._browser = browser
        self._browser_args = args
        self._browser_kwgs = kwgs

        self.start()

    def start(self):
        super(Application, self).__init__(
            self._url,
            browser=self._browser,
            executable_path=self._webdriver_path,
            *self._browser_args,
            **self._browser_kwgs)

        self.webdriver.maximize_window()
        self.webdriver.set_page_load_timeout(config.PAGE_TIMEOUT)
        self.webdriver.get(self.app_url)

    @property
    def current_page(self):
        """Define current page"""
        current_path = urlparse.urlparse(self.current_url).path
        for page in self._registered_pages:
            if re.match(page.url, current_path):
                return getattr(self, camel2snake(page.__name__))
        else:
            raise Exception("Can't define current page")

    @property
    def current_url(self):
        """Get current URL."""
        return self.webdriver.current_url

    def open(self, page):
        """Open page or url.

        Args:
            page (page|str): page class or url string.
        """
        url = page if isinstance(page, (str, unicode)) else page.url
        if not url.startswith('http'):
            url = self.app_url + url
        self.webdriver.get(url)

    def flush_session(self):
        """Delete all cookies.

        It forces flushes user session by cookies deleting.
        """
        self.webdriver.delete_all_cookies()

    def restart(self):
        """Restart browser with the same profile dir."""
        self.quit()
        self.start()
