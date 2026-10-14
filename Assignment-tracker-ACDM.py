import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib
import calendar
from datetime import datetime, date

#pampaganda ehe

BG = "#F5FAFD"
WHITE = "#FFFFFF"
SKY = "#BFE7F5"
SKY_DARK = "#78C8E6"
PRIMARY = "#58B9DE"
PRIMARY_DARK = "#3AA6CF"
PASTEL_BLUE = "#DDF3FA"
PASTEL_MINT = "#E3F6F0"
PASTEL_YELLOW = "#FFF7D6"
PASTEL_PINK = "#FCE7EF"
PASTEL_RED = "#FFE1E1"
TEXT = "#35515E"
MUTED = "#78909C"
BORDER = "#D7EAF2"
DANGER = "#D9534F"

DB_NAME = "studytrack.db"

#database connection

def connect_db():
    return sqlite3.connect(DB_NAME)


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def setup_database():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'Student'
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            subject TEXT NOT NULL,
            due_date TEXT NOT NULL,
            due_time TEXT DEFAULT '11:59 PM',
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    cur.execute("PRAGMA table_info(assignments)")
    columns = [row[1] for row in cur.fetchall()]

    if "due_time" not in columns:
        cur.execute(
            "ALTER TABLE assignments "
            "ADD COLUMN due_time TEXT DEFAULT '11:59 PM'"
        )

    conn.commit()
    conn.close()

#main application class

class StudyTrackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("STUDYTRACK - Assignment Management System")
        self.root.geometry("1180x760")
        self.root.minsize(980, 650)
        self.root.configure(bg=BG)

        self.current_user = None

        self.setup_style()
        self.show_login()

#ganda ng buhay

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background=BG)
        style.configure("Card.TFrame", background=WHITE)
        style.configure("White.TFrame", background=WHITE)

        style.configure(
            "TLabel",
            background=BG,
            foreground=TEXT,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Card.TLabel",
            background=WHITE,
            foreground=TEXT,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Title.TLabel",
            background=BG,
            foreground=TEXT,
            font=("Segoe UI", 28, "bold")
        )

        style.configure(
            "CardTitle.TLabel",
            background=WHITE,
            foreground=TEXT,
            font=("Segoe UI", 24, "bold")
        )

        style.configure(
            "MutedCard.TLabel",
            background=WHITE,
            foreground=MUTED,
            font=("Segoe UI", 10)
        )

        style.configure(
            "TButton",
            background=SKY,
            foreground=TEXT,
            font=("Segoe UI", 10, "bold"),
            padding=(14, 10),
            borderwidth=0
        )

        style.map(
            "TButton",
            background=[
                ("active", SKY_DARK),
                ("pressed", SKY_DARK)
            ]
        )

        style.configure(
            "Primary.TButton",
            background=PRIMARY,
            foreground=WHITE,
            font=("Segoe UI", 10, "bold"),
            padding=(16, 11),
            borderwidth=0
        )

        style.map(
            "Primary.TButton",
            background=[
                ("active", PRIMARY_DARK),
                ("pressed", PRIMARY_DARK)
            ]
        )

        style.configure(
            "Secondary.TButton",
            background="#EAF6FB",
            foreground=TEXT,
            font=("Segoe UI", 10, "bold"),
            padding=(14, 10),
            borderwidth=0
        )

        style.map(
            "Secondary.TButton",
            background=[
                ("active", "#DCEFF7"),
                ("pressed", "#CFE8F3")
            ]
        )

        style.configure(
            "Danger.TButton",
            background="#FFDADA",
            foreground=DANGER,
            font=("Segoe UI", 10, "bold"),
            padding=(14, 10),
            borderwidth=0
        )

        style.configure(
            "TEntry",
            fieldbackground="#F9FCFE",
            foreground=TEXT,
            padding=9,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER
        )

        style.configure(
            "TCombobox",
            fieldbackground="#F9FCFE",
            foreground=TEXT,
            padding=8
        )

        style.configure(
            "Treeview",
            background=WHITE,
            fieldbackground=WHITE,
            foreground=TEXT,
            rowheight=38,
            font=("Segoe UI", 10),
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background=PASTEL_BLUE,
            foreground=TEXT,
            font=("Segoe UI", 10, "bold"),
            padding=9,
            borderwidth=0
        )

        style.map(
            "Treeview",
            background=[("selected", SKY)],
            foreground=[("selected", TEXT)]
        )

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg=BG)

#login and register
 
    def show_login(self):
        self.clear_window()

        container = tk.Frame(self.root, bg=BG)
        container.pack(fill="both", expand=True)

        left_panel = tk.Frame(container, bg=PASTEL_BLUE, width=430)
        left_panel.pack(side="left", fill="both")
        left_panel.pack_propagate(False)

        left_content = tk.Frame(left_panel, bg=PASTEL_BLUE)
        left_content.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            left_content,
            text="STUDYTRACK",
            bg=PASTEL_BLUE,
            fg=TEXT,
            font=("Segoe UI", 32, "bold")
        ).pack()

        tk.Label(
            left_content,
            text="Assignment Management System",
            bg=PASTEL_BLUE,
            fg=MUTED,
            font=("Segoe UI", 12)
        ).pack(pady=(8, 0))

        tk.Label(
            left_content,
            text="Plan • Track • Complete",
            bg=PASTEL_BLUE,
            fg=TEXT,
            font=("Segoe UI", 11, "bold")
        ).pack(pady=(28, 0))

        right_panel = tk.Frame(container, bg=BG)
        right_panel.pack(side="right", fill="both", expand=True)

        card = tk.Frame(
            right_panel,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=42,
            pady=40
        )
        card.place(relx=0.5, rely=0.5, anchor="center", width=445)

        tk.Label(
            card,
            text="Welcome back",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 25, "bold")
        ).pack(anchor="w")

        tk.Label(
            card,
            text="Enter your account details to continue.",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(5, 24))

        tk.Label(
            card,
            text="Gmail",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        self.login_email = ttk.Entry(card)
        self.login_email.pack(fill="x", pady=(6, 16), ipady=2)

        tk.Label(
            card,
            text="Password",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        password_row = tk.Frame(card, bg=WHITE)
        password_row.pack(fill="x", pady=(6, 20))

        self.login_password = ttk.Entry(password_row, show="*")
        self.login_password.pack(side="left", fill="x", expand=True, ipady=2)

        show_password = tk.BooleanVar(value=False)

        def toggle_password():
            self.login_password.config(
                show="" if show_password.get() else "*"
            )

        ttk.Checkbutton(
            card,
            text="Show password",
            variable=show_password,
            command=toggle_password
        ).pack(anchor="w", pady=(0, 16))

        ttk.Button(
            card,
            text="LOG IN",
            style="Primary.TButton",
            command=self.login
        ).pack(fill="x")

        ttk.Button(
            card,
            text="CREATE ACCOUNT",
            style="Secondary.TButton",
            command=self.show_register
        ).pack(fill="x", pady=(10, 0))

        tk.Label(
            card,
            text="ANTIOQUIA  •  CAÑETE  •  DIMAANDAL  •  MORALES",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(pady=(24, 0))

        self.login_password.bind("<Return>", lambda event: self.login())
        self.login_email.focus_set()

    def login(self):
        email = self.login_email.get().strip().lower()
        password = self.login_password.get()

        if not email or not password:
            messagebox.showwarning(
                "Missing Information",
                "Please enter your Gmail and password."
            )
            return

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id, name, email, role
            FROM users
            WHERE email = ? AND password = ?
            """,
            (email, hash_password(password))
        )

        user = cur.fetchone()
        conn.close()

        if not user:
            messagebox.showerror(
                "Login Failed",
                "Incorrect Gmail or password."
            )
            return

        self.current_user = {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "role": user[3]
        }

        self.show_dashboard()

# mag register na tayo pag ayaw mo di wag
 
    def show_register(self):
        self.clear_window()

        card = tk.Frame(
            self.root,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=44,
            pady=32
        )

        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=520
        )

        tk.Label(
            card,
            text="Create account",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 25, "bold")
        ).pack(anchor="w")

        tk.Label(
            card,
            text="Fill in your details below.",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(5, 22))

        def add_label(text):
            tk.Label(
                card,
                text=text,
                bg=WHITE,
                fg=TEXT,
                font=("Segoe UI", 10, "bold")
            ).pack(anchor="w")

        add_label("Full Name")
        self.reg_name = ttk.Entry(card)
        self.reg_name.pack(fill="x", pady=(5, 12), ipady=2)

        add_label("Gmail")
        self.reg_email = ttk.Entry(card)
        self.reg_email.pack(fill="x", pady=(5, 12), ipady=2)

        add_label("Password")
        self.reg_password = ttk.Entry(card, show="*")
        self.reg_password.pack(fill="x", pady=(5, 12), ipady=2)

        add_label("Confirm Password")
        self.reg_confirm = ttk.Entry(card, show="*")
        self.reg_confirm.pack(fill="x", pady=(5, 12), ipady=2)

        add_label("Account Type")
        self.role = tk.StringVar(value="Student")

        role_box = ttk.Combobox(
            card,
            textvariable=self.role,
            values=["Student"],
            state="readonly"
        )
        role_box.pack(fill="x", pady=(5, 18))

        ttk.Button(
            card,
            text="SUBMIT",
            style="Primary.TButton",
            command=self.register
        ).pack(fill="x")

        ttk.Button(
            card,
            text="BACK TO LOGIN",
            style="Secondary.TButton",
            command=self.show_login
        ).pack(fill="x", pady=(10, 0))

        self.reg_confirm.bind("<Return>", lambda event: self.register())
        self.reg_name.focus_set()

    def register(self):
        name = self.reg_name.get().strip()
        email = self.reg_email.get().strip().lower()
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()
        role = self.role.get()

        if not all([name, email, password, confirm]):
            messagebox.showwarning(
                "Missing Information",
                "Please complete all fields."
            )
            return

        if not email.endswith("@gmail.com") or " " in email:
            messagebox.showwarning(
                "Invalid Gmail",
                "Please use a valid Gmail address."
            )
            return

        if password != confirm:
            messagebox.showerror(
                "Password Error",
                "Passwords do not match."
            )
            return

        if len(password) < 6:
            messagebox.showwarning(
                "Password Error",
                "Password must contain at least 6 characters."
            )
            return

        conn = connect_db()
        cur = conn.cursor()

        try:
            cur.execute(
                """
                INSERT INTO users (name, email, password, role)
                VALUES (?, ?, ?, ?)
                """,
                (
                    name,
                    email,
                    hash_password(password),
                    role
                )
            )

            conn.commit()

            messagebox.showinfo(
                "Account Created",
                "Your account has been successfully created."
            )

            self.show_login()

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Account Exists",
                "That Gmail is already registered."
            )
        finally:
            conn.close()

#dash ni lancelot to guys

    def show_dashboard(self):
        self.clear_window()

        header = tk.Frame(
            self.root,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        header.pack(fill="x")

        header_left = tk.Frame(header, bg=WHITE)
        header_left.pack(side="left", padx=22, pady=17)

        tk.Label(
            header_left,
            text="STUDYTRACK",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w")

        tk.Label(
            header_left,
            text=f"Welcome, {self.current_user['name']}",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w")

        ttk.Button(
            header,
            text="LOG OUT",
            style="Secondary.TButton",
            command=self.logout
        ).pack(side="right", padx=22, pady=18)

        tk.Label(
            header,
            text=f"{self.current_user['role']}",
            bg=PASTEL_BLUE,
            fg=TEXT,
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=6
        ).pack(side="right", pady=18)

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=20, pady=18)

        stats = tk.Frame(body, bg=BG)
        stats.pack(fill="x", pady=(0, 14))

        self.pending_label = self.create_stat_card(
            stats, "Pending", "0", PASTEL_YELLOW
        )

        self.completed_label = self.create_stat_card(
            stats, "Completed", "0", PASTEL_MINT
        )

        self.upcoming_label = self.create_stat_card(
            stats, "Upcoming", "0", PASTEL_BLUE
        )

        self.overdue_label = self.create_stat_card(
            stats, "Overdue", "0", PASTEL_RED
        )

        action_bar = tk.Frame(body, bg=BG)
        action_bar.pack(fill="x", pady=(0, 12))

        ttk.Button(
            action_bar,
            text="+ ADD ASSIGNMENT",
            style="Primary.TButton",
            command=self.add_assignment
        ).pack(side="left")

        ttk.Button(
            action_bar,
            text="MARK COMPLETED",
            command=self.mark_completed
        ).pack(side="left", padx=8)

        ttk.Button(
            action_bar,
            text="DELETE",
            style="Danger.TButton",
            command=self.delete_assignment
        ).pack(side="left")

        ttk.Button(
            action_bar,
            text="REFRESH",
            style="Secondary.TButton",
            command=self.refresh_tasks
        ).pack(side="right")

        table_card = tk.Frame(
            body,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        table_card.pack(fill="both", expand=True)

        table_frame = tk.Frame(table_card, bg=WHITE)
        table_frame.pack(fill="both", expand=True, padx=12, pady=12)

        self.tree = ttk.Treeview(
            table_frame,
            columns=(
                "title",
                "subject",
                "date",
                "time",
                "status",
                "description"
            ),
            show="headings"
        )

        headings = {
            "title": ("Assignment", 180),
            "subject": ("Subject", 130),
            "date": ("Due Date", 115),
            "time": ("Due Time", 100),
            "status": ("Status", 105),
            "description": ("Description", 320)
        }

        for column, (label, width) in headings.items():
            self.tree.heading(column, text=label)
            self.tree.column(column, width=width, anchor="w")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.tag_configure(
            "completed",
            background=PASTEL_MINT
        )
        self.tree.tag_configure(
            "overdue",
            background=PASTEL_RED
        )
        self.tree.tag_configure(
            "today",
            background=PASTEL_YELLOW
        )

        self.refresh_tasks()

    def create_stat_card(self, parent, title, value, color):
        card = tk.Frame(
            parent,
            bg=color,
            padx=18,
            pady=12
        )

        card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        tk.Label(
            card,
            text=title,
            bg=color,
            fg=MUTED,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")

        value_label = tk.Label(
            card,
            text=value,
            bg=color,
            fg=TEXT,
            font=("Segoe UI", 20, "bold")
        )
        value_label.pack(anchor="w")

        return value_label

#assignment adding bago ml ehe

    def add_assignment(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Assignment")
        dialog.geometry("530x700")
        dialog.resizable(False, False)
        dialog.configure(bg=BG)
        dialog.transient(self.root)
        dialog.grab_set()

        card = tk.Frame(
            dialog,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=30,
            pady=28
        )
        card.pack(fill="both", expand=True, padx=18, pady=18)

        tk.Label(
            card,
            text="Add Assignment",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")

        tk.Label(
            card,
            text="Enter the assignment details and choose the deadline.",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(4, 20))

        def field_label(text):
            tk.Label(
                card,
                text=text,
                bg=WHITE,
                fg=TEXT,
                font=("Segoe UI", 10, "bold")
            ).pack(anchor="w")

        field_label("Assignment Title")
        title = ttk.Entry(card)
        title.pack(fill="x", pady=(5, 12), ipady=2)

        field_label("Subject")
        subject = ttk.Entry(card)
        subject.pack(fill="x", pady=(5, 12), ipady=2)

        field_label("Due Date")

        date_row = tk.Frame(card, bg=WHITE)
        date_row.pack(fill="x", pady=(5, 12))

        selected_date = tk.StringVar(
            value=date.today().strftime("%Y-%m-%d")
        )

        date_entry = ttk.Entry(
            date_row,
            textvariable=selected_date,
            state="readonly"
        )
        date_entry.pack(side="left", fill="x", expand=True, ipady=2)

        ttk.Button(
            date_row,
            text="CALENDAR",
            style="Secondary.TButton",
            command=lambda: self.open_calendar(
                dialog,
                selected_date
            )
        ).pack(side="left", padx=(8, 0))

        field_label("Due Time")

        time_row = tk.Frame(card, bg=WHITE)
        time_row.pack(fill="x", pady=(5, 12))

        selected_hour = tk.StringVar(value="11")
        selected_minute = tk.StringVar(value="59")
        selected_period = tk.StringVar(value="PM")

        hour_box = ttk.Combobox(
            time_row,
            width=7,
            textvariable=selected_hour,
            values=[f"{hour:02d}" for hour in range(1, 13)],
            state="readonly"
        )
        hour_box.pack(side="left")

        tk.Label(
            time_row,
            text=":",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 12, "bold")
        ).pack(side="left", padx=5)

        minute_box = ttk.Combobox(
            time_row,
            width=7,
            textvariable=selected_minute,
            values=[f"{minute:02d}" for minute in range(0, 60, 5)] + ["59"],
            state="readonly"
        )
        minute_box.pack(side="left")

        period_box = ttk.Combobox(
            time_row,
            width=7,
            textvariable=selected_period,
            values=["AM", "PM"],
            state="readonly"
        )
        period_box.pack(side="left", padx=(8, 0))

        ttk.Button(
            time_row,
            text="NOW",
            style="Secondary.TButton",
            command=lambda: self.set_current_time(
                selected_hour,
                selected_minute,
                selected_period
            )
        ).pack(side="right")

        field_label("Description")

        description = tk.Text(
            card,
            height=5,
            bg="#F9FCFE",
            fg=TEXT,
            insertbackground=TEXT,
            relief="solid",
            bd=1,
            font=("Segoe UI", 10),
            wrap="word"
        )
        description.pack(fill="x", pady=(5, 10))

        def save_assignment():
            title_value = title.get().strip()
            subject_value = subject.get().strip()
            due_date_value = selected_date.get().strip()
            due_time_value = (
                f"{selected_hour.get()}:"
                f"{selected_minute.get()} "
                f"{selected_period.get()}"
            )

            description_value = description.get(
                "1.0",
                "end"
            ).strip()

            if not title_value or not subject_value:
                messagebox.showwarning(
                    "Missing Information",
                    "Please enter the assignment title and subject.",
                    parent=dialog
                )
                return

            try:
                datetime.strptime(
                    due_date_value,
                    "%Y-%m-%d"
                )

                datetime.strptime(
                    due_time_value,
                    "%I:%M %p"
                )
            except ValueError:
                messagebox.showerror(
                    "Invalid Deadline",
                    "Please choose a valid date and time.",
                    parent=dialog
                )
                return

            conn = connect_db()
            cur = conn.cursor()

            cur.execute(
                """
                INSERT INTO assignments (
                    user_id,
                    title,
                    description,
                    subject,
                    due_date,
                    due_time,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, 'Pending')
                """,
                (
                    self.current_user["id"],
                    title_value,
                    description_value,
                    subject_value,
                    due_date_value,
                    due_time_value
                )
            )

            conn.commit()
            conn.close()

            dialog.destroy()
            self.refresh_tasks()

            messagebox.showinfo(
                "Saved",
                "Assignment submitted successfully."
            )

        ttk.Button(
            card,
            text="ADD TASK",
            style="Primary.TButton",
            command=save_assignment
        ).pack(fill="x", pady=(0, 8))

        ttk.Button(
            card,
            text="CANCEL",
            style="Secondary.TButton",
            command=dialog.destroy
        ).pack(fill="x", pady=(10, 0))

        title.focus_set()

    def set_current_time(
        self,
        hour_var,
        minute_var,
        period_var
    ):
        now = datetime.now()

        hour = now.strftime("%I")
        minute = now.strftime("%M")
        period = now.strftime("%p")

        rounded_minute = int(minute)
        rounded_minute = int(round(rounded_minute / 5) * 5)

        if rounded_minute >= 60:
            rounded_minute = 55

        hour_var.set(hour)
        minute_var.set(f"{rounded_minute:02d}")
        period_var.set(period)

#date pero walang kayo

    def open_calendar(self, parent, selected_date):
        popup = tk.Toplevel(parent)
        popup.title("Choose Date")
        popup.geometry("390x410")
        popup.resizable(False, False)
        popup.configure(bg=WHITE)
        popup.transient(parent)
        popup.grab_set()

        try:
            current_date = datetime.strptime(
                selected_date.get(),
                "%Y-%m-%d"
            ).date()
        except ValueError:
            current_date = date.today()

        state = {
            "year": current_date.year,
            "month": current_date.month
        }

        header = tk.Frame(
            popup,
            bg=WHITE,
            padx=14,
            pady=14
        )
        header.pack(fill="x")

        month_label = tk.Label(
            header,
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 14, "bold")
        )
        month_label.pack(side="left", expand=True)

        calendar_frame = tk.Frame(
            popup,
            bg=WHITE,
            padx=12,
            pady=6
        )
        calendar_frame.pack(fill="both", expand=True)

        def previous_month():
            if state["month"] == 1:
                state["month"] = 12
                state["year"] -= 1
            else:
                state["month"] -= 1

            draw_calendar()

        def next_month():
            if state["month"] == 12:
                state["month"] = 1
                state["year"] += 1
            else:
                state["month"] += 1

            draw_calendar()

        ttk.Button(
            header,
            text="<",
            style="Secondary.TButton",
            command=previous_month
        ).pack(side="left")

        ttk.Button(
            header,
            text=">",
            style="Secondary.TButton",
            command=next_month
        ).pack(side="right")

        def choose_day(day_number):
            picked = date(
                state["year"],
                state["month"],
                day_number
            )

            selected_date.set(
                picked.strftime("%Y-%m-%d")
            )

            popup.destroy()

        def draw_calendar():
            for widget in calendar_frame.winfo_children():
                widget.destroy()

            month_label.config(
                text=(
                    f"{calendar.month_name[state['month']]} "
                    f"{state['year']}"
                )
            )

            day_names = [
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
                "Sun"
            ]

            for column, day_name in enumerate(day_names):
                tk.Label(
                    calendar_frame,
                    text=day_name,
                    bg=WHITE,
                    fg=MUTED,
                    font=("Segoe UI", 9, "bold"),
                    width=5
                ).grid(
                    row=0,
                    column=column,
                    padx=2,
                    pady=(5, 8)
                )

            month_days = calendar.monthcalendar(
                state["year"],
                state["month"]
            )

            today = date.today()

            for row_index, week in enumerate(
                month_days,
                start=1
            ):
                for column, day_number in enumerate(week):
                    if day_number == 0:
                        continue

                    button_bg = WHITE
                    button_fg = TEXT

                    if (
                        day_number == today.day
                        and state["month"] == today.month
                        and state["year"] == today.year
                    ):
                        button_bg = SKY

                    button = tk.Button(
                        calendar_frame,
                        text=str(day_number),
                        width=5,
                        height=2,
                        bg=button_bg,
                        fg=button_fg,
                        activebackground=SKY_DARK,
                        activeforeground=TEXT,
                        relief="flat",
                        cursor="hand2",
                        command=lambda d=day_number: choose_day(d)
                    )

                    button.grid(
                        row=row_index,
                        column=column,
                        padx=2,
                        pady=2
                    )

            for column in range(7):
                calendar_frame.grid_columnconfigure(
                    column,
                    weight=1
                )

        footer = tk.Frame(
            popup,
            bg=WHITE,
            padx=14,
            pady=10
        )
        footer.pack(fill="x")

        ttk.Button(
            footer,
            text="TODAY",
            style="Primary.TButton",
            command=lambda: (
                selected_date.set(
                    date.today().strftime("%Y-%m-%d")
                ),
                popup.destroy()
            )
        ).pack(fill="x")

        draw_calendar()

#task status kayo lang wala

    def get_display_status(
        self,
        due_date,
        due_time,
        stored_status
    ):
        if stored_status == "Completed":
            return "Completed"

        try:
            deadline = datetime.strptime(
                f"{due_date} {due_time}",
                "%Y-%m-%d %I:%M %p"
            )
        except ValueError:
            return stored_status

        now = datetime.now()

        if deadline < now:
            return "Overdue"

        if deadline.date() == date.today():
            return "Due Today"

        return "Pending"

    def refresh_tasks(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                id,
                title,
                subject,
                due_date,
                due_time,
                status,
                description
            FROM assignments
            WHERE user_id = ?
            ORDER BY due_date ASC, due_time ASC
            """,
            (self.current_user["id"],)
        )

        rows = cur.fetchall()
        conn.close()

        pending_count = 0
        completed_count = 0
        upcoming_count = 0
        overdue_count = 0

        for row in rows:
            (
                assignment_id,
                title,
                subject,
                due_date,
                due_time,
                stored_status,
                description
            ) = row

            due_time = due_time or "11:59 PM"

            display_status = self.get_display_status(
                due_date,
                due_time,
                stored_status
            )

            tag = ""

            if display_status == "Completed":
                completed_count += 1
                tag = "completed"

            elif display_status == "Overdue":
                overdue_count += 1
                tag = "overdue"

            elif display_status == "Due Today":
                pending_count += 1
                upcoming_count += 1
                tag = "today"

            else:
                pending_count += 1
                upcoming_count += 1

            self.tree.insert(
                "",
                "end",
                iid=str(assignment_id),
                values=(
                    title,
                    subject,
                    due_date,
                    due_time,
                    display_status,
                    description
                ),
                tags=(tag,)
            )

        self.pending_label.config(
            text=str(pending_count)
        )
        self.completed_label.config(
            text=str(completed_count)
        )
        self.upcoming_label.config(
            text=str(upcoming_count)
        )
        self.overdue_label.config(
            text=str(overdue_count)
        )

    def mark_completed(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select an assignment first."
            )
            return

        assignment_id = selected[0]

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE assignments
            SET status = 'Completed'
            WHERE id = ? AND user_id = ?
            """,
            (
                assignment_id,
                self.current_user["id"]
            )
        )

        conn.commit()
        conn.close()

        self.refresh_tasks()

    def delete_assignment(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select an assignment first."
            )
            return

        if not messagebox.askyesno(
            "Delete Assignment",
            "Are you sure you want to delete this assignment?"
        ):
            return

        assignment_id = selected[0]

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            """
            DELETE FROM assignments
            WHERE id = ? AND user_id = ?
            """,
            (
                assignment_id,
                self.current_user["id"]
            )
        )

        conn.commit()
        conn.close()

        self.refresh_tasks()

    def logout(self):
        self.current_user = None
        self.show_login()

#dito na tatakbo syempre last na eh

if __name__ == "__main__":
    setup_database()

    root = tk.Tk()
    app = StudyTrackApp(root)
    root.mainloop()