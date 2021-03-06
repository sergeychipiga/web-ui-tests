"""
---------
Base page
---------
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

import pom
from pom import ui
from selenium.webdriver.common.by import By

from ui_tests.app import ui as _ui

__all__ = [
    'PageBase',
]


@ui.register_ui(
    combobox_lang=_ui.ComboBox(By.NAME, "language-picker"))
class Footer(ui.Block):
    """Footer."""


@ui.register_ui(footer=Footer(By.TAG_NAME, "footer"))
class PageBase(pom.Page):
    """Base application page."""
