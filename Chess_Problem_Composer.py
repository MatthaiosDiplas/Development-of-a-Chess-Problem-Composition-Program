import chess
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from genetic_algorithm import run_evolution, close_engine
from chess_problem_themes import THEMES, THEME_DESCRIPTIONS, THEME_MATE_DEPTHS

def start_gui():
    root = tk.Tk()
    root.title("Chess Problem Composer")
    root.geometry("680x500")
    root.resizable(False, False)

    font_main = ("Segoe UI", 12)

    label = tk.Label(root, text="Select a theme:", font=font_main)
    label.pack(pady=(15, 5))

    theme_var = tk.StringVar(value=list(THEMES.keys())[0])
    theme_combo = ttk.Combobox(
        root,
        textvariable=theme_var,
        values=list(THEMES.keys()),
        state="readonly",
        font=font_main
    )
    theme_combo.pack(pady=5)

    theme_desc = tk.Text(
        root,
        height=4,
        width=70,
        wrap="word",
        font=("Segoe UI", 11),
        fg="blue",
        bg=root.cget("bg"),
        relief="flat"
    )
    theme_desc.pack(pady=(5, 10))
    theme_desc.config(state="disabled")

    def update_description(*args):
        selected = theme_var.get()
        desc = THEME_DESCRIPTIONS.get(selected, "No description available.")
        theme_desc.config(state="normal")
        theme_desc.delete("1.0", "end")
        theme_desc.tag_configure("center", justify="center")
        theme_desc.insert("1.0", desc, "center")
        theme_desc.config(state="disabled")

    theme_var.trace_add("write", update_description)
    update_description()

    board_display = tk.Text(root, height=10, width=65, font=("Courier New", 13), wrap="none", bd=1, relief="sunken")
    board_display.tag_configure("center", justify="center")
    board_display.pack(pady=(5, 5))
    board_display.config(state="disabled", cursor="arrow")
    board_display.bind("<MouseWheel>", lambda e: "break")
    board_display.bind("<Button-4>", lambda e: "break")
    board_display.bind("<Button-5>", lambda e: "break")

    def disable_selection(event):
        return "break"

    for seq in ("<Button-1>", "<B1-Motion>", "<Control-c>", "<Control-x>", "<Control-v>"):
        board_display.bind(seq, disable_selection)

    fen_string = [""]

    copy_btn = tk.Button(root, text="Copy FEN", font=font_main)

    def copy_fen():
        if fen_string[0]:
            root.clipboard_clear()
            root.clipboard_append(fen_string[0])
            messagebox.showinfo("Copied", "FEN copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No FEN to copy.")

    copy_btn.config(command=copy_fen)

    start_btn = tk.Button(root, text="Create Chess Problem", font=font_main)
    start_btn.pack(pady=10)

    def on_start():
        selected = theme_var.get()
        if selected not in THEMES:
            messagebox.showerror("Error", "Please select a valid theme.")
            return

        start_btn.config(state='disabled')
        theme_combo.config(state='disabled')
        board_display.config(state="normal")
        board_display.delete("1.0", "end")
        board_display.config(state="disabled")
        copy_btn.pack_forget()
        fen_string[0] = ""  # Reset FEN storage

        def run():
            try:
                fen, fitness = run_evolution(THEMES[selected])
                fen_string[0] = fen

                def update_ui():
                    mate_in = THEME_MATE_DEPTHS.get(selected)
                    board = chess.Board(fen)
                    board_str = str(board)

                    text_block = (
                        f"{board_str}\n\n"
                        f"White to play and mate in {mate_in} moves\n"
                    )
                    board_display.config(state="normal")
                    board_display.delete("1.0", "end")
                    board_display.insert("1.0", text_block, "center")
                    board_display.config(state="disabled")
                    copy_btn.pack(pady=5)
                    start_btn.config(state='normal')
                    theme_combo.config(state='readonly')

                root.after(0, update_ui)

            except Exception as e:
                root.after(0, lambda: messagebox.showerror("Error", str(e)))
                root.after(0, lambda: start_btn.config(state="normal"))
                root.after(0, lambda: theme_combo.config(state='readonly'))

        threading.Thread(target=run, daemon=True).start()

    start_btn.config(command=on_start)

    def on_closing():
        try:
            close_engine()
        except Exception as e:
            print("Cleanup error:", e)
        finally:
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    start_gui()
