import customtkinter as ctk
from tkinter import messagebox
from tkextrafont import Font
from PIL import Image
from Theme import Color
from dashboard import dashboard as _db
from constants import db
from util import *
import sql_commands
import datetime
import _tkinter
from functools import partial
import subprocess 

#print(ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100) 

class loginUI(ctk.CTk):

    __is_PasswordVisible = True

    def __init__(self):
        super().__init__()
        self.attempt = 0
        try:
            #Transitioning to new font style
            Font(file="Font/DMSans-Bold.ttf")
            Font(file="Font/DMSans-Medium.ttf")
            Font(file='Font/DMSans-Regular.ttf')

            #Use DM Mono for numbers
            Font(file="Font/DMMono-Light.ttf")
            Font(file="Font/DMMono-Medium.ttf")
            Font(file="Font/DMMono-Regular.ttf")

        except _tkinter.TclError:
            pass

        '''functions and processes'''
        def report_exceed_attempt():
            _usn = database.fetch_data(sql_commands.get_usn, (self.user_entry.get(),))
            _usn = None if len(_usn) == 0 else _usn[0][0]
            database.exec_nonquery([[sql_commands.record_login_report, (_usn, self.user_entry.get())]])
            messagebox.showwarning('Login Error', 'Login Attempts Exceeds 3 times\nIt will be reported to the owner', parent = self)
            self.destroy()

        def login(_):
            try:
                salt = database.fetch_data(f'SELECT {db.acc_cred.SALT} FROM {db.ACC_CRED} WHERE {db.USERNAME} COLLATE LATIN1_GENERAL_CS = ?',
                                        (self.user_entry.get(), ))[0][0]
            except IndexError:
                self.attempt += 1
                if self.attempt == 3:
                    report_exceed_attempt()
                    return
                self.password_entry.delete(0, ctk.END)
                messagebox.showinfo('Error', 'Username Or Password Incorrect', parent = self)
                return
            count = database.fetch_data(f'SELECT COUNT(*) FROM {db.ACC_CRED} WHERE {db.USERNAME} COLLATE LATIN1_GENERAL_CS = ? AND {db.acc_cred.PASSWORD} = ?',
                                        (self.user_entry.get(), encrypt.pass_encrypt(self.password_entry.get(), salt)['pass']))
            
            if count[0][0] == 0:
                self.password_entry.delete(0, ctk.END)
                self.attempt += 1
                if self.attempt == 3:
                    report_exceed_attempt()
                    return
                messagebox.showinfo('Error', 'Username Or Password Incorrect', parent = self)
            else:
                if database.fetch_data('SELECT state FROM acc_info WHERE usn = ?', (self.user_entry.get(), ))[0][0] == 0:
                    messagebox.showerror("Failed to Login", "The Account you're been\nlogged has been deactivated.\nInquire to the admin", parent = self)
                    return
                current_datetime = datetime.datetime.now();
                data_key = encrypt.pass_encrypt(self.password_entry.get(), datetime.datetime.now())['pass']
                database.exec_nonquery([[f"INSERT INTO {db.LOG_HIST} VALUES (?, ?, ?, ?)",
                                        (self.user_entry.get(), current_datetime.date(), current_datetime.time(), current_datetime.time())],
                                        [f"UPDATE {db.ACC_CRED} set {db.acc_cred.ENTRY_OTP} = ? where {db.USERNAME} = ?",
                                        (data_key, self.user_entry.get())]])
                self.withdraw()
                _db(self, data_key, current_datetime)

        def set_scale(resolution: tuple[int, int] = None):
            scaling_dictionary = {(1920,1080): 1.5, (1536, 864): 1.25, (1280,720): 1, (1097,617):0.85}
            
            if resolution:
               return scaling_dictionary.get(resolution)
            
            
        '''Import Icons and Images'''
        self.bg_img = ctk.CTkImage(light_image=Image.open("image/bg.png"),size=(1920,1080))
        self.logo_img = ctk.CTkImage(light_image=Image.open("image/logo.png"),size=(80,80))
        self.user_icon = ctk.CTkImage(light_image=Image.open("image/user_icon.png"),size=(30,30))
        self.pass_icon = ctk.CTkImage(light_image=Image.open("image/pass_icon.png"),size=(30,30))
        self.show_icon = ctk.CTkImage(light_image=Image.open("image/view.png"),size=(28,28))
        self.hide_icon = ctk.CTkImage(light_image=Image.open("image/hide.png"),size=(28,28))


        '''Setting values of the root window'''
        title_name = "J.Z. Angeles Veterinary Clinic"
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        #print(set_scale((width, height)))
        
        
        #ctk.set_widget_scaling(set_scale((width, height)))
        #ctk.set_window_scaling(set_scale((width, height)))
        #print( width, height, '|', set_scale((width, height)))
        
        root_w = 500
        root_h = 600
        pos_x = width/2 - root_w/2
        pos_y = height/2 - root_h/2

        #self.attributes("-fullscreen", True)
        self.title(title_name)
        self.geometry('%dx%d+%d+%d' % (root_w,root_h,pos_x,pos_y))
        self.minsize(root_w,root_h)
        self.configure(fg_color=Color.Blue_Oxford)
        
        '''Background Image'''
        self.main_bg = ctk.CTkLabel(self, text='', image=self.bg_img)
        self.main_bg.place(x=0, y=0, relwidth=1, relheight=1)

        '''Main frame'''
        self.main_frame =  ctk.CTkFrame(self,corner_radius=5, height=self._current_height - 80, width=self._current_width - 130,
                                        fg_color=Color.White_Lotion, bg_color=Color.Blue_LapisLazuli)
        self.main_frame.place(relx=0.5, rely=0.5, anchor='c')
        self.main_frame.grid_propagate(False)

        self.main_frame.grid_columnconfigure(0,weight=1)
        self.main_frame.grid_rowconfigure(6, weight=1)

        '''container for company logo and name'''
        self.title_cont = ctk.CTkFrame(self.main_frame, fg_color='transparent')
        self.title_cont.grid(row=0,column=0, padx=10, pady=(40,10))

        self.logo_label = ctk.CTkLabel(self.title_cont, text="", image=self.logo_img)
        self.logo_label.pack(side='left',padx=(10,5), pady=10)
        self.name_label = ctk.CTkLabel(self.title_cont, text=title_name, font=('DM Sans Medium',23),
                                       wraplength=200, justify='left', text_color=Color.Blue_Maastricht)
        self.name_label.pack(side='right',padx=(5,10), pady=10)

        self.login_label = ctk.CTkLabel(self.main_frame, text='Login', font=('DM Sans Medium',22),
                                        text_color=Color.Blue_Maastricht)
        self.login_label.grid(row=1,column=0,sticky="w",padx=(42,10),pady=(10,5))

        self.user_label = ctk.CTkLabel(self.main_frame, text='Username', font=('DM Sans Medium',17),
                                       text_color=Color.Grey_Davy)
        self.user_label.grid(row=2, column=0,sticky='sw',padx=(42,10),pady=(0,0))

        '''Frame for the username entry'''
        self.user_frame = ctk.CTkFrame(self.main_frame, border_color=Color.Grey_Davy, border_width=2,
                                       fg_color=Color.White_Milk)
        self.user_frame.grid(row=3, column=0,sticky='ew',padx=(44,35))

        self.user_icon_label = ctk.CTkLabel(self.user_frame, text='', image=self.user_icon)
        self.user_icon_label.pack(side='left', padx=(5,0),pady=(5))
        self.user_entry = ctk.CTkEntry(self.user_frame, height=round(height * 0.03),font=('DM Sans Medium',16),border_width=0,
                                       fg_color=Color.White_Milk, text_color=Color.Blue_Maastricht)
        self.user_entry.pack(side='right', fill='x', expand=True,padx=(5,10),pady=(5))

        self.password_label = ctk.CTkLabel(self.main_frame, text='Password', font=('DM Sans Medium',17),
                                       text_color=Color.Grey_Davy)
        self.password_label.grid(row=4, column=0,sticky='sw',padx=(42,10),pady=(20,0))

        '''Frame for the password entry'''
        self.pass_frame = ctk.CTkFrame(self.main_frame, border_color=Color.Grey_Davy, border_width=2,
                                       fg_color=Color.White_Milk)
        self.pass_frame.grid(row=5, column=0,sticky='ew',padx=(44,35))

        self.pass_icon_label = ctk.CTkLabel(self.pass_frame, text='',image=self.pass_icon)
        self.pass_icon_label.pack(side='left', padx=(5,0),pady=(5))

        self.password_entry = ctk.CTkEntry(self.pass_frame,height=round(height * 0.03),font=('DM Sans Medium',16),border_width=0,
                                       fg_color=Color.White_Milk, show='●')
        self.password_entry.pack(side='left', fill='x', expand=True,padx=(3),pady=(5))
        self.show_pass_btn =ctk.CTkButton(self.pass_frame,width=28,height=28, image=self.hide_icon, text="",fg_color='transparent', hover=False,
                                          command=self.show_pass)
        self.show_pass_btn.pack(side='right', padx=(0,5), pady=(5))
        '''login button'''
        self.login_button = ctk.CTkButton(self.main_frame, text="LOGIN", height=50,
                                          font=('DM Sans Medium',20),text_color='#FFFFFF',
                                          fg_color=Color.Blue_Cobalt,corner_radius=5,
                                          command= partial(login, None)
                                          )
        self.login_button.grid(row=7, column=0, sticky='nsew', padx=(42,35),pady=(0,35))

        '''shortcut key'''
        self.bind('<Return>', login)

    '''For showing the password'''
    def show_pass(self):
        if self.__is_PasswordVisible is True:
            self.password_entry.configure(show="")
            self.show_pass_btn.configure(image=self.show_icon)
            self.__is_PasswordVisible = False
        else:
            self.password_entry.configure(show="*")
            self.show_pass_btn.configure(image=self.hide_icon)
            self.__is_PasswordVisible = True

    def wm_deiconify(self) -> None:
        self.password_entry.delete(0, ctk.END)
        return super().wm_deiconify()

if __name__ == '__main__':
    if database.fetch_db_profile() is None:
        messagebox.showerror("Database Error", "Unable to Connect to the database\nProceed to database and network settings")
    else:
        Data = subprocess.check_output(['wmic', 'product', 'get', 'name']) 
        a = str(Data) 
        try: 
            for i in range(len(a)): 
                app = a.split("\\r\\r\\n")[6:][i]
                if 'MariaDB' in app:
                    if float(app.split(' ')[1]) < 11:
                        messagebox.showwarning("Old MariaDB Version", "The Version of your MariaDB was\nbelow the requirements (v 11.0)\nInstall the version 11.0 or latest")
                        break
                    else:
                        app = loginUI()
                        app.mainloop()
                        break
        except IndexError as e: 
            messagebox.showerror("Unable to proceed", "MariaDB is not installed on your computer,\nInstall version 11.0 or the latest")

    #app = loginUI()
    #app.mainloop()