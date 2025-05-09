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

        # Console Text Area with Scrollbar
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

        # Buttons Frame
        buttons_frame = ttk.Frame(frame)
        buttons_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(5,0))
        
        copy_button = ttk.Button(buttons_frame, text="Copy Log", command=self.copy_console_log)
        copy_button.pack(side=tk.LEFT, padx=(0,5))
        
        clear_button = ttk.Button(buttons_frame, text="Clear Console", command=self.clear_console_log)
        clear_button.pack(side=tk.LEFT)

    def log_to_console(self, message):
        if not hasattr(self, 'console_text_widget'): # Ensure widget exists
            return
        try:
            self.console_text_widget.config(state=tk.NORMAL)
            self.console_text_widget.insert(tk.END, str(message) + "\n")
            self.console_text_widget.see(tk.END)
            self.console_text_widget.config(state=tk.DISABLED)
        except tk.TclError: # Widget might be destroyed during app close
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
        # Log File Selection
        log_file_label = ttk.Label(frame, text="Everquest Log File:")
        log_file_label.grid(row=0, column=0, sticky="w", pady=5, padx=5)

        self.log_file_entry = ttk.Entry(frame, width=50)
        self.log_file_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
        self.log_file_entry.insert(0, self.log_file_path)

        log_file_button = ttk.Button(frame, text="Browse", command=self.browse_log_file)
        log_file_button.grid(row=0, column=2, sticky="w", pady=5, padx=5)

        # Trigger Phrase (Optional customization)
        trigger_label = ttk.Label(frame, text="Cleric Who Trigger:")
        trigger_label.grid(row=1, column=0, sticky="w", pady=5, padx=5)

        self.trigger_entry = ttk.Entry(frame, width=50)
        self.trigger_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
        self.trigger_entry.insert(0, "<CLERIC CH WHO>") # Default trigger

        # Cleric Channel Selection
        cleric_channel_label = ttk.Label(frame, text="Cleric Channel:")
        cleric_channel_label.grid(row=2, column=0, sticky="w", pady=5, padx=5)

        self.cleric_channel_options = [str(i) for i in range(1, 10)] # "1" through "9"
        self.selected_cleric_channel_var = tk.StringVar(value=self.selected_cleric_channel)
        self.cleric_channel_dropdown = ttk.Combobox(
            frame,
            textvariable=self.selected_cleric_channel_var,
            values=self.cleric_channel_options,
            state="readonly",
            width=5 # Narrower width for single digit
        )
        self.cleric_channel_dropdown.grid(row=2, column=1, sticky="w", pady=5, padx=5) # Place next to label
        self.cleric_channel_dropdown.bind("<<ComboboxSelected>>", self.on_cleric_channel_selected)


        # Clear Button - Move down one row
        clear_button = ttk.Button(frame, text="Clear All", command=self.clear_all)
        clear_button.grid(row=3, column=0, sticky="w", pady=10, padx=5)


    def create_assignments_tab(self, frame):
        # Cleric Who Button
        cleric_who_button = ttk.Button(frame, text="Cleric Who", command=self.gather_clerics)
        cleric_who_button.grid(row=0, column=0, sticky="w", pady=5, padx=5)

        # Add/Remove Cleric Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=0, column=1, columnspan=2, sticky="w", pady=5, padx=0) # Use a frame for buttons

        add_cleric_button = ttk.Button(button_frame, text="Add Cleric", command=self.add_cleric)
        add_cleric_button.pack(side=tk.LEFT, padx=5)

        remove_cleric_button = ttk.Button(button_frame, text="Remove Selected", command=self.remove_cleric)
        remove_cleric_button.pack(side=tk.LEFT, padx=5)


        # Cleric List and Fluffers (Placeholder - will use Listbox or similar)
        clerics_label = ttk.Label(frame, text="Clerics:")
        clerics_label.grid(row=1, column=0, sticky="w", pady=5, padx=5)

        # Clerics Listbox with Scrollbar
        clerics_list_frame = ttk.Frame(frame)
        clerics_list_frame.grid(row=2, column=0, sticky="nsew", pady=5, padx=5)
        clerics_list_frame.rowconfigure(0, weight=1)
        clerics_list_frame.columnconfigure(0, weight=1)

        self.clerics_scrollbar = ttk.Scrollbar(clerics_list_frame, orient=tk.VERTICAL)
        self.clerics_listbox = tk.Listbox(clerics_list_frame, width=30, height=10, exportselection=False, yscrollcommand=self.clerics_scrollbar.set)
        self.clerics_scrollbar.config(command=self.clerics_listbox.yview)
        
        self.clerics_listbox.grid(row=0, column=0, sticky="nsew")
        self.clerics_scrollbar.grid(row=0, column=1, sticky="ns")


        # Frame for cleric listbox action buttons (Move Up/Down)
        cleric_buttons_frame = ttk.Frame(frame)
        cleric_buttons_frame.grid(row=2, column=1, sticky="ns", padx=(0,5), pady=5) # Next to clerics_listbox

        move_up_button = ttk.Button(cleric_buttons_frame, text="Move Up", command=self.move_cleric_up)
        move_up_button.pack(pady=2, fill=tk.X)
        move_down_button = ttk.Button(cleric_buttons_frame, text="Move Down", command=self.move_cleric_down)
        move_down_button.pack(pady=2, fill=tk.X)

        # Frame for Fluffer assignment buttons (Move to Fluffers/Chain)
        fluffer_actions_frame = ttk.Frame(frame)
        fluffer_actions_frame.grid(row=2, column=2, sticky="ns", padx=(0,5), pady=5) # Next to cleric_buttons_frame

        move_to_fluffers_button = ttk.Button(fluffer_actions_frame, text=">> Fluffers", command=self.move_to_fluffers)
        move_to_fluffers_button.pack(pady=2, fill=tk.X)
        move_to_chain_button = ttk.Button(fluffer_actions_frame, text="<< Chain", command=self.move_to_chain)
        move_to_chain_button.pack(pady=2, fill=tk.X)


        fluffers_label = ttk.Label(frame, text="Fluffers:")
        fluffers_label.grid(row=1, column=3, sticky="w", pady=5, padx=5) # Adjusted column

        # Fluffers Listbox with Scrollbar
        fluffers_list_frame = ttk.Frame(frame)
        fluffers_list_frame.grid(row=2, column=3, sticky="nsew", pady=5, padx=5) # Adjusted column
        fluffers_list_frame.rowconfigure(0, weight=1)
        fluffers_list_frame.columnconfigure(0, weight=1)

        self.fluffers_scrollbar = ttk.Scrollbar(fluffers_list_frame, orient=tk.VERTICAL)
        self.fluffers_listbox = tk.Listbox(fluffers_list_frame, width=30, height=10, exportselection=False, yscrollcommand=self.fluffers_scrollbar.set)
        self.fluffers_scrollbar.config(command=self.fluffers_listbox.yview)

        self.fluffers_listbox.grid(row=0, column=0, sticky="nsew")
        self.fluffers_scrollbar.grid(row=0, column=1, sticky="ns")


        # Bind drag and drop events (Only for moving between lists now)
        self.clerics_listbox.bind("<<ListboxSelect>>", self.on_listbox_select)
        # self.clerics_listbox.bind("<ButtonPress-1>", self.start_drag) # D&D for reorder removed
        # self.clerics_listbox.bind("<B1-Motion>", self.drag_motion)    # D&D for reorder removed
        # self.clerics_listbox.bind("<ButtonRelease-1>", self.drop)     # D&D for reorder removed

        self.fluffers_listbox.bind("<<ListboxSelect>>", self.on_listbox_select)
        # Bind D&D for moving items *from* fluffers_listbox
        self.fluffers_listbox.bind("<ButtonPress-1>", self.start_drag)
        self.fluffers_listbox.bind("<B1-Motion>", self.drag_motion)
        self.fluffers_listbox.bind("<ButtonRelease-1>", self.drop)
        
        # Bind D&D for moving items *from* clerics_listbox (to fluffers)
        self.clerics_listbox.bind("<ButtonPress-1>", self.start_drag)
        self.clerics_listbox.bind("<B1-Motion>", self.drag_motion)
        self.clerics_listbox.bind("<ButtonRelease-1>", self.drop)


        self.drag_data = {"item": None, "origin_listbox": None}

        # Slowable Checkbox
        self.slowable_var = tk.BooleanVar()
        slowable_checkbox = ttk.Checkbutton(frame, text="Slowable?", variable=self.slowable_var, command=self.toggle_slow_timing)
        slowable_checkbox.grid(row=3, column=0, sticky="w", pady=5, padx=5)

        # Seconds Dropdown
        seconds_label = ttk.Label(frame, text="Chain Timing (sec):")
        seconds_label.grid(row=4, column=0, sticky="w", pady=5, padx=5)
        self.seconds_options = ["Custom", "1", "1.1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5", "5.5", "6"]
        self.selected_seconds_var = tk.StringVar(value=self.selected_seconds)
        self.seconds_dropdown = ttk.Combobox(frame, textvariable=self.selected_seconds_var, values=self.seconds_options, state="readonly")
        self.seconds_dropdown.grid(row=4, column=1, sticky="w", pady=5, padx=5)
        self.seconds_dropdown.bind("<<ComboboxSelected>>", self.on_timing_selected)

        # Slow Seconds Dropdown (Initially hidden)
        self.slow_seconds_label = ttk.Label(frame, text="Slow Timing (sec):")
        self.selected_slow_seconds_var = tk.StringVar(value=self.selected_slow_seconds)
        self.slow_seconds_dropdown = ttk.Combobox(frame, textvariable=self.selected_slow_seconds_var, values=self.seconds_options, state="readonly")
        self.slow_seconds_dropdown.bind("<<ComboboxSelected>>", self.on_slow_timing_selected)

        # Create Macros Button - Placed on row 6 to leave space for slow timing dropdown
        create_macros_button = ttk.Button(frame, text="Create Macros", command=self.create_macros)
        create_macros_button.grid(row=6, column=0, columnspan=2, sticky="w", pady=10, padx=5) # Span columns for better placement potentially

        # Configure grid weights for resizing
        frame.columnconfigure(0, weight=1) # Clerics listbox column
        frame.columnconfigure(3, weight=1) # Fluffers listbox column
        frame.rowconfigure(2, weight=1) # Row containing listboxes


    def create_macros_tab(self, frame):
        # Assignments Message (Placeholder)
        assignments_message_label = ttk.Label(frame, text="Assignments Message:")
        assignments_message_label.grid(row=0, column=0, sticky="w", pady=5, padx=5)

        self.assignments_message_text = tk.Text(frame, height=5, width=60)
        self.assignments_message_text.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=5, padx=5)

        copy_assignments_button = ttk.Button(frame, text="Copy Assignments Message", command=self.copy_assignments_message)
        copy_assignments_button.grid(row=2, column=0, sticky="w", pady=5, padx=5)

        # Individual Macros (Placeholder - will be dynamically generated)
        macros_label = ttk.Label(frame, text="Individual Macros:")
        macros_label.grid(row=3, column=0, sticky="w", pady=10, padx=5)

        # Scrollable area for macro buttons
        macros_canvas_frame = ttk.Frame(frame)
        macros_canvas_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=5, padx=5)
        macros_canvas_frame.rowconfigure(0, weight=1)
        macros_canvas_frame.columnconfigure(0, weight=1)

        self.macros_canvas = tk.Canvas(macros_canvas_frame)
        self.macros_scrollbar = ttk.Scrollbar(macros_canvas_frame, orient="vertical", command=self.macros_canvas.yview)
        self.macros_frame_inner = ttk.Frame(self.macros_canvas) # This frame will hold the buttons

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
        
        # self.macros_frame_inner.columnconfigure(0, weight=1) # Allow inner frame to expand - buttons pack vertically

        # Configure grid weights for resizing
        frame.columnconfigure(0, weight=1) # This was for the whole macros_tab frame
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(4, weight=1)


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
        self.assignments = {} # Clear previous assignments
        self.fluffers = [] # Clear previous fluffers
        self.update_fluffers_listbox()
        self.generate_assignments() # Auto-assign chain numbers
        self.update_macros_tab() # Clear old macros

    def _reverse_readline(self, filename, buf_size=8192):
        """A generator that returns the lines of a file in reverse order."""
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
                    
                    # Decode buffer, handling potential errors
                    try:
                        buffer_str = buffer_bytes.decode('utf-8')
                    except UnicodeDecodeError:
                        try:
                            buffer_str = buffer_bytes.decode('latin-1') # Fallback encoding
                        except UnicodeDecodeError:
                            buffer_str = buffer_bytes.decode('ascii', errors='ignore') # Final fallback

                    lines = buffer_str.splitlines()

                    if segment is not None:
                        if buffer_str[-1] != '\n' and lines: # Check if lines is not empty
                            lines[-1] += segment
                        else:
                            yield segment
                    
                    if lines: # Check if lines is not empty before accessing segment
                        segment = lines[0]
                    else: # If lines is empty (e.g. chunk of null bytes or undecodable)
                        if segment is not None: # Yield previous segment if it exists
                            yield segment
                        segment = None # Reset segment
                        continue


                    for index in range(len(lines) - 1, 0, -1):
                        if lines[index]:
                            yield lines[index]
                if segment is not None: # Yield the last segment
                    yield segment
        except FileNotFoundError:
            # This error should ideally be caught before calling _reverse_readline
            # but as a safeguard:
            messagebox.showerror("Error", f"Log file not found: {filename}")
            yield from () # Return an empty generator
        except Exception as e:
            messagebox.showerror("Error", f"Error reading log file in _reverse_readline: {e}")
            yield from ()


    def parse_log_for_clerics(self, log_path, trigger):
        """
        Parses the log file efficiently from the end to find clerics
        listed after the most recent trigger phrase.
        """
        clerics_found = []
        lines_after_trigger_reversed = []
        trigger_found_in_log = False
        
        self.log_to_console(f"Starting reverse read for trigger: '{trigger}' in '{log_path}'")

        try:
            # Check if file exists before attempting to read
            if not os.path.exists(log_path):
                messagebox.showerror("Error", f"Log file not found: {log_path}")
                self.log_to_console(f"ERROR: Log file not found: {log_path}")
                return []

            for line_idx, line in enumerate(self._reverse_readline(filename=log_path)):
                # self.log_to_console(f"Reverse Read Line {line_idx}: {line[:100]}") # Log snippet of line
                if trigger in line:
                    self.log_to_console(f"Trigger '{trigger}' found in line: {line}")
                    trigger_found_in_log = True
                    break
                lines_after_trigger_reversed.append(line)
            self.log_to_console(f"Finished reverse read. Trigger found: {trigger_found_in_log}. Lines collected before trigger (reversed order): {len(lines_after_trigger_reversed)}")

        except Exception as e: # Catch any other exceptions during file processing
            messagebox.showerror("Error", f"An error occurred while parsing the log: {e}")
            self.log_to_console(f"ERROR during log parsing (reverse read): {e}")
            return []


        if not trigger_found_in_log:
            self.log_to_console("Trigger not found in the entire log during reverse scan.")
            return [] # Trigger not found in the entire log

        # The lines_after_trigger_reversed are in reverse order, so reverse them back
        actual_lines_after_trigger = lines_after_trigger_reversed[::-1]
        self.log_to_console(f"Lines to process (chronological order, after trigger): {len(actual_lines_after_trigger)}")
        # For brevity, log only a few lines if many
        if len(actual_lines_after_trigger) > 10:
            for i, l in enumerate(actual_lines_after_trigger[:5]):
                self.log_to_console(f"  Start Line {i}: {l}")
            self.log_to_console("  ...")
            for i, l in enumerate(actual_lines_after_trigger[-5:]):
                self.log_to_console(f"  End Line {len(actual_lines_after_trigger)-5+i}: {l}")
        else:
            for i, l in enumerate(actual_lines_after_trigger):
                self.log_to_console(f"  Line {i}: {l}")

        
        # State machine variables
        # found_trigger_in_forward_pass = False # Stage 0 removed, this is no longer needed
        found_players_header = False
        found_start_marker = False 

        # Define markers
        players_header_text = "Players on EverQuest:"
        start_marker_text = "---" # Note: EQ logs use "---------------------------"
        # Let's adjust start_marker_text to be more specific if needed, or use `in` for broader match.
        # For now, `in` is used, which is fine for "---" within "---------------------------"
        end_marker_prefixes = ("There is ", "There are ")
        
        common_ignored_keywords = [
            "Players", "Guild", "Anonymous", "Roleplaying", "Auction", "General", 
            "Say", "Shout", "OOC", "There", "You", "It", "AFK" 
        ]
        self.log_to_console(f"Starting forward pass. States: header={found_players_header}, start_marker={found_start_marker}")

        for i, line_content in enumerate(actual_lines_after_trigger):
            self.log_to_console(f"  Processing line {i}: '{line_content[:100]}...'") # Log snippet
            self.log_to_console(f"    State: header={found_players_header}, start_marker={found_start_marker}")

            # Stage 1: Look for "Players on EverQuest:"
            # (Formerly Stage 0 was to find the trigger line, but actual_lines_after_trigger already starts after it)
            if not found_players_header:
                if players_header_text in line_content:
                    found_players_header = True
                    self.log_to_console("    Stage 1: Found players header. Advancing.")
                else:
                    self.log_to_console("    Stage 1: Players header not found. Skipping.")
                continue 

            # Stage 2: Look for "---" (start_marker)
            if not found_start_marker: 
                if start_marker_text in line_content: # Using `in` for "---"
                    found_start_marker = True
                    self.log_to_console("    Stage 2: Found start marker ('---'). Advancing (will skip this line for name parsing).")
                else:
                    self.log_to_console("    Stage 2: Start marker not found. Skipping.")
                continue 
            
            self.log_to_console("    Stage 3: Attempting to parse name or find end marker.")
            # Stage 3: Parse names or find end marker
            if any(line_content.strip().startswith(prefix) for prefix in end_marker_prefixes):
                self.log_to_console(f"    Stage 3: End marker found ('{line_content.strip()}'). Stopping parse.")
                break 

            line_no_timestamp = re.sub(r'^\[.*?\]\s*', '', line_content).strip()
            self.log_to_console(f"      Line (no timestamp): '{line_no_timestamp}'")
            
            match = re.search(r'^(?:AFK\s+)?\[\d+\s+\w+\]\s+(\w+)', line_no_timestamp)
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
            self.generate_assignments() # Regenerate assignments and macros

    def remove_cleric(self):
        selected_indices = self.clerics_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select a cleric to remove.")
            return

        # Get the alias of the selected cleric
        selected_alias = self.clerics_listbox.get(selected_indices[0])

        # Remove from self.clerics list
        if selected_alias in self.clerics:
            self.clerics.remove(selected_alias)

        # Remove from self.fluffers list if present
        if selected_alias in self.fluffers:
            self.fluffers.remove(selected_alias)
            self.update_fluffers_listbox()

        # Update the listbox display
        self.update_assignments_listbox()

        # Regenerate assignments and macros
        self.generate_assignments()
        self.update_macros_tab()

    def on_listbox_select(self, event):
        # Clear drag data if selection changes without drag
        self.drag_data = {"item": None, "origin_listbox": None}

    def start_drag(self, event):
        widget = event.widget
        try:
            # Get the index of the item clicked
            index = widget.nearest(event.y)
            # Get the item text
            item = widget.get(index)
            # Store the item and the originating listbox
            self.drag_data["item"] = item
            self.drag_data["origin_listbox"] = widget
            # Optionally highlight the item being dragged
            widget.selection_clear(0, tk.END)
            widget.selection_set(index)
            widget.activate(index)
            # Change cursor to indicate dragging
            self.root.config(cursor="hand2") # "hand2" is a common dragging cursor
        except:
            # Click was not on an item
            self.drag_data = {"item": None, "origin_listbox": None}
            self.root.config(cursor="") # Reset cursor if drag fails to start


    def drag_motion(self, event):
        # This method is called as the mouse moves with the button pressed.
        # We can ensure the cursor remains as "hand2" if a drag is in progress.
        if self.drag_data["item"] is not None:
            self.root.config(cursor="hand2")
        else:
            self.root.config(cursor="")


    def drop(self, event):
        target_widget = event.widget
        item = self.drag_data["item"]
        origin_listbox = self.drag_data["origin_listbox"]

        # Reset cursor to default
        self.root.config(cursor="")

        # Reset drag data early
        dragged_item = self.drag_data["item"]
        origin_lb = self.drag_data["origin_listbox"]
        self.drag_data = {"item": None, "origin_listbox": None}

        if dragged_item is None or origin_lb is None:
            # Drag didn't start properly or was cancelled implicitly
            return

        # Handle drop onto the same listbox (Reordering) - This logic is being removed for clerics_listbox
        # D&D reordering within clerics_listbox is disabled in favor of Move Up/Down buttons.
        # D&D reordering within fluffers_listbox was never explicitly a feature, and buttons are preferred.
        # if target_widget == origin_lb == self.clerics_listbox:
            # try:
            #     target_index = target_widget.nearest(event.y)
            #     if target_widget.get(target_index) == dragged_item: # Don't allow dropping onto itself
            #         return
            #     original_index = list(origin_lb.get(0, tk.END)).index(dragged_item)
            #     if original_index < target_index:
            #          target_index -=1 
            #     self.clerics.pop(original_index)
            #     self.clerics.insert(target_index, dragged_item)
            #     self.update_assignments_listbox()
            #     self.generate_assignments()
            #     self.update_macros_tab()
            # except ValueError: pass
            # except Exception as e: print(f"Error during reorder: {e}")
            # finally:
            #      origin_lb.selection_clear(0, tk.END)
            #      target_widget.selection_clear(0, tk.END)
            # return

        # Determine the target listbox for cross-list moves
        if target_widget == self.clerics_listbox:
            target_listbox_name = "clerics"
        elif target_widget == self.fluffers_listbox:
            target_listbox_name = "fluffers"
        else:
            # Dropped onto something that isn't a listbox
            return

        # Perform the move between lists
        if origin_lb == self.clerics_listbox and target_listbox_name == "fluffers":
            # Move from Clerics to Fluffers
            if dragged_item in self.clerics:
                self.clerics.remove(dragged_item)
                if dragged_item not in self.fluffers: # Avoid duplicates in fluffers
                    self.fluffers.append(dragged_item)
                self.update_assignments_listbox()
                self.update_fluffers_listbox()
                self.generate_assignments() # Regenerate assignments and macros
                self.update_macros_tab() # Ensure macros reflect change

        elif origin_lb == self.fluffers_listbox and target_listbox_name == "clerics":
            # Move from Fluffers to Clerics
            if dragged_item in self.fluffers:
                self.fluffers.remove(dragged_item)
                if dragged_item not in self.clerics: # Avoid duplicates in clerics
                    # Add back to the end of the main list for now
                    # Reordering within clerics list is handled separately if dropped on itself
                    self.clerics.append(dragged_item)
                self.update_assignments_listbox()
                self.update_fluffers_listbox()
                self.generate_assignments() # Regenerate assignments and macros
                self.update_macros_tab() # Ensure macros reflect change

        # Clear selection after drop
        origin_lb.selection_clear(0, tk.END)
        target_widget.selection_clear(0, tk.END)


    def toggle_slow_timing(self):
        self.is_slowable = self.slowable_var.get()
        if self.is_slowable:
            # Place slow timing widgets on row 5
            self.slow_seconds_label.grid(row=5, column=0, sticky="w", pady=5, padx=5)
            self.slow_seconds_dropdown.grid(row=5, column=1, sticky="w", pady=5, padx=5)
        else:
            # Remove them when checkbox is unchecked
            self.slow_seconds_label.grid_forget()
            self.slow_seconds_dropdown.grid_forget()

    def on_timing_selected(self, event):
        new_selection = self.selected_seconds_var.get()
        if new_selection == "Custom":
            custom_value = simpledialog.askfloat(
                "Custom Chain Timing",
                "Enter custom timing in seconds (e.g., 2.7):",
                parent=self.root,
                minvalue=0.1,  # Example minimum value
                maxvalue=60.0  # Example maximum value
            )
            if custom_value is not None: # User entered a value and clicked OK
                self.selected_seconds = str(custom_value)
                # Combobox still shows "Custom", self.selected_seconds has the actual numeric string
            else: # User cancelled or closed the dialog
                # Revert combobox display to the actual current numeric value stored in self.selected_seconds
                # This ensures it doesn't stay on "Custom" if no valid custom value was set.
                self.selected_seconds_var.set(self.selected_seconds)
        else: # A specific numeric option was chosen
            self.selected_seconds = new_selection
        # print(f"Selected timing: {self.selected_seconds}") # For debugging

    def on_slow_timing_selected(self, event):
        new_selection = self.selected_slow_seconds_var.get()
        if new_selection == "Custom":
            custom_value = simpledialog.askfloat(
                "Custom Slow Timing",
                "Enter custom slow timing in seconds (e.g., 5.2):",
                parent=self.root,
                minvalue=0.1,
                maxvalue=60.0
            )
            if custom_value is not None:
                self.selected_slow_seconds = str(custom_value)
            else:
                self.selected_slow_seconds_var.set(self.selected_slow_seconds)
        else:
            self.selected_slow_seconds = new_selection
        # print(f"Selected slow timing: {self.selected_slow_seconds}") # For debugging

    def on_cleric_channel_selected(self, event):
        """Handles selection changes in the cleric channel dropdown."""
        self.selected_cleric_channel = self.selected_cleric_channel_var.get()
        self.save_settings()
        # Update the assignments message immediately if assignments exist
        if self.assignments:
             self.update_assignments_message()
        # print(f"Selected cleric channel: {self.selected_cleric_channel}") # For debugging

    def move_cleric_up(self):
        selected_indices = self.clerics_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select a cleric to move up.")
            return
        
        current_index = selected_indices[0]
        if current_index > 0: # Can't move up if already at the top
            cleric_to_move = self.clerics.pop(current_index)
            self.clerics.insert(current_index - 1, cleric_to_move)
            
            self.update_assignments_listbox()
            self.clerics_listbox.selection_set(current_index - 1) # Keep selection on moved item
            self.clerics_listbox.activate(current_index - 1)
            self.generate_assignments()
            self.update_macros_tab()

    def move_cleric_down(self):
        selected_indices = self.clerics_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select a cleric to move down.")
            return

        current_index = selected_indices[0]
        if current_index < len(self.clerics) - 1: # Can't move down if already at the bottom
            cleric_to_move = self.clerics.pop(current_index)
            self.clerics.insert(current_index + 1, cleric_to_move)

            self.update_assignments_listbox()
            self.clerics_listbox.selection_set(current_index + 1) # Keep selection on moved item
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
                self.clerics.append(cleric_to_move) # Add to end of main list
            
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

        # Update assignments message text area
        self.update_assignments_message()

    def generate_chain_numbers(self, count):
        numbers = []
        for i in range(count):
            if i < 9:
                numbers.append(f"{(i+1)*111:03}") # 111, 222, ..., 999
            else:
                # After 999, use AAA, BBB, etc.
                # A = 65 in ASCII
                char_code = 65 + (i - 9)
                if char_code <= 90: # Up to ZZZ
                     numbers.append(chr(char_code) * 3)
                else:
                    # Handle beyond ZZZ if needed, though 18 clerics is max
                    pass # Not needed for up to 18

        return numbers

    def update_assignments_message(self):
        # Use the selected cleric channel
        channel = self.selected_cleric_channel_var.get()
        message = f"/{channel} CH Chain: "
        chain_list = []
        for num, alias in self.assignments.items():
            chain_list.append(f"{num} {alias}")
        message += ", ".join(chain_list) + "\n"

        pause_value = int(float(self.selected_seconds) * 10)
        # Use the selected cleric channel
        message += f"/{channel} {self.selected_seconds} sec cheal chain pre-slow (/pause {pause_value})"

        if self.is_slowable:
            slow_pause_value = int(float(self.selected_slow_seconds) * 10)
            message += f". {self.selected_slow_seconds} sec cheal chain slowed (/pause {slow_pause_value})"
        message += "\n"

        # Use the selected cleric channel
        message += f"/{channel} Patch Heals(Fluffers): "
        if self.fluffers:
            message += "(" + ", ".join(self.fluffers) + ")"
        # If no fluffers, the template implies just the label, so no empty parens needed.
        # The original template was: /2 Patch Heals(Fluffers): (%Fluff Alias1%, %Fluff Alias2%, %Fluff Alias 3%)
        # This change makes it: /2 Patch Heals(Fluffers): (FluffAlias1, FluffAlias2) OR /2 Patch Heals(Fluffers): 
        # If fluffers list is empty, it will just be "/2 Patch Heals(Fluffers): \n"
        # If there are fluffers, it will be "/2 Patch Heals(Fluffers): (ClericA, ClericB)\n"
        message += "\n"

        self.assignments_message_text.delete(1.0, tk.END)
        self.assignments_message_text.insert(tk.END, message)


    def create_macros(self):
        # Clear previous macro buttons
        for widget in self.macros_frame_inner.winfo_children():
            widget.destroy()

        chain_numbers = list(self.assignments.keys())
        for i, (num, alias) in enumerate(self.assignments.items()):
            next_assignment = chain_numbers[i+1] if i+1 < len(chain_numbers) else "N/A" # Handle last cleric

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
        macro_template = """/pause 1, /stand
/cast #
/cast #
/pause {pause_value}, /shout {assignment} CH on %t {assignment} {seconds} Second Chain %n mana
/shout {next_assignment} Go  {next_assignment}! {seconds} Second Chain"""

        macro = macro_template.format(
            pause_value=pause_value,
            assignment=assignment,
            next_assignment=next_assignment,
            seconds=seconds
        )
        return macro

    def copy_assignments_message(self):
        text = self.assignments_message_text.get(1.0, tk.END).strip()
        self.copy_to_clipboard(text)
        messagebox.showinfo("Copied", "Assignments message copied to clipboard.")

    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

    def clear_all(self):
        # self.log_file_path = "" # Keep log file path
        # self.log_file_entry.delete(0, tk.END) # Keep log file path in entry
        self.clerics = []
        self.assignments = {}
        self.fluffers = []
        self.update_assignments_listbox()
        self.update_fluffers_listbox()
        self.assignments_message_text.delete(1.0, tk.END)
        for widget in self.macros_frame_inner.winfo_children():
            widget.destroy()
        # self.save_settings() # Settings are saved when log path changes or cleric channel changes.
                           # Clearing data does not require re-saving settings unless a setting itself was cleared.
                           # Since log_file_path is preserved, no need to call save_settings here if its only purpose
                           # was to clear the path. If other settings were to be cleared by clear_all, this might change.
                           # For now, preserving log_file_path means we don't touch settings.json here.
                           # If other app settings were cleared (e.g. trigger phrase to default), then save_settings would be needed.
                           # Current request is only about log file path.

    def save_settings(self):
        settings = {
            "log_file_path": self.log_file_path,
            "cleric_channel": self.selected_cleric_channel_var.get() # Save selected channel
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
                # Load cleric channel, default to "2" if not found or invalid
                loaded_channel = settings.get("cleric_channel", "2")
                if loaded_channel not in self.cleric_channel_options: # Ensure loaded value is valid
                    loaded_channel = "2"
                self.selected_cleric_channel = loaded_channel
                # Ensure the StringVar for the Combobox is also updated after loading
                # This needs to happen *after* create_widgets normally, so we set the instance var here
                # and the Combobox's StringVar will pick it up during init.
                # Let's refine: set the instance var here, and ensure create_setup_tab uses it.
        except FileNotFoundError:
            # Set defaults if file not found
            self.log_file_path = ""
            self.selected_cleric_channel = "2"
        except Exception as e:
            print(f"Error loading settings: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ClericCHApp(root)
    root.mainloop()
