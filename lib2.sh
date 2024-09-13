#!/bin/bash

# تحديث النظام وتثبيت الحزم الأساسية
apt update && apt install -y curl build-essential sudo python3.11-venv

# إنشاء وتفعيل البيئة الافتراضية
python3 -m venv final
source final/bin/activate

# تحديد مسار الملف المصدر والوجهة
SOURCE_FILE2="/data/data/com.termux/files/home/ScoRe/source.py"
DESTINATION_DIR2="/root/"

# نسخ الملف إلى وجهته
cp "$SOURCE_FILE2" "$DESTINATION_DIR2"

# التحقق من نجاح النسخ
if [ $? -eq 0 ]; then
    echo "✎┊‌ The files was copied successfully. ✔️"
else
    echo "✎┊‌ File copy failed. ❌"
fi

pip install sqlalchemy
pip install aiohttp
pip install lxml_html_clean
pip install pillow
pip install youtube-search-python
pip install yt-dlp
pip install telethon
pip install pydub
pip install waitress
pip install gunicorn
pip install ocrspace
pip install ShazamAPI
pip install akinator
pip install asyncio
pip install selenium
pip install setuptools
pip install wheel
pip install cloudscraper
pip install speechrecognition
pip install colour
pip install qrcode
pip install python-barcode
pip install jotquote
pip install glitch_this
pip install cryptg
pip install cowpy
pip install beautifulsoup4
pip install cfscrape
pip install cryptography
pip install moviepy
pip install pyquery
pip install tswift
pip install wikipedia
pip install fontTools
pip install emoji==1.7.0
pip install fonttools
pip install geopy
pip install gitpython
pip install google-api-python-client
pip install google-auth-httplib2
pip install google-auth-oauthlib
pip install gsearch
pip install gtts
pip install hachoir
pip install heroku3
pip install html-telegraph-poster
pip install humanize
pip install justwatch
pip install kwot
pip install lottie
pip install lxml
pip install covid
pip install jikanpy
pip install lyricsgenius
pip install markdown
pip install motor
pip install patool
pip install prettytable
pip install psutil
pip install pyfiglet
pip install PyGithub
pip install programmingquotes
pip install pygments
pip install psycopg2-binary
pip install pylast
pip install pymediainfo
pip install pySmartDL
pip install pytuneteller
pip install pytz
pip install wget
pip install urlextract
pip install search-engine-parser
pip install selenium
pip install spamwatch
pip install speedtest-cli
pip install sqlalchemy
pip install sqlalchemy-json
pip install telegraph
pip install tgcrypto
pip install validators
pip install vcsi
pip install ipaddress
pip install wand
pip install ujson==5.8.0
pip install youtube_dl==2021.5.16
pip install user_agent
pip install img2html
pip install googletrans-py
pip install ipaddress
pip install img2html
pip install webcolors
pip install py-googletrans
pip install googletrans==4.0.0-rc1
if [ $? -eq 0 ]; then
    echo "✎┊‌ Libraries loaded successfully. "
else
    echo "✎┊‌ Libraries failed. ❌"
fi

cp /data/data/com.termux/files/home/ScoR/lib2.sh /root/
