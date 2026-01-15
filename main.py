import customtkinter as ctk
import threading
import time
import sys
import json
import ctypes

from pynput.keyboard import Listener, Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController


def hide_console():
    if sys.platform == "win32":
        try:
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd != 0:
                ctypes.windll.user32.ShowWindow(hwnd, 0)
        except Exception:
            pass


class AppState:
    def __init__(self):
        self.hc_delay_ms = 85
        self.kp_delay_ms = 85
        self.aa_delay_ms = 85

        self.valid_switch_keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.hide_key = "Key.insert"

        self.hc_enabled = False
        self.kp_enabled = False
        self.aa_enabled = False

        self.hc_bind = "f"
        self.kp_bind = "Key.ctrl_l"
        self.aa_bind = "g"

        self.hc_slot_1 = "3"
        self.hc_slot_2 = "4"

        self.kp_key_1 = "x"
        self.kp_key_2 = "2"

        self.aa_key_1 = "v"
        self.aa_key_2 = "c"
        self.aa_key_3 = "2"

        self.is_hc_running = False
        self.kp_key_held = False
        self.aa_key_held = False

        self.current_slot = "6"
        self.window_hidden = False


state = AppState()
keyboard = KeyboardController()
mouse = MouseController()


def run_hc_sequence():
    delay = state.hc_delay_ms / 1500.0

    if state.current_slot != state.hc_slot_2:
        if not state.is_hc_running:
            return

        keyboard.press(state.hc_slot_1)
        keyboard.release(state.hc_slot_1)
        time.sleep(delay)

        if not state.is_hc_running:
            return

        mouse.click(Button.right)
        time.sleep(delay)

        if not state.is_hc_running:
            return

        keyboard.press(state.hc_slot_2)
        keyboard.release(state.hc_slot_2)
        time.sleep(delay)

    while state.is_hc_running:
        mouse.click(Button.right)
        time.sleep(delay)
        if not state.is_hc_running:
            break

        mouse.click(Button.left)
        time.sleep(delay)
        if not state.is_hc_running:
            break

        mouse.click(Button.right)
        time.sleep(delay)
        if not state.is_hc_running:
            break

        mouse.click(Button.left)
        time.sleep(delay)


def run_kp_sequence():
    delay = state.kp_delay_ms / 1000.0

    keyboard.press(state.kp_key_1)
    keyboard.release(state.kp_key_1)
    time.sleep(delay)

    mouse.click(Button.right)
    time.sleep(delay)

    keyboard.press(state.kp_key_2)
    keyboard.release(state.kp_key_2)


def run_aa_sequence():
    delay = state.aa_delay_ms / 1500.0

    keyboard.press(state.aa_key_1)
    keyboard.release(state.aa_key_1)
    time.sleep(delay)

    mouse.click(Button.right)
    time.sleep(delay)

    keyboard.press(state.aa_key_2)
    keyboard.release(state.aa_key_2)
    time.sleep(delay)

    mouse.click(Button.right)
    time.sleep(delay)

    keyboard.press(state.aa_key_3)
    keyboard.release(state.aa_key_3)
    time.sleep(delay)

    mouse.click(Button.right)


def format_key_string(key):
    return str(key).replace("'", "")


def on_key_press(key):
    try:
        k_str = format_key_string(key)

        if app.binding_mode:
            app.finish_binding(k_str)
            return

        if hasattr(key, "char") and key.char:
            if key.char.lower() in state.valid_switch_keys:
                state.current_slot = key.char.lower()

        if k_str == state.hide_key:
            app.toggle_visibility()

        if state.hc_enabled:
            if k_str == state.hc_bind and not state.is_hc_running:
                state.is_hc_running = True
                threading.Thread(target=run_hc_sequence, daemon=True).start()

        if state.kp_enabled:
            if k_str == state.kp_bind and not state.kp_key_held:
                state.kp_key_held = True
                threading.Thread(target=run_kp_sequence, daemon=True).start()

        if state.aa_enabled:
            if k_str == state.aa_bind and not state.aa_key_held:
                state.aa_key_held = True
                threading.Thread(target=run_aa_sequence, daemon=True).start()

    except Exception as e:
        print(f"Key error: {e}")


def on_key_release(key):
    try:
        k_str = format_key_string(key)

        if app.binding_mode:
            return

        if state.hc_enabled and k_str == state.hc_bind:
            state.is_hc_running = False

        if state.kp_enabled and k_str == state.kp_bind:
            state.kp_key_held = False

        if state.aa_enabled and k_str == state.aa_bind:
            state.aa_key_held = False

    except Exception:
        pass


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


class ProximaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("")
        self.overrideredirect(True)
        self.geometry("1000x650")
        self.configure(fg_color="#0a0a0a")

        self._drag_start_x = 0
        self._drag_start_y = 0
        self.binding_mode = False
        self.binding_target_func = None
        self.binding_button_ref = None

        if sys.platform == "win32":
            try:
                hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
                exstyle = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
                exstyle = (exstyle | 0x00040000) & ~0x00000080
                ctypes.windll.user32.SetWindowLongW(hwnd, -20, exstyle)
                ctypes.windll.user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, 0x0027)
            except Exception:
                pass

        self.listener = Listener(on_press=on_key_press, on_release=on_key_release)
        self.listener.start()
        self.show_console_simulation()

    def show_console_simulation(self):
        self.console_frame = ctk.CTkFrame(self, fg_color="black", corner_radius=0)
        self.console_frame.pack(fill="both", expand=True)

        ascii_art = r"""
 ███████████                                  ███                           
░░███░░░░░███                                ░░░                            
 ░███    ░███ ████████   ██████  █████ █████ ████  █████████████    ██████  
 ░██████████ ░░███░░███ ███░░███░░███ ░░███ ░░███ ░░███░░███░░███  ░░░░░███ 
 ░███░░░░░░   ░███ ░░░ ░███ ░███ ░░░█████░   ░███  ░███ ░███ ░███   ███████ 
 ░███         ░███     ░███ ░███  ███░░░███  ░███  ░███ ░███ ░███  ███░░███ 
 █████        █████    ░░██████  █████ █████ █████ █████░███ █████░░████████
░░░░░        ░░░░░      ░░░░░░  ░░░░░ ░░░░░ ░░░░░ ░░░░░ ░░░ ░░░░░  ░░░░░░░░ 
"""

        self.label_ascii = ctk.CTkLabel(
            self.console_frame,
            text="",
            font=("Consolas", 14),
            text_color="#00ff00",
            justify="left",
        )
        self.label_ascii.place(relx=0.5, rely=0.4, anchor="center")

        self.label_status = ctk.CTkLabel(
            self.console_frame,
            text="",
            font=("Consolas", 12),
            text_color="white",
        )
        self.label_status.place(relx=0.5, rely=0.6, anchor="center")

        self.after(500, lambda: self.type_text(self.label_ascii, ascii_art, 0))
        self.after(2500, lambda: self.label_status.configure(text="starting Proxima..."))
        self.after(4000, self.transition_to_main_gui)

    def type_text(self, label, text, index):
        if index < len(text):
            label.configure(text=text[: index + 1])
            self.after(3, lambda: self.type_text(label, text, index + 5))

    def transition_to_main_gui(self):
        self.console_frame.destroy()
        hide_console()
        self.build_main_gui()

    def toggle_visibility(self):
        if state.window_hidden:
            self.after(0, self.deiconify)
            state.window_hidden = False
        else:
            self.after(0, self.withdraw)
            state.window_hidden = True

    def start_binding(self, callback_func, btn_widget):
        if self.binding_mode:
            return
        self.binding_mode = True
        self.binding_target_func = callback_func
        self.binding_button_ref = btn_widget
        self.binding_button_ref.configure(text="...", fg_color="#cc0000")
        self.focus_set()

    def finish_binding(self, key_str):
        if self.binding_target_func:
            self.binding_target_func(key_str)

        if self.binding_button_ref:
            display_text = key_str.replace("Key.", "").upper()
            if len(display_text) > 6:
                display_text = display_text[:6]
            self.binding_button_ref.configure(text=display_text, fg_color="#2b2d31")

        self.binding_mode = False
        self.binding_target_func = None
        self.binding_button_ref = None

    def start_drag(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def do_drag(self, event):
        x = self.winfo_x() + event.x - self._drag_start_x
        y = self.winfo_y() + event.y - self._drag_start_y
        self.geometry(f"+{x}+{y}")

    def build_main_gui(self):
        outer_frame = ctk.CTkFrame(self, fg_color="#0a0a0a", corner_radius=20)
        outer_frame.pack(fill="both", expand=True, padx=0, pady=0)

        self.main_container = ctk.CTkFrame(outer_frame, fg_color="#1a1a1a", corner_radius=15)
        self.main_container.pack(fill="both", expand=True, padx=2, pady=2)

        self.titlebar = ctk.CTkFrame(self.main_container, height=40, fg_color="#0f0f0f", corner_radius=0)
        self.titlebar.pack(fill="x", side="top")
        self.titlebar.pack_propagate(False)

        self.titlebar.bind("<Button-1>", self.start_drag)
        self.titlebar.bind("<B1-Motion>", self.do_drag)

        title_left = ctk.CTkFrame(self.titlebar, fg_color="transparent")
        title_left.pack(side="left", padx=15)

        app_title = ctk.CTkLabel(title_left, text="Proxima", font=("Arial", 16, "bold"), text_color="#ffffff")
        app_title.pack(side="left", padx=(0, 10))
        app_title.bind("<Button-1>", self.start_drag)
        app_title.bind("<B1-Motion>", self.do_drag)

        credits = ctk.CTkLabel(title_left, text="By bzpass", font=("Arial", 11), text_color="#6a6a6a")
        credits.pack(side="left")
        credits.bind("<Button-1>", self.start_drag)
        credits.bind("<B1-Motion>", self.do_drag)

        btn_frame = ctk.CTkFrame(self.titlebar, fg_color="transparent")
        btn_frame.pack(side="right", padx=10)

        btn_minimize = ctk.CTkButton(
            btn_frame,
            text="—",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color="#2b2d31",
            command=self.iconify,
            corner_radius=6,
            font=("Segoe UI", 13, "bold"),
        )
        btn_minimize.pack(side="left", padx=2)

        btn_close = ctk.CTkButton(
            btn_frame,
            text="×",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color="#cc0000",
            text_color="#ffffff",
            command=self.quit,
            corner_radius=6,
            font=("Segoe UI", 16, "bold"),
        )
        btn_close.pack(side="left", padx=2)

        content_frame = ctk.CTkFrame(self.main_container, fg_color="#1a1a1a")
        content_frame.pack(fill="both", expand=True, padx=0, pady=0)

        self.sidebar = ctk.CTkFrame(content_frame, width=180, fg_color="#141414", corner_radius=0)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)

        sidebar_header = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        sidebar_header.pack(fill="x", pady=20, padx=20)

        ctk.CTkLabel(sidebar_header, text="MACROS", font=("Arial", 11, "bold"), text_color="#6a6a6a").pack(anchor="w")

        self.btn_macros = ctk.CTkButton(
            self.sidebar,
            text="Crystal",
            height=35,
            fg_color="#2b2d31",
            hover_color="#3b3d41",
            font=("Arial", 13),
            corner_radius=8,
            anchor="w",
            command=self.show_macros_tab,
        )
        self.btn_macros.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(self.sidebar, text="OTHER", font=("Arial", 11, "bold"), text_color="#6a6a6a").pack(
            anchor="w", padx=20, pady=(20, 10)
        )

        self.btn_config = ctk.CTkButton(
            self.sidebar,
            text="Settings",
            height=35,
            fg_color="transparent",
            hover_color="#2b2d31",
            font=("Arial", 13),
            corner_radius=8,
            anchor="w",
            command=self.show_config_tab,
        )
        self.btn_config.pack(fill="x", padx=15, pady=5)

        self.main_area = ctk.CTkScrollableFrame(content_frame, fg_color="#1a1a1a", corner_radius=0)
        self.main_area.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        self.create_macro_frame()
        self.create_config_frame()
        self.show_macros_tab()

    def create_macro_frame(self):
        self.macro_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")

        header_frame = ctk.CTkFrame(self.macro_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(header_frame, text="Crystal Macros", font=("Arial", 22, "bold"), text_color="#ffffff").pack(
            side="left"
        )
        ctk.CTkLabel(
            header_frame, text="Configure your end crystal PVP automation", font=("Arial", 12), text_color="#6a6a6a"
        ).pack(side="left", padx=(15, 0))

        self.var_hc = ctk.BooleanVar(value=state.hc_enabled)
        self.var_kp = ctk.BooleanVar(value=state.kp_enabled)
        self.var_aa = ctk.BooleanVar(value=state.aa_enabled)

        self.hc_delay_label = None
        self.kp_delay_label = None
        self.aa_delay_label = None

        self.create_macro_card(
            "HC",
            "Hit Crystal",
            "Auto place obsidian and hit crystal",
            self.var_hc,
            state.hc_bind,
            lambda k: setattr(state, "hc_bind", k),
            "hc",
            [
                ("Keybind", state.hc_bind, lambda k: setattr(state, "hc_bind", k)),
                ("Crystal Slot", state.hc_slot_1, lambda k: setattr(state, "hc_slot_1", k)),
                ("Obsidian Slot", state.hc_slot_2, lambda k: setattr(state, "hc_slot_2", k)),
            ],
        )

        self.create_macro_card(
            "KP",
            "Key Pearl",
            "Auto throws a enderpearl in the direction you're looking at",
            self.var_kp,
            state.kp_bind,
            lambda k: setattr(state, "kp_bind", k),
            "kp",
            [
                ("Keybind", state.kp_bind, lambda k: setattr(state, "kp_bind", k)),
                ("Pearl Slot", state.kp_key_1, lambda k: setattr(state, "kp_key_1", k)),
                ("Switch Back Slot", state.kp_key_2, lambda k: setattr(state, "kp_key_2", k)),
            ],
        )

        self.create_macro_card(
            "AA",
            "Auto Anchor",
            "Anchors automatically with just one button press",
            self.var_aa,
            state.aa_bind,
            lambda k: setattr(state, "aa_bind", k),
            "aa",
            [
                ("Keybind", state.aa_bind, lambda k: setattr(state, "aa_bind", k)),
                ("Anchor Slot", state.aa_key_1, lambda k: setattr(state, "aa_key_1", k)),
                ("Glowstone Slot", state.aa_key_2, lambda k: setattr(state, "aa_key_2", k)),
                ("Exploding Item", state.aa_key_3, lambda k: setattr(state, "aa_key_3", k)),
            ],
        )

    def create_macro_card(self, icon_text, title, description, var, bind_val, update_bind_func, macro_type, settings):
        card = ctk.CTkFrame(self.macro_frame, fg_color="#0f0f0f", corner_radius=12)
        card.pack(fill="x", pady=(0, 15))

        card_inner = ctk.CTkFrame(card, fg_color="transparent")
        card_inner.pack(fill="both", expand=True, padx=20, pady=20)

        header_frame = ctk.CTkFrame(card_inner, fg_color="transparent")
        header_frame.pack(fill="x")

        left_side = ctk.CTkFrame(header_frame, fg_color="transparent")
        left_side.pack(side="left", fill="x", expand=True)

        icon_frame = ctk.CTkFrame(left_side, fg_color="#2b5a8f", corner_radius=8, width=40, height=40)
        icon_frame.pack(side="left")
        icon_frame.pack_propagate(False)

        ctk.CTkLabel(icon_frame, text=icon_text, font=("Arial", 14, "bold"), text_color="#ffffff").place(
            relx=0.5, rely=0.5, anchor="center"
        )

        title_frame = ctk.CTkFrame(left_side, fg_color="transparent")
        title_frame.pack(side="left", padx=(12, 0))

        ctk.CTkLabel(title_frame, text=title, font=("Arial", 15, "bold"), text_color="#ffffff").pack(anchor="w")
        ctk.CTkLabel(title_frame, text=description, font=("Arial", 11), text_color="#6a6a6a").pack(anchor="w")

        toggle_switch = ctk.CTkSwitch(
            header_frame,
            text="",
            width=48,
            height=24,
            variable=var,
            onvalue=True,
            offvalue=False,
            command=self.update_states,
            fg_color="#3a3a3a",
            progress_color="#4a9eff",
            button_color="#ffffff",
            button_hover_color="#e0e0e0",
            corner_radius=999,
            border_width=0,
            bg_color="transparent"
        )
        toggle_switch.pack(side="right")

        settings_frame = ctk.CTkFrame(card_inner, fg_color="transparent")
        settings_frame.pack(fill="x", pady=(20, 0))
        settings_frame.grid_columnconfigure(0, weight=1)
        settings_frame.grid_columnconfigure(1, weight=1)

        for idx, (label, value, update_func) in enumerate(settings):
            row = idx // 2
            col = idx % 2

            setting_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
            setting_frame.grid(
                row=row,
                column=col,
                sticky="ew",
                padx=(0, 15) if col == 0 else (0, 0),
                pady=(0, 12),
            )

            ctk.CTkLabel(setting_frame, text=label, font=("Arial", 11), text_color="#8a8a8a").pack(anchor="w")

            if update_func:
                display_text = value.replace("Key.", "").upper()
                if len(display_text) > 8:
                    display_text = display_text[:8]

                btn = ctk.CTkButton(
                    setting_frame,
                    text=display_text,
                    height=32,
                    fg_color="#2b2d31",
                    hover_color="#3b3d41",
                    font=("Arial", 12),
                    corner_radius=6,
                )
                btn.configure(command=lambda b=btn, f=update_func: self.start_binding(f, b))
                btn.pack(fill="x", pady=(5, 0))

        delay_frame = ctk.CTkFrame(card_inner, fg_color="transparent")
        delay_frame.pack(fill="x", pady=(8, 0))

        delay_label_frame = ctk.CTkFrame(delay_frame, fg_color="transparent")
        delay_label_frame.pack(fill="x", pady=(0, 5))

        ctk.CTkLabel(delay_label_frame, text="Delay (MS)", font=("Arial", 11), text_color="#8a8a8a").pack(
            side="left"
        )

        if macro_type == "hc":
            delay_val = state.hc_delay_ms
            self.hc_delay_label = ctk.CTkLabel(
                delay_label_frame, text=f"{delay_val} ms", font=("Arial", 11, "bold"), text_color="#4a9eff"
            )
            self.hc_delay_label.pack(side="right")

            slider = ctk.CTkSlider(
                delay_frame,
                from_=10,
                to=200,
                number_of_steps=190,
                command=lambda v: self.update_hc_delay(v),
                button_color="#4a9eff",
                button_hover_color="#5eb0ff",
                progress_color="#2b5a8f",
            )
            slider.set(delay_val)
            slider.pack(fill="x")

        elif macro_type == "kp":
            delay_val = state.kp_delay_ms
            self.kp_delay_label = ctk.CTkLabel(
                delay_label_frame, text=f"{delay_val} ms", font=("Arial", 11, "bold"), text_color="#4a9eff"
            )
            self.kp_delay_label.pack(side="right")

            slider = ctk.CTkSlider(
                delay_frame,
                from_=10,
                to=200,
                number_of_steps=190,
                command=lambda v: self.update_kp_delay(v),
                button_color="#4a9eff",
                button_hover_color="#5eb0ff",
                progress_color="#2b5a8f",
            )
            slider.set(delay_val)
            slider.pack(fill="x")

        elif macro_type == "aa":
            delay_val = state.aa_delay_ms
            self.aa_delay_label = ctk.CTkLabel(
                delay_label_frame, text=f"{delay_val} ms", font=("Arial", 11, "bold"), text_color="#4a9eff"
            )
            self.aa_delay_label.pack(side="right")

            slider = ctk.CTkSlider(
                delay_frame,
                from_=10,
                to=200,
                number_of_steps=190,
                command=lambda v: self.update_aa_delay(v),
                button_color="#4a9eff",
                button_hover_color="#5eb0ff",
                progress_color="#2b5a8f",
            )
            slider.set(delay_val)
            slider.pack(fill="x")

    def update_hc_delay(self, value):
        val = int(value)
        state.hc_delay_ms = val
        if self.hc_delay_label:
            self.hc_delay_label.configure(text=f"{val} ms")

    def update_kp_delay(self, value):
        val = int(value)
        state.kp_delay_ms = val
        if self.kp_delay_label:
            self.kp_delay_label.configure(text=f"{val} ms")

    def update_aa_delay(self, value):
        val = int(value)
        state.aa_delay_ms = val
        if self.aa_delay_label:
            self.aa_delay_label.configure(text=f"{val} ms")

    def create_config_frame(self):
        self.config_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")

        header_frame = ctk.CTkFrame(self.config_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(header_frame, text="Settings", font=("Arial", 22, "bold"), text_color="#ffffff").pack(
            side="left"
        )

        general_card = ctk.CTkFrame(self.config_frame, fg_color="#0f0f0f", corner_radius=12)
        general_card.pack(fill="x", pady=(0, 15))

        general_inner = ctk.CTkFrame(general_card, fg_color="transparent")
        general_inner.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(general_inner, text="General Settings", font=("Arial", 16, "bold"), text_color="#ffffff").pack(
            anchor="w", pady=(0, 15)
        )

        hide_frame = ctk.CTkFrame(general_inner, fg_color="transparent")
        hide_frame.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(hide_frame, text="Hide Window Key", font=("Arial", 11), text_color="#8a8a8a").pack(anchor="w")

        self.btn_hide_bind = ctk.CTkButton(
            hide_frame,
            text="INSERT",
            height=32,
            fg_color="#2b2d31",
            hover_color="#3b3d41",
            font=("Arial", 12),
            corner_radius=6,
        )
        self.btn_hide_bind.configure(command=lambda: self.start_binding(lambda k: setattr(state, "hide_key", k), self.btn_hide_bind))
        self.btn_hide_bind.pack(fill="x", pady=(5, 0))

        keys_frame = ctk.CTkFrame(general_inner, fg_color="transparent")
        keys_frame.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(keys_frame, text="Valid Switch Keys (Comma separated)", font=("Arial", 11), text_color="#8a8a8a").pack(
            anchor="w"
        )

        self.entry_valid_keys = ctk.CTkEntry(keys_frame, height=32, fg_color="#2b2d31", border_width=0, font=("Arial", 12))
        self.entry_valid_keys.insert(0, ",".join(state.valid_switch_keys))
        self.entry_valid_keys.pack(fill="x", pady=(5, 10))

        ctk.CTkButton(
            keys_frame,
            text="Update Valid Keys",
            height=32,
            fg_color="#4a9eff",
            hover_color="#5eb0ff",
            font=("Arial", 12, "bold"),
            corner_radius=6,
            command=self.save_valid_keys,
        ).pack(fill="x")

        profile_card = ctk.CTkFrame(self.config_frame, fg_color="#0f0f0f", corner_radius=12)
        profile_card.pack(fill="x", pady=(0, 15))

        profile_inner = ctk.CTkFrame(profile_card, fg_color="transparent")
        profile_inner.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(profile_inner, text="Profile Management", font=("Arial", 16, "bold"), text_color="#ffffff").pack(
            anchor="w", pady=(0, 15)
        )

        btn_row = ctk.CTkFrame(profile_inner, fg_color="transparent")
        btn_row.pack(fill="x")
        btn_row.grid_columnconfigure(0, weight=1)
        btn_row.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            btn_row,
            text="Export Profile",
            height=35,
            fg_color="#2b5a8f",
            hover_color="#3b6a9f",
            font=("Arial", 12, "bold"),
            corner_radius=6,
            command=self.export_config,
        ).grid(row=0, column=0, sticky="ew", padx=(0, 8))

        ctk.CTkButton(
            btn_row,
            text="Import Profile",
            height=35,
            fg_color="#2b5a8f",
            hover_color="#3b6a9f",
            font=("Arial", 12, "bold"),
            corner_radius=6,
            command=self.import_config,
        ).grid(row=0, column=1, sticky="ew")

    def show_macros_tab(self):
        self.config_frame.pack_forget()
        self.macro_frame.pack(fill="both", expand=True)
        self.btn_macros.configure(fg_color="#2b2d31")
        self.btn_config.configure(fg_color="transparent")

    def show_config_tab(self):
        self.macro_frame.pack_forget()
        self.config_frame.pack(fill="both", expand=True)
        self.btn_config.configure(fg_color="#2b2d31")
        self.btn_macros.configure(fg_color="transparent")

    def update_states(self):
        state.hc_enabled = self.var_hc.get()
        state.kp_enabled = self.var_kp.get()
        state.aa_enabled = self.var_aa.get()

    def save_valid_keys(self):
        raw = self.entry_valid_keys.get()
        state.valid_switch_keys = [k.strip() for k in raw.split(",") if k.strip()]
        print(f"Valid keys updated: {state.valid_switch_keys}")

    def export_config(self):
        cfg = {
            "hc_bind": state.hc_bind,
            "kp_bind": state.kp_bind,
            "aa_bind": state.aa_bind,
            "hc_delay_ms": state.hc_delay_ms,
            "kp_delay_ms": state.kp_delay_ms,
            "aa_delay_ms": state.aa_delay_ms,
            "valid_keys": state.valid_switch_keys,
            "hide_key": state.hide_key,
            "hc_slots": [state.hc_slot_1, state.hc_slot_2],
            "kp_keys": [state.kp_key_1, state.kp_key_2],
            "aa_keys": [state.aa_key_1, state.aa_key_2, state.aa_key_3],
        }

        js = json.dumps(cfg)
        self.clipboard_clear()
        self.clipboard_append(js)
        print("Config copied to clipboard")

    def import_config(self):
        try:
            content = self.clipboard_get()
            cfg = json.loads(content)

            state.hc_bind = cfg.get("hc_bind", state.hc_bind)
            state.kp_bind = cfg.get("kp_bind", state.kp_bind)
            state.aa_bind = cfg.get("aa_bind", state.aa_bind)

            state.hc_delay_ms = cfg.get("hc_delay_ms", 85)
            state.kp_delay_ms = cfg.get("kp_delay_ms", 85)
            state.aa_delay_ms = cfg.get("aa_delay_ms", 85)

            state.valid_switch_keys = cfg.get("valid_keys", state.valid_switch_keys)
            state.hide_key = cfg.get("hide_key", state.hide_key)

            if "hc_slots" in cfg:
                state.hc_slot_1, state.hc_slot_2 = cfg["hc_slots"]
            if "kp_keys" in cfg:
                state.kp_key_1, state.kp_key_2 = cfg["kp_keys"]
            if "aa_keys" in cfg:
                state.aa_key_1, state.aa_key_2, state.aa_key_3 = cfg["aa_keys"]

            self.macro_frame.destroy()
            self.config_frame.destroy()
            self.create_macro_frame()
            self.create_config_frame()
            self.show_macros_tab()

            print("Config imported successfully")
        except Exception as e:
            print(f"Import failed: {e}")

if __name__ == "__main__":
    try:
        myappid = 'bravebrowser.1'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    app = ProximaApp()
    app.mainloop()


