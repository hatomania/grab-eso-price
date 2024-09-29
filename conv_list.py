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

import codecs
import csv

class Main:
    def main(self) -> int:
        with open("list1.csv", encoding="utf_8_sig") as f:
            reader = csv.reader(f)
            with codecs.open("items.yml", "w", encoding="utf-8") as f1, codecs.open("sale.yml", "w", encoding="utf-8") as f2:
                for l in reader:
                    if len(l) >= 3:
                        f1.write("{}- {} # {}\n".format(l[0], l[1], l[3]))
                        f2.write("{}- {}: [{}, 0] # {}\n".format(l[0], l[1], l[2], l[3]))
        return 0

def main() -> int:
    return Main().main()

if __name__ == '__main__':
    import sys
    sys.exit(main())
