import uuid
import hashlib
import base64
import re
import mariadb
from constants import db
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
            mdb = mariadb.connect(user= db.DB_USERNAME, password= db.PASSWORD, host= db.HOST, port= db.PORT, database= db.DB)
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
                    return False , e
        except mariadb.Error as e:
            print(cmds[0][0])
            print(e)
            return False
        db_cur.close()
        db_con.close()
        return True

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
    
def generate_word_num_id(reference: Optional[str] = None):
    pattern = re.findall(r"([a-zA-Z]+)(\d+)",reference)[0]
    res = pattern[0] + str(int(pattern[1])+1).zfill(len(pattern[1]))
    return res

def combine_lists(lists:list, key_index:tuple):
    result_dict = {}
    combined_list = []
    for l in lists:
        combined_list.extend(l)

    for item in combined_list:
        key = tuple(item[key_index[0]:key_index[1]])
        if key in result_dict:
            result_dict[key].append(item)
        else:
            result_dict[key] = [item]
    result_list = list(result_dict.values())
    return result_list

def count_inventory(given:list):
    res = []
    for item in given:
        if len(item) == 1:
            res.append(((item[0][0],) + split_unit(item[0][1]) + (item[0][3],)))
        elif len(item) == 2: 
            if item[0][-2] - item[1][-2] != 0: 
                res.append((item[0][0],) + split_unit(item[0][1]) + (abs(item[0][-2] - item[1][-2]),))
        else:
            if item[2][-2] != 0:
                if item[0][-2] - item[1][-3] == 0:
                    res.append(((item[0][0],) + split_unit(item[0][1]) + (item[2][3],)))
                else:
                    #res.append(((item[0][0],) + split_unit(item[0][1]) + (abs((item[0][3] - item[1][3]) - item[2][3]) + item[1][-3],)) )  
                    res.append(((item[0][0],) + split_unit(item[0][1]) + (abs((item[0][3] - item[1][3]) - item[2][3]),)) )  
            else:
                    res.append(((item[0][0],) + split_unit(item[0][1]) + (item[1][3],)))         
    return res
            
def validate_email(email:str = None):
    return True if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) else False

def validate_contact_num(number:str = None):
    return True if re.match(r"^[0-9+\s-]+$",number) else False

def list_to_parted_list(given_list:list, row_count:int, provide_table_count: Optional[bool] = 0 ):
    divided_list = [given_list[i:i + row_count] for i in range(0, len(given_list), row_count)]
    return ((divided_list),(len(divided_list))) if provide_table_count else divided_list

def list_filterer(source: list, reference: list):
    return [data for res in source for data in reference if set(res).issubset(data)]

def remove_unit(source: str,):
    return re.sub(r'\([^)]*\)', '', source).strip()

def custom_sort(data, key):
    #def custom_sort_key(item):
    #    return (key.get(item[-1], float('inf')), item[-1])
    return sorted(data, key=lambda item : (key.get(item[-1], float('inf')), item[-1]))

def split_unit(source: str):
    res = re.match(r'^(.*?)\s*(\((.*?)\))?$', source)
    return (res.group(1), res.group(3)) if res.group(3) else (res.group(1),)

def item_unit(source:list):
    return [(f"{data[0]} ({data[1]})") if data[1] else (data[0]) for data in source]
  
def item_concat_unit(source:list): #BRUH
    return [(data[0], f"{data[1]} ({data[2]})", data[3], data[4], data[5], data[6]) if data[2] else (data[0], data[1], data[3], data[4], data[5], data[6]) for data in source]

def selling_concat_unit(source:list): #BRUH
    return [(data[0], data[1], f"{data[2]} ({data[3]})") if data[3] else (data[0], data[1], data[2]) for data in source]

def convert_date(date: str | datetime.datetime | datetime.date, date_format: str, convertion_format: str, value: Literal['str', 'datetime'] = 'str') -> str | datetime.datetime:
    d = datetime.datetime.strptime(date, date_format) if isinstance(date, datetime.datetime | datetime.date) else date
    val = datetime.datetime.strptime(d, date_format).strftime(convertion_format)
    if value == 'datetime':
        return datetime.datetime.strptime(val, convertion_format)
    return val

def not_in_set(reference_list:list, source_list:list):
    return [element for element in reference_list if element not in source_list]

def remove_special_char(word:str, list_of_char:list = ['(',')']):
    return ''.join(filter(lambda x: x not in list_of_char, word))

def sum_similar_elements(source: list):
    element_sum = {}
    for item in source:
        key = item
        price = float(item[-2].strip('₱').replace(',', '')) 
        if key in element_sum:
            element_sum[key][0] += price
            element_sum[key][1] += 1
        else:
            element_sum[key] = [price, 1]
    return [((key[0:3]) + (value[1],) +  (f'₱{format_price(value[0])}',)+ (key[3],)) for key, value in element_sum.items()]
     
def record_action(usn: str, _type: str, action_code: str):
    database.exec_nonquery([["INSERT INTO action_history(usn, type, ACTION, action_date) VALUES (?, ?, ?, CURRENT_TIMESTAMP)", (usn, _type,  action_code)]])

def decode_action(type_code: str):
    if type_code.startswith('INVM'):
        temp = re.findall(r'/(\w+)+', type_code)
        return f'Create Transaction {temp[-1]}'
    if type_code.startswith('CRI'):
        temp = re.findall(r'/(\w+)+', type_code)
        return f'Receive item {temp[-1]}'
    if type_code.startswith('TRNM'):
        temp = re.findall(r'/(\w+)+', type_code)
        return f'Create Transaction {temp[-1]}'
    if type_code.startswith('DPSM'):
        temp = re.findall(r'/(\w+)+', type_code)
        return f'Create Transaction {temp[-1]}'
    if type_code.startswith('DPSO'):
        temp = re.findall(r'/(\w+)+', type_code)
        return f'Create Transaction {temp[-1]}'
    if type_code.startswith('INVV'):
        temp = re.findall(r'/(\w+)+', type_code)
        return f'Void Invoice {temp[-1]} auth: {temp[1]}'
    if type_code.startswith('EITS'):
        temp = re.findall(r'/(\w+)+', type_code)
        return f'add {temp[0]} to the service\'s inventory'
    if type_code.startswith('DSPS'):
        temp = re.findall(r'/(\w+)+', type_code)
        return f'dispoe {temp[1]} stocks of {temp[0]}'

def text_overflow_ellipsis(lbl: ctk.CTkLabel, width: int = None, lines: int = 1, width_padding: int = 0,):
    font_tool = ctk.CTkFont(lbl._font[0], lbl._font[1]) if isinstance(lbl._font, tuple) else lbl._font

    ellipsis_length:int = (font_tool.measure("..."))
    txt_dvd: list = [[]]
    label_text = str(lbl._text)

    if font_tool.measure(label_text) < ((int(lbl._current_width) if width is None else width) - ellipsis_length - width_padding) or width is None:
        return
    #if cutting is not necessary at all
    
    def ellipse(sentence: str) -> str:
        ans = ""
    
        for st in sentence:
            if font_tool.measure(ans + st) < width - ellipsis_length:
                ans += st
            else:
                ans += "..."
                break
        return (ans).split()
    #add ellipsis for the word to fit
    
    for wrd in label_text.split():
        if font_tool.measure(" ".join(txt_dvd[-1]) + wrd) > width * .95:
            if len(txt_dvd) < lines:
                txt_dvd.append([])
        txt_dvd[-1].append(wrd)
    # split the sentence by words, creates new line if it reaches the max width and add all the remaining words at the last line

    txt_dvd[-1] = ellipse(" ".join(txt_dvd[-1]))
    lbl.configure(text = '\n'.join([" ".join(s) for s in txt_dvd]))