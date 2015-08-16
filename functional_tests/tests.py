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

        self.fail('Finish the test!')