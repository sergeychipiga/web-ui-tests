"""
--------------------
Application fixtures
--------------------
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

import pytest

from ui_tests import app as _app
from ui_tests import config

__all__ = [
    'app',
]


@pytest.yield_fixture
def app(request):
    """Function fixture to start web application."""
    app = _app.Application(config.APP_URL, request.config.option.browser)

    yield app

    app.quit()
