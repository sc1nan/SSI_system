import uuid
import hashlib
import base64
import re
import mariadb
from constants import db
from functools import partial
from Theme import *
from typing import *
import datetime
from random import randint
import customtkinter as ctk


class encrypt:
    def pass_encrypt(pss, slt = None):
        salt = base64.urlsafe_b64encode(uuid.uuid4().bytes) if slt == None else str(slt).encode('utf-8')
        encryptor = hashlib.sha256()
        encryptor.update(str(pss).encode('utf-8') + salt)
        encrypted_password = encryptor.hexdigest()
        #encrypt the initial pass

        for _ in range(int(re.findall(r'\d{2}', encrypted_password)[0]) + len(pss)):
            encryptor.update(str(encrypted_password).encode('utf-8') + salt)
            encrypted_password = encryptor.hexdigest()
        #repeatedly encrypt the pass at the certain time

        return {"pass": encrypted_password, "salt": salt}

class database:
    def fetch_db_profile():
        try:
            mdb = mariadb.connect(user= 'root', password= db.PASSWORD, host= db.HOST, port= db.PORT, database= db.DB)
            return mdb
        except mariadb.Error as e:
            print(e)
            pass
        return None

    def fetch_data(cmd, tup:tuple = None) -> list | None:
        db_con = database.fetch_db_profile()
        try:
            db_cur = db_con.cursor()
            db_cur.execute(cmd, tup)
            return db_cur.fetchall()
        except mariadb.Error as e:
            print(e)
        return None

    def exec_nonquery(cmds):
        db_con = database.fetch_db_profile()
        try:
            db_cur = db_con.cursor()
            for i in range(len(cmds)):
                try:
                    db_cur.execute(cmds[i][0], cmds[i][1])
                    db_con.commit()
                except mariadb.IntegrityError as e:
                    print(f'command {i+1} error pushing', '\nreason: ', e)
        except mariadb.Error as e:
            print(cmds[0][0])
            print(e)
            return
        db_cur.close()
        db_con.close()

def brighten_color(hexcode: str, i: int = 1):
    c = re.findall(r'[\d\w]{2}', hexcode)
    r = c[0]
    g = c[1]
    b = c[2]
    r = int(r, base=16)
    g = int(g, base=16)
    b = int(b, base=16)
    r = 00 if r * i < 0 else 255 if r * i > 255 else round(r * i)
    g = 00 if g * i < 0 else 255 if g * i > 255 else round(g * i)
    b = 00 if b * i < 0 else 255 if b * i > 255 else round(b * i)
    return "#%02x%02x%02x" % (r,g,b)

def price_format_to_float(val: str) -> float:
    return float(val.replace(',',''))

def format_price(val: float) -> str:
    return '{:,.2f}'.format(val)

def date_to_words(date):
    months = [
        "", "January", "February", "March", "April", "May", "June", "July",
        "August", "September", "October", "November", "December"
    ]
    month, day, year = date.split('-')

    if day.startswith('0'):
        day = day[1]
    day = int(day)
    if day > 31 or day < 1:
        return "Invalid day"

    month = int(month)
    if month > 12 or month < 1:
        return "Invalid month"
    month = months[month]

    # Combining day, month, and year
    return "{} {}, {}".format(month, day, year)

def generateId(initial: Optional[str] = None, length: Union[int, None] = 12) -> str:
    num = randint(0, 16 if length <= 1 else 16**(length - len(initial or '')))
    hex_str = str(hex(num))[2:]

    if len(initial or '' + hex_str) == length:
        return f'%s%s' % (initial, hex_str)
    elif len(initial or '' + hex_str) < length:
        return f'%s%s' % (initial, hex_str.zfill(length - 1))
    #return f'%s%s' % (initial or '', hexStr if len(hexStr) == (length - 1) else hexStr.zfill(length - 1))

def convert_date(date: str | datetime.datetime | datetime.date, date_format: str, convertion_format: str, value: Literal['str', 'datetime'] = 'str') -> str | datetime.datetime:
    d = datetime.datetime.strptime(date, date_format) if isinstance(date, datetime.datetime | datetime.date) else date
    val = datetime.datetime.strptime(d, date_format).strftime(convertion_format)
    if value == 'datetime':
        return datetime.datetime.strptime(val, convertion_format)
    return val

def record_action(usn: str, _type: str, action_code: str):
    database.exec_nonquery([["INSERT INTO action_history VALUES (?, ?, ?, CURRENT_TIMESTAMP)", (usn, _type,  action_code)]])

def decode_action(type_code: str):
    if type_code.startswith('INVM'):
        temp = re.findall(r'/(\w+)+', type_code)
        return f'Make the Invoice {temp[-1]}' 

def text_overflow_elipsis(lbl: ctk.CTkLabel, width: int = None, lines: int = 1, width_padding: int = 0,):
    font_tool = ctk.CTkFont(lbl._font[0], lbl._font[1]) if isinstance(lbl._font, tuple) else lbl._font

    ellipsis_length:int = (font_tool.measure("..."))
    txt_dvd: list = []
    index_holder: int = 0
    label_text = str(lbl._text)

    if font_tool.measure(label_text) < ((int(lbl._current_width) if width is None else width) - ellipsis_length - width_padding):
        return

    for i in range(lines):
        txt: str = ""
        if i == lines - 1:
            for _ in range(index_holder, len(label_text)):
                if font_tool.measure(txt + label_text[i]) < ((int(lbl._current_width) if width is None else width) - ellipsis_length - width_padding):
                    txt += label_text[index_holder]
                    index_holder += 1
                else:
                    print(f"{txt[1:] if txt.startswith(' ') else txt}...")
                    txt_dvd.append(f"{txt[1:] if txt.startswith(' ') else txt}...")
                    break
        else:
            for _ in range(index_holder, len(label_text)):
                if font_tool.measure(txt + label_text[i]) < ((int(lbl._current_width) if width is None else width) - width_padding):
                    try:    
                        if label_text[index_holder] == " ":
                            temp: str = re.findall(r'(\w+) ', label_text[index_holder:])[0]
                            if(font_tool.measure(" " + txt + temp) > ((int(lbl._current_width) if width is None else width) - width_padding)):
                                print(f"{txt[1:] if txt.startswith(' ') else txt}\n")
                                txt_dvd.append(f"{txt[1:] if txt.startswith(' ') else txt}\n")
                                break
                        if label_text[index_holder] == "\n":
                            print(f"{txt[1:] if txt.startswith(' ') else txt}\n")
                            txt_dvd.append(f"{txt[1:] if txt.startswith(' ') else txt}\n")
                        txt += label_text[index_holder]
                        index_holder += 1
                    except:
                        print(f"{label_text[index_holder + 1:] if label_text[index_holder:].startswith(' ') else label_text[index_holder:]}\n")
                        txt_dvd.append(f"{label_text[index_holder + 1:] if label_text[index_holder:].startswith(' ') else label_text[index_holder:]}\n")
                        break
                else:
                    print(f"{txt[1:] if txt.startswith(' ') else txt}\n")
                    txt_dvd.append(f"{txt[1:] if txt.startswith(' ') else txt}\n")
                    break
    lbl.configure(text = ''.join(txt_dvd))



''' example of inserting data
usn = 'admin'
pss = encrypt.pass_encrypt('admin', None)
database.exec_nonquery([[f'INSERT INTO {db.ACC_CRED} VALUES (?, ?, ?, ?)', (usn, pss["pass"], pss['salt'], None)],
                        [f'INSERT INTO {db.ACC_INFO} VALUES (?, ?, ?)', ('admin', 'admin', 'admin')]])
'''
