import pygame
import sys
import random


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.width = 300
        self.height = 300
        self.unit_len = self.width // 30
        self.tick_frame = 10
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.snake = [(150, 150)]
        # self.snake = [
        #     (
        #         random.randint(0, self.width - self.unit_len),
        #         random.randint(0, self.height - self.unit_len),
        #     )
        # ]
        self.direction = (self.unit_len, 0)
        self.food = (
            random.randint(0, (self.width - self.unit_len) // self.unit_len)
            * self.unit_len,
            random.randint(0, (self.height - self.unit_len) // self.unit_len)
            * self.unit_len,
        )
        self.score = 0

    def update(self):
        # Move the snake
        head = self.snake[-1]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        new_head = (new_head[0] % self.width, new_head[1] % self.height)
        self.snake.append(new_head)

        # Check if the snake has eaten the food
        if new_head == self.food:
            self.score += 1
            self.food = (
                random.randint(0, (self.width - self.unit_len) // self.unit_len)
                * self.unit_len,
                random.randint(0, (self.height - self.unit_len) // self.unit_len)
                * self.unit_len,
            )
        else:
            self.snake.pop(0)

    def render(self):
        self.display.fill((0, 0, 0))
        for segment in self.snake:
            pygame.draw.rect(
                self.display,
                (30, 30, 30),
                pygame.Rect(segment[0], segment[1], self.unit_len, self.unit_len),
            )
        pygame.draw.rect(
            self.display,
            (30, 30, 30),
            pygame.Rect(self.food[0], self.food[1], self.unit_len, self.unit_len),
        )
        font = pygame.font.SysFont(None, 20)
        score_text = font.render(f"Score: {self.score}", True, (50, 50, 50))
        self.display.blit(score_text, [0, 0])
        pygame.display.update()

    def is_game_over(self):
        # Check if the snake has collided with the wall
        # head = self.snake[-1]
        # if (
        #     head[0] < 0
        #     or head[0] >= self.width
        #     or head[1] < 0
        #     or head[1] >= self.height
        # ):
        #     return True

        # Check if the snake has collided with itself
        if len(self.snake) != len(set(self.snake)):
            return True
        return False

    def show_final_score(self):
        self.display.fill((0, 0, 0))  # Clear the screen
        font = pygame.font.SysFont(None, 35)
        message = font.render(f"Final Score: {self.score}", True, (50, 50, 50))
        message_rect = message.get_rect(center=(self.width / 2, self.height / 2))

        # Draw a rectangle as the background for the final score
        pygame.draw.rect(self.display, (30, 30, 30), message_rect.inflate(20, 20))
        self.display.blit(message, message_rect)
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
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != (
                        0,
                        self.unit_len,
                    ):
                        self.direction = (0, -self.unit_len)
                    elif event.key == pygame.K_DOWN and self.direction != (
                        0,
                        -self.unit_len,
                    ):
                        self.direction = (0, self.unit_len)
                    elif event.key == pygame.K_LEFT and self.direction != (
                        self.unit_len,
                        0,
                    ):
                        self.direction = (-self.unit_len, 0)
                    elif event.key == pygame.K_RIGHT and self.direction != (
                        -self.unit_len,
                        0,
                    ):
                        self.direction = (self.unit_len, 0)

            self.update()
            self.render()
            if self.is_game_over():
                running = False
                self.show_final_score()
            self.clock.tick(self.tick_frame)


def main():
    game = SnakeGame()
    game.run()


if __name__ == "__main__":
    main()
