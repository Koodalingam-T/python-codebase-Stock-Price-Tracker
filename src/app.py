import sys
import os
# Ensure app can find charting module locally inside src folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from tkinter import messagebox
import yfinance as yf
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from charting import plot_intraday_chart

ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue") 

class ModernStockApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MarketPulse Tracker & Charting")
        self.geometry("520x780") 
        self.resizable(False, False)
        
        self.refresh_job = None
        self.refresh_interval = 5000  

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # UI Core Layout Setup
        self.title_label = ctk.CTkLabel(self, text="📊 MarketPulse Analytics", font=ctk.CTkFont(family="Helvetica", size=22, weight="bold"))
        self.title_label.pack(pady=(20, 5))
        
        self.subtitle_label = ctk.CTkLabel(self, text="Real-time NSE Market Dashboard & Trends", font=ctk.CTkFont(family="Helvetica", size=12), text_color="#64748b")
        self.subtitle_label.pack(pady=(0, 15))

        # Input Row
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(pady=5, padx=30, fill="x")

        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Enter NSE Ticker", height=45, font=ctk.CTkFont(size=14), justify="center")
        self.entry.pack(side="left", expand=True, fill="x", padx=(0, 10))
        self.entry.insert(0, "WIPRO") 

        self.search_btn = ctk.CTkButton(self.input_frame, text="Track Asset", height=45, font=ctk.CTkFont(weight="bold"), command=self.start_tracking)
        self.search_btn.pack(side="right")

        # Metadata Card
        self.display_card = ctk.CTkFrame(self, corner_radius=12)
        self.display_card.pack(pady=10, padx=30, fill="x")

        self.name_label = ctk.CTkLabel(self.display_card, text="Company Name", font=ctk.CTkFont(size=16, weight="bold"), text_color="#3b82f6")
        self.name_label.pack(pady=(15, 2), padx=20, anchor="w")

        self.price_label = ctk.CTkLabel(self.display_card, text="₹ 0.00", font=ctk.CTkFont(size=28, weight="bold"))
        self.price_label.pack(pady=2, padx=20, anchor="w")

        self.sector_label = ctk.CTkLabel(self.display_card, text="Sector: --  |  Industry: --", font=ctk.CTkFont(size=12), text_color="#94a3b8")
        self.sector_label.pack(pady=(2, 15), padx=20, anchor="w")

        # Chart Container Card
        self.chart_card = ctk.CTkFrame(self, corner_radius=12)
        self.chart_card.pack(pady=10, padx=30, fill="both", expand=True)
        
        self.chart_title = ctk.CTkLabel(self.chart_card, text="📈 Today's Price Movement (Intraday)", font=ctk.CTkFont(size=13, weight="bold"))
        self.chart_title.pack(pady=(10, 0))

        self.fig, self.ax = plt.subplots(figsize=(5, 2.5), tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_card)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(5, 10))

        # Bottom Summary Card
        self.summary_box = ctk.CTkTextbox(self, font=ctk.CTkFont(size=11), height=100, corner_radius=12)
        self.summary_box.pack(pady=10, padx=30, fill="x")
        self.summary_box.insert("0.0", "Search for an active public asset to display summary insights...")
        self.summary_box.configure(state="disabled")

        self.status_label = ctk.CTkLabel(self, text="● Standing by.", font=ctk.CTkFont(size=11), text_color="#64748b")
        self.status_label.pack(pady=(0, 10))

        self.start_tracking()

    def start_tracking(self):
        if self.refresh_job:
            self.after_cancel(self.refresh_job)
            self.refresh_job = None
        self.fetch_stock_data_loop()

    def fetch_stock_data_loop(self):
        symbol = self.entry.get().strip().upper()
        if not symbol:
            return

        if not symbol.endswith(".NS") and not symbol.endswith(".BO"):
            symbol = f"{symbol}.NS"

        try:
            ticker = yf.Ticker(symbol)
            info = ticker.fast_info
            meta = ticker.info

            company_name = meta.get('longName', symbol)
            last_price = info['last_price']
            currency = "₹" if info['currency'] == "INR" else info['currency']
            sector = meta.get('sector', 'N/A')
            industry = meta.get('industry', 'N/A')
            summary = meta.get('longBusinessSummary', 'No description available.')

            self.name_label.configure(text=f"🏢 {company_name}")
            self.price_label.configure(text=f"{currency} {last_price:,.2f}")
            self.sector_label.configure(text=f"📂 Sector: {sector}  |  🏭 Industry: {industry}")

            self.summary_box.configure(state="normal")
            self.summary_box.delete("0.0", "end")
            self.summary_box.insert("0.0", f"📝 Summary: {summary}")
            self.summary_box.configure(state="disabled")

            # Call chart update from modular script file smoothly
            plot_intraday_chart(self.ax, self.canvas, ticker)

            timestamp = datetime.now().strftime("%H:%M:%S")
            self.status_label.configure(text=f"● Live tracking active. Last updated at {timestamp}", text_color="#10b981")

        except Exception:
            self.status_label.configure(text="● Connection Error. Retrying...", text_color="#ef4444")

        self.refresh_job = self.after(self.refresh_interval, self.fetch_stock_data_loop)

    def on_closing(self):
        """Safely shuts down CustomTkinter internal timers and closes the app."""
        # 1. Turn off our custom background stock update loop
        if self.refresh_job:
            self.after_cancel(self.refresh_job)
            self.refresh_job = None
        
        # 2. Close open matplotlib chart windows to free up memory
        plt.close('all') 
        
        # 3. Hide the window from the screen immediately so the app feels fast
        self.withdraw()
        
        # 4. CRITICAL FIX: Tell the app to clear out any leftover CustomTkinter 
        # background animation or scaling tasks before completely destroying itself.
        self.update_idletasks()
        
        # 5. Cleanly close the app engine once everything is idle
        self.destroy()


if __name__ == "__main__":
    app = ModernStockApp()
    app.mainloop()
