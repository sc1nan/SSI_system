from typing import Optional, Tuple, Union
import customtkinter as ctk
import tkinter as tk
from typing import *

from customtkinter.windows.widgets.font import CTkFont
from util import *
from functools import partial
from util import brighten_color
import re
from tkinter import messagebox;
from tkcalendar import Calendar
import datetime
from PIL import Image
import sql_commands
import sys

class customcustomtkinter:
    class ctkButtonFrame(ctk.CTkFrame):
        def __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: Optional[Union[int, str]] = None,
                     border_width: Optional[Union[int, str]] = None, bg_color: Union[str, Tuple[str, str]] = "transparent",
                     fg_color: Optional[Union[str, Tuple[str, str]]] = None, border_color: Optional[Union[str, Tuple[str, str]]] = None,
                     background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                     overwrite_preferred_drawing_method: Union[str, None] = None, command: Union[Callable[[],None], None] = None,
                     hover: bool = True, hover_color: Union[str, Tuple[str, str]] = "transparent",
                     double_click_command: Union[Callable[[],None], None] = None, **kwargs):
            super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color,
                             background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
            # sets the default properties of a frame

            self.og_color = self._fg_color
            self._hover_color = hover_color
            self._command = [] if isinstance(command, list) else [command]
            self._hover = hover
            self._doulbe_click_command = double_click_command
            #make a reference/encapsulation from extended arguments

            self.bind('<Button-1>', self.response)
            self.bind('<Double-Button-1>', None if self._doulbe_click_command == None else self._doulbe_click_command)
            self.pack_propagate(0)
            self.grid_propagate(0)
            self.update_button(hover)
            #set the property as a button

        def response(self, _: any = None):
                click_color = (brighten_color(self._hover_color[0], 1.25, brighten_color(self._hover_color[1], 1.25))) if isinstance(self._hover_color, tuple) else brighten_color(self._hover_color, 1.45)
                self.configure(fg_color = click_color)
                self.update()
                self.after(50)
                self.configure(fg_color = self._hover_color)
                for cmd in self._command:
                    if callable(cmd):
                        cmd()
        #click response of the button; includes the flash when clicked

        def update_button(self, is_hover: bool = True):
            if is_hover:
                self.bind('<Enter>', lambda _: self.configure(fg_color = self._hover_color))
                self.bind('<Leave>', lambda _: self.configure(fg_color = self.og_color))
            else:
                self.unbind('<Enter>', None)
                self.unbind('<Leave>', None)
        #update the frame's external properties

        def update_children(self):
            child = self.winfo_children()
            for i in child:
                i.unbind('<Button-1>', None)
                i.bind('<Button-1>', self.response)
                i.unbind('<Double-Button-1>', None)
                i.bind('<Double-Button-1>', None if self._doulbe_click_command == None else self._doulbe_click_command)
                if self._hover:
                    i.bind('<Enter>', lambda _: self.configure(fg_color = self._hover_color))
                    i.bind('<Leave>', lambda _: self.configure(fg_color = self.og_color))
                else:
                    i.unbind('<Enter>', None)
                    i.unbind('<Leave>', None)
        #update all the children properties to mimic the button properties

        def configure(self, require_redraw=False, command: Optional[Callable[[], None]] = None, hover: Optional[bool] = None,
                      hover_color: Optional[Union[str, Tuple[str, str]]] = None, **kwargs):
            if command is not None:
                self._command = [] if isinstance(command, list) else [command]
                self.unbind('<Button-1>', None)
                self.bind('<Button-1>', self.response)
                self.update_children()
            if hover_color is not None:
                self._hover_color = hover_color
                self.unbind('<Enter>', None)
                self.bind('<Enter>', lambda _: self.configure(fg_color = self._hover_color))
            if hover is not None:
                self._hover = hover
                self.update_button(hover)
                self.update_children()
            if 'double_click_command' in kwargs:
                self.unbind('<Double-Button-1>', None)
                self._doulbe_click_command = kwargs['double_click_command']
                self.bind('<Double-Button-1>', kwargs['double_click_command'])
                self.update_children()
                kwargs.pop('double_click_command')
            if 'og_color' in kwargs:
                self.og_color = kwargs['og_color']
                kwargs['fg_color'] = kwargs['og_color']
                kwargs.pop('og_color')
            return super().configure(require_redraw, **kwargs)
        #override configure function of frame, allowing to add those external arguments
    #button frame: a frame with a properties of a buttons

    class menubar(ctk.CTkFrame):
        def __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: Optional[Union[int, str]] = None,
                     border_width: Optional[Union[int, str]] = None, bg_color: Union[str, Tuple[str, str]] = "transparent",
                     fg_color: Optional[Union[str, Tuple[str, str]]] = None, border_color: Optional[Union[str, Tuple[str, str]]] = None,
                     background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                     overwrite_preferred_drawing_method: Union[str, None] = None, position: tuple = (0, 0, 'c'), **kwargs):
            super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors,
                             overwrite_preferred_drawing_method, **kwargs)

            self._position = position
            self._shadow = ctk.CTkFrame(master, 0, 0)
            self.pack_propagate(0)
            self.grid_propagate(0)

        def place(self):
            #place shadow here
            return super().place(relx = self._position[0], rely = self._position[1], anchor = self._position[2])
        #override the place to place a shadow first

        def update_pos(self,  position: tuple = (0, 0, 'c')):
            self.deiconify()
            self._position = position
            self.place()
        #update the position, including the shadow

        def deiconify(self):
            self._shadow.place_forget()
            self.place_forget()
        #hide the menubar

    class scrollable_menubar(ctk.CTkScrollableFrame):
        def __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: Optional[Union[int, str]] = None,
                     border_width: Optional[Union[int, str]] = None, bg_color: Union[str, Tuple[str, str]] = "transparent",
                     fg_color: Optional[Union[str, Tuple[str, str]]] = None, border_color: Optional[Union[str, Tuple[str, str]]] = None,
                     background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                     overwrite_preferred_drawing_method: Union[str, None] = None, position: tuple = (0, 0, 'c'), **kwargs):
            super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors,
                             overwrite_preferred_drawing_method, **kwargs)

            self._position = position
            self._shadow = ctk.CTkFrame(master, 0, 0)

        def place(self):
            #place shadow here
            return super().place(relx = self._position[0], rely = self._position[1], anchor = self._position[2])
        #override the place to place a shadow first

        def update_pos(self,  position: tuple = (0, 0, 'c')):
            self.deiconify()
            self._position = position
            self.place()
        #update the position, including the shadow

        def deiconify(self):
            self._shadow.place_forget()
            self.place_forget()
        #hide the menubar

    class cctkTreeView(ctk.CTkFrame):
        def __init__(self, master: any, data: Union [Union[tuple, list], None] = None, width: int = 200, height: int = 200, corner_radius: Optional[Union[int, str]] = None,
                     border_width: Optional[Union[int, str]] = None, bg_color: Union[str, Tuple[str, str]] = "transparent",
                     fg_color: Optional[Union[str, Tuple[str, str]]] = Color.White_Platinum, border_color: Optional[Union[str, Tuple[str, str]]] = None,
                     background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                     overwrite_preferred_drawing_method: Union[str, None] = None,


                     column_format: str = '/Title1:x-t/Title2:x-t/Title3:x-t!30!30',
                     header_color: Union[str, tuple] = Color.Blue_Cobalt, data_grid_color: Union[list, tuple] = (Color.White_Ghost, Color.Grey_Bright_2),
                     selected_color: Union [tuple, str] = "#2C74B3",
                     conditional_colors: Union[dict, None] = {-1: {-1:None}}, navbar_font: tuple = ('DM Sans Medium', 16),
                     row_font: tuple = ('DM Sans Medium', 14), row_hover_color: Union [tuple, str] = '#2C74B3', content_color: Optional[Union[str, Tuple[str, str]]] = 'transparent',
                     double_click_command: Union[Callable[[],None], None] = None, record_text_color: Optional[Union[str, Tuple[str, str]]] = Color.Blue_Maastricht,
                     nav_text_color: Optional[Union[str, Tuple[str, str]]] = "white",
                     bd_configs: Union[List[Tuple[int, Union[List[ctk.CTkLabel], ctk.CTkLabel]]], None] = None, bd_pop_list: list = None,
                     c_bd_configs: Optional[Tuple[str, Union[List[Tuple[int, Union[List[ctk.CTkLabel], ctk.CTkLabel]]], None]]] = None,
                     bd_message: Optional[str] = 'Are you sure you want to delete the data',
                     bd_commands = None, spinner_config: Optional[Tuple[int, int, int, str, str, Literal['multiply', 'add']]] = None, 
                     spinner_val_range: Tuple[int, int] = None, spinner_command: callable = None, spinner_initial_val: int = 0, **kwargs):

            super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors,
                             overwrite_preferred_drawing_method, **kwargs)

            if not re.fullmatch(r'(\/\w+:(x|\d+)-(\w+|\#\w+))+\!\d+\!\d+', column_format):
                ctk.CTkLabel(self, text='Wrong format\nCheck for errors').place(relx = .5, rely = .5, anchor = 'c')
                return;
            #check if the format follows the guideline, if it doesn't it will only pop a label
            self._bd_pop_list: list = bd_pop_list
            self._column_format  = column_format
            self.column_titles = [s.replace('/', '') for s in re.findall(r'\/\w+', self._column_format)]
            self.column_types = [str(s) for s in re.findall(r'\-(\w+|\#\w+)', self._column_format)]
            total_fixed_width = sum([int(s) for s in re.findall(r'\:(x|\d+)', self._column_format) if str(s).isnumeric()])
            x_width = (self._current_width - (total_fixed_width + 14)) / len(re.findall(r'\:x', self._column_format))//1
            #set the measurements of the treeview according to the format given

            self.data_frames = []
            self._data = []
            self.data_grid_btn_mng = None
            self.column_widths = [x_width - 1 if s == 'x' else int(s) - 1 for s in re.findall(r'\:(x|\d+)', self._column_format)]
            self._header_heights = int(re.findall(r'\!(\d+)', column_format)[0])
            self._data_grid_heights = int(re.findall(r'\!(\d+)', column_format)[1])
            self._header_color = header_color
            self._data_grid_color = (data_grid_color[0], data_grid_color[1]) if isinstance(data_grid_color, tuple) else((data_grid_color[0][0], data_grid_color[1][0]), (data_grid_color[0][1], data_grid_color[1][1]))
            self._conditional_colors = conditional_colors
            self.navbar_font = navbar_font
            self.row_font = row_font
            self._selected_color =selected_color
            self._row_hover_color = row_hover_color
            self._double_click_command = double_click_command
            self.bd_configs = bd_configs
            self.c_bd_configs = c_bd_configs
            self._record_text_color = record_text_color
            self._content_color = content_color
            self._nav_text_color = nav_text_color
            self.bd_commands = bd_commands
            self.spinner_val_range = spinner_val_range or [customcustomtkinter.cctkSpinnerCombo.MIN_VAL, customcustomtkinter.cctkSpinnerCombo.MAX_VAL]
            self.spinner_config = spinner_config
            self.spinner_command = spinner_command
            self.spinner_initial_val = spinner_initial_val
            self._bd_message=bd_message
            #encapsulate other arguments

            self.pack_propagate(0)
            self.grid_propagate(0)
            self.grid_rowconfigure(1, weight=1)

            #make the root frame fixed in sizesz
            for i in range(len(self.column_titles)):
                btn = None
                title = ' '.join(re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', self.column_titles[i]))
                if self.column_types[i] == 't' or self.column_types[i] == '#' or self.column_types[i] == 'q':
                    btn = customcustomtkinter.ctkButtonFrame(self, self.column_widths[i], self._header_heights, 0, fg_color= self._header_color,
                                                             hover_color= brighten_color(self._header_color, 1.75))
                    title = ctk.CTkLabel(btn, text=title, font=self.navbar_font, text_color=self._nav_text_color)
                    title.place(relx = .5, rely = .5, anchor = 'c',)
                    btn.update_children()
                else:
                    btn = ctk.CTkLabel(self, self.column_widths[i], self._header_heights, 0, fg_color= self._header_color,
                                       text=title, font= self.navbar_font, text_color=self._nav_text_color)
                btn.grid(row = 0, column = i, sticky='we', padx = (1,0))
                self.update()
            #generate the header bar

            self.scroll_bar_btn = customcustomtkinter.ctkButtonFrame(self, 14, self._header_heights, 0, fg_color=self._header_color,
                                                                     hover_color= brighten_color('#006611', 1.75),
                                                                     command = lambda: self.contents._parent_canvas.yview_moveto(0 if (self.contents._parent_canvas.yview()[1] > .5) else 1))
            self.scroll_bar_btn.grid(row = 0, column = len(self.column_titles), sticky='nsew')
            #additional button that will serve as go to top/down of a scroll bar

            self.contents = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color=self._content_color)
            self.contents.grid(row = 1, column = 0, columnspan = len(self.column_titles) + 1, sticky = 'news')
            #the data grid holder

            '''initial generation here'''
            if(data is not None):
                self.add_data(data)
            #generates data grid

            self.data_grid_btn_mng = customcustomtkinterutil.button_manager(self.data_frames, self._selected_color, True, None)
            #add a radio button like properties from each of the rows of the data grid

        def id_func(self, dlt_btn: ctk.CTkButton, val):
            lbl = dlt_btn.master.master.winfo_children()[self.column_types.index('q')]
            lbl.configure(text = str(int(lbl.cget('text')) + val))

        def bd_func(self, dlt_btn: ctk.CTkButton):
            if messagebox.askyesno('Warning', self._bd_message, parent = self):
                data_mngr_index = self.data_grid_btn_mng._buttons.index(dlt_btn.master.master)
                if callable(self.bd_commands):
                    self.bd_commands(data_mngr_index)

                if self._bd_pop_list is not None:
                    if len(self._bd_pop_list) > 0:
                        self._bd_pop_list.pop(data_mngr_index)
                self.data_grid_btn_mng._buttons.pop(data_mngr_index)
                self.data_grid_btn_mng._og_color.pop(data_mngr_index)
                #remove the row from the button manager

                if self.data_grid_btn_mng.active == dlt_btn.master.master:
                    self.data_grid_btn_mng.active = None
                #active button was set to none if it was destroyed
                if(self.bd_configs is not None):
                    self.bd_deduction(dlt_btn)

                if(self.c_bd_configs is not None):
                    if(self.c_bd_configs[0] in self._data[data_mngr_index]):
                        self.c_bd_deduction(dlt_btn)

                dlt_btn.master.master.destroy()
                self._data.pop(data_mngr_index)
                for i in range(data_mngr_index, len(self.data_frames)):
                    color = self._data_grid_color[0] if i % 2 == 0 else self._data_grid_color[1]
                    self.data_grid_btn_mng._og_color[i] = color
                    self.data_frames[i].og_color = color
                    self.data_frames[i].configure(fg_color = color)
                    if '#' in str(self.column_types):
                        for j in range(len(self.column_types)):
                            if '#' in self.column_types[j]:
                                lbl: ctk.CTkLabel = self.data_frames[i].winfo_children()[j]
                                lbl.configure(text = int(lbl._text) - 1)
                    #update the number order of the frames
                #update the fg color of each of the frames, maintaining the alternating pattern

        def add_data(self, data: Union[tuple, list], update_button_manager: bool = False):
            d = [data] if isinstance(data, tuple) else data
            for i in range(len(d)):
                tI = 0;
                frm = customcustomtkinter.ctkButtonFrame(self.contents, height=self._data_grid_heights, width=15,
                                                         fg_color=self._data_grid_color[0] if len(self.data_frames) % 2 == 0 else self._data_grid_color[1],
                                                         corner_radius= 0, hover_color= self._row_hover_color,
                                                         double_click_command= self._double_click_command)
                self.data_frames.append(frm)
                self._data.append(d[i])
                if self.data_grid_btn_mng is not None:
                    self.data_grid_btn_mng._og_color.append(frm._fg_color)
                for j in range(len(self.column_widths)):
                    #for label type column
                    if self.column_types[j][0] in ['t', '#']:
                        temp_lbl = ctk.CTkLabel(frm, text= d[i][tI] if self.column_types[j][0] in ['t','T'] else (len(self._data)), width = self.column_widths[j],
                                            justify = ctk.RIGHT, font= self.row_font, text_color = self._record_text_color)
                        txt_clr = self._record_text_color if j not in self._conditional_colors else self._conditional_colors[j].get(temp_lbl._text, self._record_text_color)
                        temp_lbl.configure(text_color = txt_clr)
                        temp_lbl._label.grid_forget()
                        temp_lbl._label.grid(row = 0, column=0, sticky='nsew', padx=(12, 12))
                        temp_lbl._label.configure(anchor= 'w' if self.column_types[j][1] == 'l' else 'e' if self.column_types[j][1] == 'r' else 'c')
                        temp_lbl.pack(side = tk.LEFT, fill = 'y', padx = (1,0))
                        text_overflow_ellipsis(temp_lbl, self.column_widths[j] * .9)
                    #for info tab column
                    elif self.column_types[j] == 'iT':
                        temp:customcustomtkinter.info_tab = customcustomtkinter.info_tab(frm, width= self.column_widths[j], corner_radius= 0,
                                                                                         border_width=0, fg_color='transparent')
                        temp.pack(side = tk.LEFT, fill = 'y', padx = (1,0))
                        #modified_data = list(self._data[-1]).insert(j, temp.val)
                    #for special type column
                    else:
                        temp = ctk.CTkFrame(frm, width= self.column_widths[j], corner_radius= 0, border_width=0, fg_color='transparent')
                        temp.pack(side = tk.LEFT, fill = 'y', padx = (1,0))
                        if self.column_types[j] == 'bD':
                            dlt_btn = ctk.CTkButton(temp, self._data_grid_heights * .8, self._data_grid_heights * .8, fg_color=Color.Red_Pastel, hover_color=Color.Red_Pastel_Hover ,text='-')
                            dlt_btn.configure(command = partial(self.bd_func, dlt_btn))
                            dlt_btn.place(relx = .5, rely = .5, anchor = 'c')
                            continue;
                        elif self.column_types[j] == 'id':
                            spinner = customcustomtkinter.cctkSpinnerCombo(temp ,step_count=1, entry_font=("Lucida", 16), bg_color='transparent', fg_color='transparent', val_range= self.spinner_val_range, initial_val= self.spinner_initial_val, command= self.spinner_command)
                            spinner.place(relx = .5, rely = .5, anchor = 'c')

                    if self.column_types[j][0] == 't':
                        tI += 1
                # generates the content from the frame

                if self.spinner_config:
                    temp_spinner: customcustomtkinter.cctkSpinnerCombo = frm.winfo_children()[self.spinner_config[0]].winfo_children()[0]
                    text_source: ctk.CTkLabel = frm.winfo_children()[self.spinner_config[1]]
                    text_reciever: ctk.CTkLabel = frm.winfo_children()[self.spinner_config[2]]
                    source_format = self.spinner_config[3]
                    reciever_format = self.spinner_config[4]
                    mode = self.spinner_config[5]
                    #modified_data:list = list(self._data[i])
                    modified_data:list = list(d[i])
                    modified_data.insert(self.spinner_config[0] - self._column_format.count("#"), temp_spinner.value)

                    temp_spinner_command = temp_spinner._command
                    def modified_spinner_command(_: any = None):
                        if source_format != "":
                            formatted_text_source = float(re.sub(f"[{source_format}]", "", text_source._text))
                            #formatted_text_source = float(re.search(source_format, text_source._text)[0])
                        else:
                            formatted_text_source = float(text_source._text)
                        formatted_text_source = formatted_text_source * temp_spinner.value if mode == 'multiply' else formatted_text_source + temp_spinner.value
                        text_reciever.configure(text = reciever_format.format(formatted_text_source) if reciever_format != "" else formatted_text_source)
                        modified_data[self.spinner_config[0]  - self._column_format.count("#")] = temp_spinner.value
                        modified_data[self.spinner_config[2]  - self._column_format.count("#")] = text_reciever._text
                        self._data[self.data_frames.index(frm)] = tuple(modified_data)
                        if temp_spinner_command:
                            temp_spinner_command(temp_spinner.value)
                    #initial calling to modify the reciever

                    temp_spinner.configure(command = modified_spinner_command)
                    modified_spinner_command()
                #sets on which spinner would interact on which table

                frm.update_children()
                frm.pack(fill = 'x', pady = (1,0))
                self.contents.update()
                
            if update_button_manager:
                self.data_grid_btn_mng.update_buttons()

        def update_table(self, data: Union[tuple, list]):
            for i in self.data_frames:
                i.destroy()
            self.data_frames = []
            self._data = []
            self.add_data(data)
            self.data_grid_btn_mng = customcustomtkinterutil.button_manager(self.data_frames, self._selected_color, True, None)

        def bd_deduction(self, btn: ctk.CTkButton):
            for tup in self.bd_configs:
                item = float(price_format_to_float(btn.master.master.winfo_children()[tup[0]]._text[1:]))
                if isinstance(tup[1], list):
                    for lbls in tup[1]:
                        lbls.configure(text = format_price(float(price_format_to_float(lbls._text[1:])) - item))
                else:
                    tup[1].configure(text = format_price(float(price_format_to_float(tup[1]._text[1:])) - item))

        def c_bd_deduction(self, btn: ctk.CTkButton):
            for tup in self.c_bd_configs[1]:
                item = float(price_format_to_float(btn.master.master.winfo_children()[tup[0]]._text[1:]))
                if isinstance(tup[1], list):
                    for lbls in tup[1]:
                        lbls.configure(text = format_price(float(price_format_to_float(lbls._text[1:])) - item))
                else:
                    tup[1].configure(text = format_price(float(price_format_to_float(tup[1]._text[1:])) - item))

        def delete_all_data(self):
            for frm in self.data_frames:
                frm.destroy()
                self.data_frames.pop(0)
            #self.data_grid_btn_mng._buttons.clear()
            #self.data_grid_btn_mng._og_color.clear()
            self.data_grid_btn_mng = customcustomtkinterutil.button_manager(self.data_frames, self._selected_color, True, None)
            self._data = []

        def configure(self, require_redraw=False, **kwargs):
            if 'double_click_command' in kwargs:
                for i in self.data_frames:
                    self._double_click_command = kwargs['double_click_command']
                    i.configure(double_click_command = kwargs['double_click_command'])
                kwargs.pop('double_click_command')

            if 'spinner_command' in kwargs:
                self.spinner_command = kwargs['spinner_command']    
                if self.spinner_config:
                    for fr in self.data_frames:
                        spinner: customcustomtkinter.cctkSpinnerCombo = fr.winfo_children()[self.spinner_config[0]].winfo_children()[0]
                        if self.spinner_config is not None:
                            text_source: ctk.CTkLabel = fr.winfo_children()[self.spinner_config[1]]
                            text_reciever: ctk.CTkLabel = fr.winfo_children()[self.spinner_config[2]]
                            source_format = self.spinner_config[3]
                            reciever_format = self.spinner_config[4]
                            mode = self.spinner_config[5]
                            modified_data:list = list(self._data[self.data_frames.index(fr)])

                            temp_spinner_command = self.spinner_command
                            def modified_spinner_command(_: any = None):
                                if source_format != "":
                                    formatted_text_source = float(re.sub(f"[{source_format}]", "", text_source._text))
                                    #formatted_text_source = float(re.search(source_format, text_source._text)[0])
                                else:
                                    formatted_text_source = float(text_source._text)
                                formatted_text_source = formatted_text_source * spinner.value if mode == 'multiply' else formatted_text_source + spinner.value
                                text_reciever.configure(text = reciever_format.format(formatted_text_source) if reciever_format != "" else formatted_text_source)
                                modified_data[self.spinner_config[0] - self._column_format.count("#")] = spinner.value
                                modified_data[self.spinner_config[2] - self._column_format.count("#")] = text_reciever._text
                                self._data[self.data_frames.index(fr)] = tuple(modified_data)
                                if temp_spinner_command:
                                    temp_spinner_command(spinner.value)
                            spinner._command = modified_spinner_command
                        else:
                            spinner.configure(command = kwargs['spinner_command'])
                kwargs.pop('spinner_command')
            return super().configure(require_redraw, **kwargs)
        
        def get_selected_data(self):
            if(self.data_grid_btn_mng.active is None):
                return None
            return self._data[self.data_frames.index(self.data_grid_btn_mng.active)]
        
        def remove_selected_data(self):
            index = self.get_active_index()
            self.data_grid_btn_mng._og_color.pop(index)
            frame: ctk.CTkFrame = self.data_frames[index]

            frame.pack_forget()
            for fr in frame.winfo_children():
                fr.pack_forget()
                fr.destroy()
            frame.destroy()
            #sequence needed to delete the data_frames to the table; to prevent multiple exceptions

            self.data_frames.pop(index)
            self.data_grid_btn_mng.active = None
            self.data_grid_btn_mng.update_buttons()

        def get_active_index(self):
            return self.data_frames.index(self.data_grid_btn_mng.active)

    class tk_calendar(ctk.CTkToplevel):
        def __init__(self, label,format, *args, fg_color: str or Tuple[str, str] or None = None, date_format: str ="numerical",
                     min_date = None, max_date = None, set_date_callback: callable = None, date_select_default: datetime.datetime = None
                     ,**kwargs):
            super().__init__(*args, fg_color=fg_color, **kwargs)
            
            def set_date():
                date_text = None
                self.withdraw()
                if "numerical" in date_format:
                    #label.configure(text= ( format % (self.cal.get_date())))
                    date_text = str(self.cal.get_date())
                elif "raw" in date_format:
                    date_text = self.cal.selection_get()
                elif "word" in date_format:
                    #label.configure(text= f"{util.date_to_words(str(self.cal.get_date()))}")
                    date_text = str(date_to_words(str(self.cal.get_date())))
                else:
                    date_text = "Invalid Format"

                if str(type(label)) == "<class 'tkinter.StringVar'>":
                    label.set(date_text)
                else:
                    label.configure(text=date_text)
                
                if set_date_callback:
                    set_date_callback()

            position_X = (self.winfo_screenwidth()/2)
            position_Y = (self.winfo_screenheight()/2)-(400/2)


            self.title("Calendar")
            self.geometry("%dx%d+%d+%d"%(400,400,position_X,position_Y))
            self.resizable(0,0)

            date = date_select_default or datetime.datetime.now()

            self.cal = Calendar(self, year=date.year, month=date.month, day=date.day, showweeknumbers=False, date_pattern="mm-dd-yyyy",
                                mindate=min_date, maxdate = max_date, normalbackground="#EAEAEA", weekendbackground="#F3EFE0")
            self.cal.pack(fill="both", expand=True, padx=5, pady=5)

            self.set_date = ctk.CTkButton(self, text="Set Date", font=("Robot", 16), command=set_date)
            self.set_date.pack(pady=10)
            
            self.grab_set()
            self.attributes('-topmost',1)

        def withdraw(self):
            self.grab_release()
            return super().withdraw()


    class cctkSpinnerCombo(ctk.CTkFrame):
        MAX_VAL = 2147483647
        MIN_VAL = -2147483648
        NUM_ONLY = 'num_only'
        CLICK_ONLY = 'click_only'
        def __init__(self, master: any, width: int = 100, height: int = 30, corner_radius: Optional[Union[int, str]] = None,
                    border_width: Optional[Union[int, str]] = None, bg_color: Union[str, Tuple[str, str]] = "transparent",
                    fg_color: Optional[Union[str, Tuple[str, str]]] = None, border_color: Optional[Union[str, Tuple[str, str]]] = None,
                    background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                    overwrite_preferred_drawing_method: Union[str, None] = None,
                    #custom arguments
                    button_font: Optional[Tuple[str, int, str]] = ("DM Sans Medium",14), button_color: Optional[Union[str, Tuple[str, str]]] = (Color.Red_Pastel, '#3B8ED0'),
                    button_hover_color:  Optional[Union[str, Tuple[str, str]]] = (Color.Red_Pastel_Hover,"#36719F"), button_font_color: Optional[Union[str, Tuple[str, str]]] = ("black", "white"),
                    entry_font: Optional[Tuple[str, int, str]] = None, entry_text_color: Union[str, Tuple[str, str]] = 'black',
                    entry_fg_color:Optional[Tuple[str, int, str]] = None,
                    step_count: int = 1, val_range: Optional[Tuple[int, int]] = None, command:Callable = None,
                    increase_callback: callable = None, decrease_callback: callable = None,
                    base_val:int = 0, initial_val: int = 0, state: str = ctk.NORMAL, mode: Literal['num_only', 'click_only'] = 'num_only' ,**kwargs):
            super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

            self._btn_font = button_font
            self._step_count = step_count
            self._command  = command
            self._increase_callback = increase_callback
            self._decrease_callback = decrease_callback
            self._fg_color = fg_color
            self._btn_color = (button_color, button_color) if isinstance(button_color, str) else button_color
            self._btn_hover_color = (button_hover_color, button_hover_color) if isinstance(button_hover_color, str) else button_hover_color
            self._val_range = val_range or (self.MIN_VAL, self.MAX_VAL)
            self._val_range = (self._val_range[1], self._val_range[0]) if self._val_range[0] > self._val_range[1] else self._val_range
            self.value = initial_val;
            self._base_val = base_val
            self._entry_text_color = entry_text_color
            self._state = state
            self._mode = mode

            self.grid_columnconfigure((0,2), weight=0)
            self.grid_columnconfigure(1, weight=1)

            '''events'''

            self.sub_button = ctk.CTkButton(self,text="-", command=partial(self.change_value, -1), text_color=button_font_color,
                                            font=button_font, height=height, width=height, fg_color= self._btn_color[0], hover_color=self._btn_hover_color[0],
                                            state= self._state)
            self.sub_button.grid(row=0, column=0, padx=(width*0.05,0), pady=(height*0.1))

            self.num_entry = ctk.CTkEntry(self, height=height, width=width*.7, border_width=0, font=entry_font, text_color=entry_text_color,
                                        justify="c", fg_color='white')
            self.num_entry.configure(state= self._state)
            self.num_entry.grid(row=0, column=1, padx=(width*0.05),pady=(height*0.15))

            self.add_button = ctk.CTkButton(self, command=self.change_value, text_color=button_font_color,
                                            text="+", font=button_font,height=height, width=height, fg_color= self._btn_color[1], hover_color=self._btn_hover_color[1],
                                            state= self._state)
            self.add_button.grid(row=0, column=2, padx=(0,width*0.05),pady=(height*0.1))

            self.num_entry.insert(0, initial_val)

            #setting up the button property
            if self._mode ==  'click_only':
                self.num_entry.configure(state = 'readonly')
                #entry is uneditable
            if self._mode == 'num_only':
                stringvar = ctk.StringVar()
                stringvar.set(initial_val)
                self.num_entry.bind('<Return>', self.return_entry_func)
                self.num_entry.bind('<Button-1>', lambda _: self.num_entry.configure(state = 'normal'))
                self.num_entry.configure(textvariable = stringvar)
                stringvar.trace_add('write', self.entry_check_on_text_change_callback)
                #entry is editable but only num can be enter

        def get_val_range(self):
            try:
                return self._val_range
            except ValueError:
                return None
        
        def set_entry_state(self, state:str):
            self.num_entry.configure(state = state)

        def change_value(self, mul: int = 1):
            self.num_entry.configure(state = 'normal')
            if mul == 1 and self._increase_callback is not None and self.value < self._val_range[1]:
                self._increase_callback()
            if mul == -1 and self._decrease_callback is not None and self.value > self._val_range[0]:
                self._decrease_callback()
            try:
                val = self.value + (self._step_count * mul)
                val = self._val_range[0] if val < self._val_range[0] else self._val_range[1] if val > self._val_range[1] else val
                self.value = val;
                self.num_entry.delete(0, "end")
                self.num_entry.insert(0, val)
            except ValueError:
                return
            if self._command is not None:
                self._command()
            self.num_entry.configure(state = 'readonly')

        def entry_check_on_text_change_callback(self, _ = None, *__):
            try:
                txt = self.num_entry.get()
                if (not str(txt[-1]).isnumeric()) or len(txt) > 15:
                    #if either the last input is either not a number or the quantity is more than 15
                    self.num_entry.delete(len(txt)-1, ctk.END)
                    return
                if int(txt) not in range(self._val_range[0], self._val_range[-1]):
                    self.num_entry.delete(0, ctk.END)
                    self.num_entry.insert(0, self._val_range[0] if int(txt) < self._val_range[0] else self._val_range[-1])
                self.value = int(self.num_entry.get())
                if self._command is not None and self._mode == 'num_only':
                    self._command()
            except IndexError:
                pass

        def get(self) -> Union[int, None]:
            try:
                return int(self.num_entry.get())
            except ValueError:
                return None
        def set(self, value: int):
            self.num_entry.delete(0, ctk.END)
            self.num_entry.insert(0, str(value))

        def configure(self, require_redraw=False, **kwargs):

            if "value" in kwargs:
                self.value = kwargs["value"]
                self.num_entry.delete(0, "end")
                self.num_entry.insert(0, kwargs["value"])
                kwargs.pop("value")
            if "base_val" in kwargs:
                self._base_val = kwargs["base_val"]
                kwargs.pop("base_val")
            if "command" in kwargs:
                self._command = kwargs["command"]
                kwargs.pop("command")
            if "increase_callback" in kwargs:
                self._increase_callback = kwargs["increase_callback"]
                kwargs.pop("increase_callback")
            if "decrease_callback" in kwargs:
                self._decrease_callback = kwargs["decrease_callback"]
                kwargs.pop("decrease_callback")
            if "val_range" in kwargs:
                if isinstance(kwargs['val_range'], tuple):
                    self._val_range = kwargs['val_range']
                    if self.value < self._val_range[0]:
                        self.configure(value = self._val_range[0])
                    elif self.value > self._val_range[1]:
                        self.configure(value = self._val_range[1])
                kwargs.pop('val_range')
            if "state" in kwargs:
                self.add_button.configure(state = kwargs["state"])
                self.sub_button.configure(state = kwargs["state"])
                self.num_entry.configure(state = (kwargs["state"] if kwargs['state'] == ctk.NORMAL else "readonly"))
                kwargs.pop('state')
            if "mode" in kwargs:
                self.num_entry.unbind('<Return>', None)
                self.num_entry.unbind('<Button-1>', None)
                self.num_entry.configure(textvariable = None)
                self.num_entry.configure(state = 'readonly')
                kwargs.pop('mode')
            return super().configure(require_redraw, **kwargs)

        def return_entry_func(self, _):
            txt:str = self.num_entry.get()
            if txt.replace('-', '').isnumeric():
                val = self._val_range[0] if int(txt) < self._val_range[0] else self._val_range[1] if int(txt) > self._val_range[1] else int(txt)
                self.value = val;
                self.num_entry.delete(0, "end")
                self.num_entry.insert(0, self.value)
                if self._command is not None:
                    self._command(0)
            else:
                self.num_entry.delete(0, ctk.END)
                self.num_entry.insert(0, self.value)
            self.num_entry.configure(state = 'readonly')
    '''issue with the double call of the command'''

    class info_tab(ctk.CTkFrame):
        def __init__(self, master: any, tab_master: any, width: int = 200, height: int = 200, corner_radius: Optional[Union[int, str]] = None,
                     border_width: Optional[Union[int, str]] = None, bg_color: Union[str, Tuple[str, str]] = "transparent",
                     fg_color: Optional[Union[str, Tuple[str, str]]] = 'transparent', border_color: Optional[Union[str, Tuple[str, str]]] = None,
                     background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                     overwrite_preferred_drawing_method: Union[str, None] = None, tab: ctk.CTkFrame = None,
                     button_text: str = 'click to edit info', tab_size: Tuple[int, int] = None, **kwargs):
            super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color,
                             background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
            self.title = None
            self.value = None
            self._tab_size = tab_size
            self._tab: ctk.CTkFrame = tab(master if not isinstance(tab_master, ctk.CTkFrame) else tab_master, self._tab_size, self)
            self._button_text  = button_text
            self.button = ctk.CTkButton(self, width * .8, height * .7, 12, text = self._button_text, command= lambda: self._tab.place(relx = .5, rely=  .5, anchor = 'c'))
            self.button.place(relx = .5, rely = .5, anchor = 'c')
    
    #ON HOLD
    class cctkSearchBar(ctk.CTkFrame):
        def __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, 
                    bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, 
                    background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, 
                    
                    #Additional Arguments
                    font: Tuple[str, int] = ("Arial", 14),
                    m_width: int = 0, m_height: int = 0,
                    place_width: int = 0, place_height: int = 0,
                    dp_width:int = 200,
                    quary_command: str = None,
                    command_callback:callable = None,
                    close_command_callback: Optional[callable] = None,
                    placeholder: str = None,
                    
                    **kwargs):
            super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
            
            self._fg_color = fg_color
            self._font = font
            self.pack_propagate(0)
            self.m_height = m_height
            self.m_width = m_width
            self.command_callback = command_callback
            self.close_command_callback = close_command_callback
            #temp for storing previous restult
            self.content = []
            self.answer = None
            
            

            def command_call(i = None):
                if i != None:
                    self.answer = [(tuple(self.content[i]._text.strip().split(" - ")))]
                else:
                    self.answer = [(tuple(i.strip().split(" - "))) for i in self.current_data]
                
                self.results.place_forget()
                
                if command_callback:
                    self.command_callback()
        
            def add_results(results):
                if results:
                    for i in range(len(results)):
                        self.content.append(ctk.CTkButton(self.results, text=f'{results[i]}  ', font=self._font, corner_radius=0, width=dp_width,
                                                        height=self._current_height*0.85,fg_color=Color.White_Ghost,
                                                        border_width=1,border_color=Color.White_Platinum, hover_color=Color.White_SilverSand,
                                                        text_color=Color.Blue_Maastricht, anchor='w'))
                        self.content[i].configure(command=partial(command_call, i))
                        self.content[i].pack(fill='x', expand=1)
                        
            def clear_results():
                [s.pack_forget() for s in self.content]
                
            def close_search():
                self.search_var.set("")
                if self.close_command_callback: self.close_command_callback()

            def search_callback(var, index, mode):
                self.current_data =[]
                
                if self.search_var.get() != "" and quary_command != None:
                    raw_data = database.fetch_data(quary_command.replace("?", self.search_var.get()))
                    #print()
                    data = [(f"  {' - '.join(s)}") for s in raw_data]
                    self.current_data=data
                    
                    clear_results()
                    self.content.clear()
                    
                else:
                    clear_results()
                    self.content.clear()
                    
                if self.current_data:
                    self.results.place(relx=0,rely=0, y=self._current_height+place_height, x=self.search_label._current_width*1.5 + place_width)
                    self.search_btn.configure(state = 'normal')
                    
                    self.close_btn.pack(side="left", padx=(0, self.m_width*0.0025), pady=(self.m_height*0.0055),fill="y", expand=0)
                    add_results(self.current_data)
                else:
                    self.search_btn.configure(state = 'disabled')
                    self.close_btn.pack_forget()
                    self.results.place_forget()
                
        
            self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))
            self.close = ctk.CTkImage(light_image=Image.open("image/close.png"),size=(16,16))

            self.search_label = ctk.CTkLabel(self, text="Search", font=self._font, text_color="grey", fg_color="transparent")
            self.search_label.pack(side="left", padx=(self.m_width*0.0075,self.m_width*0.005))
            self.search_var = ctk.StringVar()

            self.search_entry = ctk.CTkEntry(self, placeholder_text=placeholder, textvariable=self.search_var, text_color='black', border_color = 'light grey',
                                            border_width=1, corner_radius=5, fg_color=Color.White_Lotion,placeholder_text_color="light grey", font=self._font,)
            self.search_entry.pack(side="left", padx=(0, self.m_width*0.0025), pady=(self.m_height*0.0055),  fill="both", expand=1)
            
            self.search_btn = ctk.CTkButton(self, text="", image=self.search, fg_color=Color.White_Lotion, hover_color="light grey", 
                                            width=self.m_width*0.005, state='disabled', command=command_call)
            self.search_btn.pack(side="left", padx=(0, self.m_width*0.0025), pady=(self.m_height*0.0055),fill="y", expand=0)

            self.close_btn = ctk.CTkButton(self, text="", image=self.close, fg_color = Color.Red_Pastel, command=close_search,
                                        hover_color = Color.Red_Tulip, state = 'normal', width=self.m_width*0.005)
            
            self.search_var.trace_add('write', search_callback)
    
            self.results = ctk.CTkFrame(self.master.master, fg_color=fg_color, height=m_height*0.75, corner_radius=0, border_width=2, border_color="light grey")
            
        def get(self):
            return self.answer
        
        def reset(self):
            self.search_var.set("")
            self.search_btn.configure(state = 'disabled')
            self.close_btn.pack_forget()
            self.results.place_forget()    
        
    class cctkPageNavigator(ctk.CTkFrame):
        def __init__(self, master: any, width: int = 190, height: int = 40, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", 
                 fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, 
                 overwrite_preferred_drawing_method: str | None = None,
                 
                 #Custom Argument
                 
                page_limit: int = 1,
                command: callable = None,
                font: Tuple[str, int] = None,
                page_fg_color: str = None,
                disable_timer: int = 0,
                
                 
                 **kwargs):
            super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
            self.propagate(0)
            self.page_count = 1
            self.command = command
            self._font = font
            self.page_limit = page_limit
            
                    
            def navigate(direction: int):
                self.prev_button.configure(state="disabled")
                self.next_button.configure(state="disabled")
                if direction:
                    self.page_count = min(self.page_count+1, self.page_limit)
                else:
                    self.page_count = max(self.page_count-1, 1)
                    
                self.page_counter.configure(text=f"{self.page_count}")
                #self.checker()
                if self.command:self.command()
                self.after(disable_timer, reenable())
            
            def reenable():
                self.prev_button.configure(state="normal")
                self.next_button.configure(state="normal")
                self.checker()
                
            self.prev_button = ctk.CTkButton(self, text="<", font=self._font, height=self._current_height, width=self._current_height-width*0.05,
                                            image=None, command=partial(navigate, 0),)
            self.prev_button.pack(side="left", padx=(width*0.025, 0), pady=(width*0.025))
            
            self.page_counter = ctk.CTkLabel(self, text="1", font=self._font, corner_radius=5, fg_color= page_fg_color)
            self.page_counter.pack(side="left", fill="both", expand=1, padx=(width*0.025), pady=(width*0.025))
            
            self.next_button = ctk.CTkButton(self, text=">", font=self._font, height=self._current_height, width=self._current_height-width*0.05
                                            , image=None, command=partial(navigate, 1))
            self.next_button.pack(side="right", padx=(0, width*0.025), pady=(width*0.025))
            self.checker()
            
        def checker(self):
            if self.page_count == 1:
                self.prev_button.configure(state="disabled")
            else:
                self.prev_button.configure(state="normal")  
            
            if self.page_count == self.page_limit:
                self.next_button.configure(state="disabled")
            else:
                self.next_button.configure(state="normal")
        
        def get(self):
            return self.page_count
        
        def update_page_limit(self, page):
            if page == 0: page = 1
            if self.page_count > page: self.page_count = 1
            self.page_counter.configure(text=self.page_count)
            self.page_limit = page
            self.checker()       

    class tkc(Calendar):
        def __init__(self, master=None, select_callback: callable = None, date_format: str ="numerical", **kw,):
            super().__init__(master, **kw)
            self.select_callback = select_callback
            self.date_format = date_format
            #self.selected_date = self.get_date()

        def _on_click(self, event):
            super()._on_click(event)     
            if self.select_callback is not None:
                self.select_callback(self.get_date())
            #self.selected_date = self.get_date()
            #return temp
    
    def cctkSelector(master, info:Optional[tuple], 
                     title:str='SELECTORS',
                     selector_search_query:str=None,
                     selector_table_setup:str=f'/No:40-#r/ID:80-tc/Name:x-tl/Sample:100-tr!33!35',
                     selector_table_query:str=None,
                     command_callback:callable=None,):
        class instance(ctk.CTkFrame):
            def __init__(self, master, info:Optional[tuple]):
                width = info[0]
                height = info[1]
                super().__init__(master, corner_radius= 0, fg_color=Color.White_Platinum)
                self.selected_value = None 
                
                def reset():
                    self.grab_release()
                    self.place_forget()
                
                def select():
                    if self.data_view.get_selected_data():
                        self.ret = self.data_view.get_selected_data()
                        if command_callback: command_callback()
                        reset()
                    else:
                        messagebox.showwarning("Warning", "No selected data", parent = self)
                
                def search_callback():
                    if len(self.search_bar.get()) == 1:
                        self.ret = list_filterer(source=self.search_bar.get(), reference=self.data)[0]
                        if command_callback: command_callback()
                        reset()
                    else:
                        self.data_view.update_table(list_filterer(source=self.search_bar.get(), reference=self.data))
                
                self.grid_columnconfigure(0, weight=1)
                self.grid_rowconfigure(0, weight=1)
                
                self.main_frame = ctk.CTkFrame(self, width=width*0.775, height=height*0.825 ,corner_radius=0, fg_color=Color.White_Lotion)
                self.main_frame.grid(row=0, column=0, padx=1, pady=1)
                self.main_frame.grid_propagate(0)
                self.main_frame.grid_columnconfigure(0, weight=1)
                self.main_frame.grid_rowconfigure(1, weight=1)
                
                self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
                self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

                ctk.CTkLabel(self.top_frame, text=title.upper(), text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.005)
                ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=reset).pack(side="right", padx=(0,width*0.01),pady=height*0.005)

                self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Lotion)
                self.content_frame.grid(row=1, column=0, sticky='nsew')
                
                self.search_bar_frame =ctk.CTkFrame(self.content_frame, fg_color='transparent')
                self.search_bar_frame.pack(fill='x', expand=0,)
                
                self.treeview_frame = ctk.CTkFrame(self.content_frame, fg_color='transparent')
                self.treeview_frame.pack()
                
                self.data_view = customcustomtkinter.cctkTreeView(self.treeview_frame,width= width * .765, height= height * .65, corner_radius=0,
                                           column_format=selector_table_setup)
                self.data_view.pack()
                
                
                self.action_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
                self.action_frame.grid(row=2, column=0, sticky='nsew', padx=(width*0.005), pady=(width*0.005))
                
                self.cancel_button = ctk.CTkButton(self.action_frame, text="Cancel", fg_color=Color.Red_Pastel, hover_color=Color.Red_Tulip,font=("DM Sans Medium",16), width=width*0.1, height=height*0.05, command=reset)
                self.cancel_button.pack(side='left', padx=(width*0.005),pady=(width*0.005))
                
                self.select_button = ctk.CTkButton(self.action_frame, text="Select", font=("DM Sans Medium",16), width=width*0.1, height=height*0.05, command=select)
                self.select_button.pack(side='right', padx=(width*0.005),pady=(width*0.005))
                
                self.search_bar = customcustomtkinter.cctkSearchBar(self.search_bar_frame, height=height*0.055, width=width*0.35, m_height=height, m_width=width, fg_color=Color.Platinum, command_callback=search_callback,
                                                 close_command_callback=None,
                                             quary_command=selector_search_query, dp_width=width*0.25, place_height=height*0, place_width=width*0, font=("DM Sans Medium", 14))
                self.search_bar.pack(side='left', padx=(width*0.005), pady=(width*0.005))
                
                #self.data_view.update_table([('Test','Test','Test')])
                
            def get(self):
                return self.ret
            
            def place(self, **kwargs):
                self.grab_set()
                self.data = database.fetch_data(selector_table_query)
                self.data_view.update_table(self.data)
                
                return super().place(**kwargs)
                
        return instance(master, info)
    
    class num_entry(ctk.CTkEntry):
        def __init__(self, master: any, width: int = 140, height: int = 28, corner_radius: int | None = None, border_width: int | None = None,
                     bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None,
                     border_color: str | Tuple[str, str] | None = None, text_color: str | Tuple[str, str] | None = None,
                     placeholder_text_color: str | Tuple[str, str] | None = None, textvariable= None, placeholder_text: str | None = None,
                     font: tuple | CTkFont | None = None, state: str = ctk.NORMAL, max_val: int = sys.maxsize,
                     before_modify_callback: callable = None, after_modify_callback: callable = None, **kwargs):
            super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, text_color, placeholder_text_color, textvariable, placeholder_text, font, state, **kwargs)
            self._before_modify_callback = before_modify_callback
            self._after_modify_callback = after_modify_callback


            def check_for_number():
                if callable(self._before_modify_callback):
                    self._before_modify_callback()

                num = self.get() or '0'
                char_format = "0123456789"

                for i in range(len(num)):
                    if num[i] not in char_format:
                        self.delete(i, i+1)
                
                num = self.get() or '0'

                if int(num[0]) == 0 and len(num) > 1:
                    self.delete(0, 1)

                if int(num) > max_val:
                    self.delete(0, ctk.END)
                    self.insert(0, max_val)

                if callable(self._after_modify_callback):
                    self._after_modify_callback()
        
            self.configure(textvariable = customcustomtkinterutil.entry_limiter(len(str(sys.maxsize)), self, check_for_number))

        def configure(self, require_redraw=False, **kwargs):
            if 'before_modify_callback' in kwargs:
                self._before_modify_callback = kwargs['before_modify_callback']
                kwargs.pop('before_modify_callback')
            if 'after_modify_callback' in kwargs:
                self._after_modify_callback = kwargs['after_modify_callback']
                kwargs.pop('after_modify_callback')
            return super().configure(require_redraw, **kwargs)
        
        def get(self):
            return super().get()
        
    class ip_entry(ctk.CTkFrame):
        def __init__(self, master: any, width: int = 200, height: int = 200, fg_color: str | Tuple[str, str] | None = None, font: Tuple[str, int] = ("Arial", 12), border_color: str | Tuple[str, str] | None = None, **kwargs):
            super().__init__(master, width, height, 0, 2 if border_color != None else 0, 'transparent', fg_color, border_color or 'black', None, None, **kwargs)

            self.width = width
            self.height = height
            self.screen = (self.width, self.height)
            self.pack_propagate(0)

            entry_spaces = .2

            self.octet1 = customcustomtkinter.num_entry(self, self.width * entry_spaces, self.height * .9, 0, placeholder_text= '255', fg_color= 'transparent', border_width= 0, font= font, max_val= 255)
            self.octet1._entry.configure(justify= ctk.CENTER)
            self.octet1.pack(side = ctk.LEFT, padx = (self.width * .01 , self.width * .0283))

            ctk.CTkLabel(self, text = '.').pack(side = ctk.LEFT, padx = (0, self.width * .0283), pady = (0, self.width * 0.006), anchor = 's')

            self.octet2 = customcustomtkinter.num_entry(self, self.width * entry_spaces, self.height * .9, 0, placeholder_text= '255', fg_color= 'transparent', border_width= 0, font= font, max_val= 255)
            self.octet2._entry.configure(justify= ctk.CENTER)
            self.octet2.pack(side = ctk.LEFT, padx = (0, self.width * .0283))

            ctk.CTkLabel(self, text = '.').pack(side = ctk.LEFT, padx = (0, self.width * .0283), pady = (0, self.width * 0.006), anchor = 's')

            self.octet3 = customcustomtkinter.num_entry(self, self.width * entry_spaces, self.height * .9, 0, placeholder_text= '255', fg_color= 'transparent', border_width= 0, font= font, max_val= 255)
            self.octet3._entry.configure(justify= ctk.CENTER)
            self.octet3.pack(side = ctk.LEFT, padx = (0, self.width * .0283))

            ctk.CTkLabel(self, text = '.').pack(side = ctk.LEFT, padx = (0, self.width * .0283), pady = (0, self.width * 0.006), anchor = 's')

            self.octet4 = customcustomtkinter.num_entry(self, self.width * entry_spaces, self.height * .9, 0, placeholder_text= '255', fg_color= 'transparent', border_width= 0, font= font, max_val= 255)
            self.octet4._entry.configure(justify= ctk.CENTER)
            self.octet4.pack(side = ctk.LEFT, padx = (self.width * .01))

            def next_focus(cur_entry: ctk.CTkEntry, next_entry: ctk.CTkEntry):
                if cur_entry.get() != '':
                    if (cur_entry.get()[-1] or 0) == '.':
                        next_entry.focus_force()

            def auto_full_focus(cur_entry: ctk.CTkEntry, next_entry: ctk.CTkEntry):
                if len(cur_entry.get()) == 3:
                    next_entry.focus_force()

            self.octet1.configure(before_modify_callback = lambda: next_focus(self.octet1, self.octet2),
                                after_modify_callback = lambda: auto_full_focus(self.octet1, self.octet2))
            self.octet2.configure(before_modify_callback = lambda: next_focus(self.octet2, self.octet3),
                                after_modify_callback = lambda: auto_full_focus(self.octet2, self.octet3))
            self.octet3.configure(before_modify_callback = lambda: next_focus(self.octet3, self.octet4),
                                after_modify_callback = lambda: auto_full_focus(self.octet3, self.octet4))

            self.entries = [self.octet1, self.octet2, self.octet3, self.octet4]

        def getIP(self):
            return ".".join([str(s.get()) or "0" for s in self.entries])
        
        def setIP(self, ip_address: str):
            if re.search(r'^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$', ip_address):
                octets = ip_address.split('.')
                for i in range(len(self.entries)):
                    self.entries[i].delete(0, ctk.END)
                    self.entries[i].insert(0, octets[i])

        def configure(self, require_redraw=False, **kwargs):
            if 'state' in kwargs:
                if kwargs['state'] == ctk.NORMAL:
                    self.octet1.configure(state = ctk.NORMAL)
                    self.octet2.configure(state = ctk.NORMAL)
                    self.octet3.configure(state = ctk.NORMAL)
                    self.octet4.configure(state = ctk.NORMAL)
                elif kwargs['state'] == ctk.DISABLED or kwargs['state'] == 'readonly':
                    if(kwargs['state'] == ctk.DISABLED):
                        self.octet1.delete(0, ctk.END)
                        self.octet2.delete(0, ctk.END)
                        self.octet3.delete(0, ctk.END)
                        self.octet4.delete(0, ctk.END)
                    self.octet1.configure(state = ctk.DISABLED)
                    self.octet2.configure(state = ctk.DISABLED)
                    self.octet3.configure(state = ctk.DISABLED)
                    self.octet4.configure(state = ctk.DISABLED)
                kwargs.pop('state')
            return super().configure(require_redraw, **kwargs)
         
class customcustomtkinterutil:
    class button_manager:
        def __init__(self, buttons: list, hold_color: str = 'transparent', switch: bool = False,
                     default_active: Optional[int] = None, state: tuple = (lambda: None, lambda: None), children: Optional[list] = None,
                     active_double_click_nullified: bool = True):
            self.active = None
            self._state = state
            self._og_color =[]
            self._switch = switch
            self._hold_color = hold_color
            self._buttons = buttons
            self._default_active = default_active
            self._children = children
            self._active_double_click_nullified = active_double_click_nullified #nullified the command if the clicked button is the active
            #setup variables

            for i in range(len(buttons)):
                if isinstance(buttons[i], customcustomtkinter.ctkButtonFrame):
                    #buttons[i]._command.append(partial(self.click, i))
                    buttons[i]._command = [partial(self.click, i, buttons[i]._command[0])]
                elif isinstance(buttons[i], ctk.CTkButton):
                    cmd = buttons[i]._command
                    buttons[i].configure(command = partial(self.click, i, cmd))
                self._og_color.append(buttons[i]._fg_color)
            #set the designated command for buttonframe and ctkbutton

        def click(self, i: int, button_command: callable = None, e: any = None):
            if self._buttons[i] is self.active and self._active_double_click_nullified:
                return
            #cancel the command if the button itself is the active

            if button_command is not None:
                button_command()
            #actual command of a button

            if self.active == self._buttons[i] and self._switch:
                if self._children is not None:
                    self._children[i].deiconify()
                self.active.configure(hover = True)
                self.active.configure(fg_color = self._og_color[i])
                self._state[0]()
                self.active = None
                return
            #if the clicked button was the active button and the switch mode is on
            elif self.active is not None:
                if self._children is not None:
                    self._children[self._buttons.index(self.active)].deiconify()
                self.active.configure(fg_color = self._og_color[self._buttons.index(self.active)])
                self.active.configure(hover = True)
                self._state[0]()
            #if theres an existing active button
            if self._children is not None:
                self._children[i].place()
            self.active = self._buttons[i]
            self.active.configure(hover = False)
            self.active.configure(fg_color = self._hold_color)
            self._state[1]()
        #setup click variable

        def deactivate_active(self):
            if self._children is not None:
                self._children[self._buttons.index(self.active)].deiconify()
            self.active.configure(hover = True)
            self.active.configure(fg_color = self._og_color[self._buttons.index(self.active)])
            self._state[0]()
            self.active = None

        def update_buttons(self):
            for i in range(len(self._buttons)):
                if isinstance(self._buttons[i], customcustomtkinter.ctkButtonFrame):
                    self._buttons[i]._command.pop()
                    self._buttons[i]._command.append(partial(self.click, i))
                '''elif isinstance(self.buttons[i], ctk.CTkButton):
                    cmd = self.buttons[i]._command
                    self.buttons[i].configure(command = partial(self.click, i, cmd))
                self._og_color.append(self.buttons[i]._fg_color)'''
            #note: not yet applicable in buttons

        def update_colors(self, button: ctk.CTkButton | customcustomtkinter.ctkButtonFrame):
            self._og_color[self._buttons.index(button)] = button._fg_color

    def entry_limiter(length: int, entry: ctk.CTkEntry, command: callable = None):
        ret = ctk.StringVar();

        def limit(var, index, mode):
            if len(entry.get()) > length:
                entry.delete(length, ctk.END)

            if callable(command):
                command()

        ret.trace_add("write", callback = limit)
        return ret
    
    
    
