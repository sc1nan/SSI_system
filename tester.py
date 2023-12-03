#from typing import Callable, Optional, Tuple, Union
from typing import Optional, Tuple, Union
import customtkinter as ctk
from tkinter import messagebox
from customcustomtkinter import customcustomtkinter as cctk, customcustomtkinterutil as cctku
from popup import notif_popup_entities as ntf, service_popup as svc_p, customer_popup, mini_popup, dashboard_popup, transaction_popups
#from decimal import Decimal
from util import *
#import sql_commands
#import PyPDF2
#from tkinter import filedialog
#import network_socket_util as nsu
import winsound
import sql_commands
from datetime import datetime as dt
import sys

ctk.set_appearance_mode('light')

class body(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.update()
        self.attributes("-fullscreen", True)
        self.screen = (self.winfo_screenwidth(), self.winfo_screenheight())

        '''#mini_popup.authorization(self, self.screen, lambda: None).place(relx = .5, rely = .5, anchor = 'c')
        self.entry = ctk.CTkEntry(self, 140, 50)
        self.entry.place(relx = .5, rely = .5, anchor = 'c')
        temp = cctku.entry_limiter(15, self.entry)
        self.entry.configure(textvariable = temp)'''

        #dashboard_popup.rescheduling_service_info(self, self.screen).place(relx = .5, rely = .5, anchor = 'c', uid= 'TR# 179')
        #data = database.fetch_data("select * from service_preceeding_schedule")[0][-2]
        #print(type(data + datetime.timedelta(days= 5)))

        #transaction_popups.svc_provider(self, self.screen).place(relx = .5, rely = .5, anchor = 'c')
        #mini_popup.stock_disposal(self, self.screen + ([['Cherrie']],), None).place(relx = .5, rely = .5, anchor = 'c', data = ())
        print(sys.maxsize)
        self.mainloop()

        '''self.entry = ctk.CTkEntry(self, font= ('Arial', 24))
        self.entry.place(relx = .5, rely = .35, anchor = 'c')
        
        self.lbl = ctk.CTkLabel(self, text = 'Timer here', font= ('Arial', 24))
        self.lbl.place(relx = .5, rely = .4, anchor = 'c')

        self.lbl1 = ctk.CTkLabel(self, text = 'Timer here', font= ('Arial', 24))
        self.lbl1.place(relx = .5, rely = .45, anchor = 'c')

        self.lbl2 = ctk.CTkLabel(self, text = 'Timer here', font= ('Arial', 24))
        self.lbl2.place(relx = .5, rely = .5, anchor = 'c')

        self.button = ctk.CTkButton(self, command= self.click)
        self.button.place(relx = .5, rely = .55, anchor = 'c')'''

        #customer_popup.new_customer(self, self.screen, lambda: None).place(relx = .5, rely = .5, anchor = 'c')
        '''data = database.fetch_data('SELECT * FROM transaction_record WHERE client_name != ?', ('N/A', ))
        data = [(s[0], s[3]) for s in data]
        modData = []
        for d in data:
            ids =  database.fetch_data(sql_commands.get_id_owner, (d[1], ))
            ids = None if len(ids) == 0 else ids[0][0]
            modData.append((d[0], d[1], ids))
        modData = [(s[2], s[0]) for s in modData if s[2] is not None]

        for d in modData:
            if database.exec_nonquery([["UPDATE transaction_record SET client_id = ? WHERE transaction_uid = ?", d]]):
                print('success')
        self.mainloop()'''
    
    '''def click(self):
        self.button.configure(state = ctk.DISABLED)
        self.lbl.configure(text = dt.now().time().__str__())
        self.after(int(self.entry.get()) * 1000 if self.entry.get().isdecimal() else 2000, lambda: self.button.configure(state = ctk.NORMAL))
        self.timer()

    def timer(self):
        if self.button._state == ctk.DISABLED:
            def temp():
                self.lbl1.configure(text = dt.now().time().__str__())
                self.timer()
            self.lbl1.after(20, temp)
        else:
            f1 = float(self.lbl._text.split(':')[-1])
            f2 = float(self.lbl1._text.split(':')[-1])
            self.lbl2.configure(text = '%.3f' % (f2 - f1))'''
    
        
body()
    #lbl.configure(text = ''.join(txt_dvd))