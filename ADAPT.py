import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import random
import time
import math
import datetime
import threading
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class PilotProSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("ADAPT-X PRO: Analytics & History Edition")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2c3e50")

        # Database Setup
        self.conn = sqlite3.connect("pilot_scores.db")
        self.create_tables()

        # State
        self.difficulty = tk.StringVar(value="medium")
        self.current_after_id = None
        
        self.show_main_menu()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                module TEXT,
                score INTEGER,
                total INTEGER,
                difficulty TEXT
            )
        ''')
        self.conn.commit()

    def save_result(self, module, score, total):
        cursor = self.conn.cursor()
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute("INSERT INTO results (date, module, score, total, difficulty) VALUES (?, ?, ?, ?, ?)",
                       (date_str, module, score, total, self.difficulty.get()))
        self.conn.commit()
        # Don't show popup here, allow seamless flow

    def clear_screen(self):
        if self.current_after_id:
            self.root.after_cancel(self.current_after_id)
            self.current_after_id = None
        for widget in self.root.winfo_children():
            widget.destroy()

    # =========================================
    # MAIN MENU
    # =========================================
    def show_main_menu(self):
        self.clear_screen()
        
        # Header
        header = tk.Frame(self.root, bg="#34495e", height=100)
        header.pack(fill=tk.X)
        tk.Label(header, text="PILOT RECRUITMENT SYSTEM", font=("Helvetica", 24, "bold"), fg="#ecf0f1", bg="#34495e").pack(pady=30)

        # Dashboard Grid
        dash = tk.Frame(self.root, bg="#2c3e50")
        dash.pack(pady=20)

        # Left Column: Tests
        frame_tests = tk.LabelFrame(dash, text=" Active Assessment ", font=("Arial", 12, "bold"), bg="#2c3e50", fg="white")
        frame_tests.grid(row=0, column=0, padx=20, pady=20, sticky="n")
        
        modes = [("Cadet (Easy)", "easy"), ("Officer (Medium)", "medium"), ("Captain (Hard)", "hard")]
        for text, mode in modes:
            tk.Radiobutton(frame_tests, text=text, variable=self.difficulty, value=mode, 
                           bg="#2c3e50", fg="white", selectcolor="#2c3e50").pack(anchor="w", padx=10, pady=2)

        tk.Button(frame_tests, text="START GENERAL KNOWLEDGE", command=self.start_live_quiz, width=25, bg="#3498db", fg="white").pack(pady=10)
        tk.Button(frame_tests, text="START SPATIAL ORIENTATION", command=self.run_spatial, width=25, bg="#3498db", fg="white").pack(pady=10)

        # Right Column: Analytics
        frame_data = tk.LabelFrame(dash, text=" Career Analytics ", font=("Arial", 12, "bold"), bg="#2c3e50", fg="white")
        frame_data.grid(row=0, column=1, padx=20, pady=20, sticky="n")

        tk.Button(frame_data, text="VIEW PROGRESS GRAPH", command=self.show_progress_graph, width=25, bg="#9b59b6", fg="white").pack(pady=10)
        tk.Button(frame_data, text="GLOBAL COMPARISON", command=self.show_global_comparison, width=25, bg="#e67e22", fg="white").pack(pady=10)
        tk.Button(frame_data, text="RESET HISTORY", command=self.reset_db, width=25, bg="#e74c3c", fg="white").pack(pady=10)

    # =========================================
    # ANALYTICS: PROGRESS GRAPH
    # =========================================
    def show_progress_graph(self):
        self.clear_screen()
        tk.Button(self.root, text="< Back to Dashboard", command=self.show_main_menu).pack(anchor="w", padx=10, pady=10)
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT date, score, total, module FROM results ORDER BY id ASC")
        data = cursor.fetchall()
        
        if not data:
            tk.Label(self.root, text="No Data Available. Complete a test first.", font=("Arial", 16), fg="white", bg="#2c3e50").pack(pady=50)
            return

        # Prepare Data
        dates = []
        percentages = []
        
        for row in data:
            # row = (date, score, total, module)
            d = row[0].split(" ")[0] # Just get the YYYY-MM-DD
            pct = (row[1] / row[2]) * 100 if row[2] > 0 else 0
            dates.append(d)
            percentages.append(pct)

        # Plotting
        fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
        ax.plot(percentages, marker='o', linestyle='-', color='#3498db', linewidth=2)
        ax.set_title("Performance History (All Modules)")
        ax.set_ylabel("Score (%)")
        ax.set_xlabel("Test Attempts")
        ax.set_ylim(0, 105)
        ax.grid(True, linestyle='--', alpha=0.6)

        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

    # =========================================
    # ANALYTICS: GLOBAL COMPARISON (Bell Curve)
    # =========================================
    def show_global_comparison(self):
        self.clear_screen()
        tk.Button(self.root, text="< Back to Dashboard", command=self.show_main_menu).pack(anchor="w", padx=10, pady=10)
        
        # 1. Get User Average
        cursor = self.conn.cursor()
        cursor.execute("SELECT score, total FROM results")
        data = cursor.fetchall()
        
        if not data:
            tk.Label(self.root, text="No Data Available.", fg="white", bg="#2c3e50").pack()
            return

        user_avgs = [(s/t)*100 for s, t in data if t > 0]
        user_mean = sum(user_avgs) / len(user_avgs)

        # 2. Generate "Global" Data (Simulated Normal Distribution)
        # Mean = 65%, Std Dev = 15%
        mu, sigma = 65, 15
        x = np.linspace(0, 100, 200)
        y = (1/(sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma)**2)

        # 3. Plot
        fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
        
        # Draw the Bell Curve
        ax.plot(x, y, color='gray', label='Global Population')
        ax.fill_between(x, y, color='gray', alpha=0.2)
        
        # Draw User Line
        ax.axvline(user_mean, color='#e74c3c', linestyle='dashed', linewidth=2, label=f'You ({user_mean:.1f}%)')
        
        # Labels
        ax.set_title("Your Aptitude vs. Global Candidate Pool")
        ax.set_xlabel("Score Percentage")
        ax.set_yticks([]) # Hide Y axis numbers (irrelevant for density)
        ax.legend()
        
        # Interpretation
        percentile = 0
        if user_mean > 65: percentile = "Above Average"
        elif user_mean < 65: percentile = "Below Average"
        else: percentile = "Average"
        
        ax.text(5, max(y)*0.8, f"Rating: {percentile}", fontsize=12, color='#e74c3c')

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

    # =========================================
    # MODULE: LIVE KNOWLEDGE
    # =========================================
    def start_live_quiz(self):
        self.clear_screen()
        tk.Label(self.root, text="Fetching Live Data...", font=("Arial", 18), fg="white", bg="#2c3e50").pack(pady=50)
        threading.Thread(target=self.load_quiz_data).start()
        
    def load_quiz_data(self):
        diff = self.difficulty.get()
        url = f"https://opentdb.com/api.php?amount=5&category=17&difficulty={diff}&type=multiple" # Category 17 = Science
        try:
            r = requests.get(url)
            data = r.json()
            if data['response_code'] == 0:
                import html
                self.q_data = []
                for item in data['results']:
                    q = html.unescape(item['question'])
                    c = html.unescape(item['correct_answer'])
                    w = [html.unescape(x) for x in item['incorrect_answers']]
                    self.q_data.append({'q': q, 'correct': c, 'wrong': w})
                self.root.after(0, self.run_quiz)
            else:
                self.root.after(0, lambda: messagebox.showerror("Error", "API Error. Try again."))
                self.root.after(0, self.show_main_menu)
        except:
            self.root.after(0, lambda: messagebox.showerror("Error", "Connection Failed."))
            self.root.after(0, self.show_main_menu)

    def run_quiz(self):
        self.q_index = 0
        self.q_score = 0
        self.show_quiz_q()

    def show_quiz_q(self):
        self.clear_screen()
        if self.q_index >= len(self.q_data):
            self.save_result("General Knowledge", self.q_score, len(self.q_data))
            messagebox.showinfo("Result", f"Score: {self.q_score}/{len(self.q_data)}")
            self.show_main_menu()
            return

        q = self.q_data[self.q_index]
        tk.Label(self.root, text=f"Q{self.q_index+1}: {q['q']}", font=("Arial", 14), fg="white", bg="#2c3e50", wraplength=800).pack(pady=30)
        
        opts = q['wrong'] + [q['correct']]
        random.shuffle(opts)
        
        for opt in opts:
            tk.Button(self.root, text=opt, command=lambda x=opt: self.check_quiz(x, q['correct']), 
                      font=("Arial", 12), width=50, bg="#ecf0f1").pack(pady=5)

    def check_quiz(self, ans, correct):
        if ans == correct: self.q_score += 1
        self.q_index += 1
        self.show_quiz_q()

    # =========================================
    # MODULE: SPATIAL (Simplified for brevity)
    # =========================================
    def run_spatial(self):
        # Using a simplified version of previous logic to fit into one file
        self.clear_screen()
        self.s_score = 0
        self.s_count = 0
        self.s_max = 5
        self.next_spatial()

    def next_spatial(self):
        if self.s_count >= self.s_max:
            self.save_result("Spatial Orientation", self.s_score, self.s_max)
            messagebox.showinfo("Result", f"Score: {self.s_score}/{self.s_max}")
            self.show_main_menu()
            return

        self.clear_screen()
        # Draw instrument logic (abbreviated)
        tk.Label(self.root, text="SPATIAL: Is the plane Climbing or Descending?", font=("Arial", 16), fg="white", bg="#2c3e50").pack(pady=10)
        
        cv = tk.Canvas(self.root, width=300, height=300, bg="#333")
        cv.pack(pady=10)
        
        is_climb = random.choice([True, False])
        self.current_ans = "Climb" if is_climb else "Descent"
        
        # Simple Visual: Blue top = climb, Brown top = descent
        fill_col = "#4da6ff" if is_climb else "#8b5a2b" # Sky vs Ground dominant
        cv.create_rectangle(0, 0, 300, 300, fill=fill_col)
        cv.create_line(100, 150, 200, 150, width=5, fill="orange") # Wings

        tk.Button(self.root, text="Climb", command=lambda: self.check_spatial("Climb"), width=20, height=2).pack(pady=5)
        tk.Button(self.root, text="Descent", command=lambda: self.check_spatial("Descent"), width=20, height=2).pack(pady=5)

    def check_spatial(self, ans):
        if ans == self.current_ans: self.s_score += 1
        self.s_count += 1
        self.next_spatial()

    def reset_db(self):
        if messagebox.askyesno("Reset", "Delete all history?"):
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM results")
            self.conn.commit()
            messagebox.showinfo("Done", "History Cleared.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PilotProSystem(root)
    root.mainloop()