import os

FOLDER_JRL = "C:\\Users\\%USERNAME%\\Saved Games\\Frontier Developments\\Elite Dangerous\\"

#ユーザー名を取得
FOLDER_JRL = FOLDER_JRL.replace(r"%USERNAME%", str(os.getlogin()))
