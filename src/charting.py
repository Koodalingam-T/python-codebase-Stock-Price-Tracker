import customtkinter as ctk
import matplotlib.pyplot as plt

def plot_intraday_chart(ax, canvas, stock_object):
    """Fetches intraday minute tracking steps and updates the canvas coordinate map."""
    try:
        df = stock_object.history(period="1d", interval="1m")
        if df.empty:
            return

        ax.clear()
        is_dark = ctk.get_appearance_mode() == "Dark"
        bg_color = "#2b2b2b" if is_dark else "#dbdbdb"
        card_color = "#1d1e22" if is_dark else "#eaeaea"
        text_color = "white" if is_dark else "black"
        
        # Determine trend direction line color
        line_color = "#10b981" if df['Close'].iloc[-1] >= df['Close'].iloc[0] else "#ef4444"

        # Apply styles safely
        ax.get_figure().patch.set_facecolor(card_color)
        ax.set_facecolor(card_color)
        
        ax.plot(df.index, df['Close'], color=line_color, linewidth=2)
        ax.tick_params(colors=text_color, labelsize=9)
        ax.spines['bottom'].set_color(text_color)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(text_color)
        ax.grid(True, color=bg_color, linestyle="--", alpha=0.3)
        
        canvas.draw()
    except Exception as e:
        print(f"Chart engine error: {e}")
