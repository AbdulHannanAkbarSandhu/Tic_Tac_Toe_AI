import pygame  # Import the pygame library for game development
import sys  # Import the sys library for system-specific parameters and functions
from AI_TicTac import initial_state, player, actions, result, winner, terminal, minimax, X, O, EMPTY  # Import game logic functions and constants from backend

# Constants for game settings
WIDTH, HEIGHT = 600, 600  # Screen dimensions
LINE_WIDTH = 15  # Width of the lines dividing the board
WIN_LINE_WIDTH = 15  # Width of the line indicating a win
BOARD_ROWS = 3  # Number of rows in the board
BOARD_COLS = 3  # Number of columns in the board
SQUARE_SIZE = WIDTH // BOARD_COLS  # Size of each square in the board
CIRCLE_RADIUS = SQUARE_SIZE // 3  # Radius of the circle representing 'O'
CIRCLE_WIDTH = 15  # Width of the circle line
CROSS_WIDTH = 25  # Width of the cross line
SPACE = SQUARE_SIZE // 4  # Space between lines in the cross
RED = (255, 0, 0)  # Color for the winning line
BG_COLOR = (28, 170, 156)  # Background color
LINE_COLOR = (23, 145, 135)  # Line color
CIRCLE_COLOR = (239, 231, 200)  # Circle color
CROSS_COLOR = (66, 66, 66)  # Cross color
BLACK = (0, 0, 0)  # Black color for end screen background
WHITE = (255, 255, 255)  # White color for text
DELAY = 2000  # Delay in milliseconds before showing the end screen

class TicTacToe:
    def __init__(self):
        pygame.init()  # Initialize all imported pygame modules
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Set up the display window
        pygame.display.set_caption('Tic Tac Toe')  # Set the window title
        self.screen.fill(BG_COLOR)  # Fill the screen with the background color
        self.font = pygame.font.Font(None, 36)  # Set the font for text
        self.board = initial_state()  # Initialize the game board
        self.game_over = False  # Flag to indicate if the game is over
        self.current_player = X  # Set the starting player

    def draw_lines(self):
        # Draw horizontal lines
        for row in range(1, BOARD_ROWS):
            pygame.draw.line(self.screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
        # Draw vertical lines
        for col in range(1, BOARD_COLS):
            pygame.draw.line(self.screen, LINE_COLOR, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

    def draw_figures(self):
        # Draw 'X' and 'O' figures on the board
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.board[row][col] == O:
                    pygame.draw.circle(self.screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
                elif self.board[row][col] == X:
                    pygame.draw.line(self.screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                    pygame.draw.line(self.screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

    def mark_square(self, row, col, player):
        # Mark a square with the player's symbol
        self.board[row][col] = player

    def available_square(self, row, col):
        # Check if a square is available (empty)
        return self.board[row][col] == EMPTY

    def check_win(self):
        # Check for a win in rows
        for row in range(BOARD_ROWS):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] and self.board[row][0] is not None:
                self.draw_win_line(row, 0, row, 2)
                return True
        # Check for a win in columns
        for col in range(BOARD_COLS):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] is not None:
                self.draw_win_line(0, col, 2, col)
                return True
        # Check for a win in diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            self.draw_win_line(0, 0, 2, 2)
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            self.draw_win_line(0, 2, 2, 0)
            return True
        return False

    def draw_win_line(self, row1, col1, row2, col2):
        # Draw the winning line
        if col1 == col2:
            pygame.draw.line(self.screen, RED, (col1 * SQUARE_SIZE + SQUARE_SIZE // 2, row1 * SQUARE_SIZE + SQUARE_SIZE // 2), (col2 * SQUARE_SIZE + SQUARE_SIZE // 2, row2 * SQUARE_SIZE + SQUARE_SIZE // 2), WIN_LINE_WIDTH)
        else:
            pygame.draw.line(self.screen, RED, (col1 * SQUARE_SIZE + SQUARE_SIZE // 2, row1 * SQUARE_SIZE + SQUARE_SIZE // 2), (col2 * SQUARE_SIZE + SQUARE_SIZE // 2, row2 * SQUARE_SIZE + SQUARE_SIZE // 2), WIN_LINE_WIDTH)

    def display_end_screen(self, result):
        # Display the end screen with the result and options to restart or quit
        self.screen.fill(BLACK)  # Fill the screen with black
        result_text = self.font.render(result, True, WHITE)  # Render the result text
        result_rect = result_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))  # Center the result text
        self.screen.blit(result_text, result_rect)  # Display the result text

        # Render and display the restart option
        restart_surface = self.font.render("Restart", True, WHITE)
        restart_rect = restart_surface.get_rect(center=(WIDTH // 2 - 100, HEIGHT // 2 + 50))
        self.screen.blit(restart_surface, restart_rect)

        # Render and display the quit option
        quit_surface = self.font.render("Quit", True, WHITE)
        quit_rect = quit_surface.get_rect(center=(WIDTH // 2 + 100, HEIGHT // 2 + 50))
        self.screen.blit(quit_surface, quit_rect)

        pygame.display.update()  # Update the display

        return restart_rect, quit_rect  # Return the rects for the options

    def restart_game(self):
        # Restart the game by resetting the board and variables
        self.screen.fill(BG_COLOR)  # Fill the screen with the background color
        self.draw_lines()  # Draw the lines on the board
        self.board = initial_state()  # Reset the board
        self.game_over = False  # Reset the game over flag
        self.current_player = X  # Reset the current player to 'X'

    def main(self):
        self.draw_lines()  # Draw the initial lines on the board

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Check if the user wants to quit
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    mouseX = event.pos[0]  # Get the x coordinate of the mouse click
                    mouseY = event.pos[1]  # Get the y coordinate of the mouse click

                    clicked_row = mouseY // SQUARE_SIZE  # Determine the row clicked
                    clicked_col = mouseX // SQUARE_SIZE  # Determine the column clicked

                    if self.available_square(clicked_row, clicked_col):
                        self.mark_square(clicked_row, clicked_col, self.current_player)  # Mark the square with the current player's symbol
                        self.draw_figures()  # Draw the updated figures on the board
                        if self.check_win():  # Check for a win
                            pygame.display.update()  # Update the display to show the winning line
                            pygame.time.delay(DELAY)  # Delay before showing the end screen
                            self.game_over = True
                            result = "You Win!"
                        elif terminal(self.board):  # Check for a tie
                            pygame.display.update()  # Update the display to show the final state
                            pygame.time.delay(DELAY)  # Delay before showing the end screen
                            self.game_over = True
                            result = "It's a Tie!"
                        self.current_player = O if self.current_player == X else X  # Switch the current player

            if self.current_player == O and not self.game_over:
                move = minimax(self.board)  # Get the AI's move using the minimax algorithm
                if move is not None:
                    self.mark_square(move[0], move[1], O)  # Mark the AI's move on the board
                    self.draw_figures()  # Draw the updated figures on the board
                    if self.check_win():  # Check for a win
                        pygame.display.update()  # Update the display to show the winning line
                        pygame.time.delay(DELAY)  # Delay before showing the end screen
                        self.game_over = True
                        result = "You Lose!"
                    elif terminal(self.board):  # Check for a tie
                        pygame.display.update()  # Update the display to show the final state
                        pygame.time.delay(DELAY)  # Delay before showing the end screen
                        self.game_over = True
                        result = "It's a Tie!"
                    self.current_player = X  # Switch the current player to 'X'

            if self.game_over:
                keys = pygame.key.get_pressed()  # Get the current state of all keyboard buttons
                restart_rect, quit_rect = self.display_end_screen(result)  # Display the end screen
                if keys[pygame.K_r]:  # Check if the 'R' key is pressed to restart
                    self.restart_game()
                elif keys[pygame.K_q]:  # Check if the 'Q' key is pressed to quit
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # Check if the user clicks on the options
                    mouseX, mouseY = pygame.mouse.get_pos()  # Get the mouse click position
                    if restart_rect.collidepoint((mouseX, mouseY)):  # Check if the restart option is clicked
                        self.restart_game()
                    elif quit_rect.collidepoint((mouseX, mouseY)):  # Check if the quit option is clicked
                        pygame.quit()
                        sys.exit()

            pygame.display.update()  # Update the display

if __name__ == "__main__":
    TicTacToe().main()  # Create an instance of the TicTacToe class and start the game