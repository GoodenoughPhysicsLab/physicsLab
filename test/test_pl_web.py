from base import *

class WebTest(PLTestBase):
    def test_get_start_page(self):
        web.get_start_page()

    def test_login(self):
        user = web.User()
        user.get_library()
        user.query_experiments()
