import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
import sql_commands
from util import *
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from constants import action
from customtkinter.windows.widgets.core_widget_classes import DropdownMenu
from decimal import Decimal
import datetime
from datetime import date
from datetime import datetime
import threading
from PIL import Image
import copy

def show_item_list(master, info:tuple, root_treeview: cctk.cctkTreeView, change_val_func):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, root_treeview: cctk.cctkTreeView, change_val_func):
            self._master = master
            width = info[0]
            height = info[1]
            #self._treeview: cctk.cctkTreeView = info[2]
            super().__init__(master, corner_radius= 0)

            '''event'''
            def proceed(_: any = None):
                if self.item_treeview.data_grid_btn_mng.active:
                    data = self.item_treeview._data[self.item_treeview.data_frames.index(self.item_treeview.data_grid_btn_mng.active)]
                    add_data = (data[0], data[2], data[2])
                    if data[0] in [s[0] for s in root_treeview._data]: # if there's existing record
                        spinner:cctk.cctkSpinnerCombo = root_treeview.data_frames[[s[0] for s in root_treeview._data].index(data[0])].winfo_children()[3].winfo_children()[0]
                        spinner.change_value()
                    else: #if there's none
                        root_treeview.add_data(add_data)
                        temp_data = root_treeview._data[-1]
                        temp_data = (temp_data[0], temp_data[1], 1, temp_data[2])
                        root_treeview._data[-1] = temp_data
                        data_frames = root_treeview.data_frames[-1]
                        spinner: cctk.cctkSpinnerCombo = data_frames.winfo_children()[3].winfo_children()[0]

                        spinner.configure(val_range = (1, data[1]))
                        change_val_func(price_format_to_float(data[2][1:]))
                        #price = price_format_to_float(data_frames.winfo_children()[2]._text[1:])

                        def spinner_command(_: any = None):
                            temp_frame = spinner.master.master
                            temp_data = root_treeview._data[root_treeview.data_frames.index(temp_frame)]
                            temp_data = (temp_data[0], temp_data[1], spinner.value, '₱' + format_price(price_format_to_float(temp_data[1][1:]) * spinner.value))
                            root_treeview._data[root_treeview.data_frames.index(temp_frame)] = temp_data
                            change_val_func(-price_format_to_float(temp_frame.winfo_children()[4]._text[1:]))
                            price = price_format_to_float(temp_frame.winfo_children()[2]._text[1:])
                            temp_frame.winfo_children()[4].configure(text = '₱' + format_price(price * spinner.value))
                            change_val_func(price_format_to_float(temp_frame.winfo_children()[4]._text[1:]))

                        spinner.configure(command = spinner_command)

                    self.place_forget()

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
            self.item_treeview = cctk.cctkTreeView(self.content_frame,data=self.data, height=height*0.65, width=width*0.505,
                                                      column_format=f"/No:{int(width*.025)}-#r/ItemName:x-tl/Stocks:{int(width*.075)}-tr/Price:{int(width*.1)}-tr!30!30",
                                                      double_click_command= proceed)
            self.item_treeview.grid(row=1, column=0, padx=(width*0.005), pady=(height*0.01), sticky="nsew")

            self.bottom_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent", width=width*0.25)
            self.bottom_frame.grid(row=2, column=0 )
            self.bottom_frame.grid_propagate(0)
            self.bottom_frame.grid_columnconfigure(1, weight=1)
            self.back_button = ctk.CTkButton(self.bottom_frame, text='Cancel', width=width*0.1, font=("Arial", 14), command=self.reset)
            self.back_button.grid(row=0, column=0, sticky="w")

            self.select_button = ctk.CTkButton(self.bottom_frame, text='Select', width=width*0.1, font=("Arial", 14), command= proceed)
            self.select_button.grid(row=0, column=1, sticky="e")

            """ self.select_button = ctk.CTkButton(self.x_fr, text='Select', command=self.get_item, width =270, font=("Poppins-Bold", 45))
            self.select_button.grid(row=0, column=2, padx=(0, 20), sticky="se") """

        def place(self, **kwargs):
            self.main_frame.pack()
            self.data = database.fetch_data(sql_commands.get_item_and_their_total_stock, None)
            #self.item_treeview.update_table(self.data)
            return super().place(**kwargs)

        def reset(self):
            self.destroy()
            #self.main_frame.place_forget()
            self.place_forget()

        '''def get_item(self, _: any = None):
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
    return instance(master, info)'''

    return instance(master, info, root_treeview, change_val_func)

def show_services_list(master, info:tuple, root_treeview: cctk.cctkTreeView, change_val_func):
    class instance(ctk.CTkFrame):

        def __init__(self, master, info:tuple, root_treeview: cctk.cctkTreeView, change_val_func):
            #self._data_reciever = data_reciever
            self._master = master
            width = info[0]
            height = info[1]
            #self._treeview: cctk.cctkTreeView = info[2]
            super().__init__(master, corner_radius= 0)

            '''event'''
            def proceed(_: any = None):
                if self.service_treeview.data_grid_btn_mng.active:
                    data = self.service_treeview._data[self.service_treeview.data_frames.index(self.service_treeview.data_grid_btn_mng.active)]
                    add_data = (data[0], data[1], data[1])
                    if data[0] in [s[0] for s in root_treeview._data]: # if there's existing record
                        spinner:cctk.cctkSpinnerCombo = root_treeview.data_frames[[s[0] for s in root_treeview._data].index(data[0])].winfo_children()[3].winfo_children()[0]
                        spinner.change_value()
                    else: #if there's none
                        root_treeview.add_data(add_data)
                        data_frames = root_treeview.data_frames[-1]
                        spinner: cctk.cctkSpinnerCombo = data_frames.winfo_children()[3].winfo_children()[0]

                        spinner.configure(val_range = (1, cctk.cctkSpinnerCombo.MAX_VAL))
                        change_val_func(price_format_to_float(data[1][1:]))
                        #price = price_format_to_float(data_frames.winfo_children()[2]._text[1:])

                        """def spinner_command(_: any = None):
                            temp_frame = spinner.master.master
                            change_val_func(-price_format_to_float(temp_frame.winfo_children()[4]._text[1:]))
                            price = price_format_to_float(temp_frame.winfo_children()[2]._text[1:])
                            temp_frame.winfo_children()[4].configure(text = '₱' + format_price(price * spinner.value))
                            change_val_func(price_format_to_float(temp_frame.winfo_children()[4]._text[1:]))

                        spinner.configure(command = spinner_command)"""
                        spinner.add_button.destroy()
                        spinner.sub_button.destroy()
                        spinner.configure(mode = cctk.cctkSpinnerCombo.CLICK_ONLY)
                    self.place_forget()

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
                                                      column_format=f"/No:{int(width*.025)}-#r/ServiceName:x-tl/Price:x-tr!30!30",
                                                      double_click_command= proceed)
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

            self.select_button = ctk.CTkButton(self.bottom_frame, text='Select', width=width*0.1, font=("Arial", 14), command= proceed)
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
                info_tab.button.configure(command = lambda: info_tab._tab.place(relx = .5, rely = .5, anchor = 'c'))
                self._data_reciever.append(info_tab)
                info_tab._tab.place(relx = .5, rely = .5, anchor = 'c')


                master.change_total_value_service(transaction_data[2])
                self.service_treeview.data_grid_btn_mng.deactivate_active()
                self.reset()
                #reset the state of this popup
    return instance(master, info, root_treeview, change_val_func)

def show_transaction_proceed(master, info:tuple, service_price, item_price, total_price, transaction_content, customer_info, parent_treeview, service_dict) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, service_price, item_price, total_price, transaction_content, customer_info, parent_treeview, service_dict):
            width = info[0]
            height = info[1]
            self.acc_cred = info[2]
            self._service_price = service_price
            self._item_price = item_price
            self._total_price = total_price
            self._transaction_content = transaction_content
            self._customer_info = customer_info
            self.service_dict = service_dict
            #encapsulation

            super().__init__(master, corner_radius= 0, fg_color='white')
            #the actual frame, modification on the frame itself goes here

            '''events'''
            def auto_pay(_: any = None):
                self.payment_entry.delete(0, ctk.END)
                #self.payment_entry.insert(0, self._total_price)
                record_transaction()

            def record_transaction():
                #return
                record_id =  database.fetch_data(sql_commands.generate_id_transaction, (None))[0][0]
                if (float(self.payment_entry.get() or '0')) < price_format_to_float(self.total_amount._text[1:]):
                    messagebox.showinfo('Invalid', 'Pay the right amount')
                    return
                #if self.service:

                list_of_service = database.fetch_data(sql_commands.get_services_names)
                list_of_service = [s[0] for s in list_of_service]

                service = [s for s in self._transaction_content if s[0] in list_of_service]
                item = [s for s in self._transaction_content if s[0] not in list_of_service]

                if(len(service) > 0):
                    temp_service_data = []
                    for i in range(len(service)):
                        for j in self.service_dict[service[i][0]]:
                            temp_service_data.append((record_id, database.fetch_data(sql_commands.get_service_uid,(service[i][0],))[0][0], service[i][0], j[0], j[1], price_format_to_float(service[i][1][1:]), 0, 0))
                    service = temp_service_data

                if(len(item) > 0):
                    item = [(record_id, database.fetch_data(sql_commands.get_uid, (s[0], ))[0][0], s[0], s[2], price_format_to_float(s[1][1:]), 0) for s in item]
                #making a modification through the old process

                database.exec_nonquery([[sql_commands.record_transaction, (record_id, self.acc_cred[0][0], self._customer_info, price_format_to_float(self.total_amount._text[1:]))]])
                #record the transaction

                database.exec_nonquery([[sql_commands.record_item_transaction_content, s] for s in item])
                #record the items from within the transaction
                database.exec_nonquery([[sql_commands.record_services_transaction_content, s] for s in service])
                #record the services from within the transaction

                for _item in item:
                    stocks = database.fetch_data(sql_commands.get_specific_stock, (_item[1], ))
                    if stocks[0][2] is None:
                        database.exec_nonquery([[sql_commands.update_non_expiry_stock, (-_item[3], _item[1])]])
                    else:
                        quan = _item[3]
                        for st in stocks:
                            if st[1] < quan:
                                quan -= st[1]
                                database.exec_nonquery([['DELETE FROM item_inventory_info WHERE UID = ? AND Expiry_Date = ?', (st[0], st[2])]])
                            elif st[1] > quan:
                                database.exec_nonquery([[sql_commands.update_expiry_stock, (-quan, _item[1], st[2])]])
                                break
                            else:
                                if stocks[-1] == st:
                                    database.exec_nonquery([[sql_commands.update_expiry_stock, (-quan, _item[1], st[2])]])
                                else:
                                    database.exec_nonquery([['DELETE FROM item_inventory_info WHERE UID = ? AND Expiry_Date = ?', (st[0], st[2])]])
                                break
                #modify the stock, applying the FIFO

                payment = float(self.payment_entry.get())
                self.change_amount.configure(text = format_price(payment - price_format_to_float(self.total_amount._text[1:])))
                #calculate and show the change

                #master.reset()
                parent_treeview.master.master.reset()
                messagebox.showinfo('Sucess', 'Transaction Complete')

                self.destroy()
                #reset into its default state """

            self.main_frame = ctk.CTkFrame(self, width=width*0.8, height=height*0.85, corner_radius=0)
            self.main_frame.pack()
            self.main_frame.grid_columnconfigure((0), weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

            ctk.CTkLabel(self.top_frame, text='Payment', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.015,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=self.reset).pack(side="right", padx=(0,width*0.01),pady=height*0.005)

            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Color[3], corner_radius=0)
            self.content_frame.grid(row=1,column=0, padx=width*0.005, pady=height*0.01, sticky="nsew")
            self.content_frame.grid_columnconfigure(0, weight=1)
            self.content_frame.grid_propagate(0)

            self.service_frame = ctk.CTkFrame(self.content_frame, corner_radius=0, fg_color="transparent")
            self.service_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            self.service_frame.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(self.service_frame, text='Services Availed:',font=("Arial", 14), fg_color="transparent").grid(row=0, column=0, padx=width*0.005, pady=(0,height*0.005), sticky="w")

            #self.service_data = [(f'{s[1]}', format_price(float(s[4]))) for s in self._services_info]
            self.service_list = cctk.cctkTreeView(self.service_frame, data=None, height=height*0.245, width=width*0.545,
                                                  column_format=f'/No:{int(width * .03)}-#c/Name:x-tl/Quantity:{int(width*0.1)}-tr/Price:{int(width * .05)}-tr!30!30')
            self.service_list.grid(row=1, column=0)

            '''self.service_total_frame = ctk.CTkFrame(self.service_frame, width=width*0.15, height=height*0.05, fg_color="light grey")
            self.service_total_frame.pack_propagate(0)
            self.service_total_frame.grid(row=2,column=0, sticky="e", pady=(5,0))

            ctk.CTkLabel(self.service_total_frame, text="Services Total:", font=("Arial", 14)).pack(side="left", padx=(width*0.0075,0))
            self.service_total_amount = ctk.CTkLabel(self.service_total_frame, text="0,000.00", font=("Arial", 14))
            self.service_total_amount.pack(side="right",  padx=(0,width*0.0075))'''

            self.item_frame = ctk.CTkFrame(self.content_frame, corner_radius=0, fg_color="transparent")
            self.item_frame.grid(row=2, column=0, padx=10, pady=(0,10), sticky="nsew")
            self.item_frame.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(self.item_frame, text='Items Availed:',font=("Arial", 14), fg_color="transparent").grid(row=0, column=0, padx=width*0.005, pady=(0,height*0.005), sticky="w")

            #self.item_data = [(f'{s[1]} * {s[3]}', format_price(float(s[4]))) for s in self._item_info]
            self.item_list = cctk.cctkTreeView(self.item_frame, data=None, height=height*0.245, width=width*0.545,
                                               column_format=f'/No:{int(width * .03)}-#c/Name:x-tl/Quantity:{int(width*0.1)}-tr/Price:{int(width * .05)}-tr!30!30')
            self.item_list.grid(row=1, column=0)

            '''self.item_total_frame = ctk.CTkFrame(self.item_frame, width=width*0.15, height=height*0.05, fg_color="light grey")
            self.item_total_frame.pack_propagate(0)
            self.item_total_frame.grid(row=2,column=0, sticky="e", pady=(5,0))

            ctk.CTkLabel(self.item_total_frame, text="Items Total:", font=("Arial", 14)).pack(side="left", padx=(width*0.0075,0))
            self.item_total_amount = ctk.CTkLabel(self.item_total_frame, text="0,000.00", font=("Arial", 14))
            self.item_total_amount.pack(side="right",  padx=(0,width*0.0075))'''

            ctk.CTkButton(self.content_frame, text="Cancel", command=self.reset).grid(row=3, column=0, padx=10, pady=(0,10), sticky="w")

            self.payment_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.White_Color[3],width=width*0.225)
            self.payment_frame.grid(row=1,column=1, padx=(0,width*0.005), pady=height*0.01, stick="nsew")
            self.payment_frame.pack_propagate(0)

            self.payment_service_frame = ctk.CTkFrame(self.payment_frame, width=width*0.15, height=height*0.05, fg_color="transparent")
            self.payment_service_frame.pack_propagate(0)
            self.payment_service_frame.pack(fill="x", pady=(height*0.005))

            ctk.CTkLabel(self.payment_service_frame, text="Service:", font=("Arial", 16)).pack(side="left", padx=(width*0.0075,0))
            self.payment_service_amount = ctk.CTkLabel(self.payment_service_frame, text="0,000.00", font=("Arial", 16))
            self.payment_service_amount.pack(side="right",  padx=(0,width*0.0075))

            self.payment_item_frame = ctk.CTkFrame(self.payment_frame, width=width*0.15, height=height*0.05, fg_color="transparent")
            self.payment_item_frame.pack_propagate(0)
            self.payment_item_frame.pack(fill="x", pady=(height*0.005))

            ctk.CTkLabel(self.payment_item_frame, text="Items:", font=("Arial", 16)).pack(side="left", padx=(width*0.0075,0))
            self.payment_item_amount = ctk.CTkLabel(self.payment_item_frame, text="0,000.00", font=("Arial", 16))
            self.payment_item_amount.pack(side="right",  padx=(0,width*0.0075))

            self.total_frame = ctk.CTkFrame(self.payment_frame, width=width*0.15, height=height*0.05, fg_color="transparent")
            self.total_frame.pack_propagate(0)
            self.total_frame.pack(fill="x", pady=(height*0.005))

            ctk.CTkLabel(self.total_frame, text="Total:", font=("Arial", 20)).pack(side="left", padx=(width*0.0075,0))
            self.total_amount = ctk.CTkLabel(self.total_frame, text="0,000.00", font=("Arial", 20), width=width*0.15, fg_color="light grey", corner_radius=5,
                                             anchor="e")
            self.total_amount.pack(side="right",  padx=(0,width*0.0075))

            self.payment_entry_frame = ctk.CTkFrame(self.payment_frame, width=width*0.15, fg_color="transparent")
            self.payment_entry_frame.pack_propagate(0)
            self.payment_entry_frame.pack(fill="x", pady=(height*0.005))

            ctk.CTkLabel(self.payment_entry_frame, text="Enter Payment:", font=("Arial", 20)).pack(padx=(width*0.0075,0), anchor="w")
            self.payment_entry = ctk.CTkEntry(self.payment_entry_frame, placeholder_text="Payment here...", font=("Arial", 20),height=height*0.05, justify="right")
            self.payment_entry.pack(fill="x", padx=(width*0.0075))

            self.change_frame = ctk.CTkFrame(self.payment_frame, width=width*0.15, height=height*0.05, fg_color="transparent")
            self.change_frame.pack_propagate(0)
            self.change_frame.pack(fill="x", pady=(height*0.005))

            ctk.CTkLabel(self.change_frame, text="Change:", font=("Arial", 20)).pack(side="left", padx=(width*0.0075,0))
            self.change_amount = ctk.CTkLabel(self.change_frame, text="0,000.00", font=("Arial", 20), width=width*0.15, fg_color="light grey", corner_radius=5, anchor="e")
            self.change_amount.pack(side="right",  padx=(0,width*0.0075))

            self.proceed_button = ctk.CTkButton(self.payment_frame, text='Proceed', font=("Arial", 20), height=height*0.085, command=record_transaction)
            self.proceed_button.pack(fill="x",side="bottom", pady=height*0.025, padx=(width*0.025))
            """
            self.total_frame = ctk.CTkFrame(self.rightmost_frame)
            self.total_frame.grid(row=0, column=0, padx=10, pady=10, sticky="new", columnspan = 2)

            self.total_lbl = ctk.CTkLabel(self.total_frame, text='Total:',font=("Arial", 25))
            self.total_lbl.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")

            self.total_val = ctk.CTkEntry(self.total_frame, height=height*0.12, width=width*0.31, font=('DM Sans Medium', 35))
            #self.total_val.insert(0, format_price(self._total_price))
            self.total_val.configure(state = 'readonly')
            self.total_val.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="n")

            self.payment_options_frame = ctk.CTkFrame(self.rightmost_frame)
            self.payment_options_frame.grid(row=1, column=0, padx=10, pady=(10, height*0.22), sticky="new", columnspan = 2)

            self.payment_lbl = ctk.CTkLabel(self.payment_options_frame, text='Payment Method:', font=("Poppins", 25))
            self.payment_lbl.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")

            self.payment_method_cbox = ctk.CTkOptionMenu(self.payment_options_frame, values=["Cash"], font=("Poppins", 25), height=height*0.08,width=width*0.31
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

            self.cancel_button = ctk.CTkButton(self.rightmost_frame, text='Cancel', command=self.reset, width=135, font=("Poppins-Bold", 45))
            self.cancel_button.grid(row=4, column=1, padx=(40, 50), pady =(10,10), sticky="ew")
            """
            self.payment_entry.focus_force()
            self.payment_entry.bind('<Shift-Return>', auto_pay)
        def reset(self):
            self.place_forget()

        def place(self, **kwargs):
            self.payment_service_amount.configure(text = self._service_price)
            self.payment_item_amount.configure(text = self._item_price)
            self.total_amount.configure(text = self._total_price)
            return super().place(**kwargs)
            #item_info, services_info, total_price, customer_info, pets_info
    return instance(master, info, service_price, item_price, total_price, transaction_content, customer_info, parent_treeview, service_dict)

def customer_info(master, info:tuple, parent_value = None) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, parent_value: tuple = None):
            self.service = None
            width = info[0]
            height = info[1]
            #basic inforamtion needed; measurement

            super().__init__(master, corner_radius= 0, fg_color="transparent")
            #the actual frame, modification on the frame itself goes here

            #self.grid_propagate(0)
            self.value: tuple = None
            self._parent_value = parent_value
            self.cal_icon= ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(15,15))
            self.sched_switch_var = ctk.StringVar(value="off")

            def automate_fill(_: any= None):
                data = database.fetch_data(sql_commands.get_pet_info_for_cust_info, (self.pet_name.get(), ))[0]
                self.animal_breed_entry.delete(0, ctk.END)
                self.animal_breed_entry.insert(0, data[0])
                self.animal_breed_entry.configure(state = ctk.DISABLED)

            def hide():
                self.place_forget()

            def discard():
                if (self.pet_name.get() != self.value[0] or self.animal_breed_entry.get() != self.value[1] or
                self.scheduled_service_val._text != self.value[2] or self.note_entry.get() != self.value[3]):
                    if messagebox.askyesno('NOTE!', 'all changes will be discarded?'):
                        self.pet_name.set('')
                        self.animal_breed_entry.delete(0, ctk.END)
                        self.note_entry.delete(0, ctk.END)
                        self.pet_name.insert(0, self.value[0] or '')
                        self.animal_breed_entry.insert(0, self.value[1] or '')
                        self.scheduled_service_val.configure( text = self.value[2] or '')
                        self.note_entry.insert(0, self.value[3] or '')
                hide()


            def record():
                date = self.scheduled_service_val._text if self.scheduled_service_val._text != 'Set Date' else str(datetime.date.today())
                self.value:tuple = (self.tables[self.pet_values.index(self.pet_name.get())] + (date, ))
                self._parent_value.value = self.value
                hide()

            def sched_swtich_event():
                if self.sched_switch_var.get() == "on":
                    self.show_calendar.configure(state="normal")
                    self.show_calendar.configure(fg_color=Color.Blue_Yale)
                else:
                    self.show_calendar.configure(state="disabled")
                    self.show_calendar.configure(fg_color="light grey")

            self.main_frame = ctk.CTkFrame(self, width=width*0.5, height=height*0.65, corner_radius=0)
            self.main_frame.pack()
            self.main_frame.grid_columnconfigure((0), weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

            ctk.CTkLabel(self.top_frame, text='Pet Info', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.015,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=hide).pack(side="right", padx=(0,width*0.01),pady=height*0.005)

            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Color[3], corner_radius=0)
            self.content_frame.grid(row=1,column=0, padx=width*0.005, pady=height*0.01, sticky="nsew")
            self.content_frame.grid_columnconfigure(0, weight=1)
            self.content_frame.grid_propagate(0)

            self.client_name_label = ctk.CTkLabel(self.content_frame, text="Client's Pet Information",font=("Arial",18))
            self.client_name_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")
            #Name label
            ctk.CTkLabel(self.content_frame, text='Select Pet:',font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nw")
            """ self.pet_frame = ctk.CTkScrollableFrame(self.content_frame, height=height*0.15, fg_color="transparent")
            self.pet_frame.grid(row=2,column=0, sticky="we") """
            self.tables = database.fetch_data(sql_commands.get_pet_name)
            self.pet_values = [s[1] for s in self.tables]
            """ 
            for pet_index in range(len(self.pet_values)):
                ctk.CTkButton(self.pet_frame, text=self.pet_values[pet_index]).pack() """
            self.pet_name = ctk.CTkOptionMenu(self.content_frame, width=width*0.45, font=("Arial", 14), values=self.pet_values, command= automate_fill)
            self.pet_name.set('')
            self.pet_name.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ns")
            
            self.animal_breed_lbl = ctk.CTkLabel(self.content_frame, text='Breed and Animal Type:',font=("Arial", 14))
            self.animal_breed_lbl.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="nw")
            #Breed and Animal Type entry
            self.animal_breed_entry = ctk.CTkEntry(self.content_frame, width=width*0.45, font=("Arial", 14))
            self.animal_breed_entry.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ns")
            
            self.schedule_service_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            self.schedule_service_frame.grid(row=5,  column=0, padx=10, pady=(10), sticky="ew")
            #Scheduled service label
            self.sched_switch = ctk.CTkSwitch(self.schedule_service_frame, text="Schedule Client?", command=sched_swtich_event, variable=self.sched_switch_var,
                                              onvalue="on", offvalue="off")
            self.sched_switch.grid(row=0, column=0, padx=(10, 0), pady=(0, 10), sticky="nw")

            self.scheduled_service_lbl = ctk.CTkLabel(self.schedule_service_frame, text="Set Schedule",font=("Arial", 14))
            self.scheduled_service_lbl.grid(row=1, column=0, padx=(10, 0), sticky="nw")
            #Scheduled service label
            self.scheduled_service_val = ctk.CTkLabel(self.schedule_service_frame, width=width*0.25, height=height*0.05,font=("Arial", 14), fg_color='light grey', text="Set Date", text_color="grey")
            self.scheduled_service_val.grid(row=2, column=0, padx=(10, 0), pady=(0, 10), sticky="nsew")
            self.show_calendar = ctk.CTkButton(self.schedule_service_frame, text="",height=height*0.05,width=width*0.03, fg_color=Color.Blue_Yale,image=self.cal_icon,
                                               command=lambda: cctk.tk_calendar(self.scheduled_service_val, "%s"), corner_radius=3)
            self.show_calendar.grid(row=2, column=1, padx = (width*0.005,0), pady = (0,height*0.015), sticky="e")

            self.x_fr = ctk.CTkFrame(self.content_frame, height=height*0.78, width=width*0.312, fg_color="transparent")

            self.x_fr.grid(row=6, column=0, padx=10, pady=10, sticky="s")

            self.back_button = ctk.CTkButton(self.x_fr, text='Back', command=discard, font=("Arial", 20))
            self.back_button.grid(row=0, column=1, padx=20, pady=(15, 15), sticky='s')

            self.select_button = ctk.CTkButton(self.x_fr, text='Confirm', command=record, font=("Arial", 20))
            self.select_button.grid(row=0, column=2, padx=(0, 20), pady=(15, 15), sticky="se")

            sched_swtich_event()
            #on out

    return instance(master, info, parent_value)

def scheduled_services(master, info:tuple, parent= None) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, parent):
            width = info[0]
            height = info[1]
            super().__init__(master, corner_radius= 0, fg_color="transparent")

            self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(15,15))
            self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))

            def hide():
                self.place_forget()

            self.main_frame = ctk.CTkFrame(self, width=width*0.75, height=height*0.75, corner_radius=0)
            self.main_frame.pack()
            self.main_frame.grid_columnconfigure((0), weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

            ctk.CTkLabel(self.top_frame, text='Scheduled Services', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.015,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=hide).pack(side="right", padx=(0,width*0.01),pady=height*0.005)

            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Color[3], corner_radius=0)
            self.content_frame.grid(row=1,column=0, padx=width*0.005, pady=height*0.01, sticky="nsew")
            self.content_frame.grid_columnconfigure(2, weight=1)
            self.content_frame.grid_rowconfigure(1, weight=1)
            self.content_frame.grid_propagate(0)

            self.search_frame = ctk.CTkFrame(self.content_frame, fg_color="light grey", width=width*0.35, height = height*0.05,)
            self.search_frame.grid(row=0, column=0,padx=(width*0.005),pady=(height*0.01), sticky="w")
            self.search_frame.pack_propagate(0)

            ctk.CTkLabel(self.search_frame,text="Search", font=("Arial", 14), text_color="grey", fg_color="transparent").pack(side="left", padx=(width*0.0075,width*0.0025))
            self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Type here...", border_width=0, corner_radius=5, fg_color="white")
            self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)
            self.search_btn = ctk.CTkButton(self.search_frame, text="", image=self.search, fg_color="white", hover_color="grey",
                                            width=width*0.005)
            self.search_btn.pack(side="left", padx=(0, width*0.0025))

            self.refresh_btn = ctk.CTkButton(self.content_frame,text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75")
            self.refresh_btn.grid(row=0, column=2,padx=(0,width*0.005),pady=(height*0.01),sticky="w")

            self.sched_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            self.sched_frame.grid(row=1, column=0, columnspan=3, sticky="nsew",padx=(width*0.005), pady=(0,height*0.01))

            self.sched_treeview = cctk.cctkTreeView(self.sched_frame, data =[], width=width*0.725, height=height*0.7,
                                               column_format=f'/No:{int(width*.025)}-#r/OR:{int(width*0.05)}-tc/ClientName:x-tl/Service:{int(width*.15)}-tr/Schedule:{int(width*.1)}-tc/Action:{int(width*.08)}-bD!30!30',)
            self.sched_treeview.pack()

    return instance(master, info, parent)

def add_particulars(master, info:tuple, root_treeview: cctk.cctkTreeView, change_val_func_item, change_val_func_service, service_dict: dict) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, root_treeview: cctk.cctkTreeView, change_val_func_item, change_val_func_service, service_dict: dict):
            width = info[0]
            height = info[1]
            super().__init__(master, corner_radius= 0, fg_color="transparent")

            '''internal data'''
            self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(15,15))
            self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
            self._service_dict = service_dict

            def hide():
                self.place_forget()
            def item_proceed(_: any = None):
                if self.item_treeview.data_grid_btn_mng.active:
                    data = self.item_treeview._data[self.item_treeview.data_frames.index(self.item_treeview.data_grid_btn_mng.active)]
                    add_data = (data[0], data[2], data[2])
                    if data[0] in [s[0] for s in root_treeview._data]: # if there's existing record
                        spinner:cctk.cctkSpinnerCombo = root_treeview.data_frames[[s[0] for s in root_treeview._data].index(data[0])].winfo_children()[3].winfo_children()[0]
                        spinner.change_value()
                    else: #if there's none
                        root_treeview.add_data(add_data)
                        temp_data = root_treeview._data[-1]
                        temp_data = (temp_data[0], temp_data[1], 1, temp_data[2])
                        root_treeview._data[-1] = temp_data
                        data_frames = root_treeview.data_frames[-1]
                        spinner: cctk.cctkSpinnerCombo = data_frames.winfo_children()[3].winfo_children()[0]

                        spinner.configure(val_range = (1, data[1]))
                        change_val_func_item(price_format_to_float(data[2][1:]))
                        #price = price_format_to_float(data_frames.winfo_children()[2]._text[1:])

                        def spinner_command(_: any = None):
                            temp_frame = spinner.master.master
                            temp_data = root_treeview._data[root_treeview.data_frames.index(temp_frame)]
                            temp_data = (temp_data[0], temp_data[1], spinner.value, '₱' + format_price(price_format_to_float(temp_data[1][1:]) * spinner.value))
                            root_treeview._data[root_treeview.data_frames.index(temp_frame)] = temp_data
                            change_val_func_item(-price_format_to_float(temp_frame.winfo_children()[4]._text[1:]))
                            price = price_format_to_float(temp_frame.winfo_children()[2]._text[1:])
                            temp_frame.winfo_children()[4].configure(text = '₱' + format_price(price * spinner.value))
                            change_val_func_item(price_format_to_float(temp_frame.winfo_children()[4]._text[1:]))

                        spinner.configure(command = spinner_command)

                    self.place_forget()

                
            def service_proceed(_: any = None):
                if len(self.client) < 1:
                    messagebox.showerror('Invalid Process', 'Assign the Client first')
                elif self.service_treeview.data_grid_btn_mng.active:
                    data = self.service_treeview._data[self.service_treeview.data_frames.index(self.service_treeview.data_grid_btn_mng.active)]
                    add_data = (data[0], data[1], data[1])
                    if data[0] in [s[0] for s in root_treeview._data]: # if there's existing record
                        spinner:cctk.cctkSpinnerCombo = root_treeview.data_frames[[s[0] for s in root_treeview._data].index(data[0])].winfo_children()[4].winfo_children()[0]
                        spinner.change_value()
                    else: #if there's none
                        root_treeview.add_data(add_data)
                        data_frames: cctk.ctkButtonFrame = root_treeview.data_frames[-1]

                        label: ctk.CTkLabel = data_frames.winfo_children()[1]
                        label_text = copy.copy(label._text)
                        label.destroy()
                        #destroy the label

                        import serviceAvailing
                        def proceed_command(data):
                            self._service_dict[label_text] = data

                        new_button = ctk.CTkButton(data_frames, corner_radius= 0,
                                                   text=label_text, width = root_treeview.column_widths[1],
                                                   command= lambda: serviceAvailing.pets(root_treeview.master, spinner.value, label_text, [s[2] for s in self.client],
                                                                                         proceed_command, None, self.winfo_screenwidth() * .65,
                                                                                         self.winfo_screenheight() * .6, fg_color= 'transparent').place(relx = .5, rely = .5,anchor = 'c'))
                        #make a button
                        for i in data_frames.winfo_children():
                            i.pack_forget()
                        modified_data_frames:list = data_frames.winfo_children()
                        modified_data_frames.insert(1, new_button)
                        for i in modified_data_frames:
                            i.pack(fill = 'y', side = 'left', padx = (1,0))
                        #repack the button frame/data frame
                        #make the label as button for patient access

                        temp_data = root_treeview._data[-1]
                        temp_data = (temp_data[0], temp_data[1], 1, temp_data[2])
                        root_treeview._data[-1] = temp_data

                        spinner: cctk.cctkSpinnerCombo = data_frames.winfo_children()[2].winfo_children()[0]
                        spinner.configure(val_range = (1, len(self.client)))
                        change_val_func_service(price_format_to_float(data[1][1:]))
                        def spinner_command(_: any = None):
                            temp_frame = spinner.master.master
                            temp_data = root_treeview._data[root_treeview.data_frames.index(temp_frame)]
                            temp_data = (temp_data[0], temp_data[1], spinner.value, '₱' + format_price(price_format_to_float(temp_data[1][1:]) * spinner.value))
                            root_treeview._data[root_treeview.data_frames.index(temp_frame)] = temp_data
                            change_val_func_service(-price_format_to_float(temp_frame.winfo_children()[3]._text[1:]))
                            price = price_format_to_float(temp_frame.winfo_children()[1]._text[1:])
                            temp_frame.winfo_children()[3].configure(text = '₱' + format_price(price * spinner.value))
                            change_val_func_service(price_format_to_float(temp_frame.winfo_children()[3]._text[1:]))
                        spinner.configure(command = spinner_command)
                        spinner.configure(mode = cctk.cctkSpinnerCombo.CLICK_ONLY)
                        #set the spinner combo of the table
                self.place_forget()
                
            def filter_func(value):
                if "All" in value:
                    self.service_frame.grid(row=1,column=0, columnspan=2, sticky="nsew", padx=(width*0.005),pady=(0,height*0.01))
                    self.item_frame.grid(row=2, column=0, columnspan=2 ,sticky="nsew",  padx=(width*0.005),pady=(0, height*0.01))
                    self.service_treeview.configure(height=height*0.4)
                    self.item_treeview.configure(height=height*0.4)
                elif "Service" in value:
                    self.service_frame.grid(row=1,column=0, columnspan=2, rowspan=2, sticky="nsew", padx=(width*0.005),pady=(0,height*0.01))
                    self.item_frame.grid_forget()
                    self.service_treeview.configure(height=height*0.75)
                    
                elif "Item" in value:
                    self.item_frame.grid(row=1, column=0, columnspan=2 , rowspan=2 ,sticky="nsew",  padx=(width*0.005),pady=(0, height*0.01))
                    self.service_frame.grid_forget()
                    self.item_treeview.configure(height=height*0.75)
                    
                    
                    
            self.filter_optionmenu_var = ctk.StringVar(value="All") 

            self.main_frame = ctk.CTkFrame(self, width=width*0.815, height=height*0.875, corner_radius=0,fg_color=Color.White_Color[3])
            self.main_frame.pack()
            self.main_frame.grid_columnconfigure((0), weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

            ctk.CTkLabel(self.top_frame, text='Particulars', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.015,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=self.reset).pack(side="right", padx=(0,width*0.01),pady=height*0.005)
            
            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            self.content_frame.grid(row=1, column=0,columnspan=2, sticky="nsew")
            
            self.content_frame.grid_columnconfigure(0, weight=1)
            self.content_frame.grid_rowconfigure((1,2), weight=1)
                
            self.search_frame = ctk.CTkFrame(self.content_frame, width=width*0.35, height = height*0.05, fg_color="light grey")
            self.search_frame.grid(row=0, column=0,sticky="w", padx=(width*0.005), pady=(height*0.01))
            self.search_frame.pack_propagate(0)

            ctk.CTkLabel(self.search_frame,text="Search", font=("Arial", 14), text_color="grey", fg_color="transparent").pack(side="left", padx=(width*0.0075,width*0.0025))
            self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Type here...", border_width=0, corner_radius=5, fg_color="white")
            self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)
            self.search_btn = ctk.CTkButton(self.search_frame, text="", image=self.search, fg_color="white", hover_color=Color.Blue_Yale,
                                            width=width*0.005)
            self.search_btn.pack(side="left", padx=(0, width*0.0025))
            
            self.filter_optionmenu = ctk.CTkOptionMenu(self.content_frame, width=width*0.1, height=height*0.05, fg_color="light grey", values=["All", "Services", "Items"], text_color="black", anchor="center")
            self.filter_optionmenu.configure(command=filter_func)
            self.filter_optionmenu.grid(row=0, column=1, sticky="nse", padx=(width*0.005), pady=(height*0.01))
            
            self.service_frame = ctk.CTkFrame(self.content_frame, corner_radius=0)
            self.service_frame.pack_propagate(0)
            
            self.service_treeview = cctk.cctkTreeView(self.service_frame, height=height*0.4, width=width*0.8,corner_radius=0,double_click_command=service_proceed, column_format=f"/No:{int(width*.025)}-#r/ServiceName:x-tl/Price:x-tr!30!30")
            self.service_treeview.pack()
            
            self.item_frame = ctk.CTkFrame(self.content_frame, corner_radius=0)
            self.item_frame.pack_propagate(0)
            
            self.data = database.fetch_data(sql_commands.get_item_and_their_total_stock, None)
            self.item_treeview = cctk.cctkTreeView(self.item_frame, data=self.data, height=height*0.4, width=width*0.8,double_click_command=item_proceed, column_format=f"/No:{int(width*.025)}-#r/ItemName:x-tl/Stocks:{int(width*.075)}-tr/Price:x-tr!30!30",)
            self.item_treeview.pack()
            
            filter_func("All")
        def reset(self):
            self.place_forget()

        def place(self, **kwargs):
            if('client' in kwargs):
                self.check_client(kwargs['client'])
                kwargs.pop('client')
            raw_data = database.fetch_data(sql_commands.get_services_and_their_price, None)
            self.main_frame.pack()
            self.data = [(s[1], s[3]) for s in raw_data]
            self.service_treeview.update_table(self.data)
            self.data = database.fetch_data(sql_commands.get_item_and_their_total_stock, None)
            return super().place(**kwargs)
        
        def check_client(self, client_name: str):
            self.client = database.fetch_data(sql_commands.get_pet_info, (client_name, ))
            
        def get_service(self, _: any = None):
            #if there's a selected item
            if self.service_treeview.data_grid_btn_mng.active is not None:
                service_name =  self.service_treeview.data_grid_btn_mng.active.winfo_children()[0]._text
                #getting the needed information for the item list
                transaction_data = database.fetch_data(sql_commands.get_services_data_for_transaction, (service_name, ))[0]
                self._treeview.add_data(transaction_data+(0, transaction_data[2]))
                return
                info_tab:cctk.info_tab = self._treeview.data_frames[-1].winfo_children()[3]
                info_tab._tab = customer_info(self._treeview.master.master, (info[0] * .8, info[1] * .8), info_tab)
                info_tab.button.configure(command = lambda: info_tab._tab.place(relx = .5, rely = .5, anchor = 'c'))
                self._data_reciever.append(info_tab)
                info_tab._tab.place(relx = .5, rely = .5, anchor = 'c')


                master.change_total_value_service(transaction_data[2])
                self.service_treeview.data_grid_btn_mng.deactivate_active()
                self.reset()
    return instance(master, info, root_treeview, change_val_func_item, change_val_func_service, service_dict)

def add_invoice(master, info:tuple, treeview_content_update_callback: callable):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, treeview_content_update_callback: callable):
            width = info[0]
            height = info[1]
            super().__init__(master,width * .835, height=height*0.92, corner_radius= 0, fg_color="transparent")
            
            self.invoice_icon = ctk.CTkImage(light_image=Image.open("image/histlogs.png"), size=(18,21))
            self.add_icon = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(17,17))
            
            self.customer_infos = []
            self.service_dict: dict = {}

            self._treeview_content_update_callback = treeview_content_update_callback

            '''constants'''
            self.services = [s[0] for s in database.fetch_data(sql_commands.get_service_data)]

            '''events'''
            def bd_commands(i):
                if self.transact_treeview._data[i][0] in [s[0] for s in database.fetch_data(sql_commands.get_services_names)]:
                    #self.patient_info.value = None
                    self.change_total_value_service(-price_format_to_float(self.transact_treeview._data[i][1][1:]))
                else:
                    self.change_total_value_item(-price_format_to_float(self.transact_treeview._data[i][3][1:]))

            def change_customer_callback(_:any):
                if len(self.service_dict) > 0:
                    if messagebox.askyesno('Change Customer', 'All of the service and its\npatient info will be reset'):
                        client = self.client_name_entry.get()
                        
                        self.service_dict = {}
                        self.transact_treeview.delete_all_data()
                        self.reset()

                        self.client_name_entry.set(client)
                        del client

                        '''initial process'''

            def save_invoice_callback():
                services = []
                items = []
                for st in self.transact_treeview._data:
                    if(st[0] in self.service_dict):
                        services.append(st)
                    else:
                        items.append(st)

                print(services, items, self.service_dict)

                formatted_svc_data = []
                uid = generateId('P', 6)

                for svc in services:
                    for svc_inf in self.service_dict[svc[0]]:
                        formatted_svc_data.append((uid, database.fetch_data(sql_commands.get_service_uid, (svc[0], ))[0][0], svc[0], svc_inf[0], svc_inf[1], price_format_to_float(svc[1][1:]), 0))
                #formatting the services into its service invoice content
                database.exec_nonquery([[sql_commands.insert_invoice_data, (uid, 'aila', self.client_name_entry.get() or 'N/A', price_format_to_float(self.price_total_amount._text[1:]), datetime.now().strftime('%Y-%m-%d'), 0, None)]])

                for it in items:
                    database.exec_nonquery([[sql_commands.insert_invoice_item_data, (uid, database.fetch_data(sql_commands.get_uid, (it[0], ))[0][0], it[0], it[2], price_format_to_float(it[1][1:]), 0)]])
                #database insertion of items

                for li in formatted_svc_data:
                    database.exec_nonquery([[sql_commands.insert_invoice_service_data, li]])
                #database insertion of services

                self._treeview_content_update_callback()
                messagebox.showinfo('Success', 'Invoice Saved')
                self.reset(True)

                
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)

            self.main_frame = ctk.CTkFrame(self, fg_color=Color.White_Color[3], corner_radius=0)
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=width*0.01, pady=height*0.02)

            self.main_frame.grid_columnconfigure(2, weight=1)
            self.main_frame.grid_rowconfigure((2),weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text='',image=self.invoice_icon).pack(side="left", padx=(width*0.015,0))
            ctk.CTkLabel(self.top_frame, text='ADD INVOICE', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.005,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.025, command=self.reset).pack(side="right", padx=(0,width*0.01))

            self.client_name_frame = ctk.CTkFrame(self.main_frame, fg_color="light grey", width=width*0.4, height=height*0.05)
            self.client_name_frame.grid(row=1, column=0, sticky="w", padx=(width*0.005), pady=(height*0.01))
            self.client_name_frame.pack_propagate(0)

            self.client_name_label = ctk.CTkLabel(self.client_name_frame, text="Client:",font=("DM Sans Medium", 15))
            self.client_name_label.pack(side="left",  padx=(width*0.01, 0), pady=(height*0.01))

            self.client_name_entry = ctk.CTkOptionMenu(self.client_name_frame,font=("DM Sans Medium", 15), fg_color="white", text_color='black', command= change_customer_callback)
            self.client_name_entry.set('')
            self.client_names = [s[0] for s in database.fetch_data(sql_commands.get_owners)]
            self.client_name_entry.configure(values = self.client_names)
            self.client_name_entry.pack(side="left", fill="x", expand=1, padx=(width*0.005), pady=(height*0.005))
            
            self.add_particulars = ctk.CTkButton(self.main_frame,text="Add Particulars", width=width*0.125, height=height*0.05, image=self.add_icon, font=("DM Sans Medium", 14),
                                               command=lambda:self.show_particulars.place(relx=0.5, rely=0.5, anchor="c", client = self.client_name_entry.get()))
            self.add_particulars.grid(row=1, column=1, sticky="w")

            self.transact_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Color[3])
            self.transact_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=(0))

            self.transact_treeview = cctk.cctkTreeView(self.transact_frame, data=[], width=width*0.8, height=height*0.685,
                                                    column_format=f'/No:{int(width*0.025)}-#r/Particulars:x-tl/UnitPrice:{int(width*0.085)}-tr/Quantity:{int(width*0.1)}-id/Total:{int(width*0.085)}-tr/Action:{int(width*.065)}-bD!30!30')
            self.transact_treeview.pack(pady=(0,0))
            self.transact_treeview.bd_commands = bd_commands
            
            self.bottom_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=height*0.05)
            self.bottom_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=(width*0.005), pady=(height*0.01))

            #self.add_particulars = ctk.CTkButton(self.bottom_frame, width=width*0.125, height=height*0.05, text='Add Particulars',
            #                                   image=self.add_icon, command=lambda:self.show_particulars.place(relx=0.5, rely=0.5, anchor="c", client = self.client_name_entry.get()))
            
            self.price_total_frame = ctk.CTkFrame(self.bottom_frame, width=width*0.125, height=height*0.05, fg_color="light grey")
        
            ctk.CTkLabel(self.price_total_frame, text="Total:", font=("Arial", 14)).pack(side="left", padx=(width*0.0075,0))
            self.price_total_amount = ctk.CTkLabel(self.price_total_frame, text="0,000.00", font=("Arial", 14))
            self.price_total_amount.pack(side="right",  padx=(0,width*0.0075))
            
            self.item_total_frame = ctk.CTkFrame(self.bottom_frame, width=width*0.125, height=height*0.05, fg_color="light grey")

            ctk.CTkLabel(self.item_total_frame, text="Item:", font=("Arial", 14)).pack(side="left", padx=(width*0.0075,0))
            self.item_total_amount = ctk.CTkLabel(self.item_total_frame, text="0,000.00", font=("Arial", 14))
            self.item_total_amount.pack(side="right",  padx=(0,width*0.0075))

            self.services_total_frame = ctk.CTkFrame(self.bottom_frame, width=width*0.125, height=height*0.05, fg_color="light grey")
        
            ctk.CTkLabel(self.services_total_frame, text="Services:", font=("Arial", 14)).pack(side="left", padx=(width*0.0075,0))
            self.services_total_amount = ctk.CTkLabel(self.services_total_frame, text="0,000.00", font=("Arial", 14))
            self.services_total_amount.pack(side="right",  padx=(0,width*0.0075)) 
            
            self.services_total_frame.pack(side="left", padx=(0,width*0.0075))
            self.services_total_frame.pack_propagate(0)
            self.item_total_frame.pack(side="left", padx=(0,width*0.0075))
            self.item_total_frame.pack_propagate(0)
            self.price_total_frame.pack(side="left")
            self.price_total_frame.pack_propagate(0)
 
            """ self.proceeed_button = ctk.CTkButton(self, text="Proceed", image=self.proceed_icon, height=height*0.05, width=width*0.1,font=("Arial", 14), compound="right",   
                                                command=lambda:transaction_popups.show_transaction_proceed(self, (width, height, acc_cred), self.services_total_amount._text,
                                                                self.item_total_amount._text, self.price_total_amount._text, self.transact_treeview._data,
                                                                self.client_name_entry.get() or 'N/A', self.transact_treeview, self.service_dict).place(relx = .5, rely = .5, anchor = 'c'))
            self.proceeed_button.grid(row=3, column=2, pady=(0,height*0.025),padx=(0, width*0.005), sticky="e")  """
            
            self.save_invoice_btn = ctk.CTkButton(self.bottom_frame,text="Save Invoice",height=height*0.05, width=width*0.09, font=("DM Sans Medium", 16), command= save_invoice_callback)
            self.save_invoice_btn.pack(side="right")
            
            self.cancel_invoice_btn = ctk.CTkButton(self.bottom_frame,text="Cancel", fg_color=Color.Red_Pastel, hover_color=Color.Red_Tulip, height=height*0.05, width=width*0.06, font=("DM Sans Medium", 16))
            self.cancel_invoice_btn.configure(command=self.reset)
            self.cancel_invoice_btn.pack(side="right", padx=(width*0.005))
            
            
            #self.show_particulars:ctk.CTkFrame = add_particulars(self,(width, height), self.transact_treeview, self.change_total_value_item, self.change_total_value_service, self.service_dict)
            self.show_particulars:ctk.CTkFrame = add_particulars(self, (width, height), self.transact_treeview, self.change_total_value_item, self.change_total_value_service, self.service_dict)
            #self.show_particulars:ctk.CTkFrame = add_particulars_demo(self,(width, height))
            
        def change_total_value_item(self, value: float):
            value = float(value)
            self.item_total_amount.configure(text = '₱' + format_price(float(price_format_to_float(self.item_total_amount._text[1:])) + value))
            self.price_total_amount.configure(text = '₱' + format_price(float(price_format_to_float(self.price_total_amount._text[1:])) + value))

        def change_total_value_service(self, value: float):
            value = float(value)
            self.services_total_amount.configure(text = '₱' + format_price(float(price_format_to_float(self.services_total_amount._text[1:])) + value))
            self.price_total_amount.configure(text = '₱' + format_price(float(price_format_to_float(self.price_total_amount._text[1:])) + value))


        def reset(self, bypass_warning: bool = False):
            if self.client_name_entry.get() != "" or len(self.transact_treeview._data) > 0:
                if bypass_warning:
                    self.client_name_entry.set("")
                    self.transact_treeview.delete_all_data()
                    self.services_total_amount.configure(text = format_price(0))
                    self.item_total_amount.configure(text = format_price(0))
                    self.price_total_amount.configure(text = format_price(0))
                    self.service_dict.clear()
                elif messagebox.askyesno("Cancel Invoice", "Are you sure you want to discard the invoice") or bypass_warning:
                    self.client_name_entry.set("")
                    self.transact_treeview.delete_all_data()
                    self.services_total_amount.configure(text = format_price(0))
                    self.item_total_amount.configure(text = format_price(0))
                    self.price_total_amount.configure(text = format_price(0))
                    self.service_dict.clear()
                else:
                    return
            self.place_forget()  
    return instance(master, info, treeview_content_update_callback)

def show_payment_proceed(master, info:tuple,):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple):
            width = info[0]
            height = info[1]
            super().__init__(master,  width=width*0.815, height=height*0.875, corner_radius= 0, fg_color="transparent")
                
            self.main_frame = ctk.CTkFrame(self, width=width*0.8155, height=height*0.885, corner_radius=0)
            self.main_frame.pack()
            self.main_frame.grid_columnconfigure((0), weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

            ctk.CTkLabel(self.top_frame, text='Payment', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.015,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=self.reset).pack(side="right", padx=(0,width*0.01),pady=height*0.005)

            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Color[3], corner_radius=0)
            
            self.content_frame.grid(row=1,column=0, sticky="nsew")
            self.content_frame.grid_columnconfigure(0, weight=1)
            self.content_frame.grid_propagate(0)
            
            self.content_frame.grid_rowconfigure(1, weight=1)

            '''events'''
            def record_transaction():
                record_id =  database.fetch_data(sql_commands.generate_id_transaction)[0][0]

                if (float(self.payment_entry.get() or '0')) < price_format_to_float(self.grand_total._text[1:]):
                    messagebox.showinfo('Invalid', 'Pay the right amount')
                    return
                #if self.service:

                item = [(record_id, database.fetch_data(sql_commands.get_uid, (s[0],))[0][0], s[0], s[1], s[2], 0) for s in self.items]
                service = [(record_id, database.fetch_data(sql_commands.get_service_uid, (s[0], ))[0][0], s[0], s[1], s[2], s[3], 0, 0) for s in self.services]
                
                print(self.cashier_name._text)
                database.exec_nonquery([[sql_commands.record_transaction, (record_id, self.cashier_name._text, self.client_name._text, price_format_to_float(self.grand_total._text[1:]))]])
                #record the transaction

                database.exec_nonquery([[sql_commands.record_item_transaction_content, s] for s in item])
                #record the items from within the transaction
                database.exec_nonquery([[sql_commands.record_services_transaction_content, s] for s in service])
                #record the services from within the transaction

                for _item in item:
                    print(_item)
                    stocks = database.fetch_data(sql_commands.get_specific_stock, (_item[1], ))
                    if stocks[0][2] is None:
                        database.exec_nonquery([[sql_commands.update_non_expiry_stock, (-_item[3], _item[1])]])
                    else:
                        quan = _item[3]
                        for st in stocks:
                            if st[1] < quan:
                                quan -= st[1]
                                database.exec_nonquery([['DELETE FROM item_inventory_info WHERE UID = ? AND Expiry_Date = ?', (st[0], st[2])]])
                            elif st[1] > quan:
                                database.exec_nonquery([[sql_commands.update_expiry_stock, (-quan, _item[1], st[2])]])
                                break
                            else:
                                if stocks[-1] == st:
                                    database.exec_nonquery([[sql_commands.update_expiry_stock, (-quan, _item[1], st[2])]])
                                else:
                                    database.exec_nonquery([['DELETE FROM item_inventory_info WHERE UID = ? AND Expiry_Date = ?', (st[0], st[2])]])
                                break
                #modify the stock, applying the FIFO

                payment = float(self.payment_entry.get())
                self.change_total.configure(text = '₱' + format_price(payment - price_format_to_float(self.grand_total._text[1:])))
                #calculate and show the change

                database.exec_nonquery([[sql_commands.set_invoice_transaction_to_recorded, (datetime.now(), self._invoice_id)]])
                messagebox.showinfo('Succeed', 'Transaction Recorded')
                self._update_callback()
                self._treeview_callback()
                self.place_forget()
                #update the table
            
            '''Transaction Info'''
            self.client_info_frame = ctk.CTkFrame(self.content_frame)
            self.client_info_frame.grid(row=0, column=0,sticky="nsew", columnspan=2, padx=width*0.005, pady=height*0.01)
            self.client_info_frame.grid_columnconfigure(2, weight=1)
            
            self.cashier_frame = ctk.CTkFrame(self.client_info_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.25)
            self.cashier_frame.grid(row=0, column=0, padx=(width*0.005,0), pady= height*0.007)
            self.cashier_frame.pack_propagate(0)
            
            ctk.CTkLabel(self.cashier_frame, text="Cashier: ", font=("DM Sans Medium", 14)).pack(side="left", padx=(width*0.01))
            self.cashier_name = ctk.CTkLabel(self.cashier_frame, text="Jane Doe",  font=("DM Sans Medium", 14))
            self.cashier_name.pack(side="left")
            
            self.time_frame = ctk.CTkFrame(self.client_info_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.25)
            self.time_frame.grid(row=0, column=3, padx=width*0.005, pady= height*0.007, sticky="nse")
            
            """ self.time_label = ctk.CTkLabel(self.time_frame, fg_color=Color.White_Platinum, corner_radius=5, font=("DM Sans Medium", 14), text=datetime.now().strftime('%H : %M : %S'), width=width*0.085)
            self.time_label.pack(side="left", padx=(width*0.005, 0)) """
            
            self.date_label = ctk.CTkLabel(self.time_frame, fg_color=Color.White_Platinum, corner_radius=5, font=("DM Sans Medium", 14), text=date.today().strftime('%B %d, %Y'), width=width*0.1)
            self.date_label.pack(side="right", padx=(width*0.005))
            
            self.receipt_frame = ctk.CTkFrame(self.content_frame)
            self.receipt_frame.grid(row=1, column=0, sticky="nsew",padx=width*0.005, pady=(0,height*0.01))
            self.receipt_frame.grid_rowconfigure(1, weight=1)
            self.receipt_frame.grid_columnconfigure(1,weight=1)
            
            self.client_frame = ctk.CTkFrame(self.receipt_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.25)
            self.client_frame.grid(row=0, column=0, padx=width*0.005, pady= height*0.007)
            self.client_frame.pack_propagate(0)
            
            ctk.CTkLabel(self.client_frame, text="Client: ", font=("DM Sans Medium", 14)).pack(side="left", padx=(width*0.01,width*0.0165))
            self.client_name = ctk.CTkLabel(self.client_frame, text="Jane Doe",  font=("DM Sans Medium", 14))
            self.client_name.pack(side="left")
            
            """ self.pet_frame = ctk.CTkFrame(self.receipt_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.25)
            self.pet_frame.grid(row=0, column=2, padx=(0,width*0.005), pady= height*0.007)
            self.pet_frame.pack_propagate(0)
            
            ctk.CTkLabel(self.pet_frame, text="Pet: ", font=("DM Sans Medium", 14)).pack(side="left", padx=(width*0.01,width*0.0165))
            self.pet_name = ctk.CTkLabel(self.pet_frame, text="Jane Doe",  font=("DM Sans Medium", 14))
            self.pet_name.pack(side="left") """
            
            self.receipt_table_frame = ctk.CTkFrame(self.receipt_frame)
            self.receipt_table_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=width*0.005, pady=(0,height*0.007) )
            self.receipt_table_frame.grid_columnconfigure(0,weight=1)
            self.receipt_table_frame.grid_rowconfigure(0, weight=1)
            
            '''TABLE SETUP'''
            
            self.receipt_table_style = ttk.Style()
            self.receipt_table_style.theme_use("clam")
            self.receipt_table_style.configure("Treeview", rowheight=int(height*0.065), background=Color.White_Platinum, foreground=Color.Blue_Maastricht, bd=0,  highlightthickness=0, font=("DM Sans Medium", 16) )
            
            self.receipt_table_style.configure("Treeview.Heading", font=("DM Sans Medium", 18), background=Color.Blue_Cobalt, borderwidth=0, foreground=Color.White_AntiFlash)
            self.receipt_table_style.layout("Treeview",[("Treeview.treearea",{"sticky": "nswe"})])
            self.receipt_table_style.map("Treeview", background=[("selected",Color.Blue_Steel)])
            
            
            self.columns = ("rec_no", "particulars","qty","unit_price", "total")
            
            self.receipt_tree = ttk.Treeview(self.receipt_table_frame, columns=self.columns, show="headings",)
           
            self.receipt_tree.heading("rec_no", text="No")
            self.receipt_tree.heading("particulars", text="Particulars")
            self.receipt_tree.heading("qty", text="Qty")
            self.receipt_tree.heading("unit_price", text="UnitPrice")
            self.receipt_tree.heading("total", text="Total")

            self.receipt_tree.column("rec_no", width=int(width*0.05),anchor="e")
            self.receipt_tree.column("particulars", width=int(width*0.4), anchor="w")
            self.receipt_tree.column("qty", width=int(width*0.085), anchor="e")
            self.receipt_tree.column("unit_price", width=int(width*0.1), anchor="e")
            self.receipt_tree.column("total", width=int(width*0.1225), anchor="e")
            
            self.receipt_tree.tag_configure("odd",background=Color.White_AntiFlash)
            self.receipt_tree.tag_configure("even",background=Color.White_Ghost)
            
            self.receipt_tree.grid(row=0, column=0, sticky="nsew")
            
            self.y_scrollbar = ttk.Scrollbar(self.receipt_table_frame, orient=tk.VERTICAL, command=self.receipt_tree.yview)
            self.receipt_tree.configure(yscroll=self.y_scrollbar.set)
            self.y_scrollbar.grid(row=0, column=1, sticky="ns")
            
            #Sample
            '''for i in range(1, 10+1):
                if (i % 2) == 0:
                    tag = "even"
                else:
                    tag ="odd"
                self.receipt_tree.insert(parent='', index='end', iid=i, text="", values=(f"{i} "," Sample",1,500,500), tags=tag )'''

            '''END TABLE SETUP'''
            self.receipt_total_frame = ctk.CTkFrame(self.receipt_frame, height=height*0.05, width=width*0.2, fg_color=Color.White_Lotion)
            self.receipt_total_frame.grid(row=2, column=2, padx=(0,width*0.005), pady= (0,height*0.007), sticky="e")
            self.receipt_total_frame.pack_propagate(0)
            
            ctk.CTkLabel(self.receipt_total_frame, text="Total: ", font=("DM Sans Medium", 16)).pack(side="left", padx=(width*0.01,width*0.0165))
            self.receipt_total_amount = ctk.CTkLabel(self.receipt_total_frame, text="₱ 000,000.00",  font=("DM Sans Medium", 16))
            self.receipt_total_amount.pack(side="right", padx=(0,width*0.01))
            
            self.payment_frame= ctk.CTkFrame(self.content_frame, width=width*0.25)
            self.payment_frame.grid(row=1, column=1, sticky="nsew", padx=(0,width*0.005), pady=(0,height*0.01))
            self.payment_frame.grid_columnconfigure(1, weight=1)
            self.payment_frame.grid_rowconfigure(1, weight=1)
            self.payment_frame.grid_propagate(0)
            
            self.pay_frame = ctk.CTkFrame(self.payment_frame, fg_color=Color.White_Lotion, height=height*0.35)
            self.pay_frame.grid(row=0, column=0, columnspan=2, padx=(width*0.005), pady=(height*0.007), sticky="nsew")
            self.pay_frame.grid_propagate(0)
            self.pay_frame.grid_columnconfigure(1, weight=1)
            
            ctk.CTkLabel(self.pay_frame, text="Services: ", font=("DM Sans Medium",16),).grid(row=0, column=0, padx=(width*0.01), pady=(height*0.025,0))
            self.services_total = ctk.CTkLabel(self.pay_frame, text="₱ 000,000.00", font=("DM Sans Medium",16), anchor='e')
            self.services_total.grid(row=0, column=2, padx=(width*0.01), pady=(height*0.025,0), sticky = 'e')
            
            ctk.CTkLabel(self.pay_frame, text="Items: ", font=("DM Sans Medium",16),).grid(row=1, column=0, padx=(width*0.01), pady=(height*0.01,0), sticky="w")
            self.items_total = ctk.CTkLabel(self.pay_frame, text="₱ 000,000.00", font=("DM Sans Medium",16), anchor= 'e')
            self.items_total.grid(row=1, column=2, padx=(width*0.01), pady=(height*0.005,height*0.01), sticky = 'e')
            
            ctk.CTkFrame(self.pay_frame, fg_color="black", height=height*0.005).grid(row=2, column=0, columnspan=3, sticky="ew", padx=(width*0.01),pady=(height*0.01,0))
            
            ctk.CTkLabel(self.pay_frame, text="Total: ", font=("DM Sans Medium",16),).grid(row=3, column=0, padx=(width*0.01), pady=(height*0.01,0), sticky="w")
            self.grand_total = ctk.CTkLabel(self.pay_frame, text="₱ 000,000.00", font=("DM Sans Medium",16), anchor='e')
            self.grand_total.grid(row=3, column=2, padx=(width*0.01), pady=(height*0.01,height*0.01), sticky = 'e')
            
            ctk.CTkLabel(self.pay_frame, text="Payment: ", font=("DM Sans Medium",16),).grid(row=4, column=0, padx=(width*0.01), pady=(height*0.025,0), sticky="w")
            self.payment_entry = ctk.CTkEntry(self.pay_frame, font=("DM Sans Medium",16), justify="right")
            self.payment_entry.grid(row=4, column=2, padx=(width*0.01), pady=(height*0.025,height*0.01),)
            
            ctk.CTkLabel(self.pay_frame, text="Change: ", font=("DM Sans Medium",16),).grid(row=5, column=0, padx=(width*0.01), pady=(height*0.01,0), sticky="w")
            self.change_total = ctk.CTkLabel(self.pay_frame, text="₱ 000,000.00", font=("DM Sans Medium",16))
            self.change_total.grid(row=5, column=2, padx=(width*0.01), pady=(height*0.005,height*0.01), sticky = 'e')
            self.change_total.focus()
            
            self.complete_button = ctk.CTkButton(self.payment_frame, text="Complete",font=("DM Sans Medium",16), command= record_transaction)
            self.complete_button.grid(row=2, column=1, sticky="nsew", padx=(width*0.005), pady=(height*0.007))
            
            self.cancel_button = ctk.CTkButton(self.payment_frame, text="Cancel", fg_color=Color.Red_Pastel, hover_color=Color.Red_Tulip
                                               ,font=("DM Sans Medium",16), width=width*0.065, height=height*0.05)
            self.cancel_button.configure(command=self.reset)
            self.cancel_button.grid(row=2, column=0, sticky="nsew", padx=(width*0.005,0), pady=(height*0.007))
        def reset(self):
            self.place_forget()

        def place(self, invoice_data: tuple, cashier: str, treeview_callback: callable, update_callback: callable, **kwargs):
            self.cashier_name.configure(text = cashier)
            self.client_name.configure(text = invoice_data[1])
            self.services_total.configure(text = invoice_data[2])
            self.items_total.configure(text = invoice_data[3])
            self.grand_total.configure(text = invoice_data[4])
            self._treeview_callback = treeview_callback
            self._update_callback = update_callback
            self._invoice_id = invoice_data[0]

            for i in self.receipt_tree.get_children():
                self.receipt_tree.delete(i)
            #emptied out the treeview

            self.services = database.fetch_data(sql_commands.get_invoice_service_content_by_id, (invoice_data[0], ))
            self.items = database.fetch_data(sql_commands.get_invoice_item_content_by_id, (invoice_data[0], ))

            modified_services = [(f'{s[0]} P:{s[1]} D:%s' % s[2].strftime('%m/%d/%y'), 1,  s[3]) for s in self.services]

            temp = self.items + modified_services
            for i in range(len(temp)):
                self.receipt_tree.insert(parent='', index='end', iid=i, text="", values=(i+1, ) +temp[i])
                
            return super().place(**kwargs)
    return instance(master, info)  