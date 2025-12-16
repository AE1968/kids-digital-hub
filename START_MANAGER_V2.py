import tkinter as tk
from tkinter import ttk
import webbrowser
import os
import requests
import threading

# =========================================================
# 🎮 KIDS DIGITAL HUB - MANAGER V2 (DASHBOARD)
# =========================================================

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Administrare Site - Kids Digital Hub")
        self.geometry("400x650")
        self.configure(bg="#f0f2f5")
        self.resizable(False, False)

        # Style Configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Segoe UI', 11, 'bold'), borderwidth=0, background="#FFF")
        
        # --- HEADER (Blue Area) ---
        header = tk.Frame(self, bg="#4a4eff", height=140)
        header.pack(fill='x')
        
        lbl_icon = tk.Label(header, text="🤖", bg="#4a4eff", fg="white", font=("Segoe UI", 24))
        lbl_icon.pack(pady=(15, 0))
        
        lbl_title = tk.Label(header, text="Panou Principal", bg="#4a4eff", fg="white", font=("Segoe UI", 16, "bold"))
        lbl_title.pack()

        # LIVE STATS BADGE
        self.lbl_stats = tk.Label(header, text="⏳ Se încarcă datele...", bg="#3d3fb5", fg="#aeb0ff", font=("Segoe UI", 10))
        self.lbl_stats.pack(pady=5, ipadx=10, ipady=2)
        
        # Start fetch thread
        threading.Thread(target=self.fetch_stats, daemon=True).start()

        # --- MENU AREA ---
        menu_frame = tk.Frame(self, bg="#f0f2f5")
        menu_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Button 1
        self.create_btn(menu_frame, "1. COMANDĂ PRODUSE NOI", "#FFF176", "black", self.action_new_products)
        
        # Status Label
        lbl_status = tk.Label(menu_frame, text="✅ Site Sincronizat Complet", bg="#f0f2f5", fg="#2e7d32", font=("Segoe UI", 9))
        lbl_status.pack(pady=5)

        # Button 2
        self.create_btn(menu_frame, "2. PREGĂTIRE PRODUS (Manual)", "#FFF176", "black", self.action_prep)

        # Separator
        tk.Frame(menu_frame, height=20, bg="#f0f2f5").pack()

        # Button 3
        self.create_btn(menu_frame, "3. MERGI LA SITE (LOCAL)", "#FFF176", "black", self.action_local)

        # Button 4
        self.create_btn(menu_frame, "4. MERGI LA SITE (ONLINE)", "#FFF176", "black", self.action_online)

        # Separator
        tk.Frame(menu_frame, height=20, bg="#f0f2f5").pack()

        # Button 5 (NEW)
        self.create_btn(menu_frame, "5. 📊 VEZI DATE & STATISTICI", "#FF7043", "white", self.action_stats)


        # Footer
        btn_drawer = tk.Button(self, text="⊞ SERTAR: Produse Noi", bg="#263238", fg="white", font=("Segoe UI", 10), bd=0, pady=10)
        btn_drawer.pack(fill='x', side='bottom')

    def create_btn(self, parent, text, bg, fg, command):
        btn = tk.Button(parent, text=text, bg=bg, fg=fg, font=("Segoe UI", 11, "bold"), bd=1, relief="solid", activebackground="#fff9c4", cursor="hand2", command=command)
        btn.pack(fill='x', pady=8, ipady=5)

    # --- ACTIONS ---

    def fetch_stats(self):
        try:
            # Fetch from CounterAPI
            r = requests.get("https://api.counterapi.dev/v1/kidsdigitalhub/view")
            data = r.json()
            count = data.get('count', 0)
            
            def update_ui():
                self.lbl_stats.config(text=f"🌍 Vizitatori Total: {count}", fg="white")
            
            self.after(0, update_ui)
        except Exception as e:
            print(e)
            self.lbl_stats.config(text="⚠️ Offline / Eroare Statistici")

    def action_new_products(self):
        print("Comanda pornita...")
        # Future hook for Python cloud script
        
    def action_prep(self):
        print("Pregatire...")

    def action_local(self):
        webbrowser.open(os.path.abspath("index.html"))

    def action_online(self):
        webbrowser.open("https://kidsdigitalhub.com")

    def action_stats(self):
        # Opens the Admin Panel where we put the stats card
        webbrowser.open(os.path.abspath("admin_messages.html"))

if __name__ == "__main__":
    app = App()
    app.mainloop()
