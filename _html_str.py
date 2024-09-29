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

from _eso_item_grabber import EsoItemPriceData


HTML_BK_STYLE_ERR = ' style="background-color:#ff0000"'
HTML_BK_STYLE = ["", ' style="background-color:#cccccc"']
HTML_BK_STYLE_NEWITEM = ' style="background-color:#ffff00"'
HTML_BK_STYLE_NEWITEM = ' style="background-color:#ffff00"'
HTML_BK_STYLE_BARGAIN1 = ' style="background-color:#33cc33"'
HTML_BK_STYLE_BARGAIN2 = ' style="background-color:#ff9966"'
HTML_BK_STYLE_LOCATION = ' style="background-color:#ffbb00"'
THIS_DIFF_IS_FINE = 5000

def _html_split() -> str:
    return "<hr>"


def _html_invalid(item_id: int) -> str:
    return "    <div{}>{}Item ID [{}] is invalid or no listed price list.</div>".format(HTML_BK_STYLE_ERR, _html_split(), item_id)


def _html_item(url: str, item: EsoItemPriceData) -> str:
    i = item.items[0]
    bk = ""
    ic = ""
    if i.price.unit <= item.sale.average:
        bk = HTML_BK_STYLE_BARGAIN1
        ic = "👍"
    elif ((i.price.unit * 0.9) <= item.sale.average) or ((i.price.unit - THIS_DIFF_IS_FINE) <= item.sale.average):
        bk = HTML_BK_STYLE_BARGAIN2
    price = "<span{}>{} x {} = {} (ave: {}) (diff: {}){}</span>".format(bk, "{:,.0f}".format(i.price.unit), i.price.amount, "{:,.0f}".format(i.price.total), "{:,.0f}".format(item.sale.average), "{:+,.0f}".format(i.price.unit - item.sale.average), ic)
    return '[{}] <a href="{}" target="_blank">{}</a> <input type="button" value="I have this❤" onclick="document.getElementById(\'{}\').innerHTML=\'\'"/><br>{}<br>{}<br>{}<br>{}'.format(i.item_id, url, i.item_name, i.item_id, i.location_name, i.guild_name, price, i.elapsed_time_as_it_is)


def _html_body_url(url: str) -> str:
    return '<a href="{}" target="_blank">{}</a><br>'.format(url, "(Go to the TTC page)")


def html_body_no_such_item_or_something(url: str, item_id: int, msg: str) -> str:
    return "    <div{}>{}{}{}</div>".format(HTML_BK_STYLE_ERR, _html_split(), _html_body_url(url), msg)


def html_body_new(url: str, item: EsoItemPriceData) -> str:
    return "    <div{}>{}{}</div>".format(HTML_BK_STYLE_NEWITEM, _html_split(), _html_item(url, item))


def html_body_no_new(url: str, item: EsoItemPriceData, counter: int) -> str:
    return '    <div id="{}"{}>{}{}</div>'.format(item.items[0].item_id, HTML_BK_STYLE[counter % len(HTML_BK_STYLE)], _html_split(), _html_item(url, item))


def html_body_eol() -> str:
    return "    <p>(EOL)</p>\n"


def html_header() -> str:
    return '''<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>grab eso price</title>
  </head>
  <body>
'''


def html_footer() -> str:
    return '''  </body>
</html>
'''


def html_time() -> str:
    return "    <p>{}</p>\n".format(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()))


def html_grabbed_info(sucess: int, total: int) -> str:
    return "    <p>{} of {} item(s) grabbed.</p>\n".format(sucess, total)


def html_location_caption(location_name: str) -> str:
    return "    <h3{}>{}</h3>\n".format(HTML_BK_STYLE_LOCATION, location_name)
