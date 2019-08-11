import socket
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class SeleniumAdminTests(StaticLiveServerTestCase):
    live_server_url = 'http://{}:7000'.format(
        socket.gethostbyname(socket.gethostname())
    )

    def setUp(self):
        self.browser = webdriver.Remote(
            command_executor="http://selenium:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME
        )

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

    def test_index(self):
        self.browser.get("%s%s" % (self.live_server_url, '/admin/'))
        self.assertTrue(self.browser.title != '')
        self.assertEqual(self.browser.title, 'ログイン | Django サイト管理')
