import tkinter as tk
from tkinter import messagebox
import random
import heapq
import time

# ─── Goal State ───────────────────────────────────────────────────────────────
TARGET = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# ─── Themes ───────────────────────────────────────────────────────────────────
THEMES = {
    "Neon": {
        "bg":           "#0a0a12",
        "surface":      "#12121f",
        "tile_bg":      "#1e1e3a",
        "tile_fg":      "#c0c8ff",
        "tile_active":  "#3030a0",
        "tile_movable": "#2a2a60",
        "empty_bg":     "#0e0e20",
        "accent":       "#5050ff",
        "accent2":      "#ff4080",
        "text":         "#d0d8ff",
        "text_muted":   "#6068a0",
        "btn_bg":       "#1e1e3a",
        "btn_fg":       "#8090ff",
        "btn_active":   "#2a2a60",
    },
    "Candy": {
        "bg":           "#fff0f8",
        "surface":      "#ffffff",
        "tile_bg":      "#ff6eb4",
        "tile_fg":      "#ffffff",
        "tile_active":  "#e0307a",
        "tile_movable": "#ff82c0",
        "empty_bg":     "#ffe0f0",
        "accent":       "#ff3a9a",
        "accent2":      "#ffaa00",
        "text":         "#660040",
        "text_muted":   "#bb5090",
        "btn_bg":       "#ffffff",
        "btn_fg":       "#ff3a9a",
        "btn_active":   "#ffe0f0",
    },
    "Forest": {
        "bg":           "#0d1a10",
        "surface":      "#142018",
        "tile_bg":      "#1e3a24",
        "tile_fg":      "#90e0a0",
        "tile_active":  "#1a5828",
        "tile_movable": "#254a2c",
        "empty_bg":     "#0f1e12",
        "accent":       "#2a8040",
        "accent2":      "#aadd44",
        "text":         "#a0d8a8",
        "text_muted":   "#507858",
        "btn_bg":       "#1e3a24",
        "btn_fg":       "#60c070",
        "btn_active":   "#254a2c",
    },
    "Golden": {
        "bg":           "#1a1408",
        "surface":      "#241c0c",
        "tile_bg":      "#3a2e10",
        "tile_fg":      "#ffd060",
        "tile_active":  "#805010",
        "tile_movable": "#4a3a14",
        "empty_bg":     "#20180a",
        "accent":       "#c08020",
        "accent2":      "#ff8040",
        "text":         "#e0c060",
        "text_muted":   "#806030",
        "btn_bg":       "#3a2e10",
        "btn_fg":       "#c08020",
        "btn_active":   "#4a3a14",
    },
    "Ice": {
        "bg":           "#f0f8ff",
        "surface":      "#ffffff",
        "tile_bg":      "#4090d0",
        "tile_fg":      "#ffffff",
        "tile_active":  "#2070b0",
        "tile_movable": "#50a0e0",
        "empty_bg":     "#d8eefb",
        "accent":       "#1060a0",
        "accent2":      "#00c8ff",
        "text":         "#1a3a5a",
        "text_muted":   "#5080a0",
        "btn_bg":       "#ffffff",
        "btn_fg":       "#1060a0",
        "btn_active":   "#e8f4ff",
    },
}


# ─── Helpers ──────────────────────────────────────────────────────────────────
def get_neighbors(i):
    r, c = divmod(i, 3)
    nb = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            nb.append(nr * 3 + nc)
    return nb


def manhattan(state):
    dist = 0
    for i, val in enumerate(state):
        if val != 0:
            gi = TARGET.index(val)
            dist += abs(i // 3 - gi // 3) + abs(i % 3 - gi % 3)
    return dist


def astar(start):
    start = tuple(start)
    open_list = [(manhattan(start), 0, start, [])]
    visited = set()
    while open_list:
        f, g, cur, path = heapq.heappop(open_list)
        if cur in visited:
            continue
        visited.add(cur)
        if list(cur) == TARGET:
            return path
        z = cur.index(0)
        for n in get_neighbors(z):
            nxt = list(cur)
            nxt[z], nxt[n] = nxt[n], nxt[z]
            t = tuple(nxt)
            if t not in visited:
                heapq.heappush(open_list, (g + 1 + manhattan(nxt), g + 1, t, path + [nxt]))
    return None


# ─── Start Screen ─────────────────────────────────────────────────────────────
class StartScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Game")
        self.root.geometry("460x560")
        self.root.resizable(False, False)
        self.theme_name = "Neon"
        self.T = THEMES[self.theme_name]

        self.root.configure(bg=self.T["bg"])
        self._build()

    def _build(self):
        T = self.T

        self.frame = tk.Frame(self.root, bg=T["bg"])
        self.frame.pack(expand=True, fill="both", padx=30, pady=30)

        tk.Label(self.frame, text="8-PUZZLE", font=("Courier", 32, "bold"),
                 fg=T["accent"], bg=T["bg"]).pack(pady=(20, 4))

        tk.Label(self.frame, text="Arrange numbers 1–8 in order",
                 font=("Courier", 11), fg=T["text_muted"], bg=T["bg"]).pack(pady=(0, 20))

        # Theme selector
        tk.Label(self.frame, text="THEME", font=("Courier", 10),
                 fg=T["text_muted"], bg=T["bg"]).pack()

        dot_row = tk.Frame(self.frame, bg=T["bg"])
        dot_row.pack(pady=8)

        self.dot_buttons = {}
        dot_colors = {
            "Neon":   "#5050ff",
            "Candy":  "#ff6eb4",
            "Forest": "#2a8040",
            "Golden": "#c08020",
            "Ice":    "#4090d0",
        }
        for name, color in dot_colors.items():
            relief = "sunken" if name == self.theme_name else "flat"
            btn = tk.Button(
                dot_row, bg=color, width=3, height=1,
                relief=relief, bd=2, cursor="hand2",
                command=lambda n=name: self._set_theme(n)
            )
            btn.pack(side="left", padx=4)
            self.dot_buttons[name] = btn

        tk.Frame(self.frame, bg=T["accent"], height=2).pack(fill="x", pady=20)

        self.start_btn = tk.Button(
            self.frame, text="START GAME",
            font=("Courier", 14, "bold"),
            bg=T["accent"], fg="#ffffff",
            activebackground=T["tile_active"],
            activeforeground="#ffffff",
            relief="flat", bd=0, padx=20, pady=10,
            cursor="hand2",
            command=self._start
        )
        self.start_btn.pack(pady=10)

    def _set_theme(self, name):
        self.theme_name = name
        self.T = THEMES[name]
        self.frame.destroy()
        self.root.configure(bg=self.T["bg"])
        self._build()

    def _start(self):
        self.frame.destroy()
        PuzzleGame(self.root, self.theme_name)


# ─── Puzzle Game ──────────────────────────────────────────────────────────────
class PuzzleGame:
    def __init__(self, root, theme_name="Neon"):
        self.root = root
        self.root.geometry("460x620")
        self.theme_name = theme_name
        self.T = THEMES[theme_name]

        self.state = TARGET[:]
        self.moves = 0
        self.seconds = 0
        self.best = None
        self.timer_id = None
        self.solving = False

        self._build_ui()
        self.shuffle()

    # ── UI Construction ────────────────────────────────────────────────────────
    def _build_ui(self):
        T = self.T
        self.root.configure(bg=T["bg"])

        # ── Top bar
        top = tk.Frame(self.root, bg=T["bg"])
        top.pack(fill="x", padx=20, pady=(14, 0))

        tk.Label(top, text="8-PUZZLE", font=("Courier", 16, "bold"),
                 fg=T["accent"], bg=T["bg"]).pack(side="left")

        # Theme dots
        dot_row = tk.Frame(top, bg=T["bg"])
        dot_row.pack(side="right")

        dot_colors = {
            "Neon": "#5050ff", "Candy": "#ff6eb4", "Forest": "#2a8040",
            "Golden": "#c08020", "Ice": "#4090d0",
        }
        self.dot_btns = {}
        for name, color in dot_colors.items():
            relief = "sunken" if name == self.theme_name else "flat"
            btn = tk.Button(dot_row, bg=color, width=2, height=1,
                            relief=relief, bd=2, cursor="hand2",
                            command=lambda n=name: self._switch_theme(n))
            btn.pack(side="left", padx=2)
            self.dot_btns[name] = btn

        # ── Stats row
        stats = tk.Frame(self.root, bg=T["bg"])
        stats.pack(fill="x", padx=20, pady=10)

        self.lbl_moves = self._stat_box(stats, "MOVES", "0")
        self.lbl_timer = self._stat_box(stats, "TIME",  "0:00")
        self.lbl_best  = self._stat_box(stats, "BEST",  "--")

        # ── Board
        board_wrap = tk.Frame(self.root, bg=T["bg"])
        board_wrap.pack(pady=6)

        self.board_frame = tk.Frame(board_wrap, bg=T["surface"],
                                    bd=0, highlightthickness=2,
                                    highlightbackground=T["accent"])
        self.board_frame.pack(padx=12, pady=12)

        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                self.board_frame,
                font=("Courier", 22, "bold"),
                width=4, height=2,
                relief="flat", bd=0, cursor="hand2",
                command=lambda idx=i: self._move(idx)
            )
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        # ── Controls
        ctrl = tk.Frame(self.root, bg=T["bg"])
        ctrl.pack(pady=8)

        for text, cmd, is_primary in [
            ("Shuffle",    self.shuffle,     False),
            ("Reset",      self.reset,       False),
            ("Auto-Solve", self.auto_solve,  True),
        ]:
            bg = T["accent"] if is_primary else T["btn_bg"]
            fg = "#ffffff"   if is_primary else T["btn_fg"]
            btn = tk.Button(
                ctrl, text=text,
                font=("Courier", 11, "bold"),
                bg=bg, fg=fg,
                activebackground=T["tile_active"],
                activeforeground="#ffffff",
                relief="flat", bd=0, padx=14, pady=7,
                cursor="hand2", command=cmd
            )
            btn.pack(side="left", padx=5)
            if text == "Auto-Solve":
                self.solve_btn = btn

        # ── Hint label
        self.hint_var = tk.StringVar(value="click a tile adjacent to the blank")
        tk.Label(self.root, textvariable=self.hint_var,
                 font=("Courier", 9), fg=T["text_muted"], bg=T["bg"]).pack(pady=4)

        self._draw()

    def _stat_box(self, parent, label, value):
        T = self.T
        frame = tk.Frame(parent, bg=T["surface"], bd=0,
                         highlightthickness=1,
                         highlightbackground=T["accent"])
        frame.pack(side="left", expand=True, fill="x", padx=5, ipady=6, ipadx=12)
        tk.Label(frame, text=label, font=("Courier", 8),
                 fg=T["text_muted"], bg=T["surface"]).pack()
        lbl = tk.Label(frame, text=value, font=("Courier", 20, "bold"),
                       fg=T["accent"], bg=T["surface"])
        lbl.pack()
        return lbl

    # ── Theme switching ────────────────────────────────────────────────────────
    def _switch_theme(self, name):
        self.theme_name = name
        self.T = THEMES[name]
        # Destroy everything and rebuild
        for widget in self.root.winfo_children():
            widget.destroy()
        self._build_ui()
        self._draw()

    # ── Drawing ────────────────────────────────────────────────────────────────
    def _draw(self, just_moved=-1):
        T = self.T
        z = self.state.index(0)
        movables = get_neighbors(z)

        for i, val in enumerate(self.state):
            btn = self.buttons[i]
            if val == 0:
                btn.config(text="", bg=T["empty_bg"],
                           fg=T["empty_bg"], cursor="arrow",
                           activebackground=T["empty_bg"])
            elif i in movables:
                btn.config(text=str(val), bg=T["tile_movable"],
                           fg=T["tile_fg"], cursor="hand2",
                           activebackground=T["tile_active"])
            else:
                btn.config(text=str(val), bg=T["tile_bg"],
                           fg=T["tile_fg"], cursor="hand2",
                           activebackground=T["tile_active"])

    # ── Game Logic ─────────────────────────────────────────────────────────────
    def _move(self, idx):
        if self.solving:
            return
        z = self.state.index(0)
        if idx not in get_neighbors(z):
            return
        self.state[z], self.state[idx] = self.state[idx], self.state[z]
        self.moves += 1
        self.lbl_moves.config(text=str(self.moves))
        if self.moves == 1:
            self._start_timer()
        self._draw(just_moved=idx)
        if self.state == TARGET:
            self._handle_win()

    def shuffle(self):
        self.solving = False
        self.solve_btn.config(state="normal")
        s = TARGET[:]
        for _ in range(80):
            z = s.index(0)
            n = random.choice(get_neighbors(z))
            s[z], s[n] = s[n], s[z]
        self.state = s
        self.moves = 0
        self.lbl_moves.config(text="0")
        self._stop_timer()
        self.seconds = 0
        self.lbl_timer.config(text="0:00")
        self.hint_var.set("click a tile adjacent to the blank")
        self._draw()

    def reset(self):
        self.solving = False
        self.solve_btn.config(state="normal")
        self.state = TARGET[:]
        self.moves = 0
        self.lbl_moves.config(text="0")
        self._stop_timer()
        self.seconds = 0
        self.lbl_timer.config(text="0:00")
        self._draw()

    def _handle_win(self):
        self._stop_timer()
        self.solving = False
        if self.best is None or self.moves < self.best:
            self.best = self.moves
            self.lbl_best.config(text=str(self.best))
        m, s = divmod(self.seconds, 60)
        msg = (
            f"🎉 Puzzle Solved!\n\n"
            f"Moves : {self.moves}\n"
            f"Time  : {m}:{s:02d}\n"
            + (f"🏆 New best: {self.best} moves!" if self.moves == self.best else "")
        )
        messagebox.showinfo("Congratulations!", msg)

    # ── Timer ──────────────────────────────────────────────────────────────────
    def _start_timer(self):
        self._stop_timer()
        self.seconds = 0
        self._tick()

    def _tick(self):
        self.seconds += 1
        m, s = divmod(self.seconds, 60)
        self.lbl_timer.config(text=f"{m}:{s:02d}")
        self.timer_id = self.root.after(1000, self._tick)

    def _stop_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    # ── Auto-Solve ─────────────────────────────────────────────────────────────
    def auto_solve(self):
        if self.state == TARGET:
            self.hint_var.set("already solved!")
            return
        self.solving = True
        self.solve_btn.config(state="disabled")
        self.hint_var.set("solving…")

        def run():
            path = astar(self.state[:])
            if not path:
                self.hint_var.set("no solution found")
                self.solving = False
                self.solve_btn.config(state="normal")
                return
            self.hint_var.set(f"solving in {len(path)} moves…")
            if self.moves == 0:
                self._start_timer()
            self._animate(path, 0)

        self.root.after(20, run)

    def _animate(self, path, step):
        if not self.solving or step >= len(path):
            self.solving = False
            self.solve_btn.config(state="normal")
            return
        self.state = path[step][:]
        self.moves += 1
        self.lbl_moves.config(text=str(self.moves))
        self._draw()
        if self.state == TARGET:
            self._handle_win()
            return
        self.root.after(260, lambda: self._animate(path, step + 1))


# ─── Run ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    StartScreen(root)
    root.mainloop()
