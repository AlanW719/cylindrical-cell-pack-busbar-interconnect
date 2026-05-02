import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import threading

class BatteryPackDesigner:
    def __init__(self, root):
        self.root = root
        self.root.title("Cylindrical Cell Battery Pack Designer")
        
        # --- THEME COLORS ---
        BG_COLOR = "#050A18"
        SIDEBAR_BG = "#0B1426"
        ACCENT_CYAN = "#00F2FF"
        TEXT_COLOR = "#E0E6ED"
        UI_FONT = ('Segoe UI', 12)
        HEADER_FONT = ('Segoe UI', 13, 'bold')

        self.root.configure(bg=BG_COLOR)
        self.root.state('zoomed')
        
        # Grid Weights for Full-Screen Expansion
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", foreground=TEXT_COLOR, background=SIDEBAR_BG, font=UI_FONT)
        style.configure("TLabelframe", foreground=ACCENT_CYAN, background=SIDEBAR_BG)
        style.configure("TLabelframe.Label", foreground=ACCENT_CYAN, background=SIDEBAR_BG, font=HEADER_FONT)

        # Sidebar
        sidebar = ttk.LabelFrame(root, text="Configuration", padding="15")
        sidebar.grid(row=0, column=0, sticky="nsw", padx=15, pady=15)
        ttk.Label(sidebar, text="Cell Parameters").grid(row=0, column=0, sticky="w", pady=(10, 0))
        
        inputs = [("Series (S)", "4"), ("Parallel (P)", "6"), 
                  ("Max (V)", "4.2"), ("Min (V)", "2.5"), ("Pulse Current (A)", "90"),
                  ("Internal Resistance (mΩ)", "4")]
        
        self.entries = {}
        for i, (txt, val) in enumerate(inputs):
            ttk.Label(sidebar, text=txt).grid(row=i+1, column=0, sticky="w", pady=5)
            e = tk.Entry(sidebar, width=12, bg="#16213E", fg=ACCENT_CYAN, font=('Consolas', 14, 'bold'), relief="flat")
            e.insert(0, val)
            e.grid(row=i+1, column=1, pady=5, padx=10)
            self.entries[txt] = e

        # --- CONNECTION TYPE OPTION ---
        ttk.Label(sidebar, text="Connection Layout").grid(row=8, column=0, sticky="w", pady=(10, 0))
        self.conn_var = tk.StringVar(value="Cross-Linked")
        tk.Radiobutton(sidebar, text="Cross-Linked (P-First)", variable=self.conn_var, value="Cross-Linked",
                       bg=SIDEBAR_BG, fg=ACCENT_CYAN, selectcolor="#16213E", font=UI_FONT).grid(row=9, column=0, columnspan=2, sticky="w")
        tk.Radiobutton(sidebar, text="Non-Cross-Linked (S-First)", variable=self.conn_var, value="Non-Cross",
                       bg=SIDEBAR_BG, fg=ACCENT_CYAN, selectcolor="#16213E", font=UI_FONT).grid(row=10, column=0, columnspan=2, sticky="w")

        self.update_btn = tk.Button(sidebar, text="Update 3D Model", command=self.start_render_thread, 
                                   bg="#0048FF", fg="white", font=HEADER_FONT, relief="flat", padx=20, pady=10)
        self.update_btn.grid(row=11, column=0, columnspan=2, pady=20)
        
        self.stats = ttk.Label(sidebar, text="", justify="left", font=UI_FONT)
        self.stats.grid(row=12, column=0, columnspan=2, sticky="w")

        # --- 3D AREA ---
        plot_container = tk.Frame(root, bg=BG_COLOR)
        plot_container.grid(row=0, column=1, sticky="nsew")
        plot_container.grid_rowconfigure(0, weight=1)
        plot_container.grid_columnconfigure(0, weight=1)

        self.fig = plt.figure(figsize=(10, 8), facecolor=BG_COLOR)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_facecolor(BG_COLOR)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_container)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky="nsew")

        self.toolbar = NavigationToolbar2Tk(self.canvas, plot_container, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.grid(row=1, column=0, sticky="ew")
        
        self.start_render_thread()

    def draw_copper(self, x_start, x_end, y_start, y_end, z, color='#CD7F32'):
        X, Y = np.meshgrid([x_start, x_end], [y_start, y_end])
        Z = np.full(X.shape, z)
        self.ax.plot_surface(X, Y, Z, color=color, alpha=0.9, shade=True, edgecolors='#8B4513', lw=0.1)

    def start_render_thread(self):
        self.update_btn.config(state="disabled", text="Rendering...")
        threading.Thread(target=self.render_logic, daemon=True).start()

    def render_logic(self):
        try:
            S = int(self.entries["Series (S)"].get())
            P = int(self.entries["Parallel (P)"].get())
            v_max = float(self.entries["Max (V)"].get())
            IR = float(self.entries["Internal Resistance (mΩ)"].get())
            A_max = float(self.entries["Pulse Current (A)"].get())
            conn_type = self.conn_var.get()
            
            self.ax.clear()
            self.ax.set_axis_off() 
            max_dim = max(S, P)
            self.ax.set_box_aspect((S/max_dim, P/max_dim, 0.4))
            
            r, h, space = 0.45, 2.0, 1.4
            theta = np.linspace(0, 2*np.pi, 20)

            for s in range(S):
                is_flipped = (s % 2 == 0) # s = 0, 1, 2, 3, ...; s%2 = 0, 1, 0, 1...; if S is odd number, s%2 == 0
                is_start = (s == 0)
                is_end = (s == S - 1)

                # --- 1. BUSBAR PLATES (TOP & BOTTOM) ---
                # TERMINALS: First and Last row ALWAYS use a single common plate
                if conn_type == "Cross-Linked":
                    # Single common busbar across all P cells
                    self.draw_copper(s*space-0.5, s*space+0.5, -0.5, (P-1)*space+0.5, h+0.05, color='#CD7F32')
                    self.draw_copper(s*space-0.5, s*space+0.5, -0.5, (P-1)*space+0.5, -0.05, color='#CD7F32')
                                            
                else:
                    if is_start or (is_end and not is_flipped):
                        self.draw_copper(s*space-0.5, s*space+0.5, -0.5, (P-1)*space+0.5, -0.05, color='#CD7F32')
                        
                    elif is_end and is_flipped:
                        self.draw_copper(s*space-0.5, s*space+0.5, -0.5, (P-1)*space+0.5, h+0.05, color='#CD7F32')                  
                        
                    # INTERNAL: Draw individual small plates for each cell to prevent cross-linking
                    for p in range(P):
                        y0 = p * space
                        self.draw_copper(s*space-0.45, s*space+0.45, y0-0.45, y0+0.45, h+0.05, color='#CD7F32')
                        self.draw_copper(s*space-0.45, s*space+0.45, y0-0.45, y0+0.45, -0.05, color='#CD7F32')

                # --- 2. SERIES BRIDGES ---
                if s < S - 1:
                    z_pos = (h + 0.05) if s % 2 == 0 else -0.05
                    if conn_type == "Cross-Linked":
                        # Parallel-First: One wide series bridge
                        self.draw_copper(s*space, (s+1)*space, -0.5, (P-1)*space+0.5, z_pos, color='#B87333')
                    else:
                        # Series-First: Individual narrow bridges per string
                        for p in range(P):
                            y0 = p * space
                            self.draw_copper(s*space-0.45, (s+1)*space+0.45, y0-0.45, y0+0.45, z_pos, color='#B87333')

                # --- 3. CELLS ---
                for p in range(P):
                    x0, y0 = s * space, p * space
                    z_cyl = np.linspace(0, h, 2)
                    T, Z = np.meshgrid(theta, z_cyl)
                    X, Y = r*np.cos(T)+x0, r*np.sin(T)+y0
                    self.ax.plot_surface(X, Y, Z, color='#39FF14', alpha=0.7, shade=True, lw=0)
                    
                    lbl = "-" if is_flipped else "+"
                    col = "#00F2FF" if is_flipped else "#FF3131"
                    self.ax.text(x0, y0, h+0.6, lbl, color=col, weight='bold', ha='center')

            self.ax.set_title(f"Cylindrical Cell Battery Pack Design ({S}S{P}P)\n{conn_type} Busbar Layout", color='white', pad=20)
            self.ax.view_init(elev=25, azim=-60)
            
            total_ir = (IR * S) / P
            P_max = v_max * S * A_max * P
            self.root.after(0, lambda: self.finalize_ui(total_ir, P_max, v_max, S))
            
        except Exception as e:
            self.root.after(0, lambda: self.reset_btn_error(str(e)))



    def finalize_ui(self, total_ir, P_max, v_max, S):
        self.canvas.draw()
        self.stats.config(text=f"Total Pack Voltage: {v_max * S:.1f} V \n Total Internal Resistance: {total_ir:.2f} mΩ \n Max. Power: {P_max/1000:.2f} kW")
        self.update_btn.config(state="normal", text="Update 3D Model")

    def reset_btn_error(self, err):
        self.update_btn.config(state="normal", text="Update 3D Model")

if __name__ == "__main__":
    root = tk.Tk()
    app = BatteryPackDesigner(root)
    root.mainloop()
