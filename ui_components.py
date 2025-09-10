import tkinter as tk
from tkinter import ttk


class UIComponents:
    def __init__(self):
        self.colors = {
            'bg_primary': '#0f1419',
            'bg_secondary': '#1e2328',
            'bg_tertiary': '#272c34',
            'accent_blue': '#00d4ff',
            'accent_red': '#ff6b6b',
            'accent_green': '#51cf66',
            'accent_orange': '#ffa726',
            'text_primary': '#ffffff',
            'text_secondary': '#a0a0a0',
            'text_tertiary': '#666666',
            'hover_bg': '#3a4048',
            'win_highlight': '#ffd43b'
        }

    def create_animated_title(self, parent):
        title_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        title_frame.pack(pady=(0, 30))

        title_label = tk.Label(
            title_frame,
            text="TIC-TAC-TOE",
            font=('Segoe UI', 32, 'bold'),
            bg=self.colors['bg_primary'],
            fg=self.colors['accent_blue']
        )
        title_label.pack()

        subtitle_label = tk.Label(
            title_frame,
            text="vs Intelligent AI",
            font=('Segoe UI', 14, 'italic'),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_secondary']
        )
        subtitle_label.pack()

        return title_frame, title_label

    def create_header_card(self, parent, stats_text, difficulty_var, difficulty_callback):
        header_card = tk.Frame(parent, bg=self.colors['bg_secondary'], relief='flat')
        header_card.pack(fill='x', pady=(0, 25))
        border_frame = tk.Frame(header_card, height=2, bg=self.colors['accent_blue'])
        border_frame.pack(fill='x')

        card_content = tk.Frame(header_card, bg=self.colors['bg_secondary'])
        card_content.pack(fill='x', padx=25, pady=20)

        stats_section = tk.Frame(card_content, bg=self.colors['bg_secondary'])
        stats_section.pack(side='left', fill='x', expand=True)

        tk.Label(
            stats_section,
            text="GAME STATISTICS",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        ).pack(anchor='w')

        stats_label = tk.Label(
            stats_section,
            text=stats_text,
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            justify='left'
        )
        stats_label.pack(anchor='w', pady=(5, 0))

        difficulty_section = tk.Frame(card_content, bg=self.colors['bg_secondary'])
        difficulty_section.pack(side='right')

        tk.Label(
            difficulty_section,
            text="AI DIFFICULTY",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        ).pack()

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TCombobox',
                        fieldbackground=self.colors['bg_tertiary'],
                        background=self.colors['bg_tertiary'],
                        foreground=self.colors['text_primary'],
                        arrowcolor=self.colors['accent_blue'],
                        borderwidth=0,
                        relief='flat')

        difficulty_combo = ttk.Combobox(
            difficulty_section,
            textvariable=difficulty_var,
            values=['Easy', 'Medium', 'Hard'],
            state='readonly',
            style='Custom.TCombobox',
            font=('Segoe UI', 12, 'bold'),
            width=8
        )
        difficulty_combo.pack(pady=(8, 0))
        difficulty_combo.bind('<<ComboboxSelected>>', difficulty_callback)

        return header_card, stats_label

    def create_game_board(self, parent, button_callback):
        board_container = tk.Frame(parent, bg=self.colors['bg_primary'])
        board_container.pack(pady=20)
        shadow_frame = tk.Frame(board_container, bg='#000000', height=4)
        shadow_frame.pack(fill='x')

        board_frame = tk.Frame(
            board_container,
            bg=self.colors['bg_secondary'],
            padx=15,
            pady=15
        )
        board_frame.pack()

        buttons = []
        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    board_frame,
                    text=' ',
                    font=('Segoe UI', 28, 'bold'),
                    width=3,
                    height=1,
                    bg=self.colors['bg_tertiary'],
                    fg=self.colors['text_primary'],
                    activebackground=self.colors['hover_bg'],
                    activeforeground=self.colors['text_primary'],
                    relief='flat',
                    bd=0,
                    command=lambda row=i, col=j: button_callback(row * 3 + col),
                    cursor='hand2'
                )
                btn.grid(row=i, column=j, padx=3, pady=3, sticky='nsew')

                btn.bind('<Enter>', lambda e, b=btn: self.on_button_hover(b, True))
                btn.bind('<Leave>', lambda e, b=btn: self.on_button_hover(b, False))

                buttons.append(btn)

        for i in range(3):
            board_frame.grid_rowconfigure(i, weight=1, minsize=80)
            board_frame.grid_columnconfigure(i, weight=1, minsize=80)

        return board_container, buttons

    def create_status_section(self, parent):
        status_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        status_frame.pack(pady=25)

        status_label = tk.Label(
            status_frame,
            text="Your turn! Make your move",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['bg_primary'],
            fg=self.colors['accent_green']
        )
        status_label.pack()

        thinking_frame = tk.Frame(status_frame, bg=self.colors['bg_primary'])
        thinking_frame.pack(pady=(10, 0))

        thinking_dots = tk.Label(
            thinking_frame,
            text="",
            font=('Segoe UI', 14),
            bg=self.colors['bg_primary'],
            fg=self.colors['accent_orange']
        )
        thinking_dots.pack()

        return status_frame, status_label, thinking_dots

    def create_control_buttons(self, parent, new_game_callback, reset_stats_callback, quit_callback):
        button_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        button_frame.pack(pady=30)

        # New Game button
        new_game_btn = tk.Button(
            button_frame,
            text="NEW GAME",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['accent_green'],
            fg='white',
            activebackground='#45b049',
            activeforeground='white',
            relief='flat',
            bd=0,
            padx=25,
            pady=12,
            command=new_game_callback,
            cursor='hand2'
        )
        new_game_btn.pack(side='left', padx=10)

        reset_stats_btn = tk.Button(
            button_frame,
            text="RESET STATS",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['accent_orange'],
            fg='white',
            activebackground='#ff8f02',
            activeforeground='white',
            relief='flat',
            bd=0,
            padx=25,
            pady=12,
            command=reset_stats_callback,
            cursor='hand2'
        )
        reset_stats_btn.pack(side='left', padx=10)

        quit_btn = tk.Button(
            button_frame,
            text="QUIT",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['accent_red'],
            fg='white',
            activebackground='#ff5252',
            activeforeground='white',
            relief='flat',
            bd=0,
            padx=25,
            pady=12,
            command=quit_callback,
            cursor='hand2'
        )
        quit_btn.pack(side='left', padx=10)
        return button_frame

    def on_button_hover(self, button, entering):
        if button['state'] != 'disabled':
            if entering:
                button.config(bg=self.colors['hover_bg'])
            else:
                button.config(bg=self.colors['bg_tertiary'])

    def update_button(self, button, text, player_type):
        if player_type == 'human':
            button.config(
                text=text,
                state='disabled',
                bg=self.colors['accent_red'],
                disabledforeground='white',
                font=('Segoe UI', 32, 'bold')
            )
        elif player_type == 'ai':
            button.config(
                text=text,
                state='disabled',
                bg=self.colors['accent_blue'],
                disabledforeground='white',
                font=('Segoe UI', 32, 'bold')
            )

    def highlight_winning_buttons(self, buttons, winning_positions):
        for pos in winning_positions:
            buttons[pos].config(
                bg=self.colors['win_highlight'],
                disabledforeground='#000000'
            )

    def reset_buttons(self, buttons):
        for btn in buttons:
            btn.config(
                text=' ',
                state='normal',
                bg=self.colors['bg_tertiary'],
                disabledforeground=self.colors['text_primary'],
                font=('Segoe UI', 28, 'bold')
            )

    def update_status(self, status_label, message, status_type):
        color_map = {
            'player_turn': self.colors['accent_green'],
            'ai_thinking': self.colors['accent_orange'],
            'human_win': self.colors['accent_green'],
            'ai_win': self.colors['accent_blue'],
            'tie': self.colors['accent_orange']
        }

        status_label.config(
            text=message,
            fg=color_map.get(status_type, self.colors['text_primary'])

        )
