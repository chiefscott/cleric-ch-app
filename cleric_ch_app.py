from tkinter import ttk, filedialog, messagebox, simpledialog
import tkinter as tk
import os
import re

class ClericCHApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Everquest Cleric CH Chain Assistant")
        self.root.geometry("600x400")

        self.log_file_path = ""
        self.clerics = [] # List of cleric aliases
        self.assignments = {} # Dict mapping chain number to cleric alias
        self.fluffers = [] # List of fluffer aliases
        self.selected_seconds = "2" # Default timing
        self.selected_slow_seconds = "4" # Default slow timing
        self.is_slowable = False
        self.selected_cleric_channel = "2" # Default cleric channel
        
        # For Macro Shout Channel Dropdown (Feature 2) - Corrected with "Say"
        self.macro_shout_options_map = {"Shout": "/shout", "Guild": "/gu", "Group": "/g", "Say": "/say", "Cleric Channel": "dynamic_cleric_channel"}
        self.selected_macro_shout_command = "/shout" # Default actual command to use

        # Load saved settings (like log file path and cleric channel)
        self.load_settings()

        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")

        # Setup Tab
        self.setup_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.setup_frame, text="Setup")
        self.create_setup_tab(self.setup_frame)

        # Assignments Tab
        self.assignments_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.assignments_frame, text="Assignments")
        self.create_assignments_tab(self.assignments_frame)

        # Macros Tab
        self.macros_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.macros_frame, text="Macros")
        self.create_macros_tab(self.macros_frame)

        # Console Tab
        self.console_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.console_frame, text="Console")
        self.create_console_tab(self.console_frame)

    def create_console_tab(self, frame):
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        console_text_frame = ttk.Frame(frame)
        console_text_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 5))
        console_text_frame.rowconfigure(0, weight=1)
        console_text_frame.columnconfigure(0, weight=1)

        self.console_scrollbar = ttk.Scrollbar(console_text_frame, orient=tk.VERTICAL)
        self.console_text_widget = tk.Text(
            console_text_frame, 
            wrap=tk.WORD, 
            state=tk.DISABLED, 
            height=10, 
            yscrollcommand=self.console_scrollbar.set
        )
        self.console_scrollbar.config(command=self.console_text_widget.yview)
        
        self.console_text_widget.grid(row=0, column=0, sticky="nsew")
        self.console_scrollbar.grid(row=0, column=1, sticky="ns")

        buttons_frame = ttk.Frame(frame)
        buttons_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(5,0))
        
        copy_button = ttk.Button(buttons_frame, text="Copy Log", command=self.copy_console_log)
        copy_button.pack(side=tk.LEFT, padx=(0,5))
        
        clear_button = ttk.Button(buttons_frame, text="Clear Console", command=self.clear_console_log)
        clear_button.pack(side=tk.LEFT)

    def log_to_console(self, message):
        if not hasattr(self, 'console_text_widget'): 
            return
        try:
            self.console_text_widget.config(state=tk.NORMAL)
            self.console_text_widget.insert(tk.END, str(message) + "\n")
            self.console_text_widget.see(tk.END)
            self.console_text_widget.config(state=tk.DISABLED)
        except tk.TclError: 
            pass

    def copy_console_log(self):
        if not hasattr(self, 'console_text_widget'):
            return
        log_content = self.console_text_widget.get(1.0, tk.END).strip()
        if log_content:
            self.root.clipboard_clear()
            self.root.clipboard_append(log_content)
            messagebox.showinfo("Copied", "Console log copied to clipboard.")
        else:
            messagebox.showinfo("Empty", "Console log is empty.")

    def clear_console_log(self):
        if not hasattr(self, 'console_text_widget'):
            return
        self.console_text_widget.config(state=tk.NORMAL)
        self.console_text_widget.delete(1.0, tk.END)
        self.console_text_widget.config(state=tk.DISABLED)
        self.log_to_console("Console cleared.")

    def create_setup_tab(self, frame):
        log_file_label = ttk.Label(frame, text="Everquest Log File:")
        log_file_label.grid(row=0, column=0, sticky="w", pady=5, padx=5)

        self.log_file_entry = ttk.Entry(frame, width=50)
        self.log_file_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
        self.log_file_entry.insert(0, self.log_file_path)

        log_file_button = ttk.Button(frame, text="Browse", command=self.browse_log_file)
        log_file_button.grid(row=0, column=2, sticky="w", pady=5, padx=5)

        trigger_label = ttk.Label(frame, text="Cleric Who Trigger:")
        trigger_label.grid(row=1, column=0, sticky="w", pady=5, padx=5)

        self.trigger_entry = ttk.Entry(frame, width=50)
        self.trigger_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
        self.trigger_entry.insert(0, "<CLERIC CH WHO>") 

        cleric_channel_label = ttk.Label(frame, text="Cleric Channel:")
        cleric_channel_label.grid(row=2, column=0, sticky="w", pady=5, padx=5)

        self.cleric_channel_options = [str(i) for i in range(1, 10)] 
        self.selected_cleric_channel_var = tk.StringVar(value=self.selected_cleric_channel)
        self.cleric_channel_dropdown = ttk.Combobox(
            frame,
            textvariable=self.selected_cleric_channel_var,
            values=self.cleric_channel_options,
            state="readonly",
            width=5 
        )
        self.cleric_channel_dropdown.grid(row=2, column=1, sticky="w", pady=5, padx=5) 
        self.cleric_channel_dropdown.bind("<<ComboboxSelected>>", self.on_cleric_channel_selected)

        clear_button = ttk.Button(frame, text="Clear All", command=self.clear_all)
        clear_button.grid(row=3, column=0, sticky="w", pady=10, padx=5)

    def create_assignments_tab(self, frame):
        cleric_who_button = ttk.Button(frame, text="Cleric Who", command=self.gather_clerics)
        cleric_who_button.grid(row=0, column=0, sticky="w", pady=5, padx=5)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=0, column=1, columnspan=2, sticky="w", pady=5, padx=0) 

        add_cleric_button = ttk.Button(button_frame, text="Add Cleric", command=self.add_cleric)
        add_cleric_button.pack(side=tk.LEFT, padx=5)

        remove_cleric_button = ttk.Button(button_frame, text="Remove Selected", command=self.remove_cleric)
        remove_cleric_button.pack(side=tk.LEFT, padx=5)

        clerics_label = ttk.Label(frame, text="Clerics:")
        clerics_label.grid(row=1, column=0, sticky="w", pady=5, padx=5)

        clerics_list_frame = ttk.Frame(frame)
        clerics_list_frame.grid(row=2, column=0, sticky="nsew", pady=5, padx=5)
        clerics_list_frame.rowconfigure(0, weight=1)
        clerics_list_frame.columnconfigure(0, weight=1)

        self.clerics_scrollbar = ttk.Scrollbar(clerics_list_frame, orient=tk.VERTICAL)
        self.clerics_listbox = tk.Listbox(clerics_list_frame, width=30, height=10, exportselection=False, yscrollcommand=self.clerics_scrollbar.set)
        self.clerics_scrollbar.config(command=self.clerics_listbox.yview)
        
        self.clerics_listbox.grid(row=0, column=0, sticky="nsew")
        self.clerics_scrollbar.grid(row=0, column=1, sticky="ns")

        cleric_buttons_frame = ttk.Frame(frame)
        cleric_buttons_frame.grid(row=2, column=1, sticky="ns", padx=(0,5), pady=5)

        move_up_button = ttk.Button(cleric_buttons_frame, text="Move Up", command=self.move_cleric_up)
        move_up_button.pack(pady=2, fill=tk.X)
        move_down_button = ttk.Button(cleric_buttons_frame, text="Move Down", command=self.move_cleric_down)
        move_down_button.pack(pady=2, fill=tk.X)

        fluffer_actions_frame = ttk.Frame(frame)
        fluffer_actions_frame.grid(row=2, column=2, sticky="ns", padx=(0,5), pady=5) 

        move_to_fluffers_button = ttk.Button(fluffer_actions_frame, text=">> Fluffers", command=self.move_to_fluffers)
        move_to_fluffers_button.pack(pady=2, fill=tk.X)
        move_to_chain_button = ttk.Button(fluffer_actions_frame, text="<< Chain", command=self.move_to_chain)
        move_to_chain_button.pack(pady=2, fill=tk.X)

        fluffers_label = ttk.Label(frame, text="Fluffers:")
        fluffers_label.grid(row=1, column=3, sticky="w", pady=5, padx=5) 

        fluffers_list_frame = ttk.Frame(frame)
        fluffers_list_frame.grid(row=2, column=3, sticky="nsew", pady=5, padx=5) 
        fluffers_list_frame.rowconfigure(0, weight=1)
        fluffers_list_frame.columnconfigure(0, weight=1)

        self.fluffers_scrollbar = ttk.Scrollbar(fluffers_list_frame, orient=tk.VERTICAL)
        self.fluffers_listbox = tk.Listbox(fluffers_list_frame, width=30, height=10, exportselection=False, yscrollcommand=self.fluffers_scrollbar.set)
        self.fluffers_scrollbar.config(command=self.fluffers_listbox.yview)

        self.fluffers_listbox.grid(row=0, column=0, sticky="nsew")
        self.fluffers_scrollbar.grid(row=0, column=1, sticky="ns")

        self.clerics_listbox.bind("<<ListboxSelect>>", self.on_listbox_select)
        self.fluffers_listbox.bind("<<ListboxSelect>>", self.on_listbox_select)
        self.fluffers_listbox.bind("<ButtonPress-1>", self.start_drag)
        self.fluffers_listbox.bind("<B1-Motion>", self.drag_motion)
        self.fluffers_listbox.bind("<ButtonRelease-1>", self.drop)
        self.clerics_listbox.bind("<ButtonPress-1>", self.start_drag)
        self.clerics_listbox.bind("<B1-Motion>", self.drag_motion)
        self.clerics_listbox.bind("<ButtonRelease-1>", self.drop)

        self.drag_data = {"item": None, "origin_listbox": None}

        self.slowable_var = tk.BooleanVar()
        slowable_checkbox = ttk.Checkbutton(frame, text="Slowable?", variable=self.slowable_var, command=self.toggle_slow_timing)
        slowable_checkbox.grid(row=3, column=0, sticky="w", pady=5, padx=5)

        seconds_label = ttk.Label(frame, text="Chain Timing (sec):")
        seconds_label.grid(row=4, column=0, sticky="w", pady=5, padx=5)
        self.seconds_options = ["Custom", "1", "1.1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5", "5.5", "6"]
        self.selected_seconds_var = tk.StringVar(value=self.selected_seconds)
        self.seconds_dropdown = ttk.Combobox(frame, textvariable=self.selected_seconds_var, values=self.seconds_options, state="readonly")
        self.seconds_dropdown.grid(row=4, column=1, sticky="w", pady=5, padx=5)
        self.seconds_dropdown.bind("<<ComboboxSelected>>", self.on_timing_selected)

        self.slow_seconds_label = ttk.Label(frame, text="Slow Timing (sec):")
        self.selected_slow_seconds_var = tk.StringVar(value=self.selected_slow_seconds)
        self.slow_seconds_dropdown = ttk.Combobox(frame, textvariable=self.selected_slow_seconds_var, values=self.seconds_options, state="readonly")
        self.slow_seconds_dropdown.bind("<<ComboboxSelected>>", self.on_slow_timing_selected)
        # Note: toggle_slow_timing will grid/grid_forget this based on checkbox

        # Macro Shout Channel Dropdown - Corrected row
        macro_shout_label = ttk.Label(frame, text="Macro Announce Via:")
        macro_shout_label.grid(row=6, column=0, sticky="w", pady=5, padx=5) # Moved to row 6
        
        self.macro_shout_display_options = list(self.macro_shout_options_map.keys())
        self.selected_macro_shout_display_var = tk.StringVar(value="Shout") 
        self.macro_shout_dropdown = ttk.Combobox(
            frame, 
            textvariable=self.selected_macro_shout_display_var, 
            values=self.macro_shout_display_options, 
            state="readonly"
        )
        self.macro_shout_dropdown.grid(row=6, column=1, sticky="w", pady=5, padx=5) # Moved to row 6
        self.macro_shout_dropdown.bind("<<ComboboxSelected>>", self.on_macro_shout_channel_selected)

        # Generate/Refresh Macros Button - Corrected row
        refresh_macros_button = ttk.Button(frame, text="Generate/Refresh Macros", command=self.refresh_all_macros_and_message)
        refresh_macros_button.grid(row=8, column=0, columnspan=2, sticky="w", pady=10, padx=5) # Moved to row 8

        frame.columnconfigure(0, weight=1) 
        frame.columnconfigure(3, weight=1) 
        frame.rowconfigure(2, weight=1) 

    def create_macros_tab(self, frame):
        assignments_message_label = ttk.Label(frame, text="Assignments Message Lines:")
        assignments_message_label.grid(row=0, column=0, sticky="w", pady=5, padx=5, columnspan=2)

        self.assignments_lines_frame = ttk.Frame(frame)
        self.assignments_lines_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5, padx=5) 
        self.assignments_lines_frame.columnconfigure(0, weight=1)

        macros_label = ttk.Label(frame, text="Individual Macros:")
        macros_label.grid(row=2, column=0, sticky="w", pady=(10,5), padx=5, columnspan=2) 

        macros_canvas_frame = ttk.Frame(frame)
        macros_canvas_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=5, padx=5)
        macros_canvas_frame.rowconfigure(0, weight=1)
        macros_canvas_frame.columnconfigure(0, weight=1)

        self.macros_canvas = tk.Canvas(macros_canvas_frame)
        self.macros_scrollbar = ttk.Scrollbar(macros_canvas_frame, orient="vertical", command=self.macros_canvas.yview)
        self.macros_frame_inner = ttk.Frame(self.macros_canvas) 

        self.macros_frame_inner.bind(
            "<Configure>",
            lambda e: self.macros_canvas.configure(
                scrollregion=self.macros_canvas.bbox("all")
            )
        )

        self.macros_canvas.create_window((0, 0), window=self.macros_frame_inner, anchor="nw")
        self.macros_canvas.configure(yscrollcommand=self.macros_scrollbar.set)

        self.macros_canvas.grid(row=0, column=0, sticky="nsew")
        self.macros_scrollbar.grid(row=0, column=1, sticky="ns")
        
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(3, weight=1) 

    def browse_log_file(self):
        filename = filedialog.askopenfilename(
            initialdir=os.path.dirname(self.log_file_path) if self.log_file_path else os.path.expanduser("~"),
            title="Select Everquest Log File",
            filetypes=(("Log files", "*.txt"), ("All files", "*.*"))
        )
        if filename:
            self.log_file_path = filename
            self.log_file_entry.delete(0, tk.END)
            self.log_file_entry.insert(0, self.log_file_path)
            self.save_settings()

    def gather_clerics(self):
        if not self.log_file_path or not os.path.exists(self.log_file_path):
            messagebox.showwarning("Warning", "Please select a valid log file first.")
            self.log_to_console("Gather Clerics: Log file path not set or invalid.")
            return
        
        self.log_to_console("--- Starting New Cleric Gather ---")
        self.log_to_console(f"Log File: {self.log_file_path}")
        trigger = self.trigger_entry.get()
        self.log_to_console(f"Trigger Phrase: {trigger}")

        clerics = self.parse_log_for_clerics(self.log_file_path, trigger)
        self.log_to_console(f"Parse_log_for_clerics returned: {clerics}")

        if not clerics:
            messagebox.showinfo("Info", f"No clerics found after the trigger '{trigger}'.")
            self.clerics = []
        else:
            self.clerics = clerics
            messagebox.showinfo("Success", f"Found {len(self.clerics)} clerics.")

        self.update_assignments_listbox()
        self.assignments = {} 
        self.fluffers = [] 
        self.update_fluffers_listbox()
        self.generate_assignments() 
        self.update_macros_tab() 

    def _reverse_readline(self, filename, buf_size=8192):
        try:
            with open(filename, 'rb') as fh:
                segment = None
                offset = 0
                fh.seek(0, os.SEEK_END)
                file_size = remaining_size = fh.tell()
                while remaining_size > 0:
                    offset = min(file_size, offset + buf_size)
                    fh.seek(file_size - offset)
                    buffer_bytes = fh.read(min(remaining_size, buf_size))
                    remaining_size -= buf_size
                    
                    try:
                        buffer_str = buffer_bytes.decode('utf-8')
                    except UnicodeDecodeError:
                        try:
                            buffer_str = buffer_bytes.decode('latin-1') 
                        except UnicodeDecodeError:
                            buffer_str = buffer_bytes.decode('ascii', errors='ignore') 

                    lines = buffer_str.splitlines()

                    if segment is not None:
                        if buffer_str[-1] != '\n' and lines: 
                            lines[-1] += segment
                        else:
                            yield segment
                    
                    if lines: 
                        segment = lines[0]
                    else: 
                        if segment is not None: 
                            yield segment
                        segment = None 
                        continue

                    for index in range(len(lines) - 1, 0, -1):
                        if lines[index]:
                            yield lines[index]
                if segment is not None: 
                    yield segment
        except FileNotFoundError:
            messagebox.showerror("Error", f"Log file not found: {filename}")
            yield from () 
        except Exception as e:
            messagebox.showerror("Error", f"Error reading log file in _reverse_readline: {e}")
            yield from ()

    def parse_log_for_clerics(self, log_path, trigger):
        clerics_found = []
        lines_after_trigger_reversed = []
        trigger_found_in_log = False
        
        self.log_to_console(f"Starting reverse read for trigger: '{trigger}' in '{log_path}'")

        try:
            if not os.path.exists(log_path):
                messagebox.showerror("Error", f"Log file not found: {log_path}")
                self.log_to_console(f"ERROR: Log file not found: {log_path}")
                return []

            for line_idx, line in enumerate(self._reverse_readline(filename=log_path)):
                if trigger in line:
                    self.log_to_console(f"Trigger '{trigger}' found in line: {line}")
                    trigger_found_in_log = True
                    break
                lines_after_trigger_reversed.append(line)
            self.log_to_console(f"Finished reverse read. Trigger found: {trigger_found_in_log}. Lines collected before trigger (reversed order): {len(lines_after_trigger_reversed)}")

        except Exception as e: 
            messagebox.showerror("Error", f"An error occurred while parsing the log: {e}")
            self.log_to_console(f"ERROR during log parsing (reverse read): {e}")
            return []

        if not trigger_found_in_log:
            self.log_to_console("Trigger not found in the entire log during reverse scan.")
            return [] 

        actual_lines_after_trigger = lines_after_trigger_reversed[::-1]
        self.log_to_console(f"Lines to process (chronological order, after trigger): {len(actual_lines_after_trigger)}")
        if len(actual_lines_after_trigger) > 10:
            for i, l in enumerate(actual_lines_after_trigger[:5]):
                self.log_to_console(f"  Start Line {i}: {l}")
            self.log_to_console("  ...")
            for i, l in enumerate(actual_lines_after_trigger[-5:]):
                self.log_to_console(f"  End Line {len(actual_lines_after_trigger)-5+i}: {l}")
        else:
            for i, l in enumerate(actual_lines_after_trigger):
                self.log_to_console(f"  Line {i}: {l}")
        
        found_players_header = False
        found_start_marker = False 

        players_header_text = "Players on EverQuest:"
        start_marker_text = "---" 
        end_marker_prefixes = ("There is ", "There are ")
        
        common_ignored_keywords = [
            "Players", "Guild", "Anonymous", "Roleplaying", "Auction", "General", 
            "Say", "Shout", "OOC", "There", "You", "It", "AFK" 
        ]
        self.log_to_console(f"Starting forward pass. States: header={found_players_header}, start_marker={found_start_marker}")

        for i, line_content in enumerate(actual_lines_after_trigger):
            self.log_to_console(f"  Processing line {i}: '{line_content[:100]}...'") 
            self.log_to_console(f"    State: header={found_players_header}, start_marker={found_start_marker}")

            if not found_players_header:
                if players_header_text in line_content:
                    found_players_header = True
                    self.log_to_console("    Stage 1: Found players header. Advancing.")
                else:
                    self.log_to_console("    Stage 1: Players header not found. Skipping.")
                continue 

            if not found_start_marker: 
                if start_marker_text in line_content: 
                    found_start_marker = True
                    self.log_to_console("    Stage 2: Found start marker ('---'). Advancing (will skip this line for name parsing).")
                else:
                    self.log_to_console("    Stage 2: Start marker not found. Skipping.")
                continue 
            
            self.log_to_console("    Stage 3: Attempting to parse name or find end marker.")
            if any(line_content.strip().startswith(prefix) for prefix in end_marker_prefixes):
                self.log_to_console(f"    Stage 3: End marker found ('{line_content.strip()}'). Stopping parse.")
                break 

            line_no_timestamp = re.sub(r'^\[.*?\]\s*', '', line_content).strip()
            self.log_to_console(f"      Line (no timestamp): '{line_no_timestamp}'")
            
            match = re.search(r'^(?:AFK\s+)?\[\d+\s+(?:Cleric|Vicar|Templar|High Priest)\]\s+(\w+)', line_no_timestamp)
            if match:
                alias = match.group(1) 
                self.log_to_console(f"      Regex match! Alias: '{alias}'")
                if alias and alias not in clerics_found and alias not in common_ignored_keywords and not alias.isdigit():
                    clerics_found.append(alias)
                    self.log_to_console(f"        Added '{alias}' to found list.")
                else:
                    self.log_to_console(f"        Filtered out '{alias}'. In found: {alias in clerics_found}, In ignored: {alias in common_ignored_keywords}, Is digit: {alias.isdigit()}")
            else:
                self.log_to_console("      No regex match for player name pattern.")
        
        self.log_to_console(f"Final clerics found: {clerics_found}")
        return clerics_found

    def update_assignments_listbox(self):
        self.clerics_listbox.delete(0, tk.END)
        for cleric in self.clerics:
            self.clerics_listbox.insert(tk.END, cleric)

    def update_fluffers_listbox(self):
        self.fluffers_listbox.delete(0, tk.END)
        for fluffer in self.fluffers:
            self.fluffers_listbox.insert(tk.END, fluffer)

    def add_cleric(self):
        from tkinter import simpledialog
        alias = simpledialog.askstring("Add Cleric", "Enter cleric alias:")
        if alias and alias not in self.clerics:
            self.clerics.append(alias)
            self.update_assignments_listbox()
            self.generate_assignments() 

    def remove_cleric(self):
        selected_indices = self.clerics_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select a cleric to remove.")
            return

        selected_alias = self.clerics_listbox.get(selected_indices[0])

        if selected_alias in self.clerics:
            self.clerics.remove(selected_alias)

        if selected_alias in self.fluffers:
            self.fluffers.remove(selected_alias)
            self.update_fluffers_listbox()

        self.update_assignments_listbox()
        self.generate_assignments()
        self.update_macros_tab()

    def on_listbox_select(self, event):
        self.drag_data = {"item": None, "origin_listbox": None}

    def start_drag(self, event):
        widget = event.widget
        try:
            index = widget.nearest(event.y)
            item = widget.get(index)
            self.drag_data["item"] = item
            self.drag_data["origin_listbox"] = widget
            widget.selection_clear(0, tk.END)
            widget.selection_set(index)
            widget.activate(index)
            self.root.config(cursor="hand2") 
        except:
            self.drag_data = {"item": None, "origin_listbox": None}
            self.root.config(cursor="") 

    def drag_motion(self, event):
        if self.drag_data["item"] is not None:
            self.root.config(cursor="hand2")
        else:
            self.root.config(cursor="")

    def drop(self, event):
        target_widget = event.widget
        self.root.config(cursor="")
        dragged_item = self.drag_data["item"]
        origin_lb = self.drag_data["origin_listbox"]
        self.drag_data = {"item": None, "origin_listbox": None}

        if dragged_item is None or origin_lb is None:
            return

        if target_widget == self.clerics_listbox:
            target_listbox_name = "clerics"
        elif target_widget == self.fluffers_listbox:
            target_listbox_name = "fluffers"
        else:
            return

        if origin_lb == self.clerics_listbox and target_listbox_name == "fluffers":
            if dragged_item in self.clerics:
                self.clerics.remove(dragged_item)
                if dragged_item not in self.fluffers: 
                    self.fluffers.append(dragged_item)
                self.update_assignments_listbox()
                self.update_fluffers_listbox()
                self.generate_assignments() 
                self.update_macros_tab() 

        elif origin_lb == self.fluffers_listbox and target_listbox_name == "clerics":
            if dragged_item in self.fluffers:
                self.fluffers.remove(dragged_item)
                if dragged_item not in self.clerics: 
                    self.clerics.append(dragged_item)
                self.update_assignments_listbox()
                self.update_fluffers_listbox()
                self.generate_assignments() 
                self.update_macros_tab() 

        origin_lb.selection_clear(0, tk.END)
        target_widget.selection_clear(0, tk.END)

    def toggle_slow_timing(self):
        self.is_slowable = self.slowable_var.get()
        if self.is_slowable:
            self.slow_seconds_label.grid(row=5, column=0, sticky="w", pady=5, padx=5)
            self.slow_seconds_dropdown.grid(row=5, column=1, sticky="w", pady=5, padx=5)
        else:
            self.slow_seconds_label.grid_forget()
            self.slow_seconds_dropdown.grid_forget()

    def on_timing_selected(self, event):
        new_selection = self.selected_seconds_var.get()
        if new_selection == "Custom":
            custom_value = simpledialog.askfloat(
                "Custom Chain Timing",
                "Enter custom timing in seconds (e.g., 2.7):",
                parent=self.root, minvalue=0.1, maxvalue=60.0
            )
            if custom_value is not None: 
                self.selected_seconds = str(custom_value)
            else: 
                self.selected_seconds_var.set(self.selected_seconds)
        else: 
            self.selected_seconds = new_selection

    def on_slow_timing_selected(self, event):
        new_selection = self.selected_slow_seconds_var.get()
        if new_selection == "Custom":
            custom_value = simpledialog.askfloat(
                "Custom Slow Timing",
                "Enter custom slow timing in seconds (e.g., 5.2):",
                parent=self.root, minvalue=0.1, maxvalue=60.0
            )
            if custom_value is not None:
                self.selected_slow_seconds = str(custom_value)
            else:
                self.selected_slow_seconds_var.set(self.selected_slow_seconds)
        else:
            self.selected_slow_seconds = new_selection

    def on_cleric_channel_selected(self, event):
        self.selected_cleric_channel = self.selected_cleric_channel_var.get()
        self.save_settings()
        if self.selected_macro_shout_display_var.get() == "Cleric Channel":
            self.selected_macro_shout_command = f"/{self.selected_cleric_channel}"
            self.log_to_console(f"Macro shout command updated to cleric channel: {self.selected_macro_shout_command}")

        if self.assignments: 
             self.update_assignments_message() 

    def on_macro_shout_channel_selected(self, event):
        selected_display_option = self.selected_macro_shout_display_var.get()
        
        if self.macro_shout_options_map[selected_display_option] == "dynamic_cleric_channel":
            self.selected_macro_shout_command = f"/{self.selected_cleric_channel_var.get()}"
        else:
            self.selected_macro_shout_command = self.macro_shout_options_map[selected_display_option]
        
        self.log_to_console(f"Macro shout command set to: {self.selected_macro_shout_command}")
        # Auto-refresh removed as per user feedback. User must click "Generate/Refresh Macros"
        # if self.macros_frame_inner.winfo_children(): 
        #     self.log_to_console("Macro shout channel changed, auto-refreshing macros.")
        #     self.refresh_all_macros_and_message()

    def move_cleric_up(self):
        selected_indices = self.clerics_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select a cleric to move up.")
            return
        
        current_index = selected_indices[0]
        if current_index > 0: 
            cleric_to_move = self.clerics.pop(current_index)
            self.clerics.insert(current_index - 1, cleric_to_move)
            
            self.update_assignments_listbox()
            self.clerics_listbox.selection_set(current_index - 1) 
            self.clerics_listbox.activate(current_index - 1)
            self.generate_assignments()
            self.update_macros_tab()

    def move_cleric_down(self):
        selected_indices = self.clerics_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select a cleric to move down.")
            return

        current_index = selected_indices[0]
        if current_index < len(self.clerics) - 1: 
            cleric_to_move = self.clerics.pop(current_index)
            self.clerics.insert(current_index + 1, cleric_to_move)

            self.update_assignments_listbox()
            self.clerics_listbox.selection_set(current_index + 1) 
            self.clerics_listbox.activate(current_index + 1)
            self.generate_assignments()
            self.update_macros_tab()

    def move_to_fluffers(self):
        selected_indices = self.clerics_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select a cleric from the 'Clerics' list to move to 'Fluffers'.")
            return
        
        cleric_to_move = self.clerics_listbox.get(selected_indices[0])
        
        if cleric_to_move in self.clerics:
            self.clerics.remove(cleric_to_move)
            if cleric_to_move not in self.fluffers:
                self.fluffers.append(cleric_to_move)
            
            self.update_assignments_listbox()
            self.update_fluffers_listbox()
            self.generate_assignments()
            self.update_macros_tab()

    def move_to_chain(self):
        selected_indices = self.fluffers_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select a cleric from the 'Fluffers' list to move to 'Clerics'.")
            return

        cleric_to_move = self.fluffers_listbox.get(selected_indices[0])

        if cleric_to_move in self.fluffers:
            self.fluffers.remove(cleric_to_move)
            if cleric_to_move not in self.clerics:
                self.clerics.append(cleric_to_move) 
            
            self.update_assignments_listbox()
            self.update_fluffers_listbox()
            self.generate_assignments()
            self.update_macros_tab()

    def generate_assignments(self):
        self.assignments = {}
        chain_clerics = [c for c in self.clerics if c not in self.fluffers]
        chain_numbers = self.generate_chain_numbers(len(chain_clerics))
        for i, cleric in enumerate(chain_clerics):
            self.assignments[chain_numbers[i]] = cleric
        self.update_assignments_message()

    def generate_chain_numbers(self, count):
        numbers = []
        for i in range(count):
            if i < 9:
                numbers.append(f"{(i+1)*111:03}") 
            else:
                char_code = 65 + (i - 9)
                if char_code <= 90: 
                     numbers.append(chr(char_code) * 3)
                else:
                    pass 
        return numbers

    def update_assignments_message(self):
        if hasattr(self, 'assignments_lines_frame'):
            for widget in self.assignments_lines_frame.winfo_children():
                widget.destroy()
        else: 
            self.log_to_console("Error: assignments_lines_frame not found in update_assignments_message.")
            return

        lines_to_display = []
        channel = self.selected_cleric_channel_var.get()

        if self.assignments: 
            chain_parts = [f"{num} {alias}" for num, alias in self.assignments.items()]
            lines_to_display.append(f"/{channel} CH Chain: " + ", ".join(chain_parts))

        if self.assignments: 
            try:
                pause_value = int(float(self.selected_seconds) * 10)
                lines_to_display.append(f"/{channel} {self.selected_seconds} sec cheal chain pre-slow (/pause {pause_value})")
            except ValueError:
                self.log_to_console(f"Warning: Could not parse self.selected_seconds ('{self.selected_seconds}') for assignment message.")
        
        if self.is_slowable and self.assignments:
            try:
                slow_pause_value = int(float(self.selected_slow_seconds) * 10)
                lines_to_display.append(f"/{channel} {self.selected_slow_seconds} sec cheal chain slowed (/pause {slow_pause_value})")
            except ValueError:
                self.log_to_console(f"Warning: Could not parse self.selected_slow_seconds ('{self.selected_slow_seconds}') for assignment message.")

        fluffers_line_text = f"/{channel} Patch Heals(Fluffers): "
        if self.fluffers:
            fluffers_line_text += "(" + ", ".join(self.fluffers) + ")"
        lines_to_display.append(fluffers_line_text)
        
        for i, line_text_content in enumerate(lines_to_display):
            line_entry_frame = ttk.Frame(self.assignments_lines_frame)
            line_entry_frame.grid(row=i, column=0, sticky="ew", pady=1) 
            line_entry_frame.columnconfigure(0, weight=1) 

            entry = ttk.Entry(line_entry_frame, width=70) 
            entry.insert(0, line_text_content)
            entry.config(state="readonly")
            entry.grid(row=0, column=0, sticky="ew", padx=(0,2))

            copy_btn = ttk.Button(line_entry_frame, text="Copy", width=5, 
                                  command=lambda text_to_copy=line_text_content: self.copy_to_clipboard(text_to_copy))
            copy_btn.grid(row=0, column=1, padx=(2,0))

    def refresh_all_macros_and_message(self):
        self.log_to_console("Refresh All: Regenerating assignments and macros.")
        self.generate_assignments() 
        self.create_macros()      
        messagebox.showinfo("Refreshed", "Assignments and macros have been refreshed.")

    def create_macros(self):
        for widget in self.macros_frame_inner.winfo_children():
            widget.destroy()

        chain_numbers = list(self.assignments.keys())
        for i, (num, alias) in enumerate(self.assignments.items()):
            next_assignment = chain_numbers[i+1] if i+1 < len(chain_numbers) else "N/A" 

            macro_text = self.generate_single_macro(alias, num, next_assignment, self.selected_seconds)
            if self.is_slowable:
                 slow_macro_text = self.generate_single_macro(alias, num, next_assignment, self.selected_slow_seconds)
                 full_macro_text = f"Hello {alias},\n\nHere is your CH Macro.\nPlease change # to what ever your Complete Heal is on your spell gems.\nMacro:\n{macro_text}\n\nSlow Macro:\n{slow_macro_text}"
            else:
                 full_macro_text = f"Hello {alias},\n\nHere is your CH Macro.\nPlease change # to what ever your Complete Heal is on your spell gems.\nMacro:\n{macro_text}"

            macro_button = ttk.Button(self.macros_frame_inner, text=f"{num} {alias} {num}", command=lambda text=full_macro_text: self.copy_to_clipboard(text))
            macro_button.pack(fill="x", pady=2)

    def generate_single_macro(self, alias, assignment, next_assignment, seconds):
        pause_value = int(float(seconds) * 10)
        shout_command = self.selected_macro_shout_command
        
        macro_template = """/pause 1, /stand
/cast #
/cast #
/pause {pause_value}, {shout_cmd} {assignment} CH on %t {assignment} {seconds} Second Chain %n mana
{shout_cmd} {next_assignment} Go  {next_assignment}! {seconds} Second Chain"""

        macro = macro_template.format(
            pause_value=pause_value,
            shout_cmd=shout_command, 
            assignment=assignment,
            next_assignment=next_assignment,
            seconds=seconds
        )
        return macro

    def copy_to_clipboard(self, text):
        if not text: 
            messagebox.showwarning("Nothing to Copy", "The text field is empty.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

    def clear_all(self):
        self.clerics = []
        self.assignments = {}
        self.fluffers = []
        self.update_assignments_listbox()
        self.update_fluffers_listbox()
        
        if hasattr(self, 'assignments_lines_frame'): 
            for widget in self.assignments_lines_frame.winfo_children():
                widget.destroy()
        
        for widget in self.macros_frame_inner.winfo_children():
            widget.destroy()

    def save_settings(self):
        settings = {
            "log_file_path": self.log_file_path,
            "cleric_channel": self.selected_cleric_channel_var.get() 
        }
        try:
            with open("settings.json", "w") as f:
                import json
                json.dump(settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                import json
                settings = json.load(f)
                self.log_file_path = settings.get("log_file_path", "")
                loaded_channel = settings.get("cleric_channel", "2")
                if loaded_channel not in self.cleric_channel_options: 
                    loaded_channel = "2"
                self.selected_cleric_channel = loaded_channel
        except FileNotFoundError:
            self.log_file_path = ""
            self.selected_cleric_channel = "2"
        except Exception as e:
            print(f"Error loading settings: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClericCHApp(root)
    root.mainloop()
