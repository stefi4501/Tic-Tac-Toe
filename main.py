import tkinter as tk
from game_logic import GameLogic
from ui_components import UIComponents


class TicTacToeAI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe vs AI")
        self.root.geometry("600x800")
        self.root.configure(bg='#0f1419')
        self.root.resizable(False, False)

        self.game_logic = GameLogic()
        self.ui_components = UIComponents()

        self.thinking_animation = False
        self.buttons = []
        self.status_label = None
        self.thinking_dots = None
        self.stats_label = None
        self.title_label = None
        self.difficulty_var = tk.StringVar(value=self.game_logic.ai_difficulty)

        self.setup_ui()
        self.animate_title()

    def setup_ui(self):
        main_container = tk.Frame(self.root, bg=self.ui_components.colors['bg_primary'])
        main_container.pack(fill='both', expand=True, padx=30, pady=20)

        title_frame, self.title_label = self.ui_components.create_animated_title(main_container)

        header_card, self.stats_label = self.ui_components.create_header_card(
            main_container,
            self.game_logic.get_formatted_stats(),
            self.difficulty_var,
            self.change_difficulty
        )

        board_container, self.buttons = self.ui_components.create_game_board(
            main_container,
            self.make_move
        )

        status_frame, self.status_label, self.thinking_dots = self.ui_components.create_status_section(
            main_container
        )

        button_frame = self.ui_components.create_control_buttons(
            main_container,
            self.new_game,
            self.reset_stats,
            self.root.quit
        )

    def animate_title(self):
        colors = [
            self.ui_components.colors['accent_blue'],
            self.ui_components.colors['accent_green'],
            self.ui_components.colors['accent_orange'],
            self.ui_components.colors['accent_red']
        ]

        def cycle_colors():
            current_color = colors[0]
            colors.append(colors.pop(0))
            self.title_label.config(fg=current_color)
            self.root.after(2000, cycle_colors)

        cycle_colors()

    def animate_thinking(self):
        if not self.thinking_animation:
            return

        dots = ["●", "●●", "●●●", "●●●●", "●●●", "●●", "●"]

        def update_dots():
            if not self.thinking_animation:
                self.thinking_dots.config(text="")
                return

            current_dots = dots[0]
            dots.append(dots.pop(0))
            self.thinking_dots.config(text=f"AI thinking {current_dots}")
            self.root.after(200, update_dots)

        update_dots()

    def change_difficulty(self, event):
        difficulty = self.difficulty_var.get()
        self.game_logic.set_difficulty(difficulty)

    def make_move(self, position):
        if not self.game_logic.make_move(position, self.game_logic.human):
            return

        self.ui_components.update_button(
            self.buttons[position],
            self.game_logic.human,
            'human'
        )

        game_result = self.game_logic.check_game_end()
        if game_result != 'continue':
            self.handle_game_end(game_result)
            return

        self.ui_components.update_status(
            self.status_label,
            "AI is analyzing the board...",
            'ai_thinking'
        )

        self.thinking_animation = True
        self.animate_thinking()
        self.root.update()

        self.root.after(800, self.execute_ai_move)

    def execute_ai_move(self):
        ai_move = self.game_logic.get_ai_move()
        self.thinking_animation = False

        if ai_move is not None:
            self.game_logic.make_move(ai_move, self.game_logic.ai)
            self.ui_components.update_button(
                self.buttons[ai_move],
                self.game_logic.ai,
                'ai'
            )

        game_result = self.game_logic.check_game_end()
        self.handle_game_end(game_result)

    def handle_game_end(self, game_result):
        if game_result == 'human_win':
            self.ui_components.update_status(
                self.status_label,
                "VICTORY! You defeated the AI!",
                'human_win'
            )
            self.highlight_winning_line()

        elif game_result == 'ai_win':
            self.ui_components.update_status(
                self.status_label,
                "AI WINS! Better luck next time!",
                'ai_win'
            )
            self.highlight_winning_line()

        elif game_result == 'tie':
            self.ui_components.update_status(
                self.status_label,
                " IT'S A TIE! Great game! ",
                'tie'
            )

        elif game_result == 'continue':
            self.ui_components.update_status(
                self.status_label,
                "Your turn! Make your move",
                'player_turn'
            )
        self.stats_label.config(text=self.game_logic.get_formatted_stats())

    def highlight_winning_line(self):
        winning_line = self.game_logic.get_winning_line()
        if winning_line:
            self.ui_components.highlight_winning_buttons(self.buttons, winning_line)

    def new_game(self):
        self.game_logic.reset_board()
        self.thinking_animation = False

        self.ui_components.reset_buttons(self.buttons)
        self.ui_components.update_status(
            self.status_label,
            "Your turn! Make your move",
            'player_turn'
        )
        self.thinking_dots.config(text="")

    def reset_stats(self):
        self.game_logic.reset_stats()
        self.stats_label.config(text=self.game_logic.get_formatted_stats())

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = TicTacToeAI()
    game.run()