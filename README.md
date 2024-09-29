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

# Run
(I'll assume you're in the "grab-eso-price" folder and have done `.\.venv\Scripts\activate.bat`.)
```
python main.py
```

# See the results
A file named "grabbed.html" will be created in the current directory. Open it in your browser.<br>
It has the function to automatically upload the file via FTP. Please read the source code for details.
