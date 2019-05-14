from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.test import LiveServerTestCase
import time


class TestLaunchRegistrationLoginPost(LiveServerTestCase):
    
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--disable-gpu')

        self.browser = webdriver.Chrome(options=chrome_options)
        # self.browser.set_window_size(1366, 768)
        # self.browser.maximize_window()

    def tearDown(self):
        self.browser.quit()
    
    def test_register(self):
        self.browser.get(self.live_server_url)
        register = self.browser.find_element_by_link_text('Register')
        register.click()
        time.sleep(1)

        first_name = self.browser.find_element_by_id('id_first_name')
        first_name.send_keys('Selenium')

        last_name = self.browser.find_element_by_id('id_last_name')
        last_name.send_keys('Automaton')

        email = self.browser.find_element_by_id('id_email')
        email.send_keys('automaton@g.com')

        username = self.browser.find_element_by_id('id_username')
        username.send_keys('selenium')

        password1 = self.browser.find_element_by_id('id_password1')
        password1.send_keys('$EGmysecr]\[9eet_code')

        password2 = self.browser.find_element_by_id('id_password2')
        password2.send_keys('$EGmysecr]\[9eet_code')

        signup = self.browser.find_element_by_id('signup')
        signup.click()
        time.sleep(1)

        # login
        login = self.browser.find_element_by_link_text('Login')
        login.click()
        time.sleep(1)

        username = self.browser.find_element_by_id('id_username')
        username.send_keys('selenium')

        password = self.browser.find_element_by_id('id_password')
        password.send_keys('$EGmysecr]\[9eet_code')
        
        login_btn = self.browser.find_element_by_id('login_login')
        login_btn.click()
        time.sleep(1)

        # checking the app name on the page
        # app_name = self.browser.find_element_by_id('app-name').text
        # self.assertIn('Bloggable', app_name)
        # time.sleep(2)

        # post something
        # post_link = self.browser.find_element_by_id('link_post')
        post_link = self.browser.find_element_by_link_text('Post')
        # print(post_link.get_attribute('href'))
        # print(post_link.is_displayed())
        post_link.click()
        time.sleep(1)

        post_title = self.browser.find_element_by_id('id_title')
        post_title.send_keys('Test automation with Selenium')
        time.sleep(1)

        # post_content = self.browser.find_element_by_tag_name('textarea')
        # post_content = self.browser.find_element_by_id('id_content').click()
        content = self.browser.find_element_by_id('id_content_ifr')
        self.browser.switch_to.frame(content)
        editor_body = self.browser.find_element_by_tag_name('body')
        editor_body.send_keys("Selenium automation testing: tinymce")
        # self.browser.execute_script("tinyMCE.activeEditor.setContent(Selenium automation tinymce)")
        # post_content.send_keys('Test driven development with SELENIUM')
        self.browser.switch_to.default_content()

        post_tags = self.browser.find_element_by_name('tags')
        post_tags.send_keys('Test, Selenium, Python')

        post_button = self.browser.find_element_by_id('btn_publish')
        post_button.submit()
        time.sleep(3)