# Standard library imports
import shutil
import os
import zipfile

# 3rd party imports
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.chrome.options import Options
import requests
from winregistry import WinRegistry as Reg


class DriverChecker:
    def __init__(self, core):
        self.core = core.lower()
        self.driver_filename = ''
        self.driver_folder = os.path.join(os.getenv('APPDATA'), 'III RPA', 'RPA Tool')
        if not os.path.isdir(self.driver_folder):
            os.makedirs(self.driver_folder)

    def do_check_and_download_driver(self):
        """
            檢查並下載Chrome Driver
            :return: Chrome Driver路徑
        """
        version = None
        if self.core == "chrome":
            version = self._check_chrome_version()
            self.driver_filename = "chromedriver_" + str(version) + ".exe"
            # 判斷存放Driver的路徑中是否已經有driver了
            if not os.path.exists(os.path.join(self.driver_folder, self.driver_filename)):
                return self._download_chrome_dirver(version)
            else:
                return {"result": True, "msg": os.path.join(self.driver_folder, self.driver_filename)}

    @property
    def driver_path(self):
        return os.path.join(self.driver_folder, self.driver_filename)

    @staticmethod
    def _check_chrome_version():
        """
            利用產品註冊碼找尋Chrome的版本號，並去掉最後一碼
            :return: Chrome版本號 【String】
        """
        reg = Reg()
        path = r"HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon"
        chrome_version = None
        for reg_value in reg.read_key(path)["values"]:
            if reg_value["value"].lower() == "version":
                chrome_version = reg_value["data"]
        # 去掉未一碼的version
        chrome_version = chrome_version.split(".")
        del chrome_version[-1]
        chrome_version = ".".join(chrome_version)
        return chrome_version

    def _download_chrome_dirver(self, version):
        """
            下載Chrome Driver
            :param version: local的Chrome版本號【String】
            :return: 處理結果回應【JSON】result(處理結果)【Boolean】 err_msg(錯誤訊息)【String】 msg(處理結果訊息)【String】
        """
        # 判斷Chrome適合使用哪個版本的Driver
        version_info_url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_' + version
        r_ver = requests.get(version_info_url)
        if r_ver.status_code != 200:
            return {"result": False, "err_msg": 'Can not connect chromedriver server: %s' % version_info_url}

        dl_url = 'https://chromedriver.storage.googleapis.com/' + r_ver.text + '/chromedriver_win32.zip'
        r = requests.get(dl_url)
        if r.status_code != 200:
            return {"result": False, "err_msg": 'Can not connect chromedriver server: %s' % version_info_url}

        # 下載Driver
        zip_save_path = os.path.join(self.driver_folder, 'chromedriver_win32_' + r_ver.text + '.zip')
        with open(zip_save_path, 'wb') as f:
            f.write(r.content)

        # Unzip
        unzip_path = self.driver_folder
        with zipfile.ZipFile(zip_save_path, "r") as zip_ref:
            zip_ref.extractall(unzip_path)

        # move and rename
        shutil.move(os.path.join(self.driver_folder, 'chromedriver.exe'),
                    os.path.join(self.driver_folder, self.driver_filename))
        os.remove(zip_save_path)
        return {"result": True, "msg": os.path.join(self.driver_folder, self.driver_filename)}

    def checker_start(self):
        """
        Message: session not created: Chrome version must be between 70 and 73
        (Driver info: chromedriver=73.0.3683.68 (47787ec04b6e38e22703e856e101e840b65afe72),platform=Windows NT 10.0.17134 x86_64)

        Message: session not created: This version of ChromeDriver only supports Chrome version 74
        (Driver info: chromedriver=74.0.3729.6
        """
        print(self.driver_path)
        if self.core == 'chrome':
            try:
                chrome_options = Options()
                chrome_options.add_argument('--headless')
                driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=chrome_options)
                driver.quit()
                return self.driver_path
            except SessionNotCreatedException as e:
                error_msg = str(e)
                print(error_msg)
                if error_msg.find('session not created: ') > -1:
                    session_error_idx = error_msg.find('session not created: ') + len('session not created: ')
                    msg1 = error_msg[session_error_idx: error_msg.find('\n')]
                    version_idx = error_msg.find('Driver info: chromedriver=') + len('Driver info: chromedriver=')
                    current_ver = int(error_msg[version_idx:error_msg.find('.')])
                    print(msg1)
                    if msg1 == 'Chrome version must be between 70 and 73':
                        print('Driver version update to 74')
                        if self._download_chrome_dirver(str(current_ver + 1)):
                            return self.checker_start()
                        else:
                            return self.driver_path
                    elif 'This version of ChromeDriver only supports Chrome version' in msg1:
                        if self._download_chrome_dirver(str(current_ver + 1)):
                            return self.checker_start()
                        else:
                            return self.driver_path
                    else:
                        # TODO download other version
                        return self.driver_path

        elif self.core == 'firefox':
            # TODO  firefox dirver checker
            return self.driver_path
