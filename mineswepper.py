import pygame
import random


class Mineswepper:
    def __init__(self):
        # Constants
        self.WIDTH = 300
        self.HEIGHT = 300
        self.BLACK = (0, 0, 0)
        self.GRAY = (50, 50, 50)
        self.DARK_GRAY = (30, 30, 30)
        self.ROWS = 10
        self.COLS = 10
        self.NUM_MINES = 18

        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Minesweeper")

        # Variables
        self.cell_size = self.WIDTH / (self.COLS + 0.2 * (self.COLS + 1))
        self.margin = 0.2 * self.cell_size
        self.revealed = [[False for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.flagged = [[False for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.board = [[" " for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.game_win = False

    def create_board(self):
        mines = set()
        # Place mines
        while len(mines) < self.NUM_MINES:
            row = random.randint(0, self.ROWS - 1)
            col = random.randint(0, self.COLS - 1)
            if (row, col) not in mines:
                mines.add((row, col))
                self.board[row][col] = "X"

        # Calculate numbers for cells adjacent to mines
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.board[row][col] == "X":
                    continue
                mine_count = 0
                for r in range(max(0, row - 1), min(self.ROWS, row + 2)):
                    for c in range(max(0, col - 1), min(self.COLS, col + 2)):
                        if self.board[r][c] == "X":
                            mine_count += 1
                if mine_count > 0:
                    self.board[row][col] = str(mine_count)

    def draw_board(self):
        ROWS = len(self.board)
        COLS = len(self.board[0])

        for row in range(ROWS):
            for col in range(COLS):
                color = self.GRAY
                pygame.draw.rect(
                    self.screen,
                    color,
                    [
                        (self.margin + self.cell_size) * col + self.margin,
                        (self.margin + self.cell_size) * row + self.margin,
                        self.cell_size,
                        self.cell_size,
                    ],
                )
                if self.flagged[row][col]:
                    pygame.draw.circle(
                        self.screen,
                        self.BLACK,
                        [
                            (self.margin + self.cell_size) * col
                            + self.margin
                            + self.cell_size // 2,
                            (self.margin + self.cell_size) * row
                            + self.margin
                            + self.cell_size // 2,
                        ],
                        self.cell_size // 4,
                        2,
                    )
                if self.revealed[row][col]:
                    if self.board[row][col] == "X":
                        pygame.draw.circle(
                            self.screen,
                            self.BLACK,
                            [
                                (self.margin + self.cell_size) * col
                                + self.margin
                                + self.cell_size // 2,
                                (self.margin + self.cell_size) * row
                                + self.margin
                                + self.cell_size // 2,
                            ],
                            self.cell_size // 4,
                        )
                    if self.board[row][col].isdigit():
                        pygame.draw.rect(
                            self.screen,
                            self.DARK_GRAY,
                            [
                                (self.margin + self.cell_size) * col + self.margin,
                                (self.margin + self.cell_size) * row + self.margin,
                                self.cell_size,
                                self.cell_size,
                            ],
                        )
                        font = pygame.font.SysFont(None, 20)
                        text = font.render(self.board[row][col], True, self.GRAY)
                        text_rect = text.get_rect(
                            center=(
                                (self.margin + self.cell_size) * col
                                + self.margin
                                + self.cell_size // 2,
                                (self.margin + self.cell_size) * row
                                + self.margin
                                + self.cell_size // 2,
                            )
                        )
                        self.screen.blit(text, text_rect)
                    if self.board[row][col] == " ":
                        pygame.draw.rect(
                            self.screen,
                            self.DARK_GRAY,
                            [
                                (self.margin + self.cell_size) * col + self.margin,
                                (self.margin + self.cell_size) * row + self.margin,
                                self.cell_size,
                                self.cell_size,
                            ],
                        )

    def reveal_cell(self, row, col):
        if self.revealed[row][col] or self.flagged[row][col]:
            return
        self.revealed[row][col] = True
        if self.board[row][col] == " ":
            for r in range(max(0, row - 1), min(len(self.board), row + 2)):
                for c in range(max(0, col - 1), min(len(self.board[0]), col + 2)):
                    self.reveal_cell(r, c)

    def check_win(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] != "X" and not self.revealed[row][col]:
                    return False
                if self.board[row][col] == "X" and self.revealed[row][col]:
                    return False
                if self.board[row][col] == "X" and not self.flagged[row][col]:
                    return False
        return True

    def show_final_result(self, win_or_lose):
        font = pygame.font.SysFont(None, 35)
        message = font.render(f"You {win_or_lose} !", True, self.GRAY)
        message_rect = message.get_rect(center=(self.WIDTH / 2, self.HEIGHT / 2))

        # Draw a rectangle as the background for the final score
        pygame.draw.rect(self.screen, (30, 30, 30), message_rect.inflate(20, 20))
        self.screen.blit(message, message_rect)
        pygame.display.update()

        # Wait for the user to press any key
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
                ):
                    waiting = False

    def run(self):
        self.create_board()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    col = int(x // (self.cell_size + self.margin))
                    row = int(y // (self.cell_size + self.margin))
                    if event.button == 1:  # Left click
                        if not self.flagged[row][col]:
                            self.reveal_cell(row, col)
                            if self.board[row][col] == "X":
                                self.revealed = [
                                    [True for _ in range(self.COLS)]
                                    for _ in range(self.ROWS)
                                ]
                                self.draw_board()
                                self.show_final_result("lose")
                                running = False
                    elif event.button == 3:  # Right click
                        self.flagged[row][col] = not self.flagged[row][col]
                if self.check_win():
                    self.game_win = True
                    break
                self.screen.fill(self.BLACK)
                self.draw_board()
                pygame.display.flip()

            if self.game_win:
                self.revealed = [
                    [True for _ in range(self.COLS)] for _ in range(self.ROWS)
                ]
                self.draw_board()
                self.show_final_result("win")
                running = False
        pygame.quit()


def main():
    game = Mineswepper()
    game.run()


if __name__ == "__main__":
    main()
