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

import ftplib

# 接続先サーバーのホスト名またはIPアドレス
HOSTNAME = "your-host.com" 
# アップロードするファイルパス
UPLOAD_SRC_PATH = "./grabbed.html" # これは変更しないでください。又はmain.pyのFILENAME_HTML_SRCと合わせてください
# アップロード先のファイルパス（STORはファイルをアップロードするためのFTPコマンドなので必要です。）
UPLOAD_DST_PATH = "STOR /grabbed.html" 
# サーバーのユーザー名
USERNAME = "your_user" 
# サーバーのログインパスワード
PASSWORD = "your_password" 
# FTPサーバポート
PORT = 21 
TIMEOUT = 5

def ftp_upload(hostname=HOSTNAME, username=USERNAME, password=PASSWORD, port=PORT, upload_src_path=UPLOAD_SRC_PATH, upload_dst_path=UPLOAD_DST_PATH, timeout=TIMEOUT):    # FTP接続/アップロード
    with ftplib.FTP() as ftp:
        ftp.connect(host=hostname, port=port, timeout=timeout)
        # パッシブモード設定
        ftp.set_pasv("true")
        # FTPサーバログイン
        ftp.login(username, password)
        with open(upload_src_path, 'rb') as fp:
            ftp.storbinary(upload_dst_path, fp)
