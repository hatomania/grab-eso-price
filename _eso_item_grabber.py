# MIT License
#
# Copyright (c) 2024 hatomania
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import selenium.common.exceptions as se


# いつまでたっても受信が完了しない例外
class ReceivingNotCompletedException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "Tried {} time(s) but was unable to complete the receiving. Please see [{}] yourself.".format(self.args[1], self.args[0])


# アイテムIDまたはアイテムの価格リストが存在しない例外
class NoSuchItemIDOrNoPriceListException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "It means that the item ID [{}] itself does not exist or no one has listed it so there is no price list. We cannot tell the difference between these. Please see [{}] yourself.".format(self.args[1], self.args[0])

    def url(self) -> str:
        return str(self.args[0])


class EsoItemPriceInfo:
    item_id: int
    item_name: str
    item_lang: str
    player_id: str
    location_name: str
    guild_name: str
    class Price:
        unit: int
        amount: int
        total: int
        def __repr__(self) -> str:
            return "[{}, {}, {}]".format(self.unit, self.amount, self.total)
    price: Price
    elapsed_time_as_it_is: str
    elapsed_time: int # not used yet
    def __str__(self) -> str:
        return '[{}, "{}", "{}", "{}", "{}", "{}", {}, "{}"]'.format(self.item_id, self.item_name, self.item_lang, self.player_id, self.location_name, self.guild_name, self.price, self.elapsed_time_as_it_is)
    def __repr__(self) -> str:
        return self.__str__()
    def __hash__(self) -> int:
        return hash(self.__str__())


class EsoItemPriceData:
    items: list[EsoItemPriceInfo]
    class Sale:
        average: int
        sales: int
        def __init__(self, average: int, sales: int) -> None:
            self.average = average
            self.sales = sales
        def __str__(self) -> str:
            return "[{}, {}]".format(self.average, self.sales)
        def __repr__(self) -> str:
            return self.__str__()
        def __hash__(self) -> int:
            return hash(self.__str__())
    #sale: dict[int:Sale] # { item_id: Sale, item_id: Sale, item_id: Sale, ...}
    sale: Sale


class EsoItemPriceInfoGrabber:
    data: EsoItemPriceData

    def __init__(self) -> None:
        pass

    def grab(self, context) -> None:
        pass

    def __del__(self) -> None:
        pass


class EsoItemPriceInfoGrabberFromWeb(EsoItemPriceInfoGrabber):
    _WEBDRIVER_IMPLICITLY_WAIT = 10 # 要素が見つかるまで待機する秒数
    _driver: webdriver.Chrome
    _url: str

    def __init__(self) -> None:
        super().__init__()
        print('starting the webdriver.')
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--ignore-permissions')
        options.add_argument('--headless')
        print('connectiong to remote browser...')
        self._driver = webdriver.Chrome(options=options)
        self._driver.implicitly_wait(float(self._WEBDRIVER_IMPLICITLY_WAIT))
        print("implicitly_wait is {}.".format(self._WEBDRIVER_IMPLICITLY_WAIT))

    def url(self) -> str:
        return self._url

    def __del__(self) -> None:
        print("The webdriver is now quitting. Please wait...")
        self._driver.quit()
        super().__del__()


class EsoItemPriceInfoGrabberFromTTC(EsoItemPriceInfoGrabberFromWeb):
    class Region:
        NA_PC   = ["us", "pc"]
        NA_XBOX = ["us", "xb"]
        NA_PS   = ["us", "ps"]
        EU_PC   = ["eu", "pc"]
        EU_XBOX = ["eu", "xb"]
        EU_PS   = ["eu", "ps"]

    class Language:
        EN = "en-US"
        JP = "ja-JP"

    _region: str
    _language: str

    _CSS_SELECTOR1 = "#search-result-view > div.content-container"
    _CSS_SELECTOR2 = _CSS_SELECTOR1 + " > div > div > table > tbody"

    def __init__(self, region: Region = Region.NA_PC, lang: Language = Language.EN) -> None:
        super().__init__()
        self.data = EsoItemPriceData()
        #self.data.items = list[EsoItemPriceInfo]()
        self._region   = region
        self._language = lang

    def set_region(self, region: Region) -> None:
        self._region = region

    def set_language(self, lang: Language) -> None:
        self._language = lang

    # 'context' is a item-id of TTC
    def grab(self, context) -> None:
        url = "https://{}.tamrieltradecentre.com/{}/Trade/SearchResult?ItemID={}&SortBy=LastSeen&lang={}".format(
            self._region[0],
            self._region[1],
            int(context),
            self._language
        )
        print("getting from {}".format(url))
        self._url = url

        is_loop = True
        cnt = 0
        TRY_CNT = 5
        while is_loop:
            try:
                self._driver.get(url)
                self._wait_finish_receiving(url)
                if (self._no_such_item()):
                    raise NoSuchItemIDOrNoPriceListException(url, context)
                self.data.items = self._find_items(context)
                self.data.sale  = self._find_sale(context)
                is_loop = False
            except se.NoSuchElementException as e:
                cnt = cnt + 1
                print("NoSuchElementException has raised. (retry {} of {})".format(cnt, TRY_CNT))
                if cnt >= TRY_CNT:
                    is_loop = False
                    raise e

    def _wait_finish_receiving(self, url_shown_exception: str) -> None:
        is_loop = True
        cnt = 0
        TRY_CNT = 5
        while is_loop:
            elm = self._driver.find_element(By.CSS_SELECTOR, self._CSS_SELECTOR1)
            if cnt <= TRY_CNT - 1 and (elm.text.startswith("Loading") or elm.text.startswith("Retrieving reCAPTCHA token")):
                time.sleep(1)
                print("waiting for receiving to complete...")
                cnt = cnt + 1
            else:
                is_loop = False
        if cnt >= TRY_CNT:
            raise ReceivingNotCompletedException(url_shown_exception, cnt)

    def _no_such_item(self) -> bool:
        elm = self._driver.find_element(By.CSS_SELECTOR, self._CSS_SELECTOR1)
        return elm.text.startswith("No trade matches your constraint")

    def _find_items(self, item_id: int) -> list[EsoItemPriceInfo]:
        items = list[EsoItemPriceInfo]()
        elm_result = self._driver.find_element(By.CSS_SELECTOR, self._CSS_SELECTOR2)
        elm_items = elm_result.find_elements(By.CLASS_NAME, "cursor-pointer")
        for e in elm_items:
            info = EsoItemPriceInfo()
            info.item_id = item_id
            info.item_name = self._find_item_name(e)
            info.item_lang = self._language
            info.player_id = self._find_listed_player_id(e)
            info.location_name = self._find_location_name(e)
            info.guild_name = self._find_guild_name(e)
            info.price = self._find_price(e)
            info.elapsed_time_as_it_is = self._find_elapsed_time_as_it_is(e)
            items.append(info)
        return items

    def _find_item_name(self, element: WebElement) -> str:
        return element.find_element(By.CSS_SELECTOR, "td > div").text

    def _find_listed_player_id(self, element: WebElement) -> str:
        return element.find_element(By.CSS_SELECTOR, "td:nth-of-type(2) > div").text

    def _find_location_name(self, element: WebElement) -> str:
        return element.find_element(By.CSS_SELECTOR, "td:nth-of-type(3) > a").text

    def _find_guild_name(self, element: WebElement) -> str:
        return element.find_element(By.CSS_SELECTOR, "td:nth-of-type(3) > div").text

    def _find_price(self, element: WebElement) -> EsoItemPriceInfo.Price:
        ret = EsoItemPriceInfo.Price()
        elm = element.find_element(By.CLASS_NAME, "gold-amount")
        ret.unit   = int(float(elm.find_element(By.CSS_SELECTOR, "span:nth-of-type(1)").text.replace(",", "")))
        ret.amount = int(elm.find_element(By.CSS_SELECTOR, "span:nth-of-type(2)").text.replace(",", ""))
        ret.total  = int(elm.find_element(By.CSS_SELECTOR, "span:nth-of-type(3)").text.replace(",", ""))
        return ret

    def _find_elapsed_time_as_it_is(self, element: WebElement) -> str:
        return element.find_element(By.CSS_SELECTOR, "td:nth-of-type(5)").text

    # This is a stub function
    import yaml
    __read_sale = False
    __sale_data: dict[int: list[int, int]] = { -1: [-1, -1] }
    def _find_sale(self, item_id: int) -> EsoItemPriceData.Sale:
        # read the sales from a yaml file. read one-time
        if self.__read_sale is False:
            with open("sale.yml", "r", encoding="utf-8") as f:
                self.__sale_data = self.yaml.full_load(f)
            self.__read_sale = True
        ret = EsoItemPriceData.Sale(-1, -1)
        for l in self.__sale_data:
            if item_id in l:
                ret = EsoItemPriceData.Sale(l[item_id][0], l[item_id][1])
                break
        return ret
    def _reset_sale(self) -> None:
        self.__read_sale = False

    def __del__(self) -> None:
        super().__del__()
