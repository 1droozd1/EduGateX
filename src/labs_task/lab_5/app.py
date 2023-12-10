import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import psycopg2
import sys
sys.path.append('/Users/dr0ozd/coding/bd_project/src')
from bd_info import *

# Функция для подключения к базе данных
def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# Получение первичного ключа для таблицы
def get_primary_key_column(table_name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT a.attname FROM pg_index i JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey) WHERE i.indrelid = '{table_name}'::regclass AND i.indisprimary;")
    primary_key_column = cur.fetchone()
    cur.close()
    conn.close()
    return primary_key_column[0] if primary_key_column else None

# Функция для получения списка таблиц
def get_tables():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = [table[0] for table in cur.fetchall()]
    cur.close()
    conn.close()
    return tables

# Функция для отображения содержимого выбранной таблицы
def show_table_content(event):
    selected_table = combo_tables.get()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {selected_table}")
    records = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()

    # Очистка старых данных
    for row in table_tree.get_children():
        table_tree.delete(row)

    # Установка новых колонок
    table_tree['columns'] = column_names
    table_tree.column("#0", width=0, stretch=tk.NO)

    # Создание заголовков
    for i in column_names:
        table_tree.heading(i, text=i)
        table_tree.column(i, anchor=tk.CENTER)

    # Вставка данных
    for row in records:
        table_tree.insert("", tk.END, values=row)

# Функция для добавления новой строки в таблицу
def add_new_record():
    selected_table = combo_tables.get()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {selected_table} LIMIT 0")
    column_names = [desc[0] for desc in cur.description]
    cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{selected_table}' AND column_default LIKE 'nextval%'")
    autoincrement_columns = [desc[0] for desc in cur.fetchall()]
    cur.close()
    conn.close()
    
    # Формируем диалоговое окно для ввода данных
    entry_values = {}
    for column in column_names:
        if column in autoincrement_columns:
            continue
        entry_values[column] = simpledialog.askstring("Input", f"Enter {column} value")

    # Проверяем, что все значения были введены
    if all(value is not None for value in entry_values.values()):
        # Формируем запрос для вставки данных
        columns = ', '.join(entry_values.keys())
        placeholders = ', '.join(['%s'] * len(entry_values))
        values = tuple(entry_values.values())
        insert_query = f"INSERT INTO {selected_table} ({columns}) VALUES ({placeholders})"
        
        # Вставляем данные в базу
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(insert_query, values)
            conn.commit()
            messagebox.showinfo("Success", "Record added successfully")
        except psycopg2.Error as e:
            messagebox.showerror("Error", e)
        finally:
            cur.close()
            conn.close()
        
    # Обновляем содержимое таблицы
    show_table_content()

# Функция удаления выбранной строки в таблице
def delete_selected_record():
    selected_item = table_tree.selection()
    if not selected_item:  # Если ничего не выбрано, ничего не делаем
        messagebox.showwarning("Warning", "Please select a record to delete.")
        return

    # Подтверждение удаления
    if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected record?"):
        selected_table = combo_tables.get()
        conn = get_db_connection()
        cur = conn.cursor()

        # Определение первичного ключа для таблицы
        cur.execute(f"SELECT a.attname FROM pg_index i JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey) WHERE i.indrelid = '{selected_table}'::regclass AND i.indisprimary;")
        primary_key_column = cur.fetchone()

        if primary_key_column:
            primary_key_column = primary_key_column[0]
            # Получаем значение первичного ключа выбранной строки
            selected_row_id = table_tree.item(selected_item)["values"][0]  # предполагается, что PK всегда первый столбец

            # SQL-запрос на удаление
            delete_query = f"DELETE FROM {selected_table} WHERE {primary_key_column} = %s"
            cur.execute(delete_query, (selected_row_id,))
            conn.commit()
            cur.close()
            conn.close()

            # Обновление интерфейса
            table_tree.delete(selected_item)
            messagebox.showinfo("Success", "Record deleted successfully.")
        else:
            cur.close()
            conn.close()
            messagebox.showerror("Error", "Could not determine the primary key for the selected record.")

# Функция вызывается при нажатии кнопки редактирования
def edit_selected_record():
    selected_item = table_tree.selection()
    if not selected_item:  # Если ничего не выбрано, ничего не делаем
        messagebox.showwarning("Warning", "Please select a record to edit.")
        return

    # Получаем выбранную строку
    selected_row = table_tree.item(selected_item)["values"]

    # Диалоговое окно для редактирования
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Record")

    # Метки и поля ввода для каждого столбца
    entries = {}
    for index, column in enumerate(table_tree["columns"]):
        ttk.Label(edit_window, text=column).grid(row=index, column=0, sticky="w")
        entry = ttk.Entry(edit_window)
        entry.insert(0, selected_row[index])
        entry.grid(row=index, column=1)
        entries[column] = entry

    # Функция обновления записи в базе данных
    def update_record():
        values = {key: entry.get() for key, entry in entries.items()}
        primary_key_column = get_primary_key_column(combo_tables.get())

        if primary_key_column:
            conn = get_db_connection()
            cur = conn.cursor()
            update_query = f"UPDATE {combo_tables.get()} SET " + ", ".join([f"{key} = %s" for key in values if key != primary_key_column])
            update_query += f" WHERE {primary_key_column} = %s"
            
            try:
                print(update_query)
                print(list(values.values()) + [str(selected_row[0])])
                cur.execute(update_query, list(map(str, list(values.values())[1:])) + [str(selected_row[0])])  # предполагается, что PK находится в первом столбце
                conn.commit()
                messagebox.showinfo("Success", "Record updated successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
            finally:
                cur.close()
                conn.close()
            
            # Обновляем дерево
            table_tree.item(selected_item, values=list(values.values()))
            edit_window.destroy()

    # Кнопка для сохранения изменений
    save_button = ttk.Button(edit_window, text="Save changes", command=update_record)
    save_button.grid(row=len(table_tree["columns"]), column=0, columnspan=2)

# Функция для отображения схемы базы данных
def show_db_schema():
    schema_path = '/Users/dr0ozd/coding/bd_project/scheme.jpeg'  # Путь к файлу изображения
    image = Image.open(schema_path)

    basewidth = 850
    wpercent = (basewidth / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    image = image.resize((basewidth, hsize), Image.LANCZOS)

    photo = ImageTk.PhotoImage(image)

    # Создание нового окна с изображением
    schema_window = tk.Toplevel()
    schema_window.title("Database Schema")
    img_label = ttk.Label(schema_window, image=photo)
    img_label.image = photo  # Сохранение ссылки на изображение
    img_label.pack()

# Создание основного окна
root = tk.Tk()
root.title("Database Management Application")

# Виджет для выбора таблиц
tables_frame = ttk.Frame(root)
tables_frame.pack(padx=10, pady=10, fill='x', expand=True)

combo_tables = ttk.Combobox(tables_frame, values=get_tables())
combo_tables.pack(side=tk.LEFT, padx=(0, 10), fill='x', expand=True)
combo_tables.bind("<<ComboboxSelected>>", show_table_content)

# Виджет для отображения содержимого таблицы
table_frame = ttk.Frame(root)
table_frame.pack(padx=10, pady=10, fill='both', expand=True)

table_tree = ttk.Treeview(table_frame)
table_tree.pack(pady=10, fill='both', expand=True)

# Кнопка для добавления новой записи
add_button = ttk.Button(root, text="Add New Record", command=add_new_record)
add_button.pack(side=tk.LEFT, padx=5, pady=5)

# Кнопка для удаления выбранной записи
delete_button = ttk.Button(root, text="Delete Selected Record", command=delete_selected_record)
delete_button.pack(side=tk.LEFT, padx=5, pady=5)

# Кнопка редактирования выбранного значения
edit_button = ttk.Button(root, text="Edit Selected Record", command=edit_selected_record)
edit_button.pack(side=tk.LEFT, padx=5, pady=5)

# Кнопка для отображения схемы базы данных
schema_button = ttk.Button(root, text="Show DB Schema", command=show_db_schema)
schema_button.pack(side=tk.LEFT, padx=5, pady=5)

root.mainloop()
