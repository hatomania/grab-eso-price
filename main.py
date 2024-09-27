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


# Seleniumのドライバは自分で用意する必要があります
# You need to prepare the Selenium driver program yourself.


import time

import codecs
import yaml
from selenium import webdriver

import _html_str as html
import _ftp_upload
import _eso_item_grabber as g

class Main:
    INTERVAL_SEC_TO_GRAB = 300
    FILENAME_ITEM_LIST = "items.yml"
    FILENAME_HTML_SRC  = "grabbed.html"
    FTP_UPLOAD = True

    _g: g.EsoItemPriceInfoGrabberFromTTC
    _item_hash = {}

    def __init__(self) -> None:
        self._g = g.EsoItemPriceInfoGrabberFromTTC(lang=g.EsoItemPriceInfoGrabberFromTTC.Language.JP)

    def _get_item_list(self) -> list[int]:
        l = []
        with open(self.FILENAME_ITEM_LIST, "r", encoding="utf-8") as f:
            l = yaml.full_load(f)
        return l

    def _grab_and_make_html_src(self, items: list[int]) -> str:
        header = ""
        body   = ""
        footer = ""
        s_cnt = 0
        for i, id in enumerate(items):
            url = ""
            try:
                self._g._reset_sale() # !!!!!! for the stub function
                self._g.grab(id)
            except g.NoSuchItemIDOrNoPriceListException as e:
                body = body + html.html_body_no_such_item_or_something(e.url(), id, str(e))
            else:
                url = self._g.url()
                item = self._g.data#.items[0]
                h = hash(item)
                if (id not in self._item_hash) or (self._item_hash[id] != h):
                    body = body + html.html_body_new(url, item)
                else:
                    body = body + html.html_body_no_new(url, item, i)
                self._item_hash[id] = h
                s_cnt = s_cnt + 1
            body = body + "\n"

        header = html.html_header() + html.html_time() + html.html_grabbed_info(s_cnt, len(items))
        body   = body + html.html_body_eol()
        footer = html.html_footer()
        return header + body + footer

    def _upload(self, html_src :str) -> None:
        with codecs.open(self.FILENAME_HTML_SRC, "w", encoding="utf-8") as f:
            f.write(html_src)
        if self._FTP_UPLOAD is True:
            _ftp_uload.ftp_upload()

    def _do(self) -> None:
        l = self._get_item_list()
        s = self._grab_and_make_html_src(l)
        self._upload(s)

    def main(self) -> int:
        current_tm = 0.0
        started_tm = time.time()
        elapsed_tm = float(self.INTERVAL_SEC_TO_GRAB) # 経過時間

        _loop = True
        while _loop:
            try:
                time.sleep(1.0)
                current_tm = time.time()

                if elapsed_tm >= self.INTERVAL_SEC_TO_GRAB:
                    started_tm = current_tm
                    print("")
                    self._do()

                print(".", end="", flush=True)
                elapsed_tm = current_tm - started_tm

            except KeyboardInterrupt:
                print("Keyboard interrupted.")
                _loop = False

        return 0

#p = grabber.EsoItemPriceInfoGrabberFromTTC(lang=grabber.EsoItemPriceInfoGrabberFromTTC.Language.JP)
#del p
#p.grab(7583)
#print(p.items)
#exit()

def _do_proc(__driver: webdriver.Chrome, __items: list[int]) -> None:
    return
    for i, id in enumerate(__items):
        pass

    i = 0
    _outstr = _html_str._html_header() + _html_str._html_time() + "    <p>{} item(s) grabbed.</p>\n".format(len(__items))
    for _item_id in __items:
        _url = "https://us.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID={}&SortBy=LastSeen&lang=ja-JP".format(_item_id)
        print("getting from {}".format(_url))
        __driver.get(_url)
        _el = __driver.find_elements(webdriver.common.by.By.CSS_SELECTOR, "#search-result-view > div.content-container > div > div > table > tbody > tr:nth-child(1)")
        if len(_el) == 0:
            _outstr = _outstr + "    <div{}><hr>".format(HTML_BK_STYLE_ERR)
            _outstr = _outstr + "Item ID [{}] is invalid.".format(_item_id)
        else:
            _el_hash = hash(_el[0].text)
            if _item_id not in _item_hash or _item_hash[_item_id] != _el_hash:
                _outstr = _outstr + "    <div{}><hr>".format(HTML_BK_STYLE_NEWITEM)
                _item_hash[_item_id] = _el_hash
            else:
                _outstr = _outstr + "    <div{}><hr>".format(HTML_BK_STYLE[i % len(HTML_BK_STYLE)])
            _outstr = _outstr + '<a href="{}" target="_blank">{}</a><br>'.format(_url, _url)
            _outstr = _outstr + _el[0].text.replace("\n", "<br>")
            i = i + 1
        _outstr = _outstr + "</div>\n"
        time.sleep(1.0)
    _outstr = _outstr + _html_str._html_footer()

    with codecs.open("./grabbed.html", "w", encoding="utf-8") as _file:
        _file.write(_outstr)
    _ftp_upload._ftp_upload()

def main():
    return Main().main()

    _options = webdriver.ChromeOptions()
    _options.add_argument('--ignore-certificate-errors')
    _options.add_argument('--ignore-ssl-errors')
    _options.add_argument('--ignore-permissions')
    _options.add_argument('--headless')

    print('connectiong to remote browser...')
    _driver = webdriver.Chrome(options=_options)
    _driver.implicitly_wait(float(WEBDRIVER_IMPLICITLY_WAIT)) # 要素が見つかるまで待機する秒数

    _current_tm = 0.0
    _started_tm = time.time()
    _elapsed_tm = float(INTERVAL_SEC_TO_GRAB) # 経過時間

    _loop = True
    while _loop:
        try:
            time.sleep(1.0)
            _current_tm = time.time()

            if _elapsed_tm >= INTERVAL_SEC_TO_GRAB:
                _started_tm = _current_tm
                _items = None
                with open("./items.yml", "r", encoding="utf-8") as _file:
                    _items = yaml.full_load(_file)
                print("")
                _do_proc(_driver, _items)

            print(".", end="", flush=True)
            _elapsed_tm = _current_tm - _started_tm
        except KeyboardInterrupt:
            print("Keyboard interrupted.")
            _loop = False

    print("the webdriver is now quiting...")
    _driver.quit()

if __name__ == '__main__':
    main()
