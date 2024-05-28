import sqlite3
from tkinter import filedialog
from typing import Any
import customtkinter as ctk
from PIL import Image
import re
import time

# custom files imports
import src.pass_checker
from src.pass_manager import PasswordManager
from src.popup_window import PopUpWindow
from src.tools import display_info, fetch_directory_paths


class MainUI(PopUpWindow):
    def __init__(self):
        super().__init__()

        self.file_path = None
        self.user_login = None
        self.password = None

        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')

        x, y = display_info()
        window_width = 700
        window_height = 450

        self.root = ctk.CTk()
        self.root.title('Password Manager')
        self.root.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

        self.frame = ctk.CTkFrame(master=self.root, corner_radius=5)
        self.frame.pack(pady=20, padx=20, fill='both', expand=True, anchor='center')

        # In Windows version image path is only 'logo3.png' because it's kept in the same folder
        try:
            self.my_image = ctk.CTkImage(dark_image=Image.open('/usr/local/pypass-manager/src/img/logo3.png'), size=(146, 189))
        except FileNotFoundError:
            self.my_image = ctk.CTkImage(dark_image=Image.open('src/img/logo3.png'), size=(146, 189))

        self.logo_image = ctk.CTkButton(master=self.frame, image=self.my_image, text='', border_width=0,
                                        fg_color='transparent', hover_color='#212121', state='disabled')
        self.logo_image.place(x=325, y=100, anchor='center')

        self.file_label = ctk.CTkLabel(master=self.frame, text='Best protection will provide USB stick dedicated '
                                                               'only to store your unique Key.')
        self.file_path_entry = ctk.CTkEntry(master=self.frame, width=350, height=25, border_width=1, corner_radius=7,
                                            placeholder_text='Select or type in here full path where your key will '
                                                             'be stored')

        self.login_entry = ctk.CTkEntry(master=self.frame, width=170, height=25, border_width=1, corner_radius=7)
        self.login_label = ctk.CTkLabel(master=self.frame, text='Login :')

        self.logout_button = ctk.CTkButton(master=self.frame, text='Logout', width=20, command=self.logout)

        self.site_entry = ctk.CTkEntry(master=self.frame, width=170, height=25, border_width=1, corner_radius=7)
        self.site_label = ctk.CTkLabel(master=self.frame, text='Site name:')

        self.password_entry = ctk.CTkEntry(master=self.frame, width=170, height=25, border_width=1, corner_radius=7,
                                           show='○')
        self.password_label = ctk.CTkLabel(master=self.frame, text='Password :')

        self.new_password_entry = ctk.CTkEntry(master=self.frame, width=170, height=25, border_width=1,
                                               corner_radius=7, show='○')

        self.checkbox = ctk.CTkCheckBox(master=self.frame, text='Show/Hide', command=self.show_hide, width=2, height=2)

        self.confirm_button = ctk.CTkButton(master=self.frame, text='Confirm', command=self.login)

        self.error_label = ctk.CTkLabel(master=self.frame, text='Incorrect password/login. Try again', text_color='red')
        self.success_label = ctk.CTkLabel(master=self.frame, text='Account have been created successfully',
                                          text_color='green')

        self.find_password_button = ctk.CTkButton(master=self.frame, text='Find Password', width=170, height=50,
                                                  font=('Arial', 17, 'bold'), command=self.search_password_window)
        self.find_password_button.bind('<Return>', self.enter_find)

        self.add_password_button = ctk.CTkButton(master=self.frame, text='Add New Password', width=170, height=50,
                                                 font=('Arial', 17, 'bold'), command=self.check_password_window)
        self.add_password_button.bind('<Return>', self.enter_add)

        self.go_back_button = ctk.CTkButton(master=self.frame, text='Menu', width=20, command=self.menu)
        self.back_to_login = ctk.CTkButton(master=self.frame, text='Login', width=20, command=self.logout)

        self.search_button = ctk.CTkButton(master=self.frame, text='Search', command=self.search_password)
        self.search_button.bind('<Return>', self.enter_search)

        self.new_user_button = ctk.CTkButton(master=self.frame, text='Create New User',
                                             command=self.create_user_window)

        self.create_user_button = ctk.CTkButton(master=self.frame, text='Create User', command=self.create_user)

        self.check_pwned_button = ctk.CTkButton(master=self.frame, text='Check password', command=self.check_password)
        self.check_pwned_button.bind('<Return>', self.enter_check)

        self.save_button = ctk.CTkButton(master=self.frame, text='Save password', command=self.save_password_window)

        self.browse_button = ctk.CTkButton(master=self.frame, width=50, text='Browse', command=self.browse_saving_path)

        self.delete_user_button = ctk.CTkButton(master=self.frame, text='Delete User', command=self.delete_user)

        self.info_label = ctk.CTkLabel(master=self.frame)

        self.password_entry.bind("<Tab>", self.focus_on, add='+')
        self.password_entry.bind("<Tab>", self.confirm_button.bind('<Return>', self.login), add='+')
        self.confirm_button.bind('<Tab>', self.focus_reset)

        self.pm = PasswordManager()

        self.login_window()

        self.root.mainloop()

    def login_window(self) -> None:
        self.logout_button.place_forget()

        self.login_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')

        self.checkbox.place(x=427, y=270, anchor='w')

        self.login_entry.place(x=330, y=230, anchor='center')
        self.login_label.place(x=237, y=230, anchor='e')

        self.password_entry.place(x=330, y=270, anchor='center')
        self.password_label.place(x=237, y=270, anchor='e')

        self.new_user_button.place(x=15, y=30, anchor='w')

        self.confirm_button.place(x=330, y=310, anchor='center')

        self.delete_user_button.place(x=572, y=30, anchor='center')
        self.delete_user_button.configure(fg_color='#D22B2B', hover_color='#880808')

        self.password_entry.bind('<Tab>', self.focus_on)
        self.confirm_button.bind('<Tab>', self.confirm_button.configure(fg_color='#1F538D'))

    def login(self, event: Any = None) -> None:
        self.user_login = self.login_entry.get()
        self.password = self.password_entry.get()

        try:
            key_p, _ = fetch_directory_paths(self.user_login)
            login, password = self.pm.get_encrypted(key_p)
            typed_login, typed_password = self.pm.encrypt_password(key_p, self.password, self.user_login)

            if login != typed_login or password != typed_password:
                self.error_label.place(x=330, y=200, anchor='center')
                self.login_entry.delete(0, 'end')
                self.password_entry.delete(0, 'end')
                time.sleep(2)
            else:
                self.menu()
                self.scan_passwords()

        except (TypeError, ValueError, FileNotFoundError, sqlite3.OperationalError):
            self.error_label.place(x=330, y=200, anchor='center')
            self.login_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            time.sleep(2)

    def scan_passwords(self):
        breached_sites = []

        key_p, site_p = fetch_directions_paths(self.user_login)
        try:
            login_data = self.pm.get_pass(key_p, site_p)

            for site, password in login_data.items():
                count = int(src.pass_checker.run_program(password))
                if count > 0:
                    breached_sites.append(site)

            message = (f'          This site passwords have been detected in hackers database:\n{breached_sites}\n '
                       f'Change those passwords to protect your accounts.')

            if len(breached_sites) > 0:
                self.create_window()
                self.info_window(message, 'Check Result')
        except KeyError:
            pass

    def create_user_window(self) -> None:
        self.clear_window()

        self.login_entry.place(x=330, y=295, anchor='center')
        self.login_label.place(x=237, y=295, anchor='e')

        self.new_password_entry.place(x=330, y=335, anchor='center')
        self.password_label.place(x=237, y=335, anchor='e')

        self.file_label.place(x=330, y=225, anchor='center')
        self.file_path_entry.place(x=330, y=255, anchor='center')

        self.browse_button.place(x=510, y=255, anchor='w')

        self.create_user_button.place(x=330, y=375, anchor='center')

        self.back_to_login.place(x=615, y=30, anchor='center')

        self.new_password_entry.bind('<Tab>', self.focus_on, add='+')
        self.new_password_entry.bind('<Tab>', self.create_user_button.bind('<Return>', self.create_user), add='+')
        self.create_user_button.bind('<Tab>', self.focus_reset)

    def create_user(self, event: Any = None) -> None:
        login = self.login_entry.get()
        password = self.new_password_entry.get()
        path = self.file_path_entry.get()

        if len(login) < 1 or len(password) < 1 or len(path) < 1:
            self.error_label.configure(text='All fields must be filled.')
            self.error_label.place(x=330, y=200, anchor='center')
            return

        try:
            process_result = self.pm.create_new_user(login, password, path)

            if process_result is True:
                self.login_entry.delete(0, 'end')
                self.password_entry.delete(0, 'end')
                self.clear_window()
                self.success_label.place(x=330, y=200, anchor='center')
                self.login_window()
            elif process_result is False:
                self.error_label.configure(text='This login already exist, pick different login.')
                self.error_label.place(x=330, y=200, anchor='center')
            elif process_result is PermissionError:
                self.error_label.configure(text='USB that you try to write you key on is write protected.'
                                                ' Change your USB attributes.')
                self.error_label.place(x=330, y=200, anchor='center')

        except FileNotFoundError:
            self.error_label.configure(text='Given path is incorrect. Please pick an existing file path.')
            self.error_label.place(x=330, y=200, anchor='center')
            self.file_path_entry.delete(0, 'end')

    def menu(self) -> None:
        self.clear_window()
        self.reset_buttons()

        self.add_password_button.focus_set()

        self.find_password_button.place(x=330, y=250, anchor='center')
        self.add_password_button.place(x=330, y=320, anchor='center')

        self.find_password_button.bind('<Tab>', self.focus_on_find)
        self.add_password_button.bind('<Tab>', self.focus_on_add)

        self.logout_button.place(x=615, y=30, anchor='center')

    def search_password_window(self) -> None:
        self.clear_window()
        self.reset_buttons()

        self.site_entry.focus_set()
        self.site_entry.delete(0, 'end')

        self.site_entry.place(x=330, y=270, anchor='center')
        self.site_label.place(x=230, y=270, anchor='e')

        self.search_button.place(x=330, y=310, anchor='center')
        self.go_back_button.place(x=15, y=30, anchor='w')
        self.logout_button.place(x=615, y=30, anchor='center')

        self.site_entry.bind('<Tab>', self.focus_on)
        self.search_button.bind('<Tab>', self.focus_out)

        self.root.bind('<Escape>', self.back_to_menu)

    def search_password(self) -> None:
        site = self.site_entry.get().lower()
        key_p, site_p = fetch_directory_paths(self.user_login)
        try:
            password = self.pm.get_pass(key_p, site_p, site)
            message = f'          Site: {site}\nPassword: {password}'

            self.site_entry.delete(0, 'end')

            self.create_window()
            self.info_window(message, 'Search Result')
        except KeyError:
            message = 'Site you entered is incorrect or does not exist.\n ' \
                      'Check your input and try again.'

            self.create_window()
            self.info_window(message, 'Search Error')

        self.site_entry.delete(0, 'end')

    def check_password_window(self) -> None:
        self.clear_window()
        self.reset_buttons()

        self.password_entry.unbind('<Tab>')
        self.save_button.unbind('<Return>')
        self.save_button.configure(text='Save password', command=self.save_password_window)

        self.password_entry.focus_set()
        self.save_button.bind('<Return>', self.enter_save)

        self.password_entry.delete(0, 'end')

        self.password_label.place(x=230, y=270, anchor='e')
        self.password_entry.place(x=330, y=270, anchor='center')

        self.check_pwned_button.place(x=330, y=310, anchor='center')
        self.save_button.place(x=330, y=350, anchor='center')
        self.go_back_button.place(x=15, y=30, anchor='w')
        self.logout_button.place(x=615, y=30, anchor='center')
        self.checkbox.place(x=427, y=270, anchor='w')

        self.info_label.configure(text='Here you can check how secure your password is. \n'
                                       'Is it included in hackers passwords data base \n'
                                       'and how many times it have been cracked/leaked/used.')
        self.info_label.place(x=330, y=222, anchor='center')

        self.password_entry.bind("<Tab>", self.focus_on)
        self.check_pwned_button.bind('<Tab>', self.focus_out)
        self.save_button.bind('<Tab>', self.focus_reset)

        self.root.bind('<Escape>', self.back_to_menu)

    def check_password(self) -> None:
        password = self.password_entry.get()
        count = int(src.pass_checker.run_program(password))
        if count > 0:
            message = f'This password was found {count} times...\nYou should use a different password.'

            self.create_window()
            self.info_window(message, 'Check Result')
        else:
            message = 'This password was NOT found. Seams secure, carry on.'

            self.create_window()
            self.info_window(message, 'Check Result')

    def save_password_window(self) -> None:
        self.clear_window()
        self.reset_buttons()

        self.site_entry.focus_set()

        self.site_entry.place(x=330, y=230, anchor='center')
        self.site_label.place(x=237, y=230, anchor='e')

        self.password_entry.place(x=330, y=270, anchor='center')
        self.password_label.place(x=237, y=270, anchor='e')
        self.checkbox.place(x=427, y=270, anchor='w')
        self.logout_button.place(x=615, y=30, anchor='center')

        self.info_label.configure(text='Duplicates WARNING ! If you use the same site name second time old password '
                                       'will be overwrite.')
        self.info_label.place(x=330, y=201, anchor='center')

        self.save_button.configure(command=self.save_password, text='Save')
        self.save_button.place(x=330, y=310, anchor='center')

        self.go_back_button.place(x=15, y=30, anchor='w')

        self.password_entry.bind("<Tab>", self.focus_on_save)
        self.save_button.bind('<Tab>', self.focus_reset)
        self.save_button.bind('<Return>', self.enter_save_password)

        # self.root.bind('<Escape>', self.back_to_menu)

    def save_password(self) -> None:
        password = self.password_entry.get()
        site = self.site_entry.get().lower()

        key_p, site_p = fetch_directory_paths(self.user_login)

        if len(password) > 0 and len(site) > 0:
            self.pm.add_password(site, password, key_p, site_p)
            message = 'Your password have been saved successfully.'

            self.create_window()
            self.info_window(message, 'Save Result')
        else:
            message = 'Something went wrong. Check entries and try again.'

            self.create_window()
            self.info_window(message, 'Save Result')

        self.password_entry.delete(0, 'end')
        self.site_entry.delete(0, 'end')

# ================================================================================================================== #
# =============================================== UTILITY METHODS= ================================================= #
# ================================================================================================================== #

    def browse_saving_path(self) -> None:
        self.file_path = filedialog.askdirectory()
        self.file_path_entry.insert(0, self.file_path)

    def logout(self) -> None:
        self.clear_window()
        self.login_window()

    def delete_user(self) -> None:
        self.create_window()
        self.delete_user_window()

    def show_hide(self) -> None:
        value = self.checkbox.get()
        if value == 1:
            self.password_entry.configure(show='')
        else:
            self.password_entry.configure(show='○')

    def clear_window(self) -> None:
        for widget in self.frame.winfo_children():
            if widget is self.logo_image:
                continue
            widget.place_forget()

# ================================ Buttons <Tab> Focus Color Change ================================ #
    
    def focus_on(self, event: Any) -> None:
        self.confirm_button.configure(fg_color='#14375E')
        self.search_button.configure(fg_color='#14375E')
        self.check_pwned_button.configure(fg_color='#14375E')
        self.create_user_button.configure(fg_color='#14375E')
    
    def focus_out(self, event: Any) -> None:
        self.check_pwned_button.configure(fg_color='#1F538D')
        self.save_button.configure(fg_color='#14375E')
        self.search_button.configure(fg_color='#1F538D')
        self.check_pwned_button.focus_set()
    
    def focus_on_add(self, event: Any) -> None:
        self.find_password_button.configure(fg_color='#14375E')
        self.add_password_button.configure(fg_color='#1F538D')
    
    def focus_on_find(self, event: Any) -> None:
        self.find_password_button.configure(fg_color='#1F538D')
        self.add_password_button.configure(fg_color='#14375E')
    
    def focus_on_save(self, event: Any) -> None:
        self.save_button.configure(fg_color='#14375E')
    
    def focus_reset(self, event: Any) -> None:
        self.reset_buttons()
        self.delete_user_button.configure(fg_color='#D22B2B', hover_color='#880808')
    
    def reset_buttons(self) -> None:
        i = 0
        for widget in self.frame.winfo_children():
            i += 1
            if i == 1:
                continue
            if re.search(r'button', str(widget)):
                widget.configure(fg_color='#1F538D')

# ================================ Buttons Command Shortcuts ================================ #

    def enter_find(self, event: Any) -> None:
        self.search_password_window()
    
    def enter_add(self, event: Any) -> None:
        self.check_password_window()
    
    def enter_search(self, event: Any) -> None:
        self.search_password()
    
    def enter_check(self, event: Any) -> None:
        self.check_password()
    
    def enter_save(self, event: Any) -> None:
        self.save_password_window()
    
    def enter_save_password(self, event: Any) -> None:
        self.save_password()
    
    def back_to_menu(self, event: Any) -> None:
        self.menu()
