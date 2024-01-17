import pygame
import sys
import random

pygame.init()

class SudokuSolver:
    def __init__(self):
        # Initialize Pygame window settings
        self.width, self.height = 450, 450
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sudoku Solver")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        # Initialize Sudoku-specific variables
        self.selected = None
        self.manual_input = False
        self.board = [[0] * 9 for _ in range(9)]  # 9x9 Sudoku board
        self.attempts = 0  # Counter for solving attempts

    def draw_setup_screen(self):
        # Display setup screen with options for manual input or a random grid
        self.screen.fill((255, 255, 255))
        manual_text = self.font.render("M for Manual Input|R for Random Grid", True, (0, 0, 0))
        manual_rect = manual_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(manual_text, manual_rect)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    # Set manual_input flag based on user choice
                    if event.key == pygame.K_m:
                        self.manual_input = True
                        waiting = False
                    elif event.key == pygame.K_r:
                        self.manual_input = False
                        self.create_random_grid()
                        waiting = False

    def create_random_grid(self):
        # Initialize the Sudoku board with zeros
        for i in range(9):
            for j in range(9):
                self.board[i][j] = 0

        # Generate a random puzzle with 20 filled cells
        for _ in range(20):
            row, col = random.randint(0, 8), random.randint(0, 8)
            num = random.randint(1, 9)
            while not self.is_valid(num, (row, col)):
                row, col = random.randint(0, 8), random.randint(0, 8)
                num = random.randint(1, 9)
            self.board[row][col] = num

    def draw_board(self):
        # Draw the Sudoku board and numbers on the Pygame window
        cell_size = self.width // 9

        for i in range(9):
            for j in range(9):
                rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)

                # Draw cell background and border
                pygame.draw.rect(self.screen, (255, 255, 255), rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)

                # Draw number in cell if not zero
                if self.board[i][j] != 0:
                    num_text = self.font.render(str(self.board[i][j]), True, (0, 0, 0))
                    num_rect = num_text.get_rect(center=rect.center)
                    self.screen.blit(num_text, num_rect)

                # Draw a yellow border around the selected cell
                if (i, j) == self.selected:
                    pygame.draw.rect(self.screen, (200, 200, 0), rect, 5)

    def solve_sudoku(self):
        # Attempt to solve the Sudoku puzzle
        self.attempts = 0  # Reset the attempts counter
        if self.solve():
            self.print_board()  # Print the solved board
        else:
            print("No solution exists.")

    def solve(self):
        # Recursive backtracking algorithm to solve the Sudoku puzzle
        empty = self.find_empty()
        if not empty:
            return True  # Solved

        row, col = empty

        for num in range(1, 10):
            if self.is_valid(num, (row, col)):
                self.board[row][col] = num
                self.attempts += 1

                if self.solve():
                    return True  # Solution found

                self.board[row][col] = 0  # Backtrack

        return False  # No solution found

    def find_empty(self):
        # Find the first empty cell in the Sudoku board
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None

    def is_valid(self, num, pos):
        # Check if placing a number in a specific position is valid
        if num in self.board[pos[0]] or num in [self.board[i][pos[1]] for i in range(9)]:
            return False

        start_row, start_col = 3 * (pos[0] // 3), 3 * (pos[1] // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False

        return True

    def print_board(self):
        # Print the current state of the Sudoku board to the console
        for row in self.board:
            print(row)

    def draw_grid(self):
        # Draw grid lines on the Pygame window to separate cells
        cell_size = self.width // 9

        for i in range(10):
            pygame.draw.line(self.screen, (0, 0, 0), (i * cell_size, 0), (i * cell_size, self.height), 2)
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * cell_size), (self.width, i * cell_size), 2)

    def get_manual_input(self):
        # Allow the user to input numbers manually by clicking on cells
        self.draw_board()
        inputting = True
        while inputting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    cell_size = self.width // 9
                    self.selected = y // cell_size, x // cell_size
                elif event.type == pygame.KEYDOWN:
                    if self.selected and pygame.K_1 <= event.key <= pygame.K_9:
                        self.board[self.selected[0]][self.selected[1]] = event.key - pygame.K_0
                        inputting = False

            self.screen.fill((255, 255, 255))
            self.draw_grid()
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(60)

    def draw_attempts_info(self):
        # Display the number of attempts made during the solving process
        attempts_text = self.font.render("Attempts: {}".format(self.attempts), True, (255, 0, 0))  # Red color
        attempts_rect = attempts_text.get_rect(center=(self.width // 2, self.height - 20))
        self.screen.blit(attempts_text, attempts_rect)

    def run(self):
        # Main game loop
        self.draw_setup_screen()

        if self.manual_input:
            self.get_manual_input()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    cell_size = self.width // 9
                    self.selected = y // cell_size, x // cell_size
                elif event.type == pygame.KEYDOWN:
                    if self.selected and pygame.K_1 <= event.key <= pygame.K_9:
                        self.board[self.selected[0]][self.selected[1]] = event.key - pygame.K_0
                    elif event.key == pygame.K_RETURN:
                        self.solve_sudoku()

            self.screen.fill((255, 255, 255))
            self.draw_grid()
            self.draw_board()
            self.draw_attempts_info()

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    # Create an instance of SudokuSolver and run the application
    sudoku_solver = SudokuSolver()
    sudoku_solver.run()
