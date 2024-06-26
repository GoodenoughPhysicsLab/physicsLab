from base import *
from typing import Optional

def is_success(res: Optional[dict]) -> bool:
    if res is None:
        return False

    if res["Message"] != "":
        return False
    return True

class WebTest(PLTestBase):
    def test_get_start_page(self):
        self.assertTrue(is_success(get_start_page()))

    def test_login(self):
        user = User()
        self.assertTrue(is_success(user.get_library()))
        self.assertTrue(is_success(user.query_experiment()))