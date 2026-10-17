import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


# --- Database Setup & Management ---
def init_database():
    try:
        connection = sqlite3.connect("school_system.db")
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age TEXT NOT NULL,
                gender TEXT NOT NULL,
                phone TEXT NOT NULL,
                grade TEXT NOT NULL
            )
        """)
        connection.commit()
        connection.close()
    except Exception as error:
        messagebox.showerror(
            "Database Error", f"Failed to connect or initialize database: {error}"
        )


# --- Main Window Initialization ---
root = tk.Tk()
root.title("Student Management System - Academic Archive")
root.geometry("1024x650")
root.config(bg="#0f172a")  # Dark modern background
root.minsize(950, 560)

# --- Field Variables ---
id_var = tk.StringVar()
name_var = tk.StringVar()
age_var = tk.StringVar()
gender_var = tk.StringVar()
phone_var = tk.StringVar()
grade_var = tk.StringVar()
search_var = tk.StringVar()

# --- Top Header ---
header_frame = tk.Frame(root, bg="#1e293b", pady=18)
header_frame.pack(fill=tk.X)

header_title = tk.Label(
    header_frame,
    text="🎓 Student Affairs Management System",
    font=("Segoe UI", 16, "bold"),
    bg="#1e293b",
    fg="#38bdf8",  # Accent cyan
)
header_title.pack()

header_subtitle = tk.Label(
    header_frame,
    text="Manage and update student academic records efficiently",
    font=("Segoe UI", 10),
    bg="#1e293b",
    fg="#94a3b8",
)
header_subtitle.pack()

# --- Main Page Container ---
main_container = tk.Frame(root, bg="#0f172a", padx=15, pady=15)
main_container.pack(fill=tk.BOTH, expand=True)

# --- Input Form Frame (Right Side) ---
form_frame = tk.LabelText = tk.LabelFrame(
    main_container,
    text=" Student Information ",
    font=("Segoe UI", 11, "bold"),
    bg="#1e293b",
    fg="#f8fafc",
    padx=15,
    pady=15,
    bd=2,
    relief=tk.GROOVE,
)
form_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)


def create_form_field(parent, label_text, variable, is_combo=False, combo_values=None):
    field_container = tk.Frame(parent, bg="#1e293b", pady=6)
    field_container.pack(fill=tk.X)

    label = tk.Label(
        field_container,
        text=label_text,
        font=("Segoe UI", 10, "bold"),
        bg="#1e293b",
        fg="#cbd5e1",
        anchor="w",
        width=13,
    )
    label.pack(side=tk.LEFT)

    if is_combo:
        widget = ttk.Combobox(
            field_container,
            textvariable=variable,
            values=combo_values or [],
            font=("Segoe UI", 10),
            state="readonly",
            justify="left",
        )
    else:
        widget = tk.Entry(
            field_container,
            textvariable=variable,
            font=("Segoe UI", 10),
            justify="left",
            bg="#334155",
            fg="white",
            insertbackground="white",
            bd=1,
            relief=tk.SOLID,
        )

    widget.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    return widget


# Dropdown Options
age_options = [str(i) for i in range(5, 21)]
gender_options = ["Male", "Female"]
grade_options = [
    "1st Primary",
    "2nd Primary",
    "3rd Primary",
    "4th Primary",
    "5th Primary",
    "6th Primary",
    "1st Intermediate",
    "2nd Intermediate",
    "3rd Intermediate",
    "1st Secondary",
    "2nd Secondary",
    "3rd Secondary",
]

# Build Form Fields
create_form_field(form_frame, "Student ID:", id_var)
create_form_field(form_frame, "Full Name:", name_var)
create_form_field(
    form_frame, "Age:", age_var, is_combo=True, combo_values=age_options
)
create_form_field(
    form_frame, "Gender:", gender_var, is_combo=True, combo_values=gender_options
)
create_form_field(form_frame, "Phone Number:", phone_var)
create_form_field(
    form_frame, "Grade Level:", grade_var, is_combo=True, combo_values=grade_options
)


# --- Core Functions ---
def refresh_table_data():
    for record in student_table.get_children():
        student_table.delete(record)

    try:
        connection = sqlite3.connect("school_system.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, age, gender, phone, grade FROM students")
        records = cursor.fetchall()
        for row in records:
            student_table.insert("", tk.END, values=row)
        connection.close()
    except Exception as error:
        messagebox.showerror(
            "Error", f"Failed to retrieve records: {error}", parent=root
        )


def clear_form_fields():
    id_var.set("")
    name_var.set("")
    age_var.set("")
    gender_var.set("")
    phone_var.set("")
    grade_var.set("")
    search_var.set("")
    if student_table.selection():
        student_table.selection_remove(student_table.selection())


def save_student_record():
    if not all(
        [
            id_var.get(),
            name_var.get(),
            age_var.get(),
            gender_var.get(),
            phone_var.get(),
            grade_var.get(),
        ]
    ):
        messagebox.showwarning(
            "Warning", "Please fill in all required fields before saving!", parent=root
        )
        return

    try:
        connection = sqlite3.connect("school_system.db")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO students (id, name, age, gender, phone, grade) VALUES (?, ?, ?, ?, ?, ?)",
            (
                id_var.get(),
                name_var.get(),
                age_var.get(),
                gender_var.get(),
                phone_var.get(),
                grade_var.get(),
            ),
        )
        connection.commit()
        connection.close()
        refresh_table_data()
        messagebox.showinfo("Success", "Student record saved successfully", parent=root)
        clear_form_fields()
    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Error",
            "This ID already exists! Please use 'Update' instead.",
            parent=root,
        )
    except Exception as error:
        messagebox.showerror(
            "Error", f"An error occurred while saving: {error}", parent=root
        )


def update_student_record():
    selected_item = student_table.focus()
    if not selected_item:
        messagebox.showwarning(
            "Warning", "Please select a student from the table to update!", parent=root
        )
        return

    if not all(
        [
            id_var.get(),
            name_var.get(),
            age_var.get(),
            gender_var.get(),
            phone_var.get(),
            grade_var.get(),
        ]
    ):
        messagebox.showwarning(
            "Warning", "Please make sure all fields are filled!", parent=root
        )
        return

    try:
        connection = sqlite3.connect("school_system.db")
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE students SET name=?, age=?, gender=?, phone=?, grade=? WHERE id=?",
            (
                name_var.get(),
                age_var.get(),
                gender_var.get(),
                phone_var.get(),
                grade_var.get(),
                id_var.get(),
            ),
        )
        connection.commit()
        connection.close()
        refresh_table_data()
        messagebox.showinfo(
            "Success", "Student record updated successfully", parent=root
        )
        clear_form_fields()
    except Exception as error:
        messagebox.showerror(
            "Error", f"An error occurred while updating: {error}", parent=root
        )


def delete_student_record():
    selected_item = student_table.focus()
    if not selected_item:
        messagebox.showwarning(
            "Warning", "Please select a student from the table to delete!", parent=root
        )
        return

    if messagebox.askyesno(
        "Confirm Deletion",
        "Are you sure you want to permanently delete this student record?",
        parent=root,
    ):
        try:
            connection = sqlite3.connect("school_system.db")
            cursor = connection.cursor()
            cursor.execute("DELETE FROM students WHERE id=?", (id_var.get(),))
            connection.commit()
            connection.close()
            refresh_table_data()
            messagebox.showinfo(
                "Success", "Student record deleted successfully", parent=root
            )
            clear_form_fields()
        except Exception as error:
            messagebox.showerror(
                "Error", f"An error occurred while deleting: {error}", parent=root
            )


def on_table_select(event):
    selected_row = student_table.focus()
    content = student_table.item(selected_row)
    row_values = content["values"]
    if row_values:
        id_var.set(row_values[0])
        name_var.set(row_values[1])
        age_var.set(str(row_values[2]))
        gender_var.set(row_values[3])
        phone_var.set(str(row_values[4]))
        grade_var.set(str(row_values[5]))


# --- Buttons Frame ---
buttons_frame = tk.Frame(form_frame, bg="#1e293b", pady=12)
buttons_frame.pack(fill=tk.X)

btn_save = tk.Button(
    buttons_frame,
    text="💾 Save Record",
    font=("Segoe UI", 10, "bold"),
    bg="#0284c7",
    fg="white",
    activebackground="#0369a1",
    activeforeground="white",
    bd=0,
    cursor="hand2",
    pady=6,
    command=save_student_record,
)
btn_save.pack(pady=4, fill=tk.X)

btn_update = tk.Button(
    buttons_frame,
    text="✏️ Update Record",
    font=("Segoe UI", 10, "bold"),
    bg="#d97706",
    fg="white",
    activebackground="#b45309",
    activeforeground="white",
    bd=0,
    cursor="hand2",
    pady=6,
    command=update_student_record,
)
btn_update.pack(pady=4, fill=tk.X)

btn_delete = tk.Button(
    buttons_frame,
    text="🗑️ Delete Record",
    font=("Segoe UI", 10, "bold"),
    bg="#dc2626",
    fg="white",
    activebackground="#b91c1c",
    activeforeground="white",
    bd=0,
    cursor="hand2",
    pady=6,
    command=delete_student_record,
)
btn_delete.pack(pady=4, fill=tk.X)

btn_clear = tk.Button(
    buttons_frame,
    text="🧹 Clear Fields",
    font=("Segoe UI", 10, "bold"),
    bg="#475569",
    fg="white",
    activebackground="#334155",
    activeforeground="white",
    bd=0,
    cursor="hand2",
    pady=6,
    command=clear_form_fields,
)
btn_clear.pack(pady=4, fill=tk.X)


# --- Table Display & Search Frame (Left Side) ---
display_frame = tk.Frame(main_container, bg="#0f172a")
display_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

search_container = tk.Frame(display_frame, bg="#0f172a", pady=5)
search_container.pack(fill=tk.X)

search_label = tk.Label(
    search_container,
    text="🔍 Quick Search (ID or Name):",
    font=("Segoe UI", 10, "bold"),
    bg="#0f172a",
    fg="#cbd5e1",
)
search_label.pack(side=tk.LEFT, padx=5)

search_entry = tk.Entry(
    search_container,
    textvariable=search_var,
    font=("Segoe UI", 10),
    justify="left",
    bg="#334155",
    fg="white",
    insertbackground="white",
    bd=1,
    relief=tk.SOLID,
)
search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)


def filter_table_records(*args):
    query_text = search_var.get().lower()
    for record in student_table.get_children():
        student_table.delete(record)

    try:
        connection = sqlite3.connect("school_system.db")
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, name, age, gender, phone, grade FROM students WHERE lower(id) LIKE ? OR lower(name) LIKE ?",
            (f"%{query_text}%", f"%{query_text}%"),
        )
        filtered_rows = cursor.fetchall()
        for row in filtered_rows:
            student_table.insert("", tk.END, values=row)
        connection.close()
    except Exception as error:
        print(f"Search error: {error}")


search_var.trace("w", filter_table_records)

# --- Treeview Table Customization ---
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Treeview.Heading",
    font=("Segoe UI", 10, "bold"),
    background="#1e293b",
    foreground="white",
)
style.configure(
    "Treeview",
    font=("Segoe UI", 10),
    rowheight=28,
    background="#1e293b",
    foreground="white",
    fieldbackground="#1e293b",
)
style.map(
    "Treeview",
    background=[("selected", "#0284c7")],
    foreground=[("selected", "white")],
)

table_columns = ("id", "name", "age", "gender", "phone", "grade")
student_table = ttk.Treeview(
    display_frame, columns=table_columns, show="headings", selectmode="browse"
)

student_table.heading("id", text="Student ID")
student_table.heading("name", text="Full Name")
student_table.heading("age", text="Age")
student_table.heading("gender", text="Gender")
student_table.heading("phone", text="Phone Number")
student_table.heading("grade", text="Grade Level")

student_table.column("id", width=80, anchor=tk.CENTER)
student_table.column("name", width=150, anchor=tk.W)
student_table.column("age", width=50, anchor=tk.CENTER)
student_table.column("gender", width=65, anchor=tk.CENTER)
student_table.column("phone", width=110, anchor=tk.CENTER)
student_table.column("grade", width=110, anchor=tk.CENTER)

table_scrollbar = ttk.Scrollbar(
    display_frame, orient=tk.VERTICAL, command=student_table.yview
)
student_table.configure(yscrollcommand=table_scrollbar.set)

student_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
table_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

student_table.bind("<ButtonRelease-1>", on_table_select)

# --- Application Startup ---
init_database()
refresh_table_data()

root.mainloop()