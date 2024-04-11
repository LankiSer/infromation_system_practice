import tkinter as tk
from tkinter import messagebox

from main_db import display


def display_user(username):
    user_window = tk.Tk()
    user_window.title(f"Кабинет пользователя: {username}")

    user_label = tk.Label(user_window, text=f"Добро пожаловать, {username}!")
    user_label.pack()

    switch_button = tk.Button(user_window, text="Перейти к данным", command=lambda: display_data(
        username))  # Добавить конкретную логику или вызов другой функции
    switch_button.pack()

    user_window.mainloop()


def display_data(username):
    display()
