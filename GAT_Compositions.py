import chess
import random
import chess.engine
import sys
import time

class GAT_Composer:
    ENGINE_PATH = r"" # Add your Stockfish path here

    def __init__(self):
        self.engine = chess.engine.SimpleEngine.popen_uci(self.ENGINE_PATH)

    def method_controller(self):
        depth = self.get_depth()
        self.compose_position(depth)
        self.show_solution()
        self.continue_generating()

    def get_depth(self):
        while True:
            try:
                depth = int(input("Enter '2' for checkmate in 2 moves or '3' for checkmate in 3 moves: "))
                if depth in {2, 3}:
                    print("Generating a chess position, please wait...\n")
                    return depth
                print("Invalid input. Please enter 2 or 3.\n")
            except ValueError:
                print("Invalid input. Please enter a number.\n")

    def compose_position(self, depth):
        start_time = time.time()  # Έναρξη χρονόμετρου
        while True:
            fen_string = self.generate_random_fen()
            if self.is_forced_mate(fen_string, depth):
                #print(f"Generated position FEN:\n{fen_string}\n")
                minimized_fen = self.economy(fen_string, depth)
                print(f"Chess_Composition FEN:\n{minimized_fen}")
                break

        end_time = time.time()  # Τέλος χρονόμετρου
        elapsed = end_time - start_time
        mins, secs = divmod(int(elapsed), 60)
        #print(f"Time taken to generate position: {mins} minutes {secs} seconds\n")
        
    def generate_random_fen(self):
        board = chess.Board()
        plies = random.randrange(20, 51, 2)  # ensures even number
        for _ in range(plies):
            legal_moves = tuple(board.legal_moves)
            if legal_moves:
                board.push(random.choice(legal_moves))
            else:
                break
        return board.fen()

    def is_forced_mate(self, fen, moves):
        board = chess.Board(fen)
        if not board.is_valid():
            return False
        '''if self.material_balance(board) >= 0:
            return False'''
        try:
            info = self.engine.analyse(board, chess.engine.Limit(depth=moves*2), multipv=2)
            best_score = info[0]["score"].pov(board.turn)
            if best_score.is_mate() and best_score.mate() == moves:
                '''first_move = info[0]["pv"][0]
                if board.is_capture(first_move) or board.gives_check(first_move):
                    return False'''
                second_best_score = info[1]["score"].pov(board.turn)
                if not second_best_score.is_mate() and second_best_score.score() <= 500: #score in centipawns
                    self.solution = board.variation_san(info[0]["pv"])
                    return True
        except (chess.engine.EngineTerminatedError, chess.engine.EngineError):
            self.terminate_process()
        return False

    '''def material_balance(self, board):
        piece_values = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9}
        material_score = lambda color: sum(piece_values[piece] * len(board.pieces(piece, color)) for piece in piece_values)
        return material_score(board.turn) - material_score(not board.turn)'''
    
    def economy(self, fen, depth):
        board = chess.Board(fen)
        original_pieces = [square for square in chess.SQUARES if board.piece_at(square) and board.piece_at(square).piece_type != chess.KING]

        for square in original_pieces:
            temp_board = board.copy()
            temp_board.remove_piece_at(square)
            temp_fen = temp_board.fen()

            if self.is_forced_mate(temp_fen, depth):
                board = temp_board  # commit removal
                #print(f"Removed piece at {chess.square_name(square)} and still mate in {depth} verified.")

        return board.fen()

    def show_solution(self):
        while True:
            response = input("Show solution? (yes/no): ").strip().lower()
            if response in {"yes", "no"}:
                if response == "yes":
                    print(f"Solution: {self.solution}\n")
                break
            print("Invalid input. Please enter 'yes' or 'no'.\n")

    def continue_generating(self):
        while True:
            choice = input("Enter 'end' to quit or 'new' to generate a new position: ").strip().lower()
            if choice == "end":
                self.terminate_process()
            elif choice == "new":
                self.method_controller()
            else:
                print("Invalid input. Please enter 'end' or 'new'.\n")

    def terminate_process(self):
        try:
            self.engine.quit()
        except Exception:
            print("Engine shut down!")
        sys.exit(0)

if __name__ == "__main__":
    GAT_Composer().method_controller()
