# Standard library
import platform
import os
import time
import itertools

# Local modules imports
from .exceptions import ElementNotFoundException
# from .driver_checker import DriverChecker

# 3rd library
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup
# from winregistry import WinRegistry as Reg


class WebControl:
    def __init__(self, url=None, profile_path=None, handless=False, browser_type='chrome', driver_path=None):
        """
            網頁控制器(based on selenium)
            :param profile_path: profile 路徑【String】
        """
        # todo 補上raise或try exception
        self.profile_path = profile_path
        self.driver_path = driver_path
        self.os = platform.system().lower()
        self.driver = None
        if browser_type == 'chrome':
            if self.driver_path:
                if not os.path.isfile(self.driver_path):
                    raise FileNotFoundError("Chrome driver is not found.")
            else:
                # 判斷存放driver的路徑是否存在
                if not os.path.exists(os.path.join(os.getenv('APPDATA'), 'III RPA', 'RPA Tool')):
                    os.makedirs(os.path.join(os.getenv('APPDATA'), 'III RPA', 'RPA Tool'))
                # 若未指定driver path，則檢查預設路徑中是否有driver
                # driver_checker = DriverChecker(browser_type)
                # # 檢查Chrome的版本
                # checker_res = driver_checker.do_check_and_download_driver()
                # if checker_res["result"]:
                #     self.driver_path = checker_res["msg"]
                #     self.__open_chrome(profile_path, self.driver_path, handless)
                #     self.window_maximize()
                #     if url is not None:
                #         self.browser_url(url)
                # else:
                #     raise ConnectionError(checker_res["err_msg"])
        else:
            # todo firefox的version判斷
            self.__open_filefox(self.driver_path, handless)

    def get_process_id(self):
        """
            取得瀏覽器的process id
            :return: process id 【String】
        """
        return self.driver.service.process.pid

    def __open_chrome(self, profile_path, driver_path, handless):
        """
            啟動瀏覽器
            :param profile_path: profile路徑 【String】
            :param driver_path: driver路徑 【String】
            :param handless: 是否啟用headless模式 【Boolean】
            :return: web driver【object】
        """

        # 取得console畫面中的log
        d = DesiredCapabilities.CHROME
        d["loggingPrefs"] = {"browser": "ALL"}

        # 設置profile
        chrome_options = Options()
        if profile_path:
            data_dir = "--user-data-dir=" + profile_path
            chrome_options.add_argument(data_dir)

        # headless mode
        if handless:
            chrome_options.add_argument('--headless')

        # 關閉自動測試軟體制的那條bar
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        if self.os != "windows":
            # 打開linux的flash
            profile = {"plugins.plugins_enabled": ["Shockwave Flash"]}
            chrome_options.add_experimental_option("prefs", profile)

        self.driver = webdriver.Chrome(executable_path=driver_path,
                                       desired_capabilities=d,
                                       chrome_options=chrome_options)
        return self.driver

    def __open_filefox(self, driver_path, handless):

        profile = webdriver.FirefoxProfile()
        profile.set_preference('intl.accept_languages', 'zh-TW')

        options = webdriver.FirefoxOptions()
        options.headless = handless
        self.driver = webdriver.Firefox(firefox_profile=profile,
                                        executable_path=driver_path,
                                        options=options)
        return self.driver

    def window_maximize(self):
        """
            將視窗最大化
            :return: None
        """
        self.driver.maximize_window()
        return None

    def browser_url(self, url):
        """
            將視窗導向某個頁面
            :param url: 要導向的URL【String】
            :return: None
        """
        self.driver.get(url)
        return None

    def get_element_tree(self):
        """
            取得頁面的Elements
            :return: 網頁的HTML Tag【String】
        """
        return self.driver.page_source

    def window_screen_shot(self, path):
        """
            將畫面截圖並存檔
            :param path: 截圖存檔路徑【String】
            :return: None
        """
        self.driver.get_screenshot_as_file(path)
        return None

    def switch_to_iframe(self, iframe_element):
        """
            將control移至iframe中
            :param iframe_element: iframe物件【object】
            :return:  None
        """
        self.driver.switch_to_frame(iframe_element)
        return None

    def switch_to_parent_frame(self, default_content=False):
        """
            移至上一層Iframe
            :param default_content: 用來判斷是否跳脫所有的iframe【Boolean】
            :return: None
        """
        if default_content:
            self.driver.switch_to.default_content()
        else:
            self.driver.switch_to.parent_frame()
        return None

    def find_element(self, target, condition, element=None, plural=False):
        """
            找尋指定Element
            :param target: 搜尋方法【String】
            :param condition: 搜尋條件【String】
            :param element: 搜尋子元件用，的母元件【Object】
            :param plural: 是否搜尋多個元件【boolean】
            :return: 搜尋結果
        """
        if plural:
            if element:
                if target == "id":
                    self.element_wait(dom_id=condition, mode="presence")
                    return element.find_elements_by_id(condition)
                elif target == "class":
                    self.element_wait(class_name=condition, mode="presence")
                    return element.find_elements_by_class_name(condition)
                elif target == "link_text":
                    return element.find_elements_by_link_text(condition)
                elif target == "partial_link":
                    return element.find_elements_by_partial_link_text(condition)
                elif target == "xpath":
                    self.element_wait(xpath=condition, mode="presence")
                    return element.find_elements_by_xpath(condition)
                elif target == "css":
                    self.element_wait(css=condition, mode="presence")
                    return element.find_elements_by_css_selector(condition)
            else:
                if target == "id":
                    return self.driver.find_element_by_id(condition)
                elif target == "class":
                    return self.driver.find_elements_by_class_name(condition)
                elif target == "link_text":
                    return self.driver.find_elements_by_link_text(condition)
                elif target == "partial_link":
                    return self.driver.find_elements_by_partial_link_text(condition)
                elif target == "xpath":
                    return self.driver.find_element_by_xpath(condition)
                elif target == "css":
                    return self.driver.find_elements_by_css_selector(condition)
        else:
            if element:
                if target == "id":
                    return element.find_element_by_id(condition)
                elif target == "class":
                    return element.find_element_by_class_name(condition)
                elif target == "link_text":
                    return element.find_element_by_link_text(condition)
                elif target == "partial_link":
                    return element.find_element_by_partial_link_text(condition)
                elif target == "xpath":
                    return element.find_element_by_xpath(condition)
                elif target == "css":
                    return element.find_element_by_css_selector(condition)
            else:
                if target == "id":
                    return self.driver.find_element_by_id(condition)
                elif target == "class":
                    return self.driver.find_element_by_class_name(condition)
                elif target == "link_text":
                    return self.driver.find_element_by_link_text(condition)
                elif target == "partial_link":
                    return self.driver.find_element_by_partial_link_text(condition)
                elif target == "xpath":
                    return self.driver.find_element_by_xpath(condition)
                elif target == "css":
                    return self.driver.find_element_by_css_selector(condition)

    def browser_pagination(self):
        """
            搜尋目前分頁物件
            :return: 搜尋結果 【list】
        """
        return self.driver.window_handles

    def switch_to_another_window(self, window):
        """
            移至分頁
            :param window: 分頁物件【Object】
            :return: None
        """
        return self.driver.switch_to.window(window)

    def create_new_tab(self):
        """
        建立新分頁
        :return:
        """
        self.driver.execute_script("window.open()")
        self.driver.switch_to_window(self.driver.window_handles[len(self.driver.window_handles) - 1])

    def mouse_click(self, model, e_id=None, e_css=None, e_xpath=None, element=None, x=None, y=None):
        """
            滑鼠的點擊
            :param model: 點擊模式【String】
            :param e_id: 要進行點擊的物件ID名稱【String】
            :param e_css: 要進行點擊的物件css名稱【String】
            :param e_xpath: 要進行點擊的物件xpath名稱【String】
            :param element: 要進行點擊的物件【object】
            :param x: 點擊的X座標【Int】
            :param y: 點擊的Y座標【Int】
            :return: None
        """
        if e_id or e_css or e_xpath:
            # 如果是填寫物件名稱的模式，則先進行搜尋
            if e_id:
                self.element_wait(dom_id=e_id, mode="clickable")
                element = self.find_element("id", e_id)
            elif e_css:
                self.element_wait(class_name=e_css, mode="clickable")
                element = self.find_element("css", e_css)
            elif e_xpath:
                self.element_wait(xpath=e_xpath, mode="clickable")
                element = self.find_element("xpath", e_xpath)
        # 進行點擊
        if not x and not y:
            if model == "left":  # 按左鍵
                element.click()
            elif model == "right":  # 按右鍵
                element.context_click()
            elif model == "double":  # 左鍵連點
                element.double_click()
        else:
            action = ActionChains(self.driver)
            if element:
                action.move_to_element_with_offset(element, x, y)
                if model == "left":  # 按左鍵
                    action.click()
                elif model == "right":  # 按右鍵
                    action.context_click()
                elif model == "double":  # 左鍵連點
                    action.double_click()
                action.perform()
            else:
                # 如果是無法找到element，單純使用座標進行點擊
                if model == "left":  # 按左鍵
                    action.move_by_offset(x, y).click().perform()
                elif model == "right":  # 按右鍵
                    action.move_by_offset(x, y).context_click().perform()
                elif model == "double":  # 左鍵連點
                    action.move_by_offset(x, y).double_click().perform()
        return None

    def mouse_move(self, e_id=None, e_css=None, e_xpath=None, element=None, x=None, y=None):
        """
            滑鼠移至
            :param e_id: 要進行移至的物件ID名稱【String】
            :param e_css: 要進行移至的物件css名稱【String】
            :param e_xpath: 要進行移至的物件xpath名稱【String】
            :param element: 要進行移至的物件【object】
            :param x: 移至的X座標【Int】
            :param y: 移至的Y座標【Int】
            :return: None
        """
        if e_id or e_css or e_xpath:
            # 如果是填寫物件名稱的模式，則先進行搜尋
            if e_id:
                element = self.find_element("id", e_id)
            elif e_css:
                element = self.find_element("css", e_css)
            elif e_xpath:
                element = self.find_element("xpath", e_xpath)
        action = ActionChains(self.driver)
        # 進行點擊
        if not x and not y:
            action.move_to_element(element).perform()
        else:
            action.move_by_offset(x, y).perform()
        return None

    @staticmethod
    def get_css_attribute(element, attribute_name):
        """
            取得元件的css樣式
            :param element: 物件【object】
            :param attribute_name: 要取得的屬性名稱【String】
            :return: element css attribute
        """
        return element.value_of_css_property(attribute_name)

    @staticmethod
    def get_element_attribute(element, attribute_name):
        """
            取得元件上的屬性
            :param element: 物件【object】
            :param attribute_name: 要取得的屬性名稱【String】
            :return: element css attribute
        """
        return element.get_attribute(attribute_name)

    @staticmethod
    def get_element_size(element):
        """
            取得元件的大小
            :param element: 物件【object】
            :return: element css attribute
        """
        return element.size

    def scroller_slip_to(self, y=None):
        """
            將scroller滑到指定高度
            :param y: Y軸高度【INT】，若沒指定則滑到最底
            :return: None
        """
        if y:
            self.do_js_script("window.scrollTo(0, " + str(y) + ");")
        else:  # 如果沒指定要滑到哪，就直接滑到最底
            last_height_js_command = "window.scrollTo(0, document.body.scrollHeight);"
            drop_command = ""
            return_scroll_height_command = ""
            if self.os == "windows":
                last_height_js_command = "return document.documentElement.scrollHeight"
                drop_command = "window.scrollTo(0, document.documentElement.scrollHeight);"
                return_scroll_height_command = "return document.documentElement.scrollHeight"
            elif self.os == "linux":
                last_height_js_command = "return document.body.scrollHeight"
                drop_command = "window.scrollTo(0, document.body.scrollHeight);"
                return_scroll_height_command = "return document.body.scrollHeight"
            last_height = self.do_js_script(last_height_js_command)
            while True:
                self.driver.execute_script(drop_command)
                time.sleep(2)
                new_height = self.do_js_script(return_scroll_height_command)
                if new_height == last_height:
                    break
                last_height = new_height
        return None

    def close_pagination(self):
        """
            關閉分頁
            :return: None
        """
        return self.driver.close()

    def get_current_url(self):
        """
            取得目前頁面的URL
            :return: 目前頁面的URL【String】
        """
        return self.driver.current_url

    def get_current_title(self):
        """
            取得目前頁面的title
            :return: 目前頁面的title【String】
        """
        return self.driver.title

    @staticmethod
    def get_element_text(element):
        """
            取得元件的的文字
            :param element:要操作的元件【Object】
            :return: 元件的文字【String】
        """
        return element.text

    def keyboard_typing(self, text, e_id=None, e_css=None, e_xpath=None, element=None, x=None, y=None, clear=False):
        """
            於元件上打字
            :param text:要打入的文字【String】
            :param e_id: 要進行輸入的物件ID名稱【String】
            :param e_css: 要進行輸入的物件css名稱【String】
            :param e_xpath: 要進行輸入的物件xpath名稱【String】
            :param element: 要進行輸入的物件【object】
            :param x: 輸入的X座標【Int】
            :param y: 輸入的Y座標【Int】
            :param clear: 輸入前是否先清除【Boolean】
            :return: None
        """
        if e_id or e_css or e_xpath:
            # 如果是填寫物件名稱的模式，則先進行搜尋
            if e_id:
                self.element_wait(dom_id=e_id, mode="presence")
                element = self.find_element("id", e_id)
            elif e_css:
                self.element_wait(css=e_css, mode="presence")
                element = self.find_element("css", e_css)
            elif e_xpath:
                self.element_wait(xpath=e_xpath, mode="presence")
                element = self.find_element("xpath", e_xpath)
        if not x and not y:
            if clear:
                element.clear()
            element.send_keys(text)
        else:
            # 先在座標上點擊一下進行focuse
            action = ActionChains(self.driver)
            action.move_by_offset(x, y).click().perform()
            action.send_keys(text).perform()
        return None

    @staticmethod
    def set_select_value(select_element, text=None, value=None, index=None):
        """
            直接操作下拉選單
            :param select_element: 搜尋到的select物件
            :param text: 要選擇的select文字
            :param value: 要選擇的select值
            :param index: 要選擇的select中的index
            :return:
        """
        select = Select(select_element)
        if text:
            select.select_by_visible_text(text)
        elif value:
            select.select_by_value(value)
        elif index:
            select.select_by_index(index)

    def element_wait(self, dom_id=None, class_name=None, xpath=None, desc=None,
                     css=None, mode='visiable', wait_time=30):
        """
        等待元件載入
        :param dom_id:
        :param class_name:
        :param xpath:
        :param css:
        :param desc: 元件的敘述, 有Error時　可以顯示這個【String】
        :param mode: 等待的模式【String】
        :param wait_time:等待時長【INT】default 30
        :return: element
        """
        wait = WebDriverWait(self.driver, wait_time)

        ec_func = EC.visibility_of
        if mode == 'visiable':
            ec_func = EC.visibility_of
        elif mode == 'clickable':
            ec_func = EC.element_to_be_clickable
        elif mode == 'presence':
            ec_func = EC.presence_of_element_located

        try:
            element = None
            if dom_id is not None:
                element = wait.until(ec_func((By.ID, dom_id)))
            elif class_name is not None:
                element = wait.until(ec_func((By.CLASS_NAME, class_name)))
            elif xpath is not None:
                element = wait.until(ec_func((By.XPATH, xpath)))
            elif css is not None:
                element = wait.until(ec_func((By.CSS_SELECTOR, css)))
            return element
        except Exception:
            raise ElementNotFoundException(dom_id=dom_id, class_name=class_name, xpath=xpath,
                                           msg=desc, mode=mode, wait_time=wait_time)

    def xpath_click(self, xpath, desc=None, wait_time=30):
        """
        點擊指定的xpath元件
        :param xpath:
        :param desc: 元件敘述, 找不到元件時 會將desc寫到error message
        :param wait_time: 等超過等待時間 將視為找不到元件
        :return: 元件
        """
        try:
            element = self.element_wait(xpath=xpath, mode='clickable', desc=desc, wait_time=wait_time)
            element.click()
            return element
        except Exception as e:
            raise e

    def xpath_select_option(self, select_xpath, value, desc=None, wait_time=30):
        """
        透過xpath選取特定的值
        :param select_xpath:
        :param value: 要選的值
        :param desc: 元件敘述, 找不到元件時 會將desc寫到error message
        :param wait_time: 等超過等待時間 將視為找不到元件
        :return: 元件
        """
        option_xpath = select_xpath + '/option[text()="' + value + '"]'
        return self.xpath_click(option_xpath, desc=desc, wait_time=wait_time)

    def xpath_text(self, xpath, desc=None, wait_time=30):
        """
        取得指定xpath元件的html顯示文字
        :param xpath:
        :param desc: 元件敘述, 找不到元件時 會將desc寫到error message
        :param wait_time: 等超過等待時間 將視為找不到元件
        :return: string
        """
        try:
            element = self.element_wait(xpath=xpath, mode='presence', desc=desc, wait_time=wait_time)
            text_for_return = element.text
        except AttributeError:
            element = self.driver.find_element_by_xpath(xpath)
            text_for_return = element.text
        return text_for_return

    def xpath_is_selected(self, xpath, desc=None, wait_time=30):
        """
        查看 xpath 元件是否被選取
        :param xpath:
        :param desc: 元件敘述, 找不到元件時 會將desc寫到error message
        :param wait_time: 等超過等待時間 將視為找不到元件
        :return: True/False
        """
        try:
            element = self.element_wait(xpath=xpath, mode='presence', desc=desc, wait_time=wait_time)
            val_for_return = element.is_selected()
        except AttributeError:
            element = self.driver.find_element_by_xpath(xpath)
            val_for_return = element.is_selected()
        return val_for_return

    def xpath_value(self, xpath, desc=None, wait_time=30):
        """
        取得xpath元件的數值(input , textarea)
        :param xpath:
        :param desc: 元件敘述, 找不到元件時 會將desc寫到error message
        :param wait_time: 等超過等待時間 將視為找不到元件
        :return: string
        """
        try:
            element = self.element_wait(xpath=xpath, mode='presence', desc=desc, wait_time=wait_time)
            val_for_return = element.get_attribute('value')
        except AttributeError:
            element = self.driver.find_element_by_xpath(xpath)
            val_for_return = element.get_attribute('value')
        return val_for_return

    def xpath_send_keys(self, xpath, keys, desc=None, wait_time=30):
        """
        對xpath元件輸入值
        :param xpath:
        :param keys: 要輸入的字
        :param desc: 元件敘述, 找不到元件時 會將desc寫到error message
        :param wait_time: 等超過等待時間 將視為找不到元件
        :return: 元件
        """
        if desc is not None:
            element = self.element_wait(xpath=xpath, mode='clickable', desc='輸入框 ' + desc, wait_time=wait_time)
        else:
            element = self.element_wait(xpath=xpath, mode='clickable', wait_time=wait_time)
        element.clear()
        element.send_keys(keys)
        return element

    def xpath_switch_iframe(self, xpath, src, desc=None, wait_time=30):
        """
        切換到指定xpath的iframe, 並檢查網址是否正確
        :param xpath:
        :param src:
        :param desc: 元件敘述, 找不到元件時 會將desc寫到error message
        :param wait_time: 等超過等待時間 將視為找不到元件
        :return: 元件
        """
        iframe = self.element_wait(xpath=xpath, mode='presence', desc=desc, wait_time=wait_time)
        if src not in iframe.get_attribute('src'):
            return Exception('iframe url error')
        self.driver.switch_to.frame(iframe)
        return iframe

    def close_browser(self):
        """
            完整關閉瀏覽器
            :return: None
        """
        self.driver.quit()
        return None

    def do_js_script(self, script):
        """
            對瀏覽器執行JS語法
            :return: 執行結果
        """
        return self.driver.execute_script(script)

    def send_key_to_browser(self, key_type):
        """
            對瀏覽器送按鍵
            :param key_type: 按鍵類別
            :return: None
        """
        if key_type.lower() == "esc":
            webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        elif key_type.lower() == "tab":
            webdriver.ActionChains(self.driver).send_keys(Keys.TAB).perform()
        return None


def xpath_soup(element):
    """
        從beautiful的element Tag計算Xpath
        :param element: bs4 text or node
        :return: xpath as string
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        """
        @type parent: bs4.element.Tag
        """
        previous = itertools.islice(parent.children, 0, parent.contents.index(child))
        xpath_tag = child.name
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)


def parse_html(source, tag_type, condition=None):
    """
        解析Html tag
        :param source: element tree【String or bs4 element tag】
        :param tag_type: html tag類別【String】
        :param condition: 搜尋條件(支援regular expression)【JSON】
        :return:
    """
    # 如果帶進來的參數是string型態，則轉換成bs4的格式
    if type(source) == str:
        source = BeautifulSoup(source, "lxml")
    if condition:
        parse_list = source.findAll(tag_type, condition)
        return parse_list
    else:
        parse_list = source.findAll(tag_type)
        return parse_list


if __name__ == "__main__":
    url = "https://www.google.com.tw/"
    web_c = WebControl(url, profile_path=None, handless=False, browser_type='chrome')
    web_c.close_browser()
