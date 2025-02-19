import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import tkinter.font as tkFont
import _tkinter
import datetime
import os
import sys
import mysql.connector
import getpass
from tkcalendar import Calendar
from hwm_dictonary import stundenplan

# ---------------------Build-Version--------------------
build_version = "v1.5.2-dev"
APP_VERSION = build_version

# -------------------- Online-Datenbank-Verbindung (MySQL) --------------------
try:
    db = mysql.connector.connect(
        host="mc-mysql01.mc-host24.de",         # z. B. "deinserver.domain.com" oder eine IP-Adresse
        user="u4203_Mtc42FNhxN",
        password="nA6U=8ecQBe@vli@SKXN9rK9",
        database="s4203_reports"
    )
    cursor = db.cursor()
    offline_mode = False
except mysql.connector.Error as err:
    offline_mode = True

if not offline_mode:
    # Tabelle für Hausaufgaben erstellen (falls noch nicht vorhanden)
    create_table_query = """
    CREATE TABLE IF NOT EXISTS hausaufgaben (
        id INT AUTO_INCREMENT PRIMARY KEY,
        fachkuerzel VARCHAR(50),
        beschreibung TEXT,
        faellig_am DATETIME
    )
    """
    cursor.execute(create_table_query)
    db.commit()

    # Tabelle für Prüfungen erstellen (falls noch nicht vorhanden)
    create_table_query_exam = """
    CREATE TABLE IF NOT EXISTS pruefungen (
        id INT AUTO_INCREMENT PRIMARY KEY,
        fachkuerzel VARCHAR(50),
        beschreibung TEXT,
        pruefungsdatum DATETIME
    )
    """
    cursor.execute(create_table_query_exam)
    db.commit()

    # Tabelle für App-Versionen
    create_table_query_version = """
    CREATE TABLE IF NOT EXISTS app_versions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        version VARCHAR(20) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """
    # Tabelle für Benutzerinformationen
    create_table_query_user = """
    CREATE TABLE IF NOT EXISTS user_app_info (
        id INT AUTO_INCREMENT PRIMARY KEY,
        windows_username VARCHAR(100) NOT NULL,
        app_version VARCHAR(20) NOT NULL,
        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY (windows_username)
    );
    """
    cursor.execute(create_table_query_version)
    cursor.execute(create_table_query_user)
    db.commit()



def get_current_subject():
    """
    Ermittelt anhand des aktuellen Wochentags und der aktuellen Uhrzeit,
    welches Fach gerade läuft und wann die Stunde endet.
    """
    current_time = datetime.datetime.now().time()
    current_day = datetime.datetime.now().strftime('%A')
    if current_day in stundenplan:
        for start, end, subject in stundenplan[current_day]:
            start_time = datetime.datetime.strptime(start, '%H:%M').time()
            end_time = datetime.datetime.strptime(end, '%H:%M').time()
            if start_time <= current_time <= end_time:
                return subject, end_time
    return None, None

# -------------------- Haupt-GUI als Notebook --------------------
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
    os.environ['TCL_LIBRARY'] = os.path.join(sys._MEIPASS, 'tcl', 'tcl8.6')
    os.environ['TK_LIBRARY'] = os.path.join(sys._MEIPASS, 'tcl', 'tk8.6')
    if not offline_mode:
        cursor.execute("SELECT COUNT(*) FROM app_versions WHERE version = %s", (APP_VERSION,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO app_versions (version) VALUES (%s)", (APP_VERSION,))
            db.commit()
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

icon_path = os.path.join(base_path, "homework_2941554.ico")
root = tk.Tk()
root.title("Multi-Funktions Manager")
try:
    root.iconbitmap(icon_path)
except Exception as e:
    messagebox.showerror("Fehler", "Icon konnte nicht geladen werden: " + str(e))

# Versions-Check und Benutzerinfo (nur bei Onlinebetrieb)
if not offline_mode:
    cursor.execute("SELECT version FROM app_versions ORDER BY created_at DESC LIMIT 1")
    result = cursor.fetchone()
    if result:
        latest_version = result[0]
        if APP_VERSION != latest_version:
            messagebox.showinfo("Update verfügbar", "Sie verwenden eine veraltete Version der App. Bitte aktualisieren Sie auf Version " + latest_version)
    current_user = getpass.getuser()
    cursor.execute("SELECT COUNT(*) FROM user_app_info WHERE windows_username = %s", (current_user,))
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO user_app_info (windows_username, app_version) VALUES (%s, %s)", (current_user, APP_VERSION))
    else:
        cursor.execute("UPDATE user_app_info SET app_version = %s, last_updated = NOW() WHERE windows_username = %s", (APP_VERSION, current_user))
    db.commit()

# -------------------- Dynamischer Font und Layout --------------------
default_font = tkFont.Font(family="Helvetica", size=12)
root.bind("<Configure>", lambda event: default_font.configure(size=max(10, int(event.width/40))))
root.config(bg="black")

# Erstelle Notebook und Tabs
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Font für ENtryfenster

entry_font = tkFont.Font(family="Helvetica", size=20)

# Füge Buttons hinzu

def on_resize(event):
    """Passt die Schriftgröße der Tabs dynamisch an."""
    new_size = max(10, event.width // 40)  # Je nach gewünschter Skalierung
    tab_font.configure(size=new_size)
    entry_font.configure(size=new_size)
    # Optional: auch das Padding skalieren, damit die Tabs höher/breiter werden
    style.configure("TNotebook.Tab", padding=(new_size, new_size // 2))


# Style + dynamisches Font-Objekt
style = ttk.Style()
tab_font = tkFont.Font(family="Helvetica", size=20)

# Notebook-Tabs bekommen dieses Font
style.configure("TNotebook.Tab", font=tab_font)

# -------------------- Tab: Stundenplan --------------------
frame_stundenplan = tk.Frame(notebook, bg="black")
notebook.add(frame_stundenplan, text="Stundenplan")

# Beispielhafter Code zum Aktualisieren des Stundenplans
def get_current_subject():
    """
    Ermittelt anhand des aktuellen Wochentags und der aktuellen Uhrzeit,
    welches Fach gerade läuft und wann die Stunde endet.
    """
    current_time = datetime.datetime.now().time()
    current_day = datetime.datetime.now().strftime('%A')  # z. B. "Monday"
    
    if current_day in stundenplan:
        for start, end, subject in stundenplan[current_day]:
            start_time = datetime.datetime.strptime(start, '%H:%M').time()
            end_time = datetime.datetime.strptime(end, '%H:%M').time()
            if start_time <= current_time <= end_time:
                return subject, end_time
    return None, None

label_subject = tk.Label(frame_stundenplan, text="Aktuelles Fach: ", font=default_font, bg="black", fg="white")
label_subject.pack(pady=10, expand=True, fill="both")
label_subject.config(anchor="center", justify="center")
label_time = tk.Label(frame_stundenplan, text="Verbleibende Zeit: ", font=default_font, bg="black", fg="white")
label_time.pack(pady=10, expand=True, fill="both")
label_time.config(anchor="center", justify="center")

def update_stundenplan_time():
    """
    Aktualisiert in regelmäßigen Abständen (jede Sekunde) die Anzeige
    für das aktuelle Fach und die verbleibende Zeit.
    """
    subject, end_time = get_current_subject()
    if subject:
        current_time = datetime.datetime.now().time()
        remaining_time = datetime.datetime.combine(datetime.date.today(), end_time) - datetime.datetime.combine(datetime.date.today(), current_time)
        label_subject.config(text=f"Aktuelles Fach: {subject}")
        label_time.config(text=f"Verbleibende Zeit: {remaining_time}")
    else:
        label_subject.config(text="Aktuelles Fach: Nichts")
        label_time.config(text="Verbleibende Zeit: N/A")
    frame_stundenplan.after(1, update_stundenplan_time)

update_stundenplan_time()

# -------------------- Sicherheit: Nur bestimmte Nutzer dürfen Einträge erfassen --------------------
def user_can_edit_entries():
    """Prüft, ob der aktuelle Windows-Benutzer 'timow' oder 'Timo' ist, oder das Passwort 'l23a' eingibt."""
    user = getpass.getuser()
    if user.lower() in ["timow", "timo"]:
        return True  # Keine Passwortabfrage nötig
    else:
        pwd = simpledialog.askstring("Passwortabfrage", "Bitte Passwort für Einträge eingeben:", show='*')
        if pwd == "l23a":
            return True
        else:
            messagebox.showerror("Fehler", "Falsches Passwort oder Abbruch.")
            return False




# -------------------- Tab: Eintrag erfassen --------------------
frame_eintrag = tk.Frame(notebook, bg="black")


def show_entry_form(entry_type=""):
    # Leere den Tab zunächst
    for widget in frame_eintrag.winfo_children():
        widget.destroy()
    if entry_type == "":
        entry_form_label = tk.Label(frame_eintrag, text="Was möchten Sie erfassen?", font=default_font, bg="black", fg="white")
        entry_form_label.pack(pady=10, fill="both", expand=True)
        entry_form_label.config(anchor="center", justify="center")
        def choose_homework():
            show_entry_form("ha")
        def choose_exam():
            show_entry_form("pr")
        entry_form_button1 = tk.Button(frame_eintrag, text="Hausaufgaben", font=default_font, command=choose_homework)
        entry_form_button1.pack(pady=10, padx=10, fill="both", expand=True, side="right")
        entry_form_button1.config(anchor="center", justify="center")
        entry_form_button2 = tk.Button(frame_eintrag, text="Prüfungen", font=default_font, command=choose_exam)
        entry_form_button2.pack(pady=10, padx=10, fill="both", expand=True, side="left")
        entry_form_button2.config(anchor="center", justify="center")
    elif entry_type == "ha":
        tk.Label(frame_eintrag, text="Hausaufgaben erfassen", font=default_font, bg="black", fg="white").pack(pady=10, fill="both", expand=True)
        tk.Label(frame_eintrag, text="Fachkürzel:",font=entry_font, bg="black", fg="white").pack(pady=5, fill="both", expand=True)
        fach_entry = tk.Entry(frame_eintrag)
        fach_entry.pack(pady=20, padx=100, fill="both", expand=True)
        tk.Label(frame_eintrag, text="Beschreibung:",font=entry_font, bg="black", fg="white").pack(pady=5, fill="both", expand=True)
        beschreibung_entry = tk.Entry(frame_eintrag)
        beschreibung_entry.pack(pady=20, padx=100, fill="both", expand=True)
        tk.Label(frame_eintrag, text="Fällig am (YYYY-MM-DD HH:MM):", font=entry_font, bg="black", fg="white").pack(pady=5, fill="both", expand=True)
        faellig_entry = tk.Entry(frame_eintrag)
        faellig_entry.pack(pady=20, padx=100, fill="both", expand=True)
        
        def save_homework_inline():
            fach = fach_entry.get().strip()
            beschreibung = beschreibung_entry.get().strip()
            faellig = faellig_entry.get().strip()
            try:
                due_date = datetime.datetime.strptime(faellig, "%Y-%m-%d %H:%M")
            except ValueError:
                messagebox.showerror("Fehler", "Bitte geben Sie das Datum im Format YYYY-MM-DD HH:MM ein.")
                return
            try:
                insert_query = "INSERT INTO hausaufgaben (fachkuerzel, beschreibung, faellig_am) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (fach, beschreibung, due_date))
                db.commit()
                messagebox.showinfo("Erfolg", "Hausaufgabe gespeichert.")
                show_entry_form("")
            except mysql.connector.Error as err:
                messagebox.showerror("Datenbankfehler", f"Fehler: {err}")
        entry_button5 = tk.Button(frame_eintrag, text="Speichern", font=default_font, command=save_homework_inline)
        entry_button5.pack(pady=20, padx=20, fill="both", expand=True, side="left")
        entry_button5.config(anchor="center", justify="center")
        entry_button6 = tk.Button(frame_eintrag, text="Abbrechen", font=default_font, command=lambda: show_entry_form(""))
        entry_button6.pack(pady=20, padx=20, fill="both", expand=True, side="right")
        entry_button6.config(anchor="center", justify="center")
    elif entry_type == "pr":
        tk.Label(frame_eintrag, text="Prüfung erfassen", font=default_font, bg="black", fg="white").pack(pady=10, fill="both", expand=True)
        tk.Label(frame_eintrag, text="Fachkürzel:", font=entry_font, bg="black", fg="white").pack(pady=5, fill="both", expand=True)
        fach_entry = tk.Entry(frame_eintrag, font=entry_font)
        fach_entry.pack(pady=20, padx=100, fill="both", expand=True)
        tk.Label(frame_eintrag, text="Beschreibung:", font=entry_font, bg="black", fg="white").pack(pady=5, fill="both", expand=True)
        beschreibung_entry = tk.Entry(frame_eintrag, font=entry_font)
        beschreibung_entry.pack(pady=20, padx=100, fill="both", expand=True)
        tk.Label(frame_eintrag, text="Prüfungsdatum (YYYY-MM-DD HH:MM):", font=entry_font, bg="black", fg="white").pack(pady=5, fill="both", expand=True)
        datum_entry = tk.Entry(frame_eintrag, font=entry_font)
        datum_entry.pack(pady=20, padx=100, fill="both", expand=True)
        
        def save_exam_inline():
            fach = fach_entry.get().strip()
            beschreibung = beschreibung_entry.get().strip()
            datum = datum_entry.get().strip()
            try:
                pruefungsdatum = datetime.datetime.strptime(datum, "%Y-%m-%d %H:%M")
            except ValueError:
                messagebox.showerror("Fehler", "Bitte geben Sie das Datum im Format YYYY-MM-DD HH:MM ein.")
                return
            try:
                insert_query = "INSERT INTO pruefungen (fachkuerzel, beschreibung, pruefungsdatum) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (fach, beschreibung, pruefungsdatum))
                db.commit()
                messagebox.showinfo("Erfolg", "Prüfung gespeichert.")
                show_entry_form("")
            except mysql.connector.Error as err:
                messagebox.showerror("Datenbankfehler", f"Fehler: {err}")
        entry_button3 =tk.Button(frame_eintrag, text="Speichern", font=default_font, command=save_exam_inline)
        entry_button3.pack(pady=20, padx=20, fill="both", expand=True, side="left")
        entry_button3.config(anchor="center", justify="center")
        entry_button4 = tk.Button(frame_eintrag, text="Abbrechen", font=default_font, command=lambda: show_entry_form(""))
        entry_button4.pack(pady=20, padx=20, fill="both", expand=True, side="right")
        entry_button4.config(anchor="center", justify="center")

# In diesem Tab starten wir mit der Auswahl
show_entry_form()






# -------------------- TAB: Hausaufgaben anzeigen (für alle Nutzer) --------------------
frame_hausaufgaben = tk.Frame(notebook, bg="black")
notebook.add(frame_hausaufgaben, text="Hausaufgaben")

def load_homework():
    # Falls offline_mode: abbrechen
    if offline_mode:
        messagebox.showerror("Fehler", "Im Offline-Modus nicht verfügbar.")
        return
    for w in frame_hausaufgaben.winfo_children():
        w.destroy()
    tk.Label(frame_hausaufgaben, text="Hausaufgaben Übersicht", font=default_font, bg="black", fg="white").pack(pady=10)

    text_box = tk.Text(frame_hausaufgaben, width=80, height=20)
    text_box.pack(padx=10, pady=10)
    try:
        cursor.execute("SELECT id, fachkuerzel, beschreibung, faellig_am FROM hausaufgaben")
        rows = cursor.fetchall()
        if not rows:
            text_box.insert(tk.END, "Keine Hausaufgaben vorhanden.")
        else:
            for r in rows:
                id_, fach, beschreibung, faellig_am = r
                text_box.insert(tk.END, f"ID: {id_}\nFach: {fach}\nBeschreibung: {beschreibung}\nFällig am: {faellig_am}\n\n")
        text_box.config(state=tk.DISABLED)
    except mysql.connector.Error as err:
        messagebox.showerror("Datenbankfehler", f"Fehler: {err}")

tk.Button(frame_hausaufgaben, text="Aktualisieren", font=default_font, command=load_homework).pack(pady=10)
load_homework()

# Fügen wir das Tab nur hinzu, wenn der Nutzer berechtigt ist
if user_can_edit_entries():
    notebook.add(frame_eintrag, text="Eintrag erfassen")
    show_entry_form()

# -------------------- Sicherheit: Nur bestimmte Nutzer dürfen die SQL-Konsole öffnen --------------------
def user_can_use_sql():
    """Prüft, ob der aktuelle Windows-Benutzer 'timow'/'Timo' ist oder das Passwort 'l23a-admin' eingibt."""
    user = getpass.getuser()
    # timow/Timo => kein Passwort
    if user.lower() in ["timow", "timo"]:
        return True
    else:
        pwd = simpledialog.askstring("Passwortabfrage", "Bitte Passwort für die SQL-Konsole eingeben:", show='*')
        if pwd == "l23a-admin":
            return True
        else:
            messagebox.showerror("Fehler", "Falsches Passwort oder Abbruch.")
            return False
        



# -------------------- TAB: SQL-Konsole (NUR für Berechtigte) --------------------
frame_sql = tk.Frame(notebook, bg="black")

def build_sql_tab():
    for w in frame_sql.winfo_children():
        w.destroy()

    tk.Label(frame_sql, text="SQL Konsole", font=default_font, bg="black", fg="white").pack(pady=10)
    tk.Label(frame_sql, text="Geben Sie Ihren SQL-Befehl ein:", bg="black", fg="white").pack(pady=5)

    sql_entry = tk.Text(frame_sql, height=4, width=80)
    sql_entry.pack(padx=10, pady=5)

    result_text = tk.Text(frame_sql, height=20, width=80)
    result_text.pack(padx=10, pady=5)
    result_text.config(state=tk.DISABLED)

    def execute_sql():
        if offline_mode:
            messagebox.showerror("Fehler", "Im Offline-Modus nicht verfügbar.")
            return
        command = sql_entry.get("1.0", tk.END).strip()
        if not command:
            messagebox.showerror("Fehler", "Bitte geben Sie einen SQL-Befehl ein.")
            return
        try:
            cursor.execute(command)
            if command.strip().lower().startswith("select"):
                rows = cursor.fetchall()
                output = "\n".join(str(r) for r in rows)
            else:
                db.commit()
                output = "Befehl erfolgreich ausgeführt."
            result_text.config(state=tk.NORMAL)
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, output)
            result_text.config(state=tk.DISABLED)
        except mysql.connector.Error as err:
            messagebox.showerror("SQL Fehler", f"Fehler beim Ausführen des Befehls: {err}")

    tk.Button(frame_sql, text="Ausführen", font=default_font, command=execute_sql).pack(pady=5)

if user_can_use_sql():
    notebook.add(frame_sql, text="SQL Konsole")
    build_sql_tab()
    
# -------------------- TAB: Kalender (für alle Nutzer, ggf. offline-Check) --------------------
frame_kalender = tk.Frame(notebook, bg="black")
notebook.add(frame_kalender, text="Kalender")

def build_calendar_tab():
    for w in frame_kalender.winfo_children():
        w.destroy()
    if offline_mode:
        tk.Label(frame_kalender, text="Kalender offline nicht verfügbar", bg="black", fg="white", font=default_font)\
            .pack(pady=20)
        return

    cal = Calendar(frame_kalender, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(padx=10, pady=10, fill='both', expand=True)
    cal.tag_config('homework', background='lightblue')
    cal.tag_config('exam', background='lightgreen')

    def on_date_selected(event):
        selected_date_str = cal.get_date()
        try:
            selected_date = datetime.datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Konvertieren des Datums: {e}")
            return
        event_ids = cal.get_calevents(selected_date)
        details = ""
        for eid in event_ids:
            try:
                text_val = cal.calevent_cget(eid, "text")
                details += text_val + "\n\n"
            except Exception as ex:
                details += f"Fehler bei Event {eid}: {ex}\n"
        if details:
            messagebox.showinfo(f"Einträge vom {selected_date_str}", details)
        else:
            messagebox.showinfo("Einträge", "Keine Einträge für dieses Datum.")

    cal.bind("<<CalendarSelected>>", on_date_selected)

    # Hausaufgaben
    try:
        cursor.execute("SELECT fachkuerzel, beschreibung, faellig_am FROM hausaufgaben")
        rows = cursor.fetchall()
        for r in rows:
            fach, beschreibung, faellig_am = r
            if isinstance(faellig_am, datetime.datetime):
                date_obj = faellig_am.date()
            else:
                try:
                    date_obj = datetime.datetime.strptime(faellig_am, "%Y-%m-%d").date()
                except:
                    continue
            cal.calevent_create(date_obj, f"Hausaufgabe: {fach}\n{beschreibung}", tags='homework')
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Laden der Hausaufgaben: {e}")

    # Prüfungen
    try:
        cursor.execute("SELECT fachkuerzel, beschreibung, pruefungsdatum FROM pruefungen")
        rows = cursor.fetchall()
        for r in rows:
            fach, beschreibung, pruefungsdatum = r
            if isinstance(pruefungsdatum, datetime.datetime):
                date_obj = pruefungsdatum.date()
            else:
                try:
                    date_obj = datetime.datetime.strptime(pruefungsdatum, "%Y-%m-%d").date()
                except:
                    continue
            cal.calevent_create(date_obj, f"Prüfung: {fach}\n{beschreibung}", tags='exam')
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Laden der Prüfungen: {e}")

    # Legende
    legend = tk.Frame(frame_kalender, bg="black")
    legend.pack(pady=10)
    tk.Label(legend, text="Hausaufgaben", bg="lightblue", font=entry_font).pack(side=tk.LEFT, padx=10)
    tk.Label(legend, text="Prüfungen", bg="lightgreen", font=entry_font).pack(side=tk.LEFT, padx=10)

build_calendar_tab()

# -------------------- TAB: Neue Funktion (für alle) --------------------
frame_neue_funktion = tk.Frame(notebook, bg="black")
notebook.add(frame_neue_funktion, text="Neue Funktion")
tk.Label(frame_neue_funktion, text="Neue Funktion", font=default_font, bg="black", fg="white").pack(pady=10)
tk.Button(frame_neue_funktion, text="Noch nicht implementiert", font=default_font,
          command=lambda: messagebox.showinfo("Neue Funktion", "Diese Funktion ist noch nicht implementiert."))\
    .pack(pady=10)

# -------------------- Offline Checks --------------------
def offline_check(func):
    def wrapper():
        if offline_mode:
            messagebox.showerror("Fehler", "Diese Funktion ist im Offline-Mode nicht verfügbar!")
        else:
            func()
    return wrapper

# Beispielweise könntest du für bestimmte Tabs (z. B. Kalender, SQL) bei Bedarf noch einen Button einbauen,
# der vor dem Aufruf offline_check prüft – im obigen Beispiel geschieht das aber bereits beim DB-Zugriff.

# -------------------- Hauptmenü-Footer --------------------
footer = tk.Label(root, text="©️ Timo Wigger    Build Version: " + build_version, bg="black", fg="white", font=default_font)
footer.pack(side=tk.BOTTOM, fill="x")

# -------------------- Mainloop --------------------
# Fenster direkt maximiert starten
root.state("zoomed")
root.mainloop()

if not offline_mode:
    cursor.close()
    db.close()
    
# Powershell command: pyinstaller --onefile --add-binary "C:\Users\timow\AppData\Local\Programs\Python\Python312\tcl\tcl8.6;./tcl/tcl8.6" --add-binary "C:\Users\timow\AppData\Local\Programs\Python\Python312\tcl\tk8.6;./tcl/tk8.6" --hidden-import=tkcalendar --hidden-import=tkcalendar.widgets --hidden-import babel.numbers --icon="C:\Users\timow\OneDrive\Documents\Python Files\homework_2941554.ico" --add-data "C:\Users\timow\OneDrive\Documents\Python Files\homework_2941554.ico;." Homework-Manager-v1.5.1-dev.pyw
