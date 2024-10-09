Please use this with care so as not to overload the TTC servers.

# grab-eso-price
 This will get the price list from TTC for the specified item ID. It will help you buy the item quickly and cheaply from guild stores all of world.

# Prepare Selenium webdriver
You need to prepare the Selenium webdriver yourself.

# clone and Python settings (an example for Windows)
```
git clone https://github.com/hatomania/grab-eso-price.git
cd grab-eso-price
python -m venv .venv
.\.venv\Scripts\activate.bat
pip install -r requirements.txt
```

# Edit list1.csv
After editing, run the following command:<br>
(I'll assume you're in the "grab-eso-price" folder and have done `.\.venv\Scripts\activate.bat`.)
```
python conv_list.py
```
The csv format:<br>
```
(row1),(row2),(row3),(row4)
...
```
`(row1)`: empty or '#'. '#' means that comment out. It will be ignored by this program.<br>
`(row2)`: Item ID. This is the value of the "ItemID" parameter in the URL when you search for a product name on TTC. It's a pain, but you'll have to look it up yourself.<br>
`(row3)`: Average sales price. Find it yourself from the TTC if you want. If the sales price is lower than this, the program will prominently display that data. You can enter 0 if you don't want it.<br>
`(row4)`: Any string. We recommend that you enter the item name or something similar for easy identification.<br>

# Run
(I'll assume you're in the "grab-eso-price" folder and have done `.\.venv\Scripts\activate.bat`.)
```
python main.py
```

# See the results
A file named "grabbed.html" will be created in the current directory. Open it in your browser.<br>
It has the function to automatically upload the file via FTP. Please read the source code for details.
