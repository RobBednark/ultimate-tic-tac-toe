import time

BOARDS = ['1', '2', '3', '4']
CELLS = ['1', '2', '3', '4']
PLAYER_X = 'X'
PLAYER_O = 'O'
FIRST_PLAYER = PLAYER_X
SPACE = ' '
STATUS_DRAW = 'DRAW'
STATUS_OPEN = 'OPEN'
class TicTacToe:
    def __init__(self, auto_moves = None, display_board = True):
        self.auto_moves = auto_moves
        self.reset()
   
    def reset(self):
        self.current_player = FIRST_PLAYER
        self.next_board = None  # None means the player can choose any board
        self.moves_made = []
        self.boards_data = {}
        self.board_status = {
            '1': STATUS_OPEN,
            '2': STATUS_OPEN,
            '3': STATUS_OPEN,
            '4': STATUS_OPEN,
        }
        self.game_status = None
        self._init_boards_data()

    def _init_boards_data(self):
        # initialize each cell to a SPACE
        # e.g., boards_data = { '11': ' ', '12': ' ', ..., '44': ' ' }
        for board in BOARDS:
            self._assign_all_board_cells(board=board, value=SPACE)

    def save_last_move_state(self):
        self.last_move_state = {
            # Note that current_player is the one making the current move, so it needs to be the other player
            'current_player': self.current_player,
            'next_board': self.next_board,
            'moves_made': self.moves_made.copy(),
            'boards_data': self.boards_data.copy(),
            'board_status': self.board_status.copy(),
            'game_status': self.game_status,
        }
    
    def undo_last_move(self):
        self.current_player = self.last_move_state['current_player']
        self.next_board = self.last_move_state['next_board']
        self.moves_made = self.last_move_state['moves_made'].copy()
        self.boards_data = self.last_move_state['boards_data'].copy()
        self.board_status = self.last_move_state['board_status'].copy()
        self.game_status = self.last_move_state['game_status']
    def get_moves_made(self):
        return self.moves_made
    def _assign_all_board_cells(self, board, value):
        for cell in CELLS:
            self.boards_data[board + cell] = value
    def get_next_move(self):
        return self.auto_moves.pop(0)
 
    def get_board_as_string(self):
        d = self.boards_data
        line = ''
        line += d['11'] + d['12'] + '|' + d['21'] + d['22'] + '\n'
        line += d['13'] + d['14'] + '|' + d['23'] + d['24'] + '\n'
        line += '--+--\n'
        line += d['31'] + d['32'] + '|' + d['41'] + d['42'] + '\n'
        line += d['33'] + d['34'] + '|' + d['43'] + d['44'] + '\n'
        return line
    
    def print_board(self):
        print(self.get_board_as_string())

    def board_is_won_by(self, board):
        # If the board is won, return who won it, else return False
        # Check for a diagonal win in a 2x2 board
        winner = False
        if (self.boards_data[board + '1'] == self.boards_data[board + '4']) and self.boards_data[board + '1'] != SPACE:
            winner = self.boards_data[board + '1']
        if (self.boards_data[board + '2'] == self.boards_data[board + '3']) and self.boards_data[board + '2'] != SPACE:
            winner = self.boards_data[board + '2']
        if winner:
            self.board_status[board] = winner
            return winner
        return False
   
    def game_is_won_by(self):
        # Check for a diagonal win in the 2x2 main board
        winner = False
        if (self.board_is_won_by('1') == self.board_is_won_by('4')) and self.board_is_won_by('1'):
            winner = self.boards_data[board + '1']
        if (self.board_is_won_by('2') == self.board_is_won_by('3')) and self.board_is_won_by('2'):
            winner = self.boards_data[board + '2']
        if winner:
            self.game_status = winner
            return winner
        if SPACE in self.boards_data.values():
            return False
        self.game_status = STATUS_DRAW
        return STATUS_DRAW
    
    def board_is_a_draw(self, board):
        # Check if a 2x2 board is full
        for cell in CELLS:
            if self.boards_data[board + cell] == SPACE:
                return False
        self.board_status[board] = STATUS_DRAW
        return True

    def board_is_available(self, board):
        return self.board_status[board] == STATUS_OPEN
    
    def get_available_boards(self):
        available_boards = []
        if self.moves_made:
            last_move = self.moves_made[-1]
            last_cell = last_move[1]
            next_board = last_cell
            if self.board_is_available(next_board):
                available_boards.append(next_board)
                return available_boards
            else:
                # assert: the next board is not available, so look through all other boards
                pass
        # Assert: there is no next board to be played
        for board in BOARDS:
            if self.board_is_available(board):
                available_boards.append(board)
        return available_boards
    
    def get_available_moves(self):
        available_moves = []
        for board in self.get_available_boards():
            for cell in CELLS:
                move = board + cell
                if self.boards_data[move] == SPACE:
                    available_moves.append(move)
        return available_moves
    
    def get_next_player(self):
        if self.current_player == 'X':
            return 'O'
        return 'X'
    def is_valid_move(self, move):
        if move not in self.boards_data.keys():
            error = f"Invalid move, cell [{move}] does not exist."
            return False, error
        if move not in self.get_available_moves():
            error = f"Invalid move, either not the required board, or cell [{move}] already has an [{self.boards_data[move]}]."
            return False, error
        return True, ''
    
    def make_move(self, move):
        # Return (Valid, Error)
        # where Valid is boolean indicating if move was valid, and
        # Error is a string describing the error if the move was invalid

        is_valid, error = self.is_valid_move(move)
        if not is_valid:
            return False, error

        # Assert: move is valid
        board_played = move[0]
        cell_played = move[1]
        
        # Save the move state before making any changes
        self.save_last_move_state()

        self.boards_data[move] = self.current_player
        winner = self.board_is_won_by(board_played)
        if winner:
            self._assign_all_board_cells(board=board_played, value=winner)
            self.board_status[board_played] = winner
        elif self.board_is_a_draw(board=board_played):
            self.board_status[board_played] = STATUS_DRAW
        # moves_made assignment *must* come before next_board assignment
        self.moves_made.append(move)
        self.next_board = cell_played if self.board_is_available(board=cell_played) else None
        self.current_player = self.get_next_player()

        return True, None
    
    def get_next_board(self, board):
        if self.board_status[board] == STATUS_OPEN:
            return board
        else:
            return None
        
    def get_open_boards(self):
        open_boards = ""
        for board in BOARDS:
            if self.board_status[board] == STATUS_OPEN:
                open_boards += board
        return open_boards

    def get_open_cells_in_board(self, board):
        open_cells = ""
        for cell in CELLS:
            if self.boards_data[board + cell] == SPACE:
                open_cells += cell
        return open_cells

    def prompt_for_move(self):
        if self.next_board:
            next_board = self.next_board
            open_cells = self.get_open_cells_in_board(next_board)
        else:
            next_board = self.get_open_boards()
            open_cells = ''
        prompt = f"Player [{self.current_player}], input move in board=[{next_board}]"
        if open_cells:
            prompt += f" cells=({open_cells})"
        prompt += ": "
        move = input(prompt)
        if len(move) == 1 and self.next_board:
            # Next board is known, and user inputted just one character, so add the board on 
            move = next_board + move
        return move

    def play(self):
        valid_move = True
        while True:
            if valid_move:
                self.print_board()
                print(f"[{len(self.moves_made)}] moves made: {self.moves_made}")

            if self.auto_moves:
                next_move = self.get_next_move()
            else:
                next_move = self.prompt_for_move()
            valid_move, error = self.make_move(next_move)

            if valid_move:
                winner = self.game_is_won_by()
                if winner == STATUS_DRAW:
                    print("Game is a draw.")
                    return winner
                if winner:
                    print(f"[{len(self.moves_made)}] moves made: {self.moves_made}")
                    print(f"Player [{winner}] won!")
                    return winner
            else:
                print(error)

class PlayAllGames:
    def __init__(self):
        DISPLAY_BOARD = True
        self.game = TicTacToe(display_board=DISPLAY_BOARD)
        self.all_games = []
    def game_completed(self):
        self.all_games.append({
            'moves': self.game.get_moves_made().copy(),
            'winner': self.game.game_is_won_by(),
            })
        print(f'Game: winner={self.game.game_is_won_by()}  moves={self.game.get_moves_made()}')
        self._yield()
    def play_all_moves(self):
        available_moves = self.game.get_available_moves()
        for move in available_moves:
            self.game.make_move(move=move)
            if self.game.game_is_won_by():
                # base case
                self.game_completed()
                self.game.undo_last_move()
                pass
            else:
                # recursive call
                self.play_all_moves()
    def _yield(self):
        SLEEP_SECS = 1
        print('Yielding, sleep={SLEEP_SECS}')
        time.sleep(SLEEP_SECS)


    def play_all_games(self):
        print('Playing all games')
        BOARD_1 = '1'
        # Iterate through all cells in board 1
        for cell in CELLS:
            print(f'Playing all games from cell={cell}')
            self.game.reset()
            move = BOARD_1 + cell
            self.game.make_move(move=move)
            # assert: the first move in board 1 has been made; now play all other games from this first move
            self.play_all_moves()



if __name__ == '__main__':
    play_all_games = True

    if play_all_games:
        play_all_games = PlayAllGames()
        play_all_games.play_all_games()
    else:
        # auto_moves = ['11', '12', '23', '34', '41', '13', '31', '21', '44']
        game = TicTacToe(auto_moves=auto_moves)
        winner = game.play()
        print(f'Winner: {winner}')
