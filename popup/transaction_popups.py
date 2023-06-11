import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
import sql_commands
from util import *
from tkinter import messagebox
from constants import action
from customtkinter.windows.widgets.core_widget_classes import DropdownMenu
from decimal import Decimal
import datetime
from PIL import Image

def show_item_list(master, info:tuple):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple):
            self._master = master
            width = info[0]
            height = info[1]
            #self._treeview: cctk.cctkTreeView = info[2]
            super().__init__(master, corner_radius= 0)
            
            self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(15,15))
            
            self.main_frame = ctk.CTkFrame(self, width=width*0.525, height=height*0.85, corner_radius=0)
            self.main_frame.pack()
            self.main_frame.pack_propagate(0)
            
            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.pack(fill="both", expand=0)

            ctk.CTkLabel(self.top_frame, text='Add Items', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.015,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=self.reset).pack(side="right", padx=(0,width*0.01),pady=height*0.005)
            
            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Color[3])
            self.content_frame.pack(fill="both", expand=1, padx=width*0.005, pady=height*0.01)
            self.content_frame.grid_columnconfigure(0, weight=1)
            self.content_frame.grid_propagate(0)

            self.search_frame = ctk.CTkFrame(self.content_frame, fg_color="light grey", width=width*0.35, height = height*0.05,)
            self.search_frame.grid(row=0, column=0,padx=(width*0.0075), pady=(height*0.01,0),sticky="w")
            self.search_frame.pack_propagate(0)

            ctk.CTkLabel(self.search_frame,text="Search", font=("Arial", 14), text_color="grey", fg_color="transparent").pack(side="left", padx=(width*0.0075,width*0.0025))
            self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Type here...", border_width=0, corner_radius=5, fg_color="white")
            self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)
            self.search_btn = ctk.CTkButton(self.search_frame, text="", image=self.search, fg_color="white",
                                            width=width*0.005)
            self.search_btn.pack(side="left", padx=(0, width*0.005))
            
            self.data = database.fetch_data(sql_commands.get_item_and_their_total_stock, None)
            self.service_treeview = cctk.cctkTreeView(self.content_frame,data=self.data, height=height*0.65, width=width*0.505, 
                                                      column_format=f"/No:{int(width*.025)}-#r/ItemName:x-tl/Stocks:{int(width*.075)}-tr/Price:{int(width*.1)}-tr!30!30")
            self.service_treeview.grid(row=1, column=0, padx=(width*0.005), pady=(height*0.01), sticky="nsew")
            
            
            """ self.data = database.fetch_data(sql_commands.get_item_and_their_total_stock, None)
            self.item_treeview = cctk.cctkTreeView(self.left_frame, self.data, self.width * .75, self.height * .65,
                                                header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent', record_text_color='black',
                                                column_format=f'/Service:x-tl/Price:{round(self.width * .15)}-tl/Stocks:{round(self.width * .15)}-tl!35!30',
                                                double_click_command= self.get_item)
            self.item_treeview.grid(row=1, column=0, padx=10, pady=10, sticky="ns") """

            """   self.rightmost_frame = ctk.CTkFrame(self.boxframe, height=self.height*0.78, width =self.width*0.312, fg_color='white')
            self.rightmost_frame.grid(row=2, column=0, padx=10, pady=10, sticky="es")

            self.x_fr = ctk.CTkFrame(self.rightmost_frame, height=self.height*0.78, width =self.width*0.312, fg_color='white')
            self.x_fr.grid(row=2, column=0, padx=10, pady=10, sticky="s")
            """ 
            
            self.bottom_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent", width=width*0.25)
            self.bottom_frame.grid(row=2, column=0 )
            self.bottom_frame.grid_propagate(0)
            self.bottom_frame.grid_columnconfigure(1, weight=1)
            self.back_button = ctk.CTkButton(self.bottom_frame, text='Cancel', width=width*0.1, font=("Arial", 14), command=self.reset)
            self.back_button.grid(row=0, column=0, sticky="w")

            self.select_button = ctk.CTkButton(self.bottom_frame, text='Select', width=width*0.1, font=("Arial", 14))
            self.select_button.grid(row=0, column=1, sticky="e") 
            
            """ self.select_button = ctk.CTkButton(self.x_fr, text='Select', command=self.get_item, width =270, font=("Poppins-Bold", 45))
            self.select_button.grid(row=0, column=2, padx=(0, 20), sticky="se") """

        def place(self, **kwargs):
            self.main_frame.pack()
            self.data = database.fetch_data(sql_commands.get_item_and_their_total_stock, None)
            #self.item_treeview.update_table(self.data)
            return super().place(**kwargs)

        def reset(self):
            self.main_frame.place_forget()
            self.place_forget()

        """ def get_item(self, _: any = None):
            #if there's a selected item
            if self.item_treeview.data_grid_btn_mng.active is not None:
                item_name =  self.item_treeview.data_grid_btn_mng.active.winfo_children()[0]._text
                #getting the needed information for the item list
                transaction_data = database.fetch_data(sql_commands.get_item_data_for_transaction, (item_name, ))[0]
                #collects part of the data needed in the transaction
                items_in_treeview = [s.winfo_children()[2]._text if self._treeview.data_frames != [] else None for s in self._treeview.data_frames]
                #search the tree view if there's an already existing item

                #if there's an already existing item
                if(item_name in items_in_treeview):
                    quantity_column: cctk.cctkSpinnerCombo = self._treeview.data_frames[items_in_treeview.index(item_name)].winfo_children()[4].winfo_children()[0]
                    quantity_column.change_value()
                    #change the value of the spinner combo; modifying the record's total price
                else:
                    self._treeview.add_data(transaction_data+(1, transaction_data[2]))
                    quantity_column: cctk.cctkSpinnerCombo = self._treeview.data_frames[-1].winfo_children()[4].winfo_children()[0]
                    price_column: ctk.CTkLabel = self._treeview.data_frames[-1].winfo_children()[6]

                    def spinner_command(mul: int = 0):
                        master.change_total_value_item(-float(price_column._text))
                        #before change

                        price_change = quantity_column._base_val * quantity_column.value
                        master.change_total_value_item(price_change)
                        price_column.configure(text = price_change)
                        #after change
                        postdata = list(self._treeview._data[self._treeview.data_frames.index(quantity_column.master.master)])
                        postdata[3] = quantity_column.value
                        postdata[4] = Decimal(price_change)
                        self._treeview._data[self._treeview.data_frames.index(quantity_column.master.master)] = tuple(postdata)
                        #update the treeview's data

                        if quantity_column._base_val * quantity_column.value >= quantity_column._base_val * quantity_column._val_range[1]:
                            quantity_column.num_entry.configure(text_color = 'red')
                            #messagebox.showinfo('NOTE!', 'Maximum stock reached')
                        else:
                            quantity_column.num_entry.configure(text_color = quantity_column._entry_text_color)

                    quantity_column.configure(command = spinner_command, base_val = transaction_data[2], value = 1, val_range = (1
                    , int(self.item_treeview.data_grid_btn_mng.active.winfo_children()[1]._text)))
                    #add a new record
                    master.change_total_value_item(transaction_data[2])

                self.item_treeview.data_grid_btn_mng.deactivate_active()
                self.reset()
                #reset the state of this popup """
    return instance(master, info)


def show_services_list(master, info:tuple, data_reciever: list):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, data_reciever: list):
            #self._data_reciever = data_reciever
            self._master = master
            width = info[0]
            height = info[1]
            #self._treeview: cctk.cctkTreeView = info[2]
            super().__init__(master, corner_radius= 0)
            
            #ctk.CTkLabel(self, text="HElp").pack()
            self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(15,15))
            
            self.main_frame = ctk.CTkFrame(self, width=width*0.45, height=height*0.85, corner_radius=0)
            self.main_frame.pack()
            self.main_frame.pack_propagate(0)
            
            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.pack(fill="both", expand=0)

            ctk.CTkLabel(self.top_frame, text='Add Service', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.015,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=self.reset).pack(side="right", padx=(0,width*0.01),pady=height*0.005)
            
            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Color[3])
            self.content_frame.pack(fill="both", expand=1, padx=width*0.005, pady=height*0.01)
            self.content_frame.grid_columnconfigure(0, weight=1)
            self.content_frame.grid_propagate(0)
            
            self.search_frame = ctk.CTkFrame(self.content_frame, fg_color="light grey", width=width*0.35, height = height*0.05,)
            self.search_frame.grid(row=0, column=0,padx=(width*0.0075), pady=(height*0.01,0),sticky="w")
            self.search_frame.pack_propagate(0)

            ctk.CTkLabel(self.search_frame,text="Search", font=("Arial", 14), text_color="grey", fg_color="transparent").pack(side="left", padx=(width*0.0075,width*0.0025))
            self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Type here...", border_width=0, corner_radius=5, fg_color="white")
            self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)
            self.search_btn = ctk.CTkButton(self.search_frame, text="", image=self.search, fg_color="white",
                                            width=width*0.005)
            self.search_btn.pack(side="left", padx=(0, width*0.005))

            #self.data = database.fetch_data(sql_commands.get_services_and_their_price)
            self.service_treeview = cctk.cctkTreeView(self.content_frame, height=height*0.65, width=width*0.425, 
                                                      column_format=f"/No:{int(width*.025)}-#r/ServiceName:x-tl/Price:x-tr!30!30")
            self.service_treeview.grid(row=1, column=0, padx=(width*0.005), pady=(height*0.01), sticky="nsew")
            
            """
            self.service_treeview = cctk.cctkTreeView(self.left_frame, height=self.height*0.65, width =self.width*0.785,
                                                      header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent', record_text_color='black',
                                                       column_format='/Services:x-tl/Price:x-tr!35!30',)
                                   
            
           
            self.rightmost_frame = ctk.CTkFrame(self.boxframe, height=self.height*0.78, width =self.width*0.312, fg_color='white')
            self.rightmost_frame.grid(row=2, column=0, padx=10, pady=10, sticky="es")

            self.x_fr = ctk.CTkFrame(self.rightmost_frame, height=self.height*0.78, width =self.width*0.312, fg_color='white')
            self.x_fr.grid(row=2, column=0, padx=10, pady=10, sticky="s")
            """
            self.bottom_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent", width=width*0.25)
            self.bottom_frame.grid(row=2, column=0 )
            self.bottom_frame.grid_propagate(0)
            self.bottom_frame.grid_columnconfigure(1, weight=1)
            self.back_button = ctk.CTkButton(self.bottom_frame, text='Cancel', width=width*0.1, font=("Arial", 14), command=self.reset)
            self.back_button.grid(row=0, column=0, sticky="w")

            self.select_button = ctk.CTkButton(self.bottom_frame, text='Select', width=width*0.1, font=("Arial", 14))
            self.select_button.grid(row=0, column=1, sticky="e") 
            
        def reset(self):
            self.place_forget()
            
        def place(self, **kwargs):
            raw_data = database.fetch_data(sql_commands.get_services_and_their_price, None)
            self.main_frame.pack()
            self.data = [(s[1], s[3]) for s in raw_data]
            self.service_treeview.update_table(self.data)
            return super().place(**kwargs)


        def get_service(self, _: any = None):
            #if there's a selected item
            if self.service_treeview.data_grid_btn_mng.active is not None:
                service_name =  self.service_treeview.data_grid_btn_mng.active.winfo_children()[0]._text
                #getting the needed information for the item list
                transaction_data = database.fetch_data(sql_commands.get_services_data_for_transaction, (service_name, ))[0]
                self._treeview.add_data(transaction_data+(0, transaction_data[2]))
                info_tab:cctk.info_tab = self._treeview.data_frames[-1].winfo_children()[3]
                info_tab._tab = customer_info(self._treeview.master.master, (info[0] * .8, info[1] * .8), info_tab)
                info_tab.button.configure(command = lambda: info_tab._tab.place(relx = .5, rely = .5, anchor = 'c'))
                self._data_reciever.append(info_tab)
                info_tab._tab.place(relx = .5, rely = .5, anchor = 'c')


                master.change_total_value_service(transaction_data[2])
                self.service_treeview.data_grid_btn_mng.deactivate_active()
                self.reset() 
                #reset the state of this popup
    return instance(master, info, data_reciever)

def show_transaction_proceed(master, info:tuple, item_info: list, services_info, total_price: float, customer_info: str, pets_info: List) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, item_info: list, services_info, total_price: float, customer_info: str, pets_raw_info: List):
            width = info[0] * .99
            height = info[1] * .99
            #basic inforamtion needed; measurement
            self._customer_info = customer_info
            self._pets_raw_info = pets_raw_info
            if(self._pets_raw_info is not None):
                self.pets_info = [s.value for s in self._pets_raw_info]
            self.acc_cred = info[3]
            self._treeview = info[2]
            self._item_info = item_info
            self._services_info = services_info
            self._total_price = total_price
            #encapsulation

            super().__init__(master, width, height=height, corner_radius= 0, fg_color='white')
            #the actual frame, modification on the frame itself goes here

            '''events'''
            def auto_pay(_: any = None):
                self.payment_entry.delete(0, ctk.END)
                self.payment_entry.insert(0, self._total_price)
                record_transaction()

            def record_transaction():
                if (float(self.payment_entry.get() or '0')) < self._total_price:
                    messagebox.showinfo('Invalid', 'Pay the right amount')
                    return
                record_id =  database.fetch_data(sql_commands.generate_id_transaction, (None))[0][0]
                database.exec_nonquery([[sql_commands.record_transaction, (record_id, self.acc_cred[0], self._customer_info, self._total_price)]])
                #record the transaction

                modified_items_list = [(record_id, s[0], s[1], s[3], float(s[2]), 0) for s in self._item_info]
                database.exec_nonquery([[sql_commands.record_item_transaction_content, s] for s in modified_items_list])
                #record the items from eithin the transaction

                modified_services_list = [(record_id, s[0], s[1], customer_info, str(datetime.datetime.strptime(self.pets_info[0][2], '%m-%d-%Y').strftime('%Y-%m-%d')), float(s[2]), 0, 0) for s in self._services_info]
                database.exec_nonquery([[sql_commands.record_services_transaction_content, s] for s in modified_services_list])
                #record the services from eithin the transaction


                for item in modified_items_list:
                    stocks = database.fetch_data(sql_commands.get_specific_stock, (item[1], ))
                    if stocks[0][2] is None:
                        database.exec_nonquery([[sql_commands.update_non_expiry_stock, (-item[3], item[1])]])
                    else:
                        quan = item[3]
                        for st in stocks:
                            if st[1] < quan:
                                quan -= st[1]
                                database.exec_nonquery([['DELETE FROM item_inventory_info WHERE UID = ? AND Expiry_Date = ?', (st[0], st[2])]])
                            elif st[1] > quan:
                                database.exec_nonquery([[sql_commands.update_expiry_stock, (-quan, item[1], st[2])]])
                                break
                            else:
                                if stocks[-1] == st:
                                    database.exec_nonquery([[sql_commands.update_expiry_stock, (-quan, item[1], st[2])]])
                                else:
                                    database.exec_nonquery([['DELETE FROM item_inventory_info WHERE UID = ? AND Expiry_Date = ?', (st[0], st[2])]])
                                break
                #modify the stock

                payment = float(self.payment_entry.get())
                self.payment_entry.configure(text_color = 'red')
                self.payment_entry.delete(0, ctk.END)
                self.payment_entry.insert(0, format_price(round(self._total_price - payment, 2)))
                #calculate and show the change

                master.reset()
                messagebox.showinfo('Sucess', 'Transaction Complete')
                self._treeview[0].delete_all_data()
                self._treeview[1].delete_all_data()
                self.destroy()
                #reset into its default state

            self.left_frame = ctk.CTkFrame(self)
            self.left_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsw")

            self.services_lbl = ctk.CTkLabel(self.left_frame, text='Services:',font=("Poppins", 45))
            self.services_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

            '''self.services_entry = ctk.CTkEntry(self.left_frame,  height=height*0.78, width=width*0.2)
            self.services_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ns")'''
            self.service_data = [(f'{s[1]}', format_price(float(s[4]))) for s in self._services_info]
            self.service_list = cctk.cctkTreeView(self.left_frame, self.service_data, height=height*0.75, width=width*0.2,
                                                  header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent', record_text_color='black',
                                                  column_format=f'/No:{int(width * .03)}-#c/Name:x-tl/Price:{int(width * .05)}-tr!50!30')
            self.service_list.grid(row=1, column=0, padx=10, pady=10, sticky="ns")

            self.right_frame = ctk.CTkFrame(self)
            self.right_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

            self.items_lbl = ctk.CTkLabel(self.right_frame, text='Items:',font=("Poppins", 45))
            self.items_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
            print(self._item_info)
            self.item_data = [(f'{s[1]} * {s[3]}', format_price(float(s[4]))) for s in self._item_info]
            self.item_list = cctk.cctkTreeView(self.right_frame, self.item_data, height=height*0.75, width=width*0.2,
                                               header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent', record_text_color='black',
                                               column_format=f'/No:{int(width * .03)}-#c/Name:x-tl/Price:{int(width * .05)}-tr!50!30')
            self.item_list.grid(row=1, column=0, padx=10, pady=10, sticky="ns")

            self.rightmost_frame = ctk.CTkFrame(self, height=height*0.78, width=width*0.312, fg_color='white')
            self.rightmost_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nse")


            self.total_frame = ctk.CTkFrame(self.rightmost_frame)
            self.total_frame.grid(row=0, column=0, padx=10, pady=10, sticky="new", columnspan = 2)

            self.total_lbl = ctk.CTkLabel(self.total_frame, text='Total:',font=("Poppins", 25))
            self.total_lbl.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")

            self.total_val = ctk.CTkEntry(self.total_frame, height=height*0.12, width=width*0.31, font=('DM Sans Medium', 35))
            self.total_val.insert(0, format_price(self._total_price))
            self.total_val.configure(state = 'readonly')
            self.total_val.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="n")

            self.payment_options_frame = ctk.CTkFrame(self.rightmost_frame)
            self.payment_options_frame.grid(row=1, column=0, padx=10, pady=(10, height*0.22), sticky="new", columnspan = 2)

            self.payment_lbl = ctk.CTkLabel(self.payment_options_frame, text='Payment Method:', font=("Poppins", 25))
            self.payment_lbl.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")

            self.payment_method_cbox = ctk.CTkOptionMenu(self.payment_options_frame, values=["Cash", "Card", "Bank Statement"], font=("Poppins", 25), height=height*0.08,width=width*0.31
                                                         ,fg_color='white', button_color='#dddddd', text_color='black')
            self.payment_method_cbox.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")

            self.payment_frame = ctk.CTkFrame(self.rightmost_frame)
            self.payment_frame.grid(row=3, column=0, padx=10, pady=(20, 10), sticky="new", columnspan = 2)

            self.payment_lbl = ctk.CTkLabel(self.payment_frame, text='Payment:',font=("Poppins", 25))
            self.payment_lbl.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")

            self.payment_entry = ctk.CTkEntry(self.payment_frame, height=height*0.12, width=width*0.31, font=('DM Sans Medium', 35))
            self.payment_entry.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="n")

            self.proceed_button = ctk.CTkButton(self.rightmost_frame, text='Proceed', command=record_transaction, width=135, font=("Poppins-Bold", 45))
            self.proceed_button.grid(row=4, column=0, padx=(40, 50), pady =(10,10), sticky="ew")

            self.cancel_button = ctk.CTkButton(self.rightmost_frame, text='Cancel', command= lambda: self.destroy(), width=135, font=("Poppins-Bold", 45))
            self.cancel_button.grid(row=4, column=1, padx=(40, 50), pady =(10,10), sticky="ew")

            self.payment_entry.focus_force()
            self.payment_entry.bind('<Shift-Return>', auto_pay)
    return instance(master, info, item_info, services_info, total_price, customer_info, pets_info)

def customer_info(master, info:tuple, parent= None) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, parent):
            width = info[0]
            height = info[1]
            #basic inforamtion needed; measurement

            super().__init__(master, width * 0.95, height=height*0.95, corner_radius= 0, fg_color="transparent")
            #the actual frame, modification on the frame itself goes here
            self.value:tuple = (None, None, None, None)
            #self.grid_propagate(0)

            def hide():
                self.place_forget()
                self.pack_forget()
                self.grid_forget()

            def discard():
                if (self.pet_name.get() != self.value[0] or self.animal_breed_entry.get() != self.value[1] or
                self.scheduled_service_val._text != self.value[2] or self.note_entry.get() != self.value[3]):
                    if messagebox.askyesno('NOTE!', 'all changes will be discarded?'):
                        self.pet_name.delete(0, ctk.END)
                        self.animal_breed_entry.delete(0, ctk.END)
                        self.note_entry.delete(0, ctk.END)
                        self.pet_name.insert(0, self.value[0] or '')
                        self.animal_breed_entry.insert(0, self.value[1] or '')
                        self.scheduled_service_val.configure( text = self.value[2] or '')
                        self.note_entry.insert(0, self.value[3] or '')
                hide()


            def record():
                self.value = (self.pet_name.get(), self.animal_breed_entry.get(), self.scheduled_service_val._text, self.note_entry.get())
                if isinstance(parent, cctk.info_tab):
                    parent.button.configure(text = f'{self.pet_name.get()}%s info (click to edit)'%('\'s' if self.pet_name.get()[-1] != 's' else '\''))
                    parent.value = self.value
                hide()


            self.left_frame = ctk.CTkFrame(self, bg_color='#c3c3c3')
            self.left_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsw")

            self.pet_info_lbl = ctk.CTkLabel(self.left_frame, text='Pet Info',font=("Poppins", 45))
            self.pet_info_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
            #Name label
            self.Name_lbl = ctk.CTkLabel(self.left_frame, text='Name:',font=("Poppins", 25))
            self.Name_lbl.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nw")
            #Name entry
            self.pet_name = ctk.CTkEntry(self.left_frame, placeholder_text='chao pan', height=height*0.09, width=width*0.795, font=("Poppins", 25))
            self.pet_name.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ns")
            #Breed and Animal Type label
            self.animal_breed_lbl = ctk.CTkLabel(self.left_frame, text='Breed and Animal Type:',font=("Poppins", 25))
            self.animal_breed_lbl.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="nw")
            #Breed and Animal Type entry
            self.animal_breed_entry = ctk.CTkEntry(self.left_frame, placeholder_text='dog', height=height*0.09, width=width*0.795, font=("Poppins", 25))
            self.animal_breed_entry.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ns")
            #calendar and note frame
            self.middle_frame = ctk.CTkFrame(self.left_frame, bg_color='#D9D9D9', fg_color='#D9D9D9')
            self.middle_frame.grid(row=5, column=0, padx=10, pady=(20, 10), sticky="nsw")
            #sched service frame
            self.schedule_service_frame = ctk.CTkFrame(self.middle_frame, bg_color='#D9D9D9')
            self.schedule_service_frame.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="nsw")
            #Scheduled service label
            self.scheduled_service_lbl = ctk.CTkLabel(self.schedule_service_frame, text='Scheduled Service:',font=("Poppins", 25))
            self.scheduled_service_lbl.grid(row=0, column=0, padx=(10, 0), pady=(0, 10), sticky="nw")
            #Scheduled service label
            self.scheduled_service_val = ctk.CTkLabel(self.schedule_service_frame, height=height*0.09, width=width*0.285, font=("Poppins", 25), fg_color='white')
            self.scheduled_service_val.grid(row=1, column=0, padx=(10, 0), pady=(0, 10), sticky="nsew")
            self.show_calendar = ctk.CTkButton(self.schedule_service_frame, text="",height=height*0.05,width=width*0.03, fg_color=Color.Blue_Yale,
                                               command=lambda: cctk.tk_calendar(self.scheduled_service_val, "%s"), corner_radius=3)
            self.show_calendar.grid(row=1, column=1, padx = (0,width*0.01), pady = (0,height*0.015), sticky="e")
            #note frame
            self.note_frame = ctk.CTkFrame(self.middle_frame, bg_color='#D9D9D9')
            self.note_frame.grid(row=0, column=1, padx=10, pady=(20, 10), sticky="nsw")
            #note label
            self.note_lbl = ctk.CTkLabel(self.note_frame, text='Note:',font=("Poppins", 25))
            self.note_lbl.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nw")
            #note entry
            self.note_entry = ctk.CTkEntry(self.note_frame, placeholder_text='a dog', height=height*0.25, width=width*0.445, font=("Poppins", 25))
            self.note_entry.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ns")


            self.rightmost_frame = ctk.CTkFrame(self, height=height*0.78, width=width*0.312, fg_color='white')
            self.rightmost_frame.grid(row=2, column=0, padx=10, pady=10, sticky="es")

            self.x_fr = ctk.CTkFrame(self.rightmost_frame, height=height*0.78, width=width*0.312, fg_color='white')

            self.x_fr.grid(row=2, column=0, padx=10, pady=10, sticky="s")

            self.back_button = ctk.CTkButton(self.x_fr, text='Back', command=discard, width=270, font=("Poppins-Bold", 45))

            self.back_button.grid(row=0, column=1, padx=20, pady=(15, 15), sticky='s')

            self.select_button = ctk.CTkButton(self.x_fr, text='Select', command=record, width=270, font=("Poppins-Bold", 45))
            self.select_button.grid(row=0, column=2, padx=(0, 20), pady=(15, 15), sticky="se")
            #on out
    return instance(master, info, parent)