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


### This program doesn't work.
### Please don't use it.


import selenium.common.exceptions as se

import _eso_item_grabber as grabber
from _eso_item_grabber import EsoItemPriceInfoGrabberFromTTC as ttc


class Main:
    _grabber: grabber.EsoItemPriceInfoGrabberFromTTC

    _FILE_NAME = "item_list.csv"
    _ENCODING  = "shift_jis"

    def __init__(self) -> None:
        self._grabber = grabber.EsoItemPriceInfoGrabberFromTTC(
            region=ttc.Region.NA_PC,
            lang=ttc.Language.JP)

    def _grab_as_en(self, item_id: int) -> str:
        self._grabber.set_language(lang=ttc.Language.EN)
        return self._grab(item_id)

    def _grab_as_ja(self, item_id: int) -> str:
        self._grabber.set_language(lang=ttc.Language.JP)
        return self._grab(item_id)

    def _grab(self, item_id: int) -> str:
        ret = ""
        try:
            self._grabber.grab(item_id)
            ret = self._grabber.items[0].item_name
        except grabber.NoSuchItemIDOrNoPriceListException:
            ret = "(NoSuchItemIDOrNoPriceListException)"
        return ret
        is_loop = True
        cnt = 0
        TRY_CNT = 5
        ret = ""
        while is_loop:
            try:
                self._grabber.grab(item_id)
            except grabber.NoSuchItemIDOrNoPriceListException:
                ret = "(NoSuchItemIDOrNoPriceListException)"
                is_loop = False
            except se.NoSuchElementException as e:
                cnt = cnt + 1
                print("NoSuchElementException raised. ({})".format(cnt))
                if cnt >= TRY_CNT:
                    is_loop = False
                    raise e
            else:
                ret = self._grabber.items[0].item_name
                is_loop = False
        return ret


    def main(self) -> int:
        start_id = sum([1 for _ in open(self._FILE_NAME, encoding=self._ENCODING)])
        with open(self._FILE_NAME, "a", encoding=self._ENCODING) as f:
            for id in range(start_id, 30000):
                write_str = "hogehoge"
                write_str = '{},"{}","{}"'.format(id, self._grab_as_en(id), self._grab_as_ja(id))
                print("[{}]".format(write_str))
                f.write("{}\n".format(write_str))


def main():
    return Main().main()


if __name__ == '__main__':
    main()
