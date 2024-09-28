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


import _eso_item_grabber as g
import _html_str as html


class ViewData:
    items: g.EsoItemPriceData
    state: Exception = None
    url: str # why are you here?


class View:
    _data: list[ViewData]
    text: str
    err_cnt: int

    def __init__(self, data: list[ViewData]) -> None:
        self._data = data
        self._create_err_cnt()
        self._convert_data()
        self._create_text()

    def _header(self) -> str:
        return str()
    def _body(self) -> str:
        text = ""
        for d in self._data:
            text = text + self._create_text_one(d)
        return text
    def _footer(self) -> str:
        return str()

    def _create_err_cnt(self) -> None:
        # ref. https://qiita.com/oioigohan/items/64b3a76edcfe5d907088
        self.err_cnt = len([a for a in self._data if a.state is not None]) # this code is fine
        #self.err_cnt = sum([a.state is not None for a in self._data]) # this code is fine too

    def _convert_data(self) -> None:
        pass

    def _create_text_one(self, data: ViewData) -> str:
        return "Why did you call me?"
    def _create_text(self) -> None:
        self.text = self._header() + self._body() + self._footer()


class ViewHtml(View):
    def __init__(self, data: list[ViewData]) -> None:
        super().__init__(data)
    def _header(self) -> str:
        return html.html_header() + html.html_time() + html.html_grabbed_info(len(self._data)-self.err_cnt, len(self._data))
    def _footer(self) -> str:
        return html.html_body_eol() + html.html_footer()


class ViewHtmlNormal(ViewHtml):
    _cnt = 0

    def __init__(self, data: list[ViewData]) -> None:
        super().__init__(data)
    def _create_text_one(self, data: ViewData) -> str:
        ret: str
        if data.state is not None:
            e: g.NoSuchItemIDOrNoPriceListException = data.state
            ret = html.html_body_no_such_item_or_something(e.url(), id, str(e)) + "\n"
        else:
            ret = html.html_body_no_new(data.url, data.items, self._cnt) + "\n"
        self._cnt = self._cnt + 1
        return ret


class ViewHtmlGroupLocation(ViewHtmlNormal):
    _group_data: dict[str, list[ViewData]] # str: location name

    def __init__(self, data: list[ViewData]) -> None:
        super().__init__(data)

    def _body(self) -> str:
        text = ""
        for k, v in self._group_data.items():
            text += html.html_location_caption(k)
            for d in v:
                text += self._create_text_one(d)
        return text

    def _convert_data(self) -> None:
        self._group_data = dict[str, list[ViewData]]()
        tmp_data_list = list[ViewData]()
        for l in self._data:
            if l.state is not None:
                continue
            # l.items means g.EsoItemPriceData
            i: g.EsoItemPriceInfo = l.items.items[0] # need only the top data. so it is the data that users need.
            appended_data = ViewData()
            #appended_data = g.EsoItemPriceData()
            appended_data.items = g.EsoItemPriceData()
            appended_data.items.items = list[g.EsoItemPriceInfo]()
            appended_data.items.items.append(i)
            appended_data.items.sale = l.items.sale
            appended_data.state = l.state
            appended_data.url = l.url
            tmp_data_list.append(appended_data)

        for l in tmp_data_list:
            if l.items.items[0].location_name not in self._group_data:
                self._group_data[l.items.items[0].location_name] = list[ViewData]()
            self._group_data[l.items.items[0].location_name].append(l)

        # sort by guild_name
        # ref. https://blog.amedama.jp/entry/2015/12/14/013805
        # ref. https://techplay.jp/column/1615
        # ref. https://qiita.com/n10432/items/e0315979286ea9121d57
        #from operator import attrgetter
        for _, v in self._group_data.items():
            v.sort(key=lambda x: x.items.items[0].guild_name)
