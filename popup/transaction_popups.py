import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
import sql_commands
from util import *
from tkinter import messagebox
from constants import action
from customtkinter.windows.widgets.core_widget_classes import DropdownMenu
from decimal import Decimal

def show_list(master, info:tuple):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple):
            self._master = master
            self.width = info[0]
            self.height = info[1]
            self._treeview: cctk.cctkTreeView = info[2]
            super().__init__(master, self.width * .8, self.height *.8, corner_radius= 0)

            self.columnconfigure(0, weight=1)
            self.rowconfigure(1, weight=1)
            self.grid_propagate(0)

            self.upper_frame = ctk.CTkFrame(self, height= self.height * .075, corner_radius= 0, fg_color='#222222')
            self.upper_frame.pack_propagate(0)
            self.upper_frame.grid(row = 0, column = 0, sticky = 'we')
            ctk.CTkLabel(self.upper_frame, text='Add Item', font=('Arial', 24)).pack(side=ctk.LEFT, padx = (12, 0))
            self.data = database.fetch_data(sql_commands.get_item_and_their_total_stock, None)
            self.lower_frame = ctk.CTkFrame(self, corner_radius=0, fg_color='#111111')
            self.item_table = cctk.cctkTreeView(self.lower_frame, self.data, self.width * .75, self.height * .65,
                                                column_format='/name:x-tl/quantity:250-tl!50!30',
                                                double_click_command= self.get_item)
            self.item_table.pack(pady = (12, 0), fill='y')
            self.select_btn = ctk.CTkButton(self.lower_frame, 120, 30, text='select', command= self.get_item)
            self.select_btn.pack(pady = (0, 12))
            self.lower_frame.grid(row = 1, column = 0, sticky = 'nsew')
            #self.back_btn = ctk.CTkButton(self, width*.03, height * .4, text='back', command= reset).pack(pady = (12, 0))

        def place(self, **kwargs):
            self.data = database.fetch_data(sql_commands.get_item_and_their_total_stock, None)
            self.item_table.update_table(self.data)
            return super().place(**kwargs)

        def reset(self):
            self.place_forget()

        def get_item(self, _: any = None):
            #if there's a selected item
            if self.item_table.data_grid_btn_mng.active is not None:
                item_name =  self.item_table.data_grid_btn_mng.active.winfo_children()[0]._text
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
                        master.change_total_value(-float(price_column._text))
                        #before change

                        price_change = quantity_column._base_val * quantity_column.value
                        master.change_total_value(price_change)
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
                    , int(self.item_table.data_grid_btn_mng.active.winfo_children()[1]._text)))
                    #add a new record
                    master.change_total_value(transaction_data[2])

                self.item_table.data_grid_btn_mng.deactivate_active()
                self.reset()
                #reset the state of this popup
    return instance(master, info)

def show_transaction_proceed(master, info:tuple, transaction_info: tuple) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, transaction_info: list):
            width = info[0]
            height = info[1]
            #basic inforamtion needed; measurement

            self.acc_cred = info[3]
            print(self.acc_cred)
            self._treeview = info[2]
            self._transaction_info = transaction_info
            #encapsulation

            super().__init__(master, width * .835, height=height*0.92, corner_radius= 0, fg_color="red")
            #the actual frame, modification on the frame itself goes here

            '''events'''
            def record_transaction():
                record_id =  database.fetch_data(sql_commands.generate_id_transaction, (None))[0][0]
                database.exec_nonquery([[sql_commands.record_transaction, (record_id, self.acc_cred[0], transaction_info[1])]])
                modified_items_list = [(record_id, s[0], s[1], float(s[2]), s[3], 0) for s in transaction_info[0]]
                database.exec_nonquery([[sql_commands.record_transaction_content, s] for s in modified_items_list])
                #record transaction

                for item in modified_items_list:
                    stocks = database.fetch_data(sql_commands.get_specific_stock, (item[1], ))
                    if stocks[0][2] is None:
                        print((-item[4], item[0]))
                        database.exec_nonquery([[sql_commands.update_non_expiry_stock, (-item[4], item[1])]])
                    else:
                        quan = item[4]
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

                master.reset()
                messagebox.showinfo('Sucess', 'Transaction Complete')
                self._treeview.delete_all_data()
                self.destroy()
                #reset into its default state

            #From here
            self.boxframe = ctk.CTkFrame(self , width * .815, height=height*0.82, bg_color='black', fg_color='white')
            self.boxframe.grid(row=1, column=1, padx=width*0.217, pady=height*0.22, sticky="nesw")
            self.boxframe.grid_columnconfigure(0, weight=1)
            self.boxframe.grid_rowconfigure(0, weight=1)

            self.left_frame = ctk.CTkFrame(self.boxframe, bg_color='#c3c3c3')
            self.left_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsw")

            self.services_lbl = ctk.CTkLabel(self.left_frame, text='Services:',font=("DM Sans Medium", 25))
            self.services_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

            self.services_entry = ctk.CTkEntry(self.left_frame, placeholder_text='item1', height=height*0.65, width=width*0.2)
            self.services_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ns")

            self.right_frame = ctk.CTkFrame(self.boxframe)
            self.right_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

            self.items_lbl = ctk.CTkLabel(self.right_frame, text='Items:',font=("DM Sans Medium", 25))
            self.items_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

            #self.items_entry = ctk.CTkEntry(self.right_frame, placeholder_text='item1', height=height*0.65, width=width*0.2)
            #self.items_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ns")4
            #self.item_data = [(s[1] + (f' x {s[3]}' if int(s[3]) > 1 else ''), format_price(float(s[4]))) for s in self._transaction_info[0]]
            self.item_data = [('item1', format_price(float(s[4]))) for s in self._transaction_info[0]]
            self.item_list = cctk.cctkTreeView(self.right_frame, self.item_data, height=height*0.55, width=width*0.2,
                                               column_format=f'/No:{int(width * .03)}-#c/Name:x-tl/Price:{int(width * .05)}-tr!50!30')
            self.item_list.grid(row=1, column=0, padx=10, pady=10, sticky="ns")

            self.rightmost_frame = ctk.CTkFrame(self.boxframe, height=height*0.78, width=width*0.312, fg_color='white')
            self.rightmost_frame.grid(row=0, column=2, padx=20, pady=10, sticky="ne")

            self.total_frame = ctk.CTkFrame(self.rightmost_frame)
            self.total_frame.grid(row=0, column=0, padx=10, pady=10, sticky="new")

            self.total_lbl = ctk.CTkLabel(self.total_frame, text='Total:',font=("DM Sans Medium", 15))
            self.total_lbl.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")

            self.total_val = ctk.CTkEntry(self.total_frame, height=height*0.12, width=width*0.285, font=('DM Sans Medium', 35))
            self.total_val.insert(0, self._transaction_info[1])
            self.total_val.configure(state = 'readonly')
            self.total_val.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="n")

            self.payment_options_frame = ctk.CTkFrame(self.rightmost_frame)
            self.payment_options_frame.grid(row=1, column=0, padx=10, pady=(10, height*0.375), sticky="new")

            self.payment_lbl = ctk.CTkLabel(self.payment_options_frame, text='Payment Method:',font=("DM Sans Medium", 15))
            self.payment_lbl.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")

            self.payment_method_cbox = ctk.CTkOptionMenu(self.payment_options_frame, values=["Cash", "Card", "Bank Statement"], height=height*0.05,width=width*0.285)
            self.payment_method_cbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

            self.proceed_button = ctk.CTkButton(self.rightmost_frame, text='Proceed', command= record_transaction)
            self.proceed_button.grid(row=3, column=0, padx=10, pady=10, sticky="sew")
            self.cancel_button = ctk.CTkButton(self.rightmost_frame, text='Cancel', command= lambda: self.destroy())
            self.cancel_button.grid(row=4, column=0, padx=10, pady=10, sticky="sew")

    return instance(master, info, transaction_info)