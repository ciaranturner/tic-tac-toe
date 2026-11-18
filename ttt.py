class Game:
    def __init__(self, ai):
        self.board = [ ['*'] * 3 for _ in range(3)]
        self.curr = 'X'
        self.ai = ai

    def get_next_move(self, curr_move) -> str:
        return 'O' if curr_move == 'X' else 'X'

    def game_over(self) -> bool:
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '*':
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

    def display_board(self) -> None:
        print()
        for i in range(2):
            print(f" {self.board[i][0]} | {self.board[i][1]} | {self.board[i][2]}  ")
            print("-----------")
        print(f" {self.board[2][0]} | {self.board[2][1]} | {self.board[2][2]}  ")
        print()

    def add_move(self, r: int, c: int) -> None:
        self.board[r][c] = self.curr

    def move_valid(self, r: int, c: int) -> bool:
        return (0 <= r <= 2) and (0 <= c <= 2) and (self.board[r][c] == '*')


    def ai_move(self):
        the_move = self.curr
        max_val = -1
        for i in range(3):
            for j in range(3):
                if self.move_valid(i, j):
                    self.curr = the_move
                    self.board[i][j] = the_move
                    res = self.mini_max(False, -float('inf'), float('inf'))
                    if res > max_val:
                        max_val = res
                        r, c = i, j
                    self.board[i][j] = '*'
        self.curr = the_move
        self.add_move(r, c)

        return (r, c)

    def mini_max(self, maximizing, alpha, beta):
        if self.game_won():
            if maximizing:
                return -1
            else:
                return 1

        if self.game_over():
            return 0

        curr_move = self.get_next_move(self.curr)

        if maximizing:
            final_eval = -float('inf')
        else:
            final_eval = float('inf')

        for i in range(3):
            for j in range(3):
                if self.move_valid(i, j):
                    self.curr = curr_move
                    self.board[i][j] = curr_move
                    res = self.mini_max((not maximizing), alpha, beta)
                    if maximizing:
                        final_eval = max(final_eval, res)
                        alpha = max(final_eval, alpha)
                        if alhpa >= beta:
                            self.board[i][j] = '*'
                            return final_eval
                    else:
                        final_eval = min(final_eval, res)
                        beta = min(final_eval, beta)
                        if alpha >= beta:
                            self.board[i][j] = '*'
                            return final_eval
                    self.board[i][j] = '*'
        return final_eval
                    

    def get_input(self) -> tuple[int, int]:
        while True:
            print()
            try:
                inpt = input(f"{self.curr}'s move: \n")
                lst = inpt.split()
                if len(lst) != 2:
                    print("Enter only two numbers")
                    continue
                r = int(lst[0])
                c = int(lst[1])
                if not self.move_valid(r, c):
                    print("This move is not valid")
                else: 
                    break
            except ValueError:
                print("Enter numbers")
            except KeyboardInterrupt:
                return None
        return (r, c)

    def intro(self):
        print()
        print("Welcome to Tic-Tac-Toe")
        if self.ai: print("Prepare to lose to an AI")
        print("Enter your moves like this: r c ")
        print("The rows are numbered from 0 to 2 top-down")
        print("The cols are numbered from 0 to 2 left to right")
        print("For example, to make your move in the top right, you would type: 0 2")
    

    def game_loop(self):
        self.intro()
        self.display_board()
        r, c = None, None
        while True:
            if self.ai == self.curr:
                print(f"AI's move ({self.curr}): ")
                r, c = self.ai_move()
            else:
                i = self.get_input()
                if not i:
                    break
                r, c = i

            self.add_move(r, c)
            self.display_board()
            if self.game_won():
                print(f"{self.curr} wins")
                break
            if self.game_over():
                print("Tie")
                break
            
            self.curr = self.get_next_move(self.curr)

        print("Thanks for playing")

if __name__ == "__main__":
    print("Welcome to Tic-Tac-Toe")
    print("Type 2 for 2-player, Type 1 to play against an AI")
    ai = None
    while not ai:
        inpt = input("2 or 1: ")
        if inpt == '2':
            break
        if inpt == '1':
            while True:
                inpt = input("You want to go first? (Y or N): " )
                if inpt in ("Y", "Yes", "Yeah"):
                    ai = 'O'
                    break
                elif inpt in ("N", "No", "Nope"):
                    ai = 'X'
                    break
            
    Game(ai).game_loop()

