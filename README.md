Mobile QQ Message Extractor
---------------------------

Disclaimer: This utility is given "as is" without any warranty. Use of this utility for decrypting messages without prior mutual consent is illegal. Developers assume no liability and are not responsible for any misuse or damage caused by this utility.

Tested on Mobile QQ V5.5.1.

Dependencies:
* Python 2
* SQLite 3

Usage:

1. Download Mobile QQ database to this computer. The database is in ```/data/data/com.tencent.mobileqq/database/```, filename is ```${qq_number}.db```, where ```${qq_number}``` is your QQ number. Root privilege is required to copy the database file.
2. Edit ```decrypt.py```, replace the IMEI number.
3. Generate database dump: ```sqlite3 ${qq_number}.db .dump >${qq_number}.sql```.
3. Decrypt message: ```./decrypt.py ${qq_number}.sql```


How to find IMEI number of your phone: Dial ```*#06#```
