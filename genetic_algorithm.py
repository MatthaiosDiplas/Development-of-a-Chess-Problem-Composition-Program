import chess.engine
import random
from deap import base, creator, tools, algorithms
from chess_problem_themes import THEMES

STOCKFISH_PATH = r"" # Add your Stockfish path here
POPULATION_SIZE = 50
GENERATIONS = 300
INITIAL_COUNTS = {
    "white": {chess.PAWN: 8, chess.KNIGHT: 2, chess.BISHOP: 2, chess.ROOK: 2, chess.QUEEN: 1, chess.KING: 1,},
    "black": {chess.PAWN: 8, chess.KNIGHT: 2, chess.BISHOP: 2, chess.ROOK: 2, chess.QUEEN: 1, chess.KING: 1,},
}

engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

# === DEAP Setup ===
def setup_deap(selected_theme):
    if "FitnessMin" not in creator.__dict__:
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    if "Individual" not in creator.__dict__:
        creator.create("Individual", list, fitness=creator.FitnessMin)
    
    toolbox = base.Toolbox()
    toolbox.register("attr_individual", lambda: [biased_random() for _ in range(64)])
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", lambda ind: evaluate(ind, selected_theme))
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.1)
    toolbox.register("select", tools.selTournament, tournsize=3)
    return toolbox

# Functions to generate random chess positions
#-------------------------------------------------------------
def biased_random():
    if random.random() < 0.5:
        return 0
    else:
        return random.randint(1, 12)
    
def value_to_piece(value):
    """Convert integer values to chess pieces."""
    if value == 0:
        return None  # Empty square
    elif value <= 6:
        return chess.Piece(value, chess.WHITE)  # White pieces (1-6)
    elif value <= 12:
        return chess.Piece(value - 6, chess.BLACK)  # Black pieces (7-12)

def array_to_chessboard(arr):
    """Convert an array of 64 integers into a chess board."""
    board = chess.Board(None)  # Start with an empty board
    for i, value in enumerate(arr):
        piece = value_to_piece(value)
        if piece:
            board.set_piece_at(i, piece)
    return board
#-------------------------------------------------------------

# Penalty functions
#-------------------------------------------------------------
def excessive_pieces_penalty(board):
    penalty = 0.0
    counts = {color: {ptype: 0 for ptype in INITIAL_COUNTS[color]} for color in ["white", "black"]}
    bishops = {"white_light": 0, "white_dark": 0, "black_light": 0, "black_dark": 0}

    for square, piece in board.piece_map().items():
        color = "white" if piece.color == chess.WHITE else "black"
        counts[color][piece.piece_type] += 1
        if piece.piece_type == chess.BISHOP:
            square_color = "light" if (chess.square_rank(square) + chess.square_file(square)) % 2 == 0 else "dark"
            bishops[f"{color}_{square_color}"] += 1
    
    for count in bishops.values():
        if count > 1:
            penalty += (count - 1) * 100

    for color in ["white", "black"]:
        for piece_type, actual in counts[color].items():
            excess = actual - INITIAL_COUNTS[color][piece_type]
            if excess > 0:
                penalty += excess * 200

    return penalty

def illegal_position_penalty(board):
    penalty = 1000
    white_king_count = 0
    black_king_count = 0

    for square_index, piece in board.piece_map().items():
        if piece.piece_type == chess.PAWN:
            rank = chess.square_rank(square_index)
            if rank == 0 or rank == 7:
                penalty += 200

        if piece.piece_type == chess.KING:
            if piece.color == chess.WHITE:
                white_king_count += 1
            else:
                black_king_count += 1

    if white_king_count != 1:
        penalty += abs(white_king_count - 1) * 300
    if black_king_count != 1:
        penalty += abs(black_king_count - 1) * 300

    return penalty

def theme_penalty(board, is_legal, theme_function, engine):
    return theme_function(board, is_legal, engine)
#-------------------------------------------------------------

def evaluate(individual, selected_theme):
    """Evaluate the fitness of an individual (chess position)."""
    board = array_to_chessboard(individual)
    penalty = excessive_pieces_penalty(board)

    if not board.is_valid():
        penalty += illegal_position_penalty(board)
        penalty += theme_penalty(board, is_legal=False, theme_function=selected_theme, engine=engine)
        return (penalty,)

    if board.turn == chess.BLACK:
       return (penalty+400,)
    
    legal_moves_count = len(list(board.legal_moves))
    if legal_moves_count < 1:
        return (penalty+300,)
    elif legal_moves_count < 2:
        penalty += 200
    elif legal_moves_count < 3:
        penalty += 100

    penalty += theme_penalty(board, is_legal=True, theme_function=selected_theme, engine=engine)
    return (penalty,)

def Economy(individual, selected_theme, original_fitness):
    """Minimize pieces in the board representation without worsening fitness."""
    def to_board(indiv):
        board = chess.Board(None)
        for i, val in enumerate(indiv):
            if val == 0:
                continue
            color = chess.WHITE if val <= 6 else chess.BLACK
            piece_type = val if val <= 6 else val - 6
            board.set_piece_at(i, chess.Piece(piece_type, color))
        return board

    def to_individual(board):
        return [
            0 if board.piece_at(i) is None else
            board.piece_at(i).piece_type if board.piece_at(i).color == chess.WHITE
            else board.piece_at(i).piece_type + 6
            for i in range(64)
        ]

    board = to_board(individual)
    fitness = original_fitness
    improved = True

    while improved:
        improved = False
        for square in list(board.piece_map().keys()):
            piece = board.piece_at(square)
            if piece.piece_type == chess.KING:
                continue

            test_board = board.copy()
            test_board.remove_piece_at(square)
            test_individual = to_individual(test_board)
            test_fitness = evaluate(test_individual, selected_theme)[0]

            if test_fitness <= fitness:
                board = test_board
                individual = test_individual
                fitness = test_fitness
                improved = True
                break

    return board, fitness

def run_evolution(selected_theme):
    toolbox = setup_deap(selected_theme)
    population = toolbox.population(n=POPULATION_SIZE)

    best_individual = None
    best_fitness = float("inf")

    for gen in range(GENERATIONS):
        algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.4, ngen=1, verbose=False)
        best = tools.selBest(population, k=1)[0]
        current_fitness = best.fitness.values[0]

        if best_individual is None or current_fitness < best_fitness:
            best_individual, best_fitness = best, current_fitness

        if current_fitness == 0:
            optimized_board, final_fitness = Economy(best_individual, selected_theme, best_fitness)
            return optimized_board.fen(), final_fitness

    optimized_board, final_fitness = Economy(best_individual, selected_theme, best_fitness)
    if final_fitness <= best_fitness:
        return optimized_board.fen(), final_fitness
    else:
        return array_to_chessboard(best_individual).fen(), best_fitness
    
def close_engine():
    engine.quit()