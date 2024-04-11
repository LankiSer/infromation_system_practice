import tkinter as tk
from tkinter import messagebox
import psycopg2
from user_kab import display_user  # Импорт функции display_user из файла user_kab.py

def on_login():
    username = login_entry.get()
    password = password_entry.get()

    conn = psycopg2.connect(
        host="localhost",
        database="inform",
        user="postgres",
        password="root"
    )
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE login = %s", (username,))
    data = cur.fetchone()

    if data is not None:
        password_from_db = data[0].strip()  # Предположим, что пароль находится во втором столбце

        if password == password_from_db:
            messagebox.showinfo("Статус входа", "Вы успешно вошли в систему!")
            root.destroy()  # Закрыть текущее окно авторизации
            display_user(username)  # Вызов функции display_user из файла user_kab.py, передача имени пользователя
        else:
            messagebox.showerror("Статус входа", "Неправильный логин или пароль.")
    else:
        messagebox.showerror("Статус входа", "Неправильный логин или пароль.")

root = tk.Tk()
root.title("Login")

login_label = tk.Label(root, text="Логин:")
login_label.pack()

login_entry = tk.Entry(root)
login_entry.pack()

password_label = tk.Label(root, text="Пароль:")
password_label.pack()

password_entry = tk.Entry(root, show="*")
password_entry.pack()

login_button = tk.Button(root, text="Войти", command=on_login)
login_button.pack()

root.mainloop()
