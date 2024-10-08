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
import copy
import yaml

import _myargs
import _html_str as html
import _ftp_upload
import _eso_item_grabber as g
import _view as v

class Main:
    INTERVAL_SEC_TO_GRAB = 300
    FILENAME_ITEM_LIST = "items.yml"
    FILENAME_HTML_SRC  = "grabbed.html"
    FTP_UPLOAD = False
    GRAB_ONCE = False

    _args: _myargs.MyArgs
    _g: g.EsoItemPriceInfoGrabberFromTTC
    _item_hash = {}

    def __init__(self) -> None:
        self._args = _myargs.MyArgs()
        #print(vars(self._args))
        self.INTERVAL_SEC_TO_GRAB = self._args.interval
        self.GRAB_ONCE = self._args.once
        self._g = g.EsoItemPriceInfoGrabberFromTTC(lang=g.EsoItemPriceInfoGrabberFromTTC.Language.EN)

    def _get_item_list(self) -> list[int]:
        l = []
        with open(self.FILENAME_ITEM_LIST, "r", encoding="utf-8") as f:
            l = yaml.full_load(f)
        return l

    def _grab(self, items: list[int]) -> list[v.ViewData]:
        vdata_list = list[v.ViewData]()
        for i, iid in enumerate(items):
            vdata = v.ViewData()
            try:
                print("({}/{}) ".format(i+1, len(items)), end="")
                self._g._reset_sale() # !!!!!! for the stub function
                self._g.grab(iid)
            except g.NoSuchItemIDOrNoPriceListException as e:
                vdata.state = copy.deepcopy(e)
            else:
                vdata.items = copy.deepcopy(self._g.data)
                vdata.url = copy.copy(self._g.url())
            vdata_list.append(vdata)
            time.sleep(1.0)
        return vdata_list

    def _grab_and_make_html_src(self, items: list[int]) -> str:
        header = ""
        body   = ""
        footer = ""
        s_cnt = 0
        for i, id in enumerate(items):
            url = ""
            try:
                print("({}/{}) ".format(i+1, len(items)), end="")
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
            time.sleep(1.0)

        header = html.html_header() + html.html_time() + html.html_grabbed_info(s_cnt, len(items))
        body   = body + html.html_body_eol()
        footer = html.html_footer()
        return header + body + footer

    def _build_view(self, vdata_list: list[v.ViewData]) -> str:
        #return v.ViewHtmlNormal(vdata_list).text
        return v.ViewHtmlGroupLocation(vdata_list).text

    def _upload(self, html_src :str) -> None:
        with codecs.open(self.FILENAME_HTML_SRC, "w", encoding="utf-8") as f:
            f.write(html_src)
        if self.FTP_UPLOAD is True:
            _ftp_upload.ftp_upload()

    def _do(self) -> None:
        l = self._get_item_list()
        d = self._grab(l)
        s = self._build_view(d)
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

                if self.GRAB_ONCE is True:
                    print("It was done once.")
                    _loop = False

            except KeyboardInterrupt:
                print("Keyboard interrupted.")
                _loop = False

        return 0

def main():
    return Main().main()

if __name__ == '__main__':
    main()
