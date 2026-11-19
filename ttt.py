import pygame

pygame.init()

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 800
COLOR_BLUE = pygame.Color(39, 116, 174)
COLOR_GOLD = pygame.Color(255, 209, 0)

FONT = "Comic Sans"

TITLE_FONT = pygame.font.SysFont(FONT, 70)
SUBTITLE_FONT = pygame.font.SysFont(FONT, 40)
BUTTON_FONT = pygame.font.SysFont(FONT, 30)
CHAR_FONT = pygame.font.SysFont(FONT, 200)


class Game:
    def __init__(self, ai: str | None, screen: pygame.Surface) -> None:
        self.board = [["*"] * 3 for _ in range(3)]
        self.curr = "X"
        self.ai = ai
        self.screen = screen

    def render_board(self) -> None:
        self.screen.fill("black")

        pygame.draw.line(
            self.screen,
            COLOR_BLUE,
            (SCREEN_WIDTH / 3, 0),
            (SCREEN_WIDTH / 3, SCREEN_HEIGHT),
        )
        pygame.draw.line(
            self.screen,
            COLOR_BLUE,
            (2 * SCREEN_WIDTH / 3, 0),
            (2 * SCREEN_WIDTH / 3, SCREEN_HEIGHT),
        )
        pygame.draw.line(
            self.screen,
            COLOR_BLUE,
            (0, SCREEN_HEIGHT / 3),
            (SCREEN_WIDTH, SCREEN_HEIGHT / 3),
        )
        pygame.draw.line(
            self.screen,
            COLOR_BLUE,
            (0, 2 * SCREEN_HEIGHT / 3),
            (SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3),
        )

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "*":
                    continue
                char_surface = pygame.font.Font.render(
                    CHAR_FONT, self.board[i][j], 1, COLOR_GOLD
                )
                cw = char_surface.get_width()
                ch = char_surface.get_height()
                self.screen.blit(
                    char_surface,
                    (
                        i * (SCREEN_WIDTH / 3) + SCREEN_WIDTH / 6 - cw / 2,
                        j * (SCREEN_HEIGHT / 3) + SCREEN_HEIGHT / 6 - ch / 2,
                    ),
                )

        pygame.display.flip()

    def get_next_move(self, curr_move: str) -> str:
        return "O" if curr_move == "X" else "X"

    def game_over(self) -> bool:
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "*":
                    return False
        return True

    def game_won(self) -> bool:
        for i in range(3):
            if self.curr == self.board[i][0] == self.board[i][1] == self.board[i][2]:
                return True
            if self.curr == self.board[0][i] == self.board[1][i] == self.board[2][i]:
                return True

        if self.curr == self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return True

        if self.curr == self.board[2][0] == self.board[1][1] == self.board[0][2]:
            return True

        return False

    def add_move(self, r: int, c: int) -> None:
        self.board[r][c] = self.curr

    def move_valid(self, r: int, c: int) -> bool:
        return (0 <= r <= 2) and (0 <= c <= 2) and (self.board[r][c] == "*")

    def ai_move(self) -> tuple[int, int]:
        the_move = self.curr
        max_val = -1
        for i in range(3):
            for j in range(3):
                if self.move_valid(i, j):
                    self.curr = the_move
                    self.board[i][j] = the_move
                    res = self.mini_max(False, -2, 2)
                    if res > max_val:
                        max_val = res
                        r, c = i, j
                    self.board[i][j] = "*"
        self.curr = the_move

        return (r, c)

    def mini_max(self, maximizing: bool, alpha: int, beta: int) -> float:
        if self.game_won():
            if maximizing:
                return -1
            else:
                return 1

        if self.game_over():
            return 0

        curr_move = self.get_next_move(self.curr)

        if maximizing:
            final_eval = -2
        else:
            final_eval = 2

        for i in range(3):
            for j in range(3):
                if self.move_valid(i, j):
                    self.curr = curr_move
                    self.board[i][j] = curr_move
                    res = self.mini_max((not maximizing), alpha, beta)
                    if maximizing:
                        final_eval = max(final_eval, res)
                        alpha = max(final_eval, alpha)
                    else:
                        final_eval = min(final_eval, res)
                        beta = min(final_eval, beta)
                    self.board[i][j] = "*"
                    if alpha >= beta:
                        return final_eval
        return final_eval

    def game_loop(self) -> str | None:
        running = True
        while running:
            r, c = None, None
            self.render_board()
            if self.ai == self.curr:
                r, c = self.ai_move()
            else:
                while r == None and running:
                    for event in pygame.event.get():
                        x, y = None, None
                        if event.type == pygame.QUIT:
                            running = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x, y = pygame.mouse.get_pos()
                        if x is not None and y is not None:
                            x = int(x // (SCREEN_WIDTH / 3))
                            y = int(y // (SCREEN_HEIGHT / 3))
                            if self.move_valid(x, y):
                                r = x
                                c = y
            if not running:
                break
            self.add_move(r,c)
            if self.game_won():
                self.render_board()
                return self.curr
            if self.game_over():
                self.render_board()
                return "N"

            self.curr = self.get_next_move(self.curr)
        return None


def intro_screens(screen: pygame.Surface, subtitle: str, option_one: str, option_two: str) -> int:
    screen.fill("black")

    title_surface = pygame.font.Font.render(TITLE_FONT, "Tic-Tac-Toe", 1, COLOR_BLUE)
    tw = title_surface.get_width()
    th = title_surface.get_height()
    screen.blit(
        title_surface, (SCREEN_WIDTH / 2 - tw / 2, SCREEN_HEIGHT * 3 / 8 - th / 2)
    )

    subtitle_surface = pygame.font.Font.render(SUBTITLE_FONT, subtitle, 1, COLOR_BLUE)
    stw = subtitle_surface.get_width()
    sth = subtitle_surface.get_height()
    screen.blit(
        subtitle_surface, (SCREEN_WIDTH / 2 - stw / 2, SCREEN_HEIGHT / 2 - sth / 2)
    )

    one_surface = pygame.font.Font.render(BUTTON_FONT, option_one, 1, COLOR_BLUE)
    ow = one_surface.get_width()
    oh = one_surface.get_height()
    one_top_left_x = SCREEN_WIDTH * 3 / 8 - ow / 2
    one_top_left_y = SCREEN_HEIGHT * 0.7 - oh / 2

    one_button_x_left = one_top_left_x - 10
    one_button_x_right = one_button_x_left + ow + 20
    one_button_y_left = one_top_left_y - 10
    one_button_y_right = one_button_y_left + oh + 20

    pygame.draw.rect(
        screen, COLOR_GOLD, (one_top_left_x - 10, one_top_left_y - 10, ow + 20, oh + 20)
    )
    screen.blit(one_surface, (one_top_left_x, one_top_left_y))

    two_surface = pygame.font.Font.render(BUTTON_FONT, option_two, 1, COLOR_BLUE)
    tw = two_surface.get_width()
    th = two_surface.get_height()
    two_top_left_x = SCREEN_WIDTH * 5 / 8 - tw / 2
    two_top_left_y = SCREEN_HEIGHT * 0.7 - th / 2

    two_button_x_left = two_top_left_x - 10
    two_button_x_right = two_button_x_left + tw + 20
    two_button_y_left = two_top_left_y - 10
    two_button_y_right = two_button_y_left + th + 20

    pygame.draw.rect(
        screen, COLOR_GOLD, (two_button_x_left, two_button_y_left, tw + 20, th + 20)
    )
    screen.blit(two_surface, (two_top_left_x, two_top_left_y))

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if (one_button_x_left < x < one_button_x_right) and (
                    one_button_y_left < y < one_button_y_right
                ):
                    return 1
                elif (two_button_x_left < x < two_button_x_right) and (
                    two_button_y_left < y < two_button_y_right
                ):
                    return 2

    return -1


def display_win_or_tie(screen: pygame.Surface, res: str) -> bool:
    pygame.draw.rect(
        screen,
        COLOR_BLUE,
        (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
    )

    display_text = None
    if res == "N":
        display_text = "Tie Game"
    else:
        display_text = f"{res} is the winner"

    text_surface = pygame.font.Font.render(SUBTITLE_FONT, display_text, 1, COLOR_GOLD)
    tw = text_surface.get_width()
    th = text_surface.get_height()

    screen.blit(text_surface, (SCREEN_WIDTH / 2 - tw / 2, SCREEN_HEIGHT * 0.4  - th / 2))

    button_surface = pygame.font.Font.render(BUTTON_FONT, "Play again?", 1, COLOR_BLUE)
    bw = button_surface.get_width()
    bh = button_surface.get_height()
    button_top_left_x = SCREEN_WIDTH * 0.5 - bw / 2
    button_top_left_y = SCREEN_HEIGHT * 0.6 - bh / 2

    button_x_left = button_top_left_x - 10
    button_x_right = button_x_left + bw + 20
    button_y_left = button_top_left_y - 10
    button_y_right = button_y_left + bh + 20

    pygame.draw.rect(
        screen, COLOR_GOLD, (button_top_left_x - 10, button_top_left_y - 10, bw + 20, bh + 20)
    )
    screen.blit(button_surface, (button_top_left_x, button_top_left_y))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if (button_x_left < x < button_x_right) and (
                    button_y_left < y < button_y_right
                ):
                    return True

if __name__ == "__main__":
    pygame.init()

    res = None
    start_val = None
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    playing = True
    while playing:
        player_count = intro_screens(screen, "How many players are there?", "One", "Two")
        if player_count == 2:
            start_val = None
        if player_count == 1:
            x_or_o = intro_screens(screen, "Do you want to play Xs or Os?", "X", "O")
            if x_or_o == 2:
                start_val = "X"
            elif x_or_o == 1:
                start_val = "O"
            else:
                start_val = "E"

        if start_val == "E" or player_count == -1:
            break
    
        res = Game(start_val, screen).game_loop()
        if res: next_game = display_win_or_tie(screen, res)
        else: break

        if not next_game:
            break

    pygame.quit()
