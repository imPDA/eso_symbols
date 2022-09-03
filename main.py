import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from utf8_iterator import utf8_iterator


class Checker:
    def __init__(self):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.allowed_characters = []

    def char_is_allowed(self):
        checkmark = self.browser.find_element(By.XPATH, '//*[@id="id_random_characters"]/i')
        return bool('fa_ok' in checkmark.get_attribute('class'))

    def start(self):
        self.open_page('https://account.elderscrollsonline.com/register/account-information')
        element_input_field = self.browser.find_element(By.XPATH, '//*[@id="user_screen_name"]')

        j = 0
        last_printout = ''
        for i, char in enumerate(utf8_iterator()):
            # We are not interested in these characters:
            # < 32 - special characters
            # 39 - "'"
            # 45 - "-"
            # 46 - "."
            # 48-122 - "0-9, A-Z, a-z
            # 127 - special character

            if i < 128:
                continue

            element_input_field.clear()
            element_input_field.send_keys('Test')

            element_input_field.send_keys(char, 'end')

            last_printout = f'{char} {i}\t'
            print(last_printout, end='')

            time.sleep(0.33)

            if self.char_is_allowed():
                j += 1
                if j >= 10:
                    print()
                    j = 0
                self.allowed_characters.append(char)
            else:
                print('\010' * len(last_printout), end='')

        self.stop()

    def enter_date(self):
        field_year = self.browser.find_element(By.XPATH, '//*[@id="date_year"]')
        field_month = self.browser.find_element(By.XPATH, '//*[@id="date_month"]')
        field_day = self.browser.find_element(By.XPATH, '//*[@id="date_day"]')

        field_year.send_keys('1997')
        # TODO: english support
        field_month.send_keys('апреля')
        field_day.send_keys('3')

        button_send = self.browser.find_element(By.XPATH, '//*[@id="age-gate"]/form/div[2]/input')
        button_send.submit()

    def open_page(self, address: str):
        self.browser.get(address)

        # if enter your date of birth presented
        # TODO: english support
        if 'ВВЕДИТЕ ДАТУ РОЖДЕНИЯ' in self.browser.page_source:
            self.enter_date()

    def stop(self):
        try:
            self.browser.close()
        except:  # Silence all exception because we can
            pass
        self.print_all_allowed_characters()

    def print_all_allowed_characters(self):
        print('Valid characters are: ')
        for i, character in enumerate(self.allowed_characters):
            if i and i % 10 == 0:
                print()
            print(character, end='\t')

    def __del__(self):
        self.stop()


if __name__ == '__main__':
    instance = Checker()
    try:
        instance.start()
    except KeyboardInterrupt:
        print('\nInterrupted, wait...')
    except WebDriverException:
        print('\nProbably, browser was closed')
    finally:
        instance = None
