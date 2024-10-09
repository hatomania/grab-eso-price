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

import argparse

class MyArgs:
    once: bool
    interval: int
    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="This will get the price list from TTC for the specified item ID. It will help you buy the item quickly and cheaply from guild stores all of the world. Please see: https://github.com/hatomania/grab-eso-price")
        parser.add_argument("--once", help="Only grab the list once then exit.", default=False, action='store_true')
        parser.add_argument("--interval", help="Interval to grab. unit: sec (default: 300)", default=300)
        args = parser.parse_args()
        self.once = bool(args.once)
        self.interval = int(args.interval)
