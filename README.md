# 📊 MarketPulse Tracker & Charting App

A modern, real-time desktop dashboard application built with Python to track National Stock Exchange (NSE) asset prices and intra-day trends effortlessly. This application avoids security scraping blocks by communicating directly with the Yahoo Finance engine.

## ✨ Key Features
- 🔄 **Auto-Refresh Loop**: Automatically fetches fresh market values every 5 seconds without UI freezing.
- 📈 **Dynamic Live Charts**: Plots minute-by-minute charts mapping today's performance from market opening until right now.
- 🎨 **Adaptive Themes**: Beautiful UI panels with rounded corners that dynamically adapt to your operating system's light or dark mode setting.
- 🛑 **Memory Leak Protection**: Safe shutdown triggers to cancel background loops and release active graphing plots instantly on close.

## 🛠️ Installation & Setup

1. **Clone or Download the Project Repository:**
   ```bash
   git clone https://github.com
   cd python-codebase-Stock-Price-Tracker
   ```

2. **Install Required Packages:**
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   Execute the core application layer file:
   ```bash
   python src/app.py
   ```

## 💡 How to Use
1. Type any active NSE ticker symbol inside the input field box (e.g., `WIPRO`, `TCS`, `TATAMOTORS`).
2. Click **Track Asset**. 
3. The dashboard will instantly pull core metadata, load the business summary, map a green or red trend chart, and begin auto-refreshing its parameters.

