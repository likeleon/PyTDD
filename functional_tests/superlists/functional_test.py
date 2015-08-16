﻿from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox();
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 사이트 접속
        self.browser.get('http://localhost:8000')

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

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: 히오스 하기', [row.text for row in rows])

        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')