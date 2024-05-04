#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import urllib.request
import json


class FindEl:
    #   TODO    Элемент изображения яндекс картинок
    YaHrefImg = (By.XPATH, '//img[starts-with(@src, "")]')
    #   TODO    Кнопка яндекс "показать еще"
    ButtonViewNext = (By.CLASS_NAME, 'Button2.Button2_width_max.'
                                     'Button2_size_l.Button2_view_action.FetchListButton-Button')

    def __init__(self):
        self.prefs = {}
        chrome_options = webdriver.ChromeOptions()
        self.prefs["profile.default_content_setting_values.notifications"] = 2
        #        self.prefs["profile.managed_default_content_settings.images"] = 2
        #       web_hidden:
        #        chrome_options.add_argument("--headless")
#        chrome_options.add_argument("--user-data-dir='C:\\Users\\mamont\\AppData\\Local\\Google\\Chrome\\'")
#        chrome_options.add_argument("--profile-directory='C:\\Users\\mamont\\AppData\\Local\\Google\\Chrome\\'")
#        chrome_options.add_argument("user-agent=" + USER_AGENT)
#        chrome_options.add_argument('--no-sandbox')
#        chrome_options.add_argument('--disable-dev-shm-usage')
        #        chrome_options.add_argument("start-maximized")
        chrome_options.add_experimental_option("prefs", self.prefs)
        self.driver_chrome = webdriver.Chrome(options=chrome_options)
        self.Wait()
        self.key = 'экзоскелет'
        self.urlYa = f'https://ya.ru/images/search?from=tabbar&text={self.key}'
        #self.urlGoogle = f'https://www.google.ru/search?q={self.key}&newwindow=1&espv=2&source=lnms&tbm=isch&sa=X'
        self.urlGoogle = f"https://www.google.com/search?newwindow=1&sca_esv=2&q={self.key}&udm=2" \
                         f"&prmd=visnmbt&sa=X&ved=2"
        self.elem = None
        self.element = None
        self.elements = None
        self.path = 'imgSave'
        #   TODO    Блок рекламы на яндексе
        self.advertisement = 'JustifierRowLayout-Incut'
        #   TODO    Рекламный банер яндекса
        self.advertisement0 = 'AdvMastHead'
        self.src = None
        self.count = 1
        self.end_count = 500
        self.positionY = 1
        # DirectInline-PCodeContainer
        # SearchRelatedGallery
        # DirectInline DirectInline_filled
        # JustifierRowLayout-Incut
        # AdvMastHead

    def element_remove_for_js_class(self, element):
        try:
            self.Wait()
            self.driver_chrome.execute_script(f"var elements = document.getElementsByClassName('{element}');"
                                              f"while (elements.length > 0) elements[0].remove();")
        except:
            print('error remove element')
            return False
        return True

    #   TODO    Ждем завершения загрузки страницы
    def Wait(self):
        # noinspection PyBroadException
        try:
            WebDriverWait(self.driver_chrome, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete")
        except:
            print('Error Wait')

    def Find(self):
        self.driver_chrome.get(self.urlYa)
        self.Wait()
        self.elements = self.driver_chrome.find_elements(By.TAG_NAME, 'a')
        for self.element in self.elements:
            self.Wait()
            text = self.element.text
            attrib = self.element.get_attribute('href')
            print(str(text) + ' - ' + str(attrib))
        #        self.element.send_keys('test\n')
        time.sleep(10)

    def ScrollPage(self):
        last_height = self.driver_chrome.execute_script("return document.body.scrollHeight")
        while True:
            # Прокрутка вниз
            self.driver_chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Пауза, пока загрузится страница.
            time.sleep(1)
            self.Wait()
            # Вычисляем новую высоту прокрутки и сравниваем с последней высотой прокрутки.
            new_height = self.driver_chrome.execute_script("return document.body.scrollHeight")
            time.sleep(1)
            if new_height == last_height:
                print("Прокрутка завершена")
                break
            last_height = new_height
            print("Появился новый контент, прокручиваем дальше")
        self.Wait()

    def ScrollTOElement(self, id_element='bfoot'):
        try:
            self.element = self.driver_chrome.find_element(By.ID, id_element)
            time.sleep(1)
            print('ok')
        except:
            print('find element bfoot error')
        last_height = self.driver_chrome.execute_script("return document.body.scrollHeight")
        time.sleep(1)
        while True:
            try:
                self.driver_chrome.execute_script("arguments[0].scrollIntoView(true);", self.element)
                time.sleep(1)
                new_height = self.driver_chrome.execute_script("return document.body.scrollHeight")
                time.sleep(1)
            except:
                print('хрен знает')
                break
            if new_height == last_height:
                print("Прокрутка завершена")
                break
            last_height = new_height
            print("Появился новый контент, прокручиваем дальше")

    def DownloadImageAsJPEGya(self, count):
        # Поиск всех картинок на странице
        img = self.driver_chrome.find_elements(*self.YaHrefImg)
        self.Wait()
        for im in img:
            try:
                # Получаем ссылку на изображение
                self.src = im.get_attribute('src')
                print('Все подряд - ' + str(self.src))
            except:
                print('error: ')
            finally:
                self.Wait()
                if self.src is not None and self.src.find('orig') == -1:
                    print(str(count) + ' - ' + str(self.src))
                    self.Wait()
                    # Загрузка изображения
                    urllib.request.urlretrieve(str(self.src), os.path.join(self.key, self.key + str(count) + '.jpg'))
                    self.Wait()
                    self.src = None
                    if count >= self.end_count:
                        break
            count += 1
        return count

    def DownloadImageAsJPEGgoogle(self, count):
        # Поиск первой картинки
        try:
            img = self.driver_chrome.find_elements(By.XPATH, '//g-img/img[starts-with(@src, "")]')
        except:
            print('find href error: ')
        self.Wait()
        for im in img:
            try:
                self.src = im.get_attribute('src')
                if self.src.find('gstatic.com/images?q=tbn:') != -1:
                    print(str(count) + ' - ' + self.src)
            except:
                print('error: ')
            count += 1
            '''
            finally:
                self.Wait()
                if self.src is not None and self.src.find('orig') == -1:
                    print(str(count) + ' - ' + str(self.src))
                    self.Wait()
                    # Загрузка изображения
                    urllib.request.urlretrieve(str(self.src), os.path.join(self.key, self.key + str(count) + '.jpg'))
                    self.Wait()
                    self.src = None
                    if count >= self.end_count:
                        break'''
            count += 1
        return count

    def Read_cookies(self):
        # Загружаем куки для повторного входа
        self.driver_chrome = webdriver.Chrome()
        self.driver_chrome.get('https://vk.com/southural2020')
        with open('vk.json', 'r') as file:
            cookies = json.load(file)
            for cookie in cookies:
                self.driver_chrome.add_cookie(cookie)
        self.Wait()
        time.sleep(50)
        self.driver_chrome.refresh()
        time.sleep(20)
    #   TODO    Сохраняем куки с помощью pickle
    def Save_cookies(self):
        with open('cookies.json', 'wb') as file:
            json.dump(self.driver_chrome.get_cookies(), file)
        return True

    def FindImg(self):
        #   TODO    Создаем директорию
        try:
            os.makedirs(self.key)
        except FileExistsError:
            print('Директория уже существует')
        #   TODO    Переходим по поисковой ссылке
        #        self.driver_chrome.get(self.urlYa)
        self.driver_chrome.get(self.urlYa)
        self.Wait()
        url = self.driver_chrome.current_url
        while True:
            if self.count >= self.end_count:
                break
            #            self.ScrollPage()
            if url.find('https://ya.ru/') != -1:
                #   TODO    Удаление рекламного банера
                print('Удаление Банера успешно') if self.element_remove_for_js_class(self.advertisement0) else print(
                    'Ошибка удаления Банера')
                time.sleep(0.5)
                print('Удаление рекламы успешно') if self.element_remove_for_js_class(self.advertisement) else print(
                    'Ошибка удаления рекламы')
                time.sleep(0.5)
                self.Wait()
                #   TODO    Скачиваем найденные фото
                self.count = self.DownloadImageAsJPEGya(self.count)
                time.sleep(1)
                #   TODO    Если мало, то жмем кнопку дальше
                try:
                    self.driver_chrome.find_element(*self.ButtonViewNext).click()
                    self.Wait()
                except:
                    print('Error Click Button View Next')
                    break
            elif url.find('https://google'):
                time.sleep(1)
                self.ScrollPage()
                time.sleep(20)
                break
        self.driver_chrome.close()

    def __del__(self):
        print('Удаление класса')


if __name__ == '__main__':
    f = FindEl()
    f.FindImg()
  
