from typing import Any
import customtkinter as ctk

from src.tools import fetch_directions_paths, delete_files, display_info
from src.pass_manager import PasswordManager


class PopUpWindow:
    def __init__(self) -> None:
        self.window = None

        self.user_password_label = None
        self.information_label = None
        self.username_label = None
        self.message_label = None
        self.path_label = None
        self.user_label = None

        self.user_password_entry = None
        self.username_entry = None

        self.confirmation_button = None

        self._login = None

    def create_window(self) -> None:
        self.window = ctk.CTkToplevel()

        x, y = display_info()
        window_width = 350
        window_height = 100

        self.window.geometry('%dx%d+%d+%d' % (window_width, window_height, x*1.25, y*1.4))

        self.message_label = ctk.CTkLabel(master=self.window, text='', font=('Arial', 12, 'bold'))
        self.user_label = ctk.CTkLabel(master=self.window, text='User name:', font=('Arial', 12, 'normal'))
        self.path_label = ctk.CTkLabel(master=self.window, text='Path: ', font=('Arial', 12, 'normal'))
        self.information_label = ctk.CTkLabel(master=self.window, text_color='red',
                                              text='Are you sure that you want to delete this account?\n'
                                              'All passwords and sites names will be lost.')

        self.window.wm_transient(self.frame)

    def info_window(self, message: str, window_title: str) -> None:
        # self.window.grab_set()   # For Windows version this line is on the end of create_window function
        self.window.title(window_title)
        self.message_label.configure(text=message, font=('Arial', 12, 'bold'))
        self.message_label.place(x=175, y=50, anchor='center')
        self.window.bind('<Escape>', self.close_window)

    def delete_user_window(self) -> None:
        self.window.title('Delete User')
        self.username_entry = ctk.CTkEntry(master=self.window, width=170, height=25, border_width=1, corner_radius=7)
        self.username_entry.place(x=185, y=20, anchor='center')
        self.username_label = ctk.CTkLabel(master=self.window, text='Login:', font=('Arial', 12, 'normal'))
        self.username_label.place(x=90, y=20, anchor='e')

        self.user_password_entry = ctk.CTkEntry(master=self.window, width=170, height=25, border_width=1,
                                                corner_radius=7, show='○')
        self.user_password_entry.place(x=185, y=48, anchor='center')
        self.user_password_label = ctk.CTkLabel(master=self.window, text='Password:', font=('Arial', 12, 'normal'))
        self.user_password_label.place(x=90, y=48, anchor='e')

        self.confirmation_button = ctk.CTkButton(master=self.window, text='Confirm', command=self._user_login)
        self.confirmation_button.place(x=185, y=80, anchor='center')

        self.user_password_entry.bind('<Tab>', self._focus_on, add='+')
        self.user_password_entry.bind('<Tab>', self.confirmation_button.bind('<Return>', self._user_login), add='+')
        self.confirmation_button.bind('<Tab>', self._focus_out)

    def _user_login(self, event: Any = None) -> None:
        self._login = self.username_entry.get()
        _password = self.user_password_entry.get()
        try:
            key_p, _ = fetch_directions_paths(self._login)

            login, password = PasswordManager().get_encrypted(key_p)
            typed_login, typed_password = PasswordManager().encrypt_password(key_p, _password, self._login)

            if login == typed_login and password == typed_password:
                self.user_password_label.configure(text_color='red')
                self.username_label.configure(text_color='red')

                self.username_entry.delete(0, 'end')
                self.user_password_entry.delete(0, 'end')
            else:
                self.close_window()
                self.create_window()
                self.confirm_deleting()
        except (TypeError, ValueError, FileNotFoundError):
            self.user_password_label.configure(text_color='red')
            self.username_label.configure(text_color='red')

            self.username_entry.delete(0, 'end')
            self.user_password_entry.delete(0, 'end')

    def delete_user_account(self) -> None:
        delete_files(self._login)
        for widget in self.window.winfo_children():
            widget.place_forget()

        self.information_label.place(x=175, y=50, anchor='center')
        self.information_label.configure(text='Account have been successfully deleted.', text_color='green')

    def confirm_deleting(self) -> None:
        accept_button = ctk.CTkButton(master=self.window, text='Yes', command=self.delete_user_account)
        accept_button.place(x=100, y=70, anchor='center')

        decline_button = ctk.CTkButton(master=self.window, text='No', command=self.close_window)
        decline_button.place(x=250, y=70, anchor='center')

        self.information_label.place(x=175, y=30, anchor='center')

        self.window.bind('<Escape>', self.close_window)

    def close_window(self, event: Any = None) -> None:
        # self.window.grab_release()
        # self.window.withdraw()
        self.window.destroy()

    def _focus_on(self, event: Any = None):
        self.confirmation_button.configure(fg_color='#14375E')

    def _focus_out(self, event: Any = None):
        self.confirmation_button.configure(fg_color='#1F538D')
