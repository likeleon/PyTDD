from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox();
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 사이트 접속
        self.browser.get(self.live_server_url)

        # 웹 페이지 타이틀과 헤더와 'To-Do'를 표시하고 있다
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # 바로 작업을 추가한다
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # "히오스 하기"라고 텍스트 상자에 입력
        inputbox.send_keys('히오스 하기')

        # 엔터키를 치면 페이지가 갱신되고 작업 모록에 아이템이 추가
        inputbox.send_keys(Keys.ENTER)
        likeleon_list_url = self.browser.current_url
        self.assertRegex(likeleon_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: 히오스 하기')

        # 다시 추가
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('히오스에서 1승 하기')
        inputbox.send_keys(Keys.ENTER)

        # 페이지는 갱신되고, 두 개 아이템이 목록에 보인다
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.check_for_row_in_list_table('2: 히오스에서 1승 하기')
        self.check_for_row_in_list_table('1: 히오스 하기')

        # 새로운 사용자인 astro가 사이트에 접속한다

        # 새로운 브라우저 세션을 이용해서 쿠키를 격리한다
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # astro가 접속한다. likeleon의 리스트는 보이지 않는다
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('히오스 하기', page_text)
        self.assertNotIn('히오스에서 1승 하기', page_text)

        # astro가 새로운 작업 아이템을 입력한다
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('사진 찍기')
        inputbox.send_keys(Keys.ENTER)

        # astro가 전용 URL을 얻는다
        astro_list_url = self.browser.current_url
        self.assertRegex(astro_list_url, '/lists/.+')
        self.assertNotEqual(astro_list_url, likeleon_list_url)

        # likeleon이 입력한 흔적이 없음을 다시 확인
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('히오스 하기', page_text)
        self.assertIn('사진 찍기', page_text)

    def test_layout_and_styling(self):
        # 메인 페이지 방문
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # 입력 상자가 가운데 배치되어 있다
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # 새로운 리스트를 시작하고 입력 상자가 가운데 배치된 것을 확인
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )