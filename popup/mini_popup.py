import customtkinter as ctk
from typing import Optional
from Theme import Color
from util import database
from util import *
from tkinter import messagebox
from PIL import Image
from typing import *
from customcustomtkinter import customcustomtkinter as cctk
import sql_commands
from constants import action
from datetime import datetime

def authorization(master, info:tuple, command_callback :Optional[callable] = None, roles: str = "('Assisstant', 'Owner')"):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, command_callback :Optional[callable]):
            width = info[0] * .4
            height = info[1] * .4
            super().__init__(master, width, height, corner_radius= 0, fg_color="white")
            self.command_callback = command_callback
            self.user_name_authorized_by = None
            self.pack_propagate(0)
            self._border_color = Color.White_Platinum
            self.authorized_roles = roles

            self.user_icon = ctk.CTkImage(light_image=Image.open("image/user_icon.png"),size=(30,30))
            self.pass_icon = ctk.CTkImage(light_image=Image.open("image/pass_icon.png"),size=(30,30))
            self.show_icon = ctk.CTkImage(light_image=Image.open("image/view.png"),size=(28,28))
            self.hide_icon = ctk.CTkImage(light_image=Image.open("image/hide.png"),size=(28,28))

            self.upper_frame = ctk.CTkFrame(self, height= height * .15, fg_color= Color.Blue_Yale, corner_radius= 0)
            self.upper_frame.pack(fill = 'x', padx=(1),pady=(1,0))
            self.upper_frame.pack_propagate(0)

            ctk.CTkLabel(self.upper_frame, text = 'Authorization', font=("DM Sans Medium", 16), text_color= 'white').pack(side = 'left', padx = (width * .01, 0))
            self.close_btn = ctk.CTkButton(self.upper_frame,  height * .12, height * .12, text= 'x', command=self.reset)

            self.close_btn.pack(side = ctk.RIGHT, padx = (0, width * .005))
            
            self.main_frame = ctk.CTkFrame(self, fg_color=Color.White_Lotion,height= height *.87, corner_radius= 0)
            self.main_frame.pack(fill = ctk.BOTH, padx=(1),pady=(0,1))
            self.main_frame.grid_propagate(0)

            self.user_label = ctk.CTkLabel(self.main_frame, text='Administrator Username', font=('DM Sans Medium',17),
                                       text_color=Color.Grey_Davy)
            self.user_label.grid(row=2, column=0,sticky='sw',pady = (width * .025, 0), padx = 44)

            self.user_frame = ctk.CTkFrame(self.main_frame, border_color=Color.Grey_Davy, border_width=2,
                                        fg_color=Color.White_Milk, width = width * .75)
            self.user_frame.grid(row=3, column=0,sticky='ew', padx=(35))

            self.user_icon_label = ctk.CTkLabel(self.user_frame, text='', image=self.user_icon)
            self.user_icon_label.pack(side='left', padx=(5,0),pady=(5))
            self.user_entry = ctk.CTkEntry(self.user_frame, width = width * .75, height=round(height * 0.03),font=('DM Sans Medium',16),border_width=0,
                                        fg_color=Color.White_Milk, text_color=Color.Blue_Maastricht)
            self.user_entry.pack(side='right', fill='x', expand=True,padx=(5,10),pady=(5))

            self.password_label = ctk.CTkLabel(self.main_frame, text='Password', font=('DM Sans Medium',17),
                                        text_color=Color.Grey_Davy)
            self.password_label.grid(row=4, column=0,sticky='sw',padx=(44,44),pady=(10,0))

            '''Frame for the password entry'''
            self.pass_frame = ctk.CTkFrame(self.main_frame, border_color=Color.Grey_Davy, border_width=2,
                                        fg_color=Color.White_Milk, width = width * .75)
            self.pass_frame.grid(row=5, column=0,sticky='ew',padx=(35))

            self.pass_icon_label = ctk.CTkLabel(self.pass_frame, text='',image=self.pass_icon)
            self.pass_icon_label.pack(side='left', padx=(5,0),pady=(5))

            self.password_entry = ctk.CTkEntry(self.pass_frame,height=round(height * 0.03),font=('DM Sans Medium',16),border_width=0,
                                        fg_color=Color.White_Milk, show='●', width = width * .75, text_color= 'black')
            self.password_entry.pack(side='left', fill='x', expand=True,padx=(3),pady=(5))
            
            self.login_button = ctk.CTkButton(self.main_frame, text="Authorize", height=45,
                                          font=('DM Sans Medium',16),text_color='#FFFFFF',
                                          fg_color=Color.Blue_Cobalt,corner_radius=5,
                                          command= self.authorize)
            self.login_button.grid(row=7, column=0, sticky='nse', padx=(42,35),pady=(20,35))


        def authorize(self, _: any = None):
            try:
                salt = database.fetch_data(f'SELECT {db.acc_cred.SALT} FROM {db.ACC_CRED} WHERE {db.USERNAME} COLLATE LATIN1_GENERAL_CS = ?',
                                        (self.user_entry.get(), ))[0][0]
            except IndexError:
                self.password_entry.delete(0, ctk.END)
                messagebox.showinfo('Error', 'Username Or Password Incorrect', parent = self)
                return
            _db = f"SELECT COUNT(*)\
                  FROM acc_cred\
                  JOIN acc_info\
                      ON acc_cred.usn = acc_info.usn\
                  WHERE acc_cred.usn COLLATE LATIN1_GENERAL_CS = ?\
                          AND acc_cred.pss = ?\
                          AND acc_info.job_position IN {self.authorized_roles}"
            print(_db)
            count = database.fetch_data(_db ,(self.user_entry.get(), encrypt.pass_encrypt(self.password_entry.get(), salt)['pass']))
            if count[0][0] == 0:
                self.password_entry.delete(0, ctk.END)
                messagebox.showinfo('Error', 'Username Or Password Incorrect', parent = self)
            else:
                if database.fetch_data('SELECT state FROM acc_info WHERE usn = ?', (self.user_entry.get(), ))[0][0] == 0:
                    messagebox.showerror("Failed to Login", "The Account you're been\nlogged has been deactivated.\nInquire to the Owner", parent = self)
                    return

                self.user_name_authorized_by = self.user_entry.get()

                if callable(self.command_callback):
                    self.command_callback()
                self.reset()

        def reset(self):
            self.password_entry.delete(0, ctk.END)
            self.user_entry.delete(0, ctk.END)
            self.place_forget()
            pass

    return instance(master, info, command_callback)

def stock_disposal(master, info:tuple, command_callback: callable = None):
    class stock_disposal(ctk.CTkFrame):
        def __init__(self, master, info:tuple, command_callback):
            width = info[0]
            height = info[1]
            self.acc_user = info[2][0][0]
            self.is_expiry_type = False
            super().__init__(master, width=width*0.4, height=height*0.55, corner_radius= 0, fg_color='transparent')
            
            self.command_callback = command_callback
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)

            self.restock = ctk.CTkImage(light_image=Image.open("image/restock_plus.png"), size=(20,20))
            self.calendar_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(18,20))
            
            disp_reason = ['Expired', 'Defective/Damaged']
            disp_reason_nexp = ['Defective/Damaged']
            
            self.combo_var = ctk.StringVar(value="")
            
            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3],)
            self.main_frame.grid(row=0, column=0, sticky="nsew")
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=4,sticky="nsew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text='', image=self.restock, anchor='w', fg_color="transparent").pack(side="left", padx=(width*0.01,0))    
            ctk.CTkLabel(self.top_frame, text='STOCK DISPOSAL', anchor='w', corner_radius=0, font=("DM Sans Medium", 14), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.0025,0))
            
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=self.reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.confirm_frame= ctk.CTkFrame(self.main_frame,fg_color=Color.White_Color[2],)
            self.confirm_frame.grid(row=1,column=0, sticky="nsew",  padx=(width*0.005), pady = (height*0.01))
            self.confirm_frame.grid_columnconfigure(0, weight=1)
            
            """NAME"""
            self.item_frame = ctk.CTkFrame(self.confirm_frame, fg_color=Color.White_Lotion)
            self.item_frame.grid(row=0, column=0, sticky='nsew', pady = (height*0.025,height*0.01), padx = (width*0.005))
            ctk.CTkLabel(self.item_frame, text="Item Name: ", font=("DM Sans Medium", 14), width=width*0.025, ).pack(side='left',pady = (height*0.01), padx = (width*0.05,0))
            self.item_name = ctk.CTkLabel(self.item_frame, text="", font=("DM Sans Medium", 14))
            self.item_name.pack(side='left',pady = (height*0.01), padx = (0))
            
            
            """EXPIRY"""
            self.expiry_frame = ctk.CTkFrame(self.confirm_frame, fg_color=Color.White_Lotion)
            
            ctk.CTkLabel(self.expiry_frame, text="Expiration Date: ", font=("DM Sans Medium", 14), width=width*0.025, ).pack(side='left',pady = (height*0.01), padx = (width*0.05,0))
            self.expiry_selection = ctk.CTkOptionMenu(self.expiry_frame, font=("DM Sans Medium", 14), corner_radius= 5, height=height*0.05, width=width*0.25)
            self.expiry_selection.set("Select an Expiry")
            self.expiry_selection.pack(side='left' ,pady = (height*0.01), padx = (0,width*0.005), fill = 'x')
            
            self.expiry_frame.grid(row=1, column=0, sticky='nsew', pady = (width*0.005), padx = (width*0.005))
            
            '''QUANTITY'''
            self.quantity_frame = ctk.CTkFrame(self.confirm_frame, fg_color=Color.White_Lotion)
            self.quantity_frame.grid(row=2, column=0, sticky='nsew', pady = (width*0.005), padx = (width*0.005))
            ctk.CTkLabel(self.quantity_frame, text="Item Quantity: ", font=("DM Sans Medium", 14), width=width*0.025, ).pack(side='left',pady = (height*0.01), padx = (width*0.05,0))
            self.stock_entry = cctk.cctkSpinnerCombo(self.quantity_frame, entry_font=("DM Mono Medium",14), val_range=(0, cctk.cctkSpinnerCombo.MAX_VAL))
            self.stock_entry.pack(side='left',pady = (height*0.01), padx = (0))

            ctk.CTkLabel(self.confirm_frame, text="Reason for disposal ", font=("DM Sans Medium", 14), width=width*0.06, anchor="e").grid(row=4, column=0, sticky="nsw",pady = (height*0.01,0), padx = (width*0.01))
            self.disposal_entry = ctk.CTkOptionMenu(self.confirm_frame, font=("DM Sans Medium",14), height=height*0.055, values=disp_reason, variable=self.combo_var, button_color=Color.Blue_Tufts,
                                                button_hover_color=Color.Blue_Steel)
            self.disposal_entry.grid(row = 5, column = 0,sticky = 'nsew', pady = (0,height*0.01), padx = (width*0.01))
            self.disposal_entry.set("Select a Reason")
            
            '''Action Frame'''
            self.action_frame = ctk.CTkFrame(self.main_frame, corner_radius=5, fg_color=Color.White_Color[2])
            self.action_frame.grid(row = 2, column = 0, sticky = 'nsew', padx=(width*0.005), pady = (0,height*0.01))
            self.action_frame.grid_columnconfigure((0,1), weight=1)
            
            self.cancel_btn = ctk.CTkButton(self.action_frame, width=width*0.075, height=height*0.05,corner_radius=5,  fg_color=Color.Red_Pastel, hover_color=Color.Red_Tulip,
                                            font=("DM Sans Medium", 16), text='Cancel', command= self.reset)
            self.cancel_btn.pack(side="left",  padx = (width*0.0075,0), pady= height*0.01) 
            
            self.dispose_btn = ctk.CTkButton(self.action_frame, width=width*0.1, height=height*0.05,corner_radius=5, font=("DM Sans Medium", 16), text='Confirm',
                                            command=self.proceed)
            self.dispose_btn.pack(side="right",  padx = (width*0.0075), pady= height*0.01)

            '''PLACEMENT'''
            # Inventory_popup.stock_disposal(self,(width, height, acc_cred, acc_info), command_callback=None).place(relx=0.5, rely=0.5,anchor='c')
        def proceed(self):
            if self.disposal_entry.get() == "Select a Reason":
                messagebox.showerror("Cannot proceed","Select a reason to continue", parent = self)
                return
            
            if self.is_expiry_type:
                date = datetime.strptime(self.expiry_selection.get(), '%b %d, %Y')
                if date > datetime.now() and 'Expired' in self.disposal_entry.get():
                    messagebox.showerror("Cannot proceed","Item aren't expired yet", parent = self)
                    return
                quantity_needed = self.stock_entry.get()
                stocks = database.fetch_data(sql_commands.get_specific_stock_ordered_by_date_added_including_not_sellable_for_expiry, (self.uid, date))
                
                for st in stocks:
                    if st[2] == quantity_needed and st == stocks[-1]:
                        database.exec_nonquery([[sql_commands.null_stocks_by_id, (st[0], )]])
                    elif st[2] > quantity_needed:
                        database.exec_nonquery([[sql_commands.deduct_stocks_by_id, (quantity_needed, st[0])]])
                        quantity_needed = 0
                        break
                        #if the  stock of an instance is higher than needed stock
                    elif st[2] <= quantity_needed:
                        database.exec_nonquery([[sql_commands.delete_stocks_by_id, (st[0], )]])
                        quantity_needed -= st[2]
                        #if the stock needed is higher than stock instance
            else:
                date = datetime.strptime(self.expiry_selection.get(), '%b %d, %Y')
                if date > datetime.now() and 'Expired' in self.disposal_entry.get():
                    messagebox.showerror("Cannot proceed","Item aren't expired yet", parent = self)
                    return
                quantity_needed = self.stock_entry.get()
                stocks = database.fetch_data(sql_commands.get_specific_stock_ordered_by_date_added_including_not_sellable, (self.uid, ))
                
                for st in stocks:
                    if st[2] == quantity_needed and st == stocks[-1]:
                        database.exec_nonquery([[sql_commands.null_stocks_by_id, (st[0], )]])
                    elif st[2] > quantity_needed:
                        database.exec_nonquery([[sql_commands.deduct_stocks_by_id, (quantity_needed, st[0])]])
                        quantity_needed = 0
                        break
                        #if the  stock of an instance is higher than needed stock
                    elif st[2] <= quantity_needed:
                        database.exec_nonquery([[sql_commands.delete_stocks_by_id, (st[0], )]])
                        quantity_needed -= st[2]
                        #if the stock needed is higher than stock instance
            record_action(self.acc_user, action.DISPOSAL_TYPE, action.ITEM_DISPOSAL % (self.uid, self.stock_entry.get(), self.acc_user))
            database.exec_nonquery([[sql_commands.set_expired_items_from_inventory, (generateId("DIS",6).upper(), None, self.uid, self.data[2], self.stock_entry.get(), self.disposal_entry.get(), self.acc_user)]])
            messagebox.showinfo("Success", "Itemp Dispose\nNote! this will be recorded", parent = self)
            self.stock_entry.set(1)
            self.reset()
        
        def reset(self):
            self.command_callback()
            self.place_forget()

        def set_quantity_limit(self):
            if self.is_expiry_type:
                date = datetime.strptime(self.expiry_selection.get(), '%b %d, %Y').strftime('%Y-%m-%d')
                max_stock = database.fetch_data(sql_commands.get_all_item_quantity_by_id_and_expiry, (self.uid, date))[0][0]
                self.stock_entry.configure(val_range = (1, int(max_stock)))
            else:
                max_stock = database.fetch_data(sql_commands.get_all_item_quantity_by_id, (self.uid, ))[0][0]
                self.stock_entry.configure(val_range = (1, int(max_stock)))
        
        def place(self, data: tuple, **kwargs):
            self.data = data
            self.uid = database.fetch_data(sql_commands.get_uid_by_brand_and_mofidied_name, (data[1], data[2], data[1], data[2]))[0][0]
            self.item_name.configure(text = data[2])
            self.is_expiry_type = data[-2] is not None

            if self.is_expiry_type:
                self.disposal_entry.configure(values = ['Expired', 'Defective/Damaged'])
                self.expiry_selection.configure(state = ctk.NORMAL)
                expiries = [s[0] for s in database.fetch_data(sql_commands.get_all_expiry_of_items_by_id, (self.uid,))]
                self.expiry_selection.configure(values = expiries)
                self.expiry_selection.set(data[-2])
            else:
                self.disposal_entry.configure(values = ['Defective/Damaged'])
                self.expiry_selection.set("Item Doesn't Expire")
                self.expiry_selection.configure(state = ctk.DISABLED)

            self.set_quantity_limit()
            return super().place(**kwargs)
        
            
    return stock_disposal(master, info, command_callback)