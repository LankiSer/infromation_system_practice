import psycopg2
from tkinter import *
from tkinter import ttk

def create_conn():
    conn = psycopg2.connect(
        host="localhost",
        database="inform",
        user="postgres",
        password="root"
    )
    return conn

def get_all_tables(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """)
    return [table[0] for table in cur.fetchall()]

def display():
    window = Tk()
    window.geometry("800x600")
    combo = ttk.Combobox(window)
    combo.pack(side=TOP, fill=X)

    tables = get_all_tables(create_conn())
    combo['values'] = tables

    tree = ttk.Treeview(window)
    tree["show"] = "headings"
    tree.pack(fill=BOTH, expand=True)

    def on_select(event):
        table_name = combo.get()
        conn = create_conn()

        tree.delete(*tree.get_children())

        display_data(table_name, conn, tree)

        for widget in window.winfo_children():
            if isinstance(widget, Button) and widget['text'] == "Добавить запись":
                widget.destroy()

        add_entry_button = Button(window, text="Добавить запись", command=lambda: add_entry_window(table_name, conn, tree))
        add_entry_button.pack(side=BOTTOM)

    combo.bind("<<ComboboxSelected>>", on_select)

    # Добавляем обработчик события для редактирования ячейки по двойному нажатию
    def on_double_click(event):
        conn = create_conn()
        table_name = combo.get()
        item = tree.selection()[0]
        column_id = tree.identify_column(event.x)
        row_values = tree.item(item, 'values')
        col_index = int(column_id.replace('#', ''))-1
        column_name = tree.column(col_index)['id']

        edit_window = Toplevel()
        edit_window.title("Редактировать ячейку")

        label = Label(edit_window, text=f"Редактировать значение в столбце '{column_name}'")
        label.pack()

        entry = Entry(edit_window)
        entry.insert(0, row_values[col_index])
        entry.pack()

        def save_changes(table_name, conn, column_name):
            new_value = entry.get()
            row_id = row_values[0]  # Assuming row_values[0] contains the row id

            update_query = f"UPDATE {table_name} SET {column_name} = %s WHERE id = %s"
            cur = conn.cursor()
            cur.execute(update_query, (new_value, row_id))
            conn.commit()
            edit_window.destroy()
            display_data(table_name, conn, tree)
        def combined_func(table_name, conn, column_name):
            save_changes(table_name, conn, column_name)
            edit_window.destroy()

        save_button = Button(edit_window, text="Сохранить", command=lambda: combined_func(table_name, conn, column_name))
        save_button.pack()

    tree.bind("<Double-1>", on_double_click)

    window.mainloop()


def display_data(table_name, conn, tree):
    tree.delete(*tree.get_children())

    cur = conn.cursor()
    cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' ORDER BY ordinal_position")
    columns = [column[0] for column in cur.fetchall()]
    tree["columns"] = tuple(columns)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center')

    cur.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()

    for row in rows:
        tree.insert('', 'end', values=row)

    def on_item_selected(event):
        col_id = (tree.identify_column(event.x))

        if col_id:
            col_no = int(col_id.lstrip("#"))
            item_id = tree.identify_row(event.y)
            values = tree.item(item_id, "values")
            selected_value = values[col_no]

    tree.bind("<ButtonRelease-1>", on_item_selected)

def add_entry_window(table_name, conn, tree):
    entry_window = Toplevel()
    entry_window.title("Добавить запись")

    cur = conn.cursor()
    cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' ORDER BY ordinal_position")

    columns = [column[0] for column in cur.fetchall()]
    entry_fields = []

    for col in columns:
        label = Label(entry_window, text=col)
        label.grid(row=columns.index(col), column=0, sticky=E)
        entry = Entry(entry_window)
        entry.grid(row=columns.index(col), column=1)
        entry_fields.append(entry)

    insert_button = Button(entry_window, text="Добавить", command=lambda: insert_entry(table_name, columns, entry_fields, conn, entry_window, tree))
    insert_button.grid(row=len(columns), columnspan=2)

def insert_entry(table_name, columns, entry_fields, conn, window, tree):
    formatted_columns = ", ".join(columns)
    placeholders = ', '.join(['%s'] * len(entry_fields))

    values = [entry.get() for entry in entry_fields]
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {table_name} ({formatted_columns}) VALUES ({placeholders})", values)
    conn.commit()
    window.destroy()
    display_data(table_name, conn, tree)





if __name__ == "__main__":
    display()

