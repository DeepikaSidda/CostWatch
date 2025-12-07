"""Widget UI for AWS Cost Widget - Premium AWS Cloud Clubs Edition."""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable

from config import WidgetConfig
from cost_fetcher import CostData, format_currency


# ═══════════════════════════════════════════════════════════════════════════════
# 🟣 AWS CLOUD CLUBS PREMIUM PURPLE THEME
# ═══════════════════════════════════════════════════════════════════════════════

# Status colors
COLOR_GREEN = "#10B981"      # Emerald - under budget
COLOR_YELLOW = "#FBBF24"     # Gold - warning
COLOR_RED = "#EF4444"        # Red - over budget

# Premium Purple Gradient Theme (AWS Cloud Clubs inspired)
COLOR_BG_DEEP = "#0D0221"        # Deep space purple (darkest)
COLOR_BG_PRIMARY = "#1A0A2E"     # Rich purple black
COLOR_BG_SECONDARY = "#2D1B4E"   # Royal purple
COLOR_BG_CARD = "#3D2066"        # Vibrant purple card
COLOR_BG_CARD_GLOW = "#4A2878"   # Card hover/glow

# Purple accent spectrum
COLOR_PURPLE_DARK = "#7C3AED"    # Violet
COLOR_PURPLE_MAIN = "#8B5CF6"    # Primary purple
COLOR_PURPLE_LIGHT = "#A78BFA"   # Light purple
COLOR_PURPLE_GLOW = "#C4B5FD"    # Soft glow purple

# Complementary accents
COLOR_PINK = "#EC4899"           # Hot pink accent
COLOR_CYAN = "#22D3EE"           # Cyan for contrast
COLOR_GOLD = "#F59E0B"           # Gold for premium feel

# Text colors
COLOR_FG = "#FAFAFA"             # Pure white
COLOR_FG_SECONDARY = "#C4B5FD"   # Soft purple text
COLOR_FG_MUTED = "#9CA3AF"       # Muted gray

# UI elements
COLOR_PROGRESS_BG = "#2D1B4E"
COLOR_BORDER_GLOW = "#8B5CF6"
COLOR_BORDER_OUTER = "#7C3AED"


def get_budget_color(percentage: float) -> str:
    """Return color based on budget consumption percentage."""
    if percentage < 75:
        return COLOR_GREEN
    elif percentage <= 90:
        return COLOR_YELLOW
    else:
        return COLOR_RED


def clamp_position(x: int, y: int, widget_width: int, widget_height: int,
                   screen_width: int, screen_height: int) -> tuple:
    """Clamp widget position to stay within screen boundaries."""
    clamped_x = max(0, min(x, screen_width - widget_width))
    clamped_y = max(0, min(y, screen_height - widget_height))
    return clamped_x, clamped_y


class AWSCostWidget:
    """Premium AWS Cost Widget with Cloud Clubs Purple Theme."""
    
    def __init__(self, config: WidgetConfig):
        self.config = config
        self.root = tk.Tk()
        self.root.title("AWS Cost Widget")
        
        # Window configuration
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg=COLOR_BG_DEEP)
        
        # Premium transparency
        try:
            self.root.attributes('-alpha', 0.96)
        except:
            pass
        
        # Widget dimensions
        self.width = 320
        self.height = 520
        
        # Position in bottom-right corner
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - self.width - 30
        y = screen_height - self.height - 80
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        
        # Drag state
        self._drag_start_x = 0
        self._drag_start_y = 0
        
        # Build premium UI
        self._create_premium_widgets()
        
        # Bind drag to header only
        self.header_frame.bind('<Button-1>', self.start_drag)
        self.header_frame.bind('<B1-Motion>', self.do_drag)
    
    def _create_premium_widgets(self):
        """Create premium glassmorphism UI with purple theme."""
        
        # ═══ OUTER GLOW BORDER ═══
        outer_glow = tk.Frame(self.root, bg=COLOR_BORDER_OUTER, padx=2, pady=2)
        outer_glow.pack(fill=tk.BOTH, expand=True)
        
        inner_glow = tk.Frame(outer_glow, bg=COLOR_BORDER_GLOW, padx=1, pady=1)
        inner_glow.pack(fill=tk.BOTH, expand=True)
        
        main_container = tk.Frame(inner_glow, bg=COLOR_BG_PRIMARY)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        self.main_frame = tk.Frame(main_container, bg=COLOR_BG_PRIMARY, padx=16, pady=14)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ═══ PREMIUM HEADER ═══
        self.header_frame = tk.Frame(self.main_frame, bg=COLOR_BG_PRIMARY, cursor="fleur")
        self.header_frame.pack(fill=tk.X, pady=(0, 8))
        
        # Animated purple orb indicator
        self.orb_canvas = tk.Canvas(
            self.header_frame, width=14, height=14,
            bg=COLOR_BG_PRIMARY, highlightthickness=0
        )
        self.orb_canvas.pack(side=tk.LEFT, padx=(0, 10))
        self._draw_premium_orb()
        
        # Two-tone title
        title_frame = tk.Frame(self.header_frame, bg=COLOR_BG_PRIMARY)
        title_frame.pack(side=tk.LEFT)
        
        aws_label = tk.Label(
            title_frame, text="AWS",
            font=("Helvetica", 17, "bold"),
            bg=COLOR_BG_PRIMARY, fg=COLOR_PURPLE_LIGHT
        )
        aws_label.pack(side=tk.LEFT)
        
        costs_label = tk.Label(
            title_frame, text=" Costs",
            font=("Helvetica", 17, "bold"),
            bg=COLOR_BG_PRIMARY, fg=COLOR_FG
        )
        costs_label.pack(side=tk.LEFT)
        
        # Premium badge
        badge_frame = tk.Frame(self.header_frame, bg=COLOR_PURPLE_DARK, padx=6, pady=2)
        badge_frame.pack(side=tk.LEFT, padx=(8, 0))
        
        badge_label = tk.Label(
            badge_frame, text="PRO",
            font=("Helvetica", 7, "bold"),
            bg=COLOR_PURPLE_DARK, fg=COLOR_FG
        )
        badge_label.pack()
        
        # Close button
        self.close_btn = tk.Button(
            self.header_frame, text="✕",
            font=("Helvetica", 12, "bold"),
            bg=COLOR_BG_SECONDARY, fg=COLOR_FG_MUTED,
            bd=0, highlightthickness=0, padx=8, pady=2,
            activebackground=COLOR_RED, activeforeground=COLOR_FG,
            command=self.close, cursor="hand2"
        )
        self.close_btn.pack(side=tk.RIGHT)
        self.close_btn.bind('<Enter>', lambda e: self.close_btn.config(bg=COLOR_RED, fg=COLOR_FG))
        self.close_btn.bind('<Leave>', lambda e: self.close_btn.config(bg=COLOR_BG_SECONDARY, fg=COLOR_FG_MUTED))
        
        # ═══ GRADIENT SEPARATOR ═══
        self._create_gradient_line(self.main_frame)

        
        # ═══ COST DISPLAY CARD ═══
        cost_outer = tk.Frame(self.main_frame, bg=COLOR_PURPLE_MAIN, padx=1, pady=1)
        cost_outer.pack(fill=tk.X, pady=(10, 10))
        
        cost_card = tk.Frame(cost_outer, bg=COLOR_BG_CARD, padx=14, pady=12)
        cost_card.pack(fill=tk.BOTH, expand=True)
        
        cost_header = tk.Frame(cost_card, bg=COLOR_BG_CARD)
        cost_header.pack(fill=tk.X)
        
        cost_icon = tk.Label(
            cost_header, text="💎",
            font=("Helvetica", 14),
            bg=COLOR_BG_CARD
        )
        cost_icon.pack(side=tk.LEFT)
        
        cost_title = tk.Label(
            cost_header, text=" Month-to-Date Spend",
            font=("Helvetica", 10),
            bg=COLOR_BG_CARD, fg=COLOR_FG_SECONDARY
        )
        cost_title.pack(side=tk.LEFT)
        
        # Large cost display with glow effect
        self.cost_label = tk.Label(
            cost_card, text="$0.00",
            font=("Helvetica", 38, "bold"),
            bg=COLOR_BG_CARD, fg=COLOR_PURPLE_GLOW
        )
        self.cost_label.pack(anchor=tk.W, pady=(8, 4))
        
        # Budget context
        self.budget_context = tk.Label(
            cost_card, text=f"of ${self.config.budget:.0f} monthly budget",
            font=("Helvetica", 9),
            bg=COLOR_BG_CARD, fg=COLOR_FG_MUTED
        )
        self.budget_context.pack(anchor=tk.W)
        
        # ═══ BUDGET PROGRESS CARD ═══
        progress_card = tk.Frame(self.main_frame, bg=COLOR_BG_CARD, padx=14, pady=10)
        progress_card.pack(fill=tk.X, pady=(0, 10))
        
        progress_header = tk.Frame(progress_card, bg=COLOR_BG_CARD)
        progress_header.pack(fill=tk.X)
        
        progress_icon = tk.Label(
            progress_header, text="📊",
            font=("Helvetica", 11),
            bg=COLOR_BG_CARD
        )
        progress_icon.pack(side=tk.LEFT)
        
        progress_title = tk.Label(
            progress_header, text=" Budget Usage",
            font=("Helvetica", 10),
            bg=COLOR_BG_CARD, fg=COLOR_FG_SECONDARY
        )
        progress_title.pack(side=tk.LEFT)
        
        self.budget_pct_label = tk.Label(
            progress_header, text="0%",
            font=("Helvetica", 13, "bold"),
            bg=COLOR_BG_CARD, fg=COLOR_GREEN
        )
        self.budget_pct_label.pack(side=tk.RIGHT)
        
        # Premium progress bar
        progress_outer = tk.Frame(progress_card, bg=COLOR_PURPLE_DARK, padx=1, pady=1)
        progress_outer.pack(fill=tk.X, pady=(8, 0))
        
        self.progress_canvas = tk.Canvas(
            progress_outer, height=12, bg=COLOR_PROGRESS_BG,
            highlightthickness=0
        )
        self.progress_canvas.pack(fill=tk.X)

        
        # ═══ TOP SERVICES SECTION ═══
        services_header = tk.Frame(self.main_frame, bg=COLOR_BG_PRIMARY)
        services_header.pack(fill=tk.X, pady=(6, 6))
        
        services_icon = tk.Label(
            services_header, text="🔥",
            font=("Helvetica", 11),
            bg=COLOR_BG_PRIMARY
        )
        services_icon.pack(side=tk.LEFT)
        
        services_title = tk.Label(
            services_header, text=" Top Services",
            font=("Helvetica", 11, "bold"),
            bg=COLOR_BG_PRIMARY, fg=COLOR_FG
        )
        services_title.pack(side=tk.LEFT)
        
        # Activity hint
        activity_hint = tk.Label(
            services_header, text="⚡24h events",
            font=("Helvetica", 7),
            bg=COLOR_BG_PRIMARY, fg=COLOR_CYAN
        )
        activity_hint.pack(side=tk.RIGHT)
        
        # Services list with scrollbar
        services_container = tk.Frame(self.main_frame, bg=COLOR_BG_PRIMARY)
        services_container.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas for scrolling
        services_canvas = tk.Canvas(
            services_container,
            bg=COLOR_BG_PRIMARY,
            highlightthickness=0,
            height=200
        )
        services_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(
            services_container,
            orient=tk.VERTICAL,
            command=services_canvas.yview,
            bg=COLOR_BG_SECONDARY,
            troughcolor=COLOR_BG_PRIMARY,
            width=12
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        services_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create frame inside canvas
        self.services_frame = tk.Frame(services_canvas, bg=COLOR_BG_PRIMARY)
        services_canvas.create_window((0, 0), window=self.services_frame, anchor=tk.NW)
        
        # Bind scroll region update
        def update_scroll_region(event=None):
            services_canvas.configure(scrollregion=services_canvas.bbox("all"))
        
        self.services_frame.bind("<Configure>", update_scroll_region)
        
        # Enable mouse wheel scrolling
        def on_mousewheel(event):
            services_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        services_canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        self.service_labels = []
        for i in range(10):
            bg = COLOR_BG_SECONDARY if i % 2 == 0 else COLOR_BG_PRIMARY
            
            frame = tk.Frame(self.services_frame, bg=bg, padx=10, pady=5)
            frame.pack(fill=tk.X, pady=1)
            
            # Rank indicator
            rank_colors = [COLOR_GOLD, COLOR_PURPLE_LIGHT, COLOR_PURPLE_MAIN, COLOR_FG_MUTED, COLOR_FG_MUTED,
                          COLOR_FG_MUTED, COLOR_FG_MUTED, COLOR_FG_MUTED, COLOR_FG_MUTED, COLOR_FG_MUTED]
            rank_label = tk.Label(
                frame, text=f"#{i+1}",
                font=("Helvetica", 8, "bold"),
                bg=bg, fg=rank_colors[i]
            )
            rank_label.pack(side=tk.LEFT, padx=(0, 6))
            
            name_label = tk.Label(
                frame, text="",
                font=("Helvetica", 9),
                bg=bg, fg=COLOR_FG,
                anchor=tk.W
            )
            name_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Activity count (events in last 24h)
            activity_label = tk.Label(
                frame, text="",
                font=("Helvetica", 8),
                bg=bg, fg=COLOR_CYAN,
                anchor=tk.E
            )
            activity_label.pack(side=tk.RIGHT, padx=(0, 8))
            
            cost_label = tk.Label(
                frame, text="",
                font=("Helvetica", 9, "bold"),
                bg=bg, fg=COLOR_PURPLE_LIGHT,
                anchor=tk.E
            )
            cost_label.pack(side=tk.RIGHT)
            
            self.service_labels.append((frame, name_label, cost_label, rank_label, activity_label))
        
        # ═══ FOOTER ═══
        footer = tk.Frame(self.main_frame, bg=COLOR_BG_PRIMARY)
        footer.pack(fill=tk.X, pady=(10, 0))
        
        self.updated_label = tk.Label(
            footer, text="",
            font=("Helvetica", 8),
            bg=COLOR_BG_PRIMARY, fg=COLOR_FG_MUTED
        )
        self.updated_label.pack(side=tk.LEFT)
        
        # Live status with pulsing effect
        live_frame = tk.Frame(footer, bg=COLOR_BG_PRIMARY)
        live_frame.pack(side=tk.RIGHT)
        
        self.live_dot = tk.Canvas(
            live_frame, width=8, height=8,
            bg=COLOR_BG_PRIMARY, highlightthickness=0
        )
        self.live_dot.pack(side=tk.LEFT, padx=(0, 4))
        self.live_dot.create_oval(1, 1, 7, 7, fill=COLOR_GREEN, outline="")
        
        live_label = tk.Label(
            live_frame, text="LIVE",
            font=("Helvetica", 8, "bold"),
            bg=COLOR_BG_PRIMARY, fg=COLOR_GREEN
        )
        live_label.pack(side=tk.LEFT)

    
    def _draw_premium_orb(self):
        """Draw animated purple orb indicator."""
        self.orb_canvas.delete("all")
        # Outer glow
        self.orb_canvas.create_oval(0, 0, 14, 14, fill=COLOR_PURPLE_DARK, outline="")
        # Inner bright
        self.orb_canvas.create_oval(2, 2, 12, 12, fill=COLOR_PURPLE_MAIN, outline="")
        # Highlight
        self.orb_canvas.create_oval(4, 4, 8, 8, fill=COLOR_PURPLE_GLOW, outline="")
    
    def _create_gradient_line(self, parent):
        """Create premium gradient separator."""
        sep_frame = tk.Frame(parent, bg=COLOR_BG_PRIMARY, height=3)
        sep_frame.pack(fill=tk.X, pady=(4, 0))
        
        # Multi-color gradient effect
        colors = [COLOR_PINK, COLOR_PURPLE_MAIN, COLOR_PURPLE_LIGHT, COLOR_CYAN]
        for color in colors:
            line = tk.Frame(sep_frame, bg=color, height=1)
            line.pack(fill=tk.X)
    
    def update_display(self, cost_data: CostData) -> None:
        """Update all UI elements with new cost data."""
        # Calculate budget percentage
        budget_pct = (cost_data.month_to_date / self.config.budget) * 100
        status_color = get_budget_color(budget_pct)
        
        # Update cost with dynamic color
        cost_color = COLOR_PURPLE_GLOW if budget_pct < 75 else status_color
        self.cost_label.config(
            text=format_currency(cost_data.month_to_date),
            fg=cost_color
        )
        
        # Update budget percentage
        self.budget_pct_label.config(text=f"{budget_pct:.1f}%", fg=status_color)
        
        # Update progress bar
        self._update_progress_bar(budget_pct)
        
        # Update services
        for i, (frame, name_label, cost_label, rank_label, activity_label) in enumerate(self.service_labels):
            if i < len(cost_data.top_services):
                service_data = cost_data.top_services[i]
                # Handle both old format (name, cost) and new format (name, cost, activity)
                if len(service_data) == 3:
                    service_name, service_cost, activity_count = service_data
                else:
                    service_name, service_cost = service_data
                    activity_count = 0
                display_name = service_name[:22] + "..." if len(service_name) > 22 else service_name
                name_label.config(text=display_name)
                cost_label.config(text=format_currency(service_cost))
                activity_label.config(text=f"⚡{activity_count}")
                frame.pack(fill=tk.X, pady=1)
            else:
                name_label.config(text="")
                cost_label.config(text="")
                activity_label.config(text="")
                frame.pack_forget()
        
        # Update timestamp
        time_str = cost_data.last_updated.strftime("%H:%M:%S")
        self.updated_label.config(text=f"🔄 {time_str}")
    
    def _update_progress_bar(self, percentage: float) -> None:
        """Update progress bar with premium styling."""
        self.progress_canvas.delete("all")
        
        canvas_width = self.progress_canvas.winfo_width()
        if canvas_width <= 1:
            canvas_width = self.width - 64
        
        fill_pct = min(percentage, 100) / 100
        fill_width = int(canvas_width * fill_pct)
        
        color = get_budget_color(percentage)
        
        if fill_width > 0:
            self.progress_canvas.create_rectangle(
                0, 0, fill_width, 12,
                fill=color, outline=""
            )
    
    def start_drag(self, event):
        """Begin drag operation."""
        self._drag_start_x = event.x
        self._drag_start_y = event.y
    
    def do_drag(self, event):
        """Move widget during drag."""
        x = self.root.winfo_x() + (event.x - self._drag_start_x)
        y = self.root.winfo_y() + (event.y - self._drag_start_y)
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x, y = clamp_position(x, y, self.width, self.height, screen_width, screen_height)
        
        self.root.geometry(f"+{x}+{y}")
    
    def close(self):
        """Close the widget gracefully."""
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Start the tkinter main loop."""
        self.root.mainloop()
