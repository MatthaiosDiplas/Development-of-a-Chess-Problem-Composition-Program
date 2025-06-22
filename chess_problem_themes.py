import chess

def No_Theme(board, is_legal, engine):
    MATE_IN = THEME_MATE_DEPTHS["No_Theme"]
    penalty = 0
    if is_legal:
        info = engine.analyse(board, chess.engine.Limit(depth=MATE_IN*2), multipv=2)
        score = info[0]["score"].pov(board.turn)
        if len(info)>1:
            second_score = info[1]["score"].pov(board.turn)
        else:
            second_score = None

        if not score.is_mate() or score.mate() < 0:
            return penalty+60
        elif score.is_mate() and score.mate() != MATE_IN:
            return penalty+50
        elif second_score is not None and second_score.is_mate() and second_score.mate() == MATE_IN:
            return penalty+40
        
    return penalty

def Albino(board, is_legal, engine):
    MATE_IN = THEME_MATE_DEPTHS["Albino"]
    penalty = 0

    # === Universal Penalties ===
    white_pawns = [square for square, piece in board.piece_map().items() if piece.piece_type == chess.PAWN and piece.color == chess.WHITE]
    valid_first_rank_pawns = [pawn for pawn in white_pawns if chess.square_rank(pawn) == 1 and chess.square_file(pawn) not in [0, 7]]
    
    if not white_pawns:
        return penalty+80
    elif not valid_first_rank_pawns:
        return penalty+70

    # === Penalties for Legal Positions ===
    if is_legal:
        info = engine.analyse(board, chess.engine.Limit(depth=MATE_IN*2), multipv=10)
        score = info[0]["score"].pov(board.turn)
        if len(info)>1:
            second_score = info[1]["score"].pov(board.turn)
        else:
            second_score = None

        if not score.is_mate() or score.mate() < 0:
            return penalty+60
        elif score.is_mate() and score.mate() != MATE_IN:
            return penalty+50
        elif second_score is not None and second_score.is_mate() and second_score.mate() == MATE_IN:
            return penalty+40

        pv_moves = info[0]["pv"]
        key_move = pv_moves[0]
        board.push(key_move)

        black_responses = list(board.legal_moves)
        if len(black_responses) < 4:
            penalty+=(4 - len(black_responses))*5

        penalty+=10
        pawn_mate_destinations = set()

        for black_move in black_responses:
            test_board = board.copy()
            test_board.push(black_move)
            response_info = engine.analyse(test_board, chess.engine.Limit(depth=MATE_IN*2), multipv=10)
            response_pv = response_info[0]["pv"]
            mate_move = response_pv[0]
            piece = test_board.piece_at(mate_move.from_square)
            if piece.piece_type == chess.PAWN and piece.color == chess.WHITE:
                if chess.square_rank(mate_move.from_square) == 1 and chess.square_file(mate_move.from_square) not in [0, 7]:
                    if mate_move.to_square not in pawn_mate_destinations:
                        penalty-=2.5
                        pawn_mate_destinations.add(mate_move.to_square)

    return penalty

def Amazon(board, is_legal, engine):
    MATE_IN = THEME_MATE_DEPTHS["Amazon"]
    penalty = 0

    # === Universal Penalties ===
    white_queens = [square for square, piece in board.piece_map().items() if piece.piece_type == chess.QUEEN and piece.color == chess.WHITE]
    
    if not white_queens:
        return penalty+80

    # === Penalties for Legal Positions ===
    if is_legal:
        info = engine.analyse(board, chess.engine.Limit(depth=MATE_IN*2), multipv=2)
        score = info[0]["score"].pov(board.turn)
        if len(info)>1:
            second_score = info[1]["score"].pov(board.turn)
        else:
            second_score = None

        if not score.is_mate() or score.mate() < 0:
            return penalty+60
        elif score.is_mate() and score.mate() != MATE_IN:
            return penalty+50
        elif second_score is not None and second_score.is_mate() and second_score.mate() == MATE_IN:
            return penalty+40

        pv_moves = info[0]["pv"]
        test_board = board.copy()

        for move in pv_moves:
            piece = test_board.piece_at(move.from_square)
            if piece.color == chess.WHITE:
                if piece.piece_type != chess.QUEEN:
                    penalty+=1
            test_board.push(move)

    return penalty

def Crusader(board, is_legal, engine):
    MATE_IN = THEME_MATE_DEPTHS["Crusader"]
    penalty = 0

    # === Universal Penalties ===
    white_knights = [square for square, piece in board.piece_map().items() if piece.piece_type == chess.KNIGHT and piece.color == chess.WHITE]
    
    if not white_knights:
        return penalty+80

    # === Penalties for Legal Positions ===
    if is_legal:
        info = engine.analyse(board, chess.engine.Limit(depth=MATE_IN*2), multipv=2)
        score = info[0]["score"].pov(board.turn)
        if len(info)>1:
            second_score = info[1]["score"].pov(board.turn)
        else:
            second_score = None

        if not score.is_mate() or score.mate() < 0:
            return penalty+60
        elif score.is_mate() and score.mate() != MATE_IN:
            return penalty+50
        elif second_score is not None and second_score.is_mate() and second_score.mate() == MATE_IN:
            return penalty+40

        pv_moves = info[0]["pv"]
        test_board = board.copy()
        original_knight_square = None

        for move in pv_moves:
            piece = test_board.piece_at(move.from_square)
            if piece.color == chess.WHITE:
                if piece.piece_type == chess.KNIGHT:
                    if original_knight_square is None:
                        original_knight_square = move.to_square
                    elif move.from_square != original_knight_square:
                        penalty+=0.5
                else:   
                    penalty+=1
            test_board.push(move)

    return penalty

def Dark_Doings(board, is_legal, engine):
    MATE_IN = THEME_MATE_DEPTHS["Dark_Doings"]
    penalty = 0

    # === Universal Penalties ===
    white_pieces = [piece for piece in board.piece_map().values() if piece.color == chess.WHITE]

    for piece in white_pieces:
        if piece.piece_type in [chess.QUEEN, chess.ROOK, chess.BISHOP]:
            return penalty+90
    if len(white_pieces) != 2:
        return penalty+80

    # === Penalties for Legal Positions ===
    if is_legal:
        info = engine.analyse(board, chess.engine.Limit(depth=MATE_IN*2), multipv=2)
        score = info[0]["score"].pov(board.turn)
        if len(info)>1:
            second_score = info[1]["score"].pov(board.turn)
        else:
            second_score = None

        if not score.is_mate() or score.mate() < 0:
            return penalty+60
        elif score.is_mate() and score.mate() != MATE_IN:
            return penalty+50
        elif second_score is not None and second_score.is_mate() and second_score.mate() == MATE_IN:
            return penalty+40

    return penalty

def Durbar(board, is_legal, engine):
    MATE_IN = THEME_MATE_DEPTHS["Durbar"]
    penalty = 0

    # === Penalties for Legal Positions ===
    if is_legal:
        info = engine.analyse(board, chess.engine.Limit(depth=MATE_IN*2), multipv=2)
        score = info[0]["score"].pov(board.turn)
        if len(info)>1:
            second_score = info[1]["score"].pov(board.turn)
        else:
            second_score = None

        if not score.is_mate() or score.mate() < 0:
            return penalty+60
        elif score.is_mate() and score.mate() != MATE_IN:
            return penalty+50
        elif second_score is not None and second_score.is_mate() and second_score.mate() == MATE_IN:
            return penalty+40

        pv_moves = info[0]["pv"]
        test_board = board.copy()
        for move in pv_moves:
            piece = test_board.piece_at(move.from_square)
            if piece.color == chess.WHITE:
                if piece.piece_type != chess.KING:
                    penalty+=1
            test_board.push(move)

    return penalty

def Excelsior(board, is_legal, engine):
    MATE_IN = THEME_MATE_DEPTHS["Excelsior"]
    penalty = 0

    # === Universal Penalties ===
    white_pawns = [square for square, piece in board.piece_map().items() if piece.piece_type == chess.PAWN and piece.color == chess.WHITE]
    valid_first_rank_pawns = [pawn for pawn in white_pawns if chess.square_rank(pawn) == 1 and chess.square_file(pawn) not in [0, 7]]
    
    if not white_pawns:
        return penalty+80
    if not valid_first_rank_pawns:
        return penalty+70

    # === Penalties for Legal Positions ===
    if is_legal:
        info = engine.analyse(board, chess.engine.Limit(depth=MATE_IN*2), multipv=2)
        score = info[0]["score"].pov(board.turn)
        if len(info)>1:
            second_score = info[1]["score"].pov(board.turn)
        else:
            second_score = None

        if not score.is_mate() or score.mate() < 0:
            return penalty+60
        elif score.is_mate() and score.mate() != MATE_IN:
            return penalty+50
        elif second_score is not None and second_score.is_mate() and second_score.mate() == MATE_IN:
            return penalty+40

        pv_moves = info[0]["pv"]
        current_board = board.copy()
        key_move = pv_moves[0]
        key_piece = current_board.piece_at(key_move.from_square)
        pawn_id = None
        if key_piece.piece_type == chess.PAWN and key_piece.color == chess.WHITE and chess.square_rank(key_move.from_square) == 1 and chess.square_rank(key_move.to_square) == 3:
            pawn_id = key_move.to_square
        else: 
            return penalty+10
            
        current_board.push(key_move)
        white_moves_count = 1
        for move in pv_moves[1:]:
            if current_board.turn == chess.WHITE:
                white_moves_count+=1
                piece = current_board.piece_at(move.from_square)
                if piece and piece.piece_type == chess.PAWN and piece.color == chess.WHITE and move.from_square == pawn_id:
                    pawn_id = move.to_square  
                else:
                    return penalty+10-2*white_moves_count
            current_board.push(move)
            if white_moves_count == MATE_IN:
                break

    return penalty

def Kluver_9(board, is_legal, engine):
    MATE_IN = THEME_MATE_DEPTHS["Kluver_9"]
    penalty = 0
    penalty_add =0
    # === Universal Penalties ===
    king = board.piece_at(chess.E8)
    rook_a8 = board.piece_at(chess.A8)
    rook_h8 = board.piece_at(chess.H8)

    if not king or king.piece_type != chess.KING or king.color != chess.BLACK:
        penalty_add += 90
    if not rook_a8 or rook_a8.piece_type != chess.ROOK or rook_a8.color != chess.BLACK:
        penalty_add += 90
    if not rook_h8 or rook_h8.piece_type != chess.ROOK or rook_h8.color != chess.BLACK:
        penalty_add += 90
    if penalty_add > 0:
        return penalty + penalty_add
    
    # === Penalties for Legal Positions ===
    if is_legal:
        info = engine.analyse(board, chess.engine.Limit(depth=MATE_IN*2), multipv=2)
        score = info[0]["score"].pov(board.turn)
        if len(info)>1:
            second_score = info[1]["score"].pov(board.turn)
        else:
            second_score = None

        if not score.is_mate() or score.mate() < 0:
            return penalty+60
        elif score.is_mate() and score.mate() != MATE_IN:
            return penalty+50
        elif second_score is not None and second_score.is_mate() and second_score.mate() == MATE_IN:
            return penalty+40
        
        temp_board = board.copy()
        try:
            temp_board.turn = chess.BLACK
            if not board.has_kingside_castling_rights(chess.BLACK):
                penalty+=5
            if not board.has_queenside_castling_rights(chess.BLACK):
                penalty+=5
        except:
            return penalty+20
        
    return penalty

def Knight_wheel(board, is_legal, engine):
    MATE_IN = THEME_MATE_DEPTHS["Knight_wheel"]
    penalty = 0

    # === Universal Penalties ===
    black_knights = [square for square, piece in board.piece_map().items() if piece.piece_type == chess.KNIGHT and piece.color == chess.BLACK]
    valid_knights = [knight for knight in black_knights if chess.square_rank(knight) in [2, 3, 4, 5] and chess.square_file(knight) in [2, 3, 4, 5]]
    
    if not black_knights:
        return penalty+80
    if not valid_knights:
        return penalty+70

    # === Penalties for Legal Positions ===
    if is_legal:
        info = engine.analyse(board, chess.engine.Limit(depth=MATE_IN*2), multipv=10)
        score = info[0]["score"].pov(board.turn)
        if len(info)>1:
            second_score = info[1]["score"].pov(board.turn)
        else:
            second_score = None

        if not score.is_mate() or score.mate() < 0:
            return penalty+60
        elif score.is_mate() and score.mate() != MATE_IN:
            return penalty+50
        elif second_score is not None and second_score.is_mate() and second_score.mate() == MATE_IN:
            return penalty+40
        
        pv_moves = info[0]["pv"]
        key_move = pv_moves[0]
        board.push(key_move)

        black_responses = list(board.legal_moves)
        black_knight_destinations = set()
        mate_list = set()
        for black_move in black_responses:
            test_board = board.copy()
            piece = test_board.piece_at(black_move.from_square)
            if piece.piece_type == chess.KNIGHT and piece.color == chess.BLACK:
                if chess.square_rank(black_move.from_square) in [2, 3, 4, 5] and chess.square_file(black_move.from_square) in [2, 3, 4, 5]:
                    if black_move.to_square not in black_knight_destinations:
                        test_board.push(black_move)
                        white_moves = list(test_board.legal_moves)
                        for move in white_moves:
                            new_test_board = test_board.copy()
                            new_test_board.push(move)
                            if new_test_board.is_game_over():
                                if move not in mate_list:
                                    mate_list.add(move)
                                else:
                                    penalty += 0.1
                        black_knight_destinations.add(black_move.to_square)
        penalty += abs (8-len(black_knight_destinations))

    return penalty

def Oktet(board, is_legal, engine):
    MATE_IN = THEME_MATE_DEPTHS["Oktet"]
    penalty = 0

    # === Universal Penalties ===
    piece_counts = { (chess.WHITE, pt): 0 for pt in range(1, 7) }
    piece_counts.update({ (chess.BLACK, pt): 0 for pt in range(1, 7) })
    for square, piece in board.piece_map().items():
        piece_counts[(piece.color, piece.piece_type)] += 1

    white_expected = {
        chess.KING: 1,
        chess.QUEEN: 1,
        chess.ROOK: 2,
        chess.BISHOP: 2,
        chess.KNIGHT: 2,
        chess.PAWN: 0
    }

    black_expected = {
        chess.KING: 1,
        chess.QUEEN: 1,
        chess.ROOK: 2,
        chess.BISHOP: 2,
        chess.KNIGHT: 2,
        chess.PAWN: 8
    }

    for pt in range(1, 7):
        if piece_counts[(chess.WHITE, pt)] != white_expected[pt]:
            penalty += abs(piece_counts[(chess.WHITE, pt)] - white_expected[pt])
        if piece_counts[(chess.BLACK, pt)] != black_expected[pt]:
            penalty += abs(piece_counts[(chess.BLACK, pt)] - black_expected[pt])

    # === Penalties for Legal Positions ===
    if is_legal:
        info = engine.analyse(board, chess.engine.Limit(depth=MATE_IN*2), multipv=2)
        score = info[0]["score"].pov(board.turn)
        if len(info) > 1:
            second_score = info[1]["score"].pov(board.turn)
        else:
            second_score = None

        if not score.is_mate() or score.mate() < 0:
            return penalty+60
        elif score.is_mate() and score.mate() != MATE_IN:
            return penalty+50
        elif second_score is not None and second_score.is_mate() and second_score.mate() == MATE_IN:
            return penalty+40

    return penalty

def Troitsky(board, is_legal, engine):
    MATE_IN = THEME_MATE_DEPTHS["Troitsky"]
    penalty = 0

    # === Universal Penalties ===
    white_bishops = [square for square, piece in board.piece_map().items() if piece.piece_type == chess.BISHOP and piece.color == chess.WHITE]
    
    if not white_bishops:
        return penalty+80

    # === Penalties for Legal Positions ===
    if is_legal:
        info = engine.analyse(board, chess.engine.Limit(depth=MATE_IN*2), multipv=2)
        score = info[0]["score"].pov(board.turn)
        if len(info)>1:
            second_score = info[1]["score"].pov(board.turn)
        else:
            second_score = None

        if not score.is_mate() or score.mate() < 0:
            return penalty+60
        elif score.is_mate() and score.mate() != MATE_IN:
            return penalty+50
        elif second_score is not None and second_score.is_mate() and second_score.mate() == MATE_IN:
            return penalty+40

        pv_moves = info[0]["pv"]
        test_board = board.copy()
        for move in pv_moves:
            test_board.push(move)
        white_pieces = [piece for piece in test_board.piece_map().values()
                        if piece.color == chess.WHITE]
        piece_count = 0
        for piece in white_pieces:
            if piece.piece_type not in [chess.KING, chess.BISHOP]:
                penalty+=5
            else:
                piece_count+=1
        penalty+=abs(2 - piece_count) * 1

    return penalty

THEMES = {
    "No_Theme": No_Theme,
    "Albino": Albino,
    "Amazon": Amazon,
    "Crusader": Crusader,
    "Dark_Doings": Dark_Doings,
    "Durbar": Durbar,
    "Excelsior": Excelsior,
    "Kluver_9": Kluver_9,
    "Knight_wheel": Knight_wheel,
    "Oktet": Oktet,
    "Troitsky": Troitsky
}

THEME_DESCRIPTIONS = {
    "No_Theme": "A problem without a specific theme.",
    "Albino": "A chess problem theme in which a white pawn on its original square, makes each of its four possible moves during the solution.",
    "Amazon": "A chess problem theme in which all the moves of White are made by the queen.",
    "Crusader": "A chess problem theme in which all the moves of White are made by the knight.",
    "Dark_Doings": "A chess problem theme in which White, except for the king, has only one knight or one pawn at their disposal.",
    "Durbar": "A chess problem theme in which all of White’s moves are made by the king, except possibly the last one.",
    "Excelsior": "A chess problem theme in which during the solution a white pawn, starting from its original square, manages to promote.",
    "Kluver_9": "A chess problem theme in which the two black rooks and the black king remain on their original squares and retain the ability to castle.",
    "Knight_wheel": "A chess problem theme in which during the solution a black knight makes any of its eight possible moves in defense, each leading to a different checkmate move by White.",
    "Oktet": "A chess problem theme in which Black has all of their pieces at their disposal, while White has all of their pieces except pawns.",
    "Troitsky": "A chess problem theme in which in the final position White is left with only their king and one bishop."
}

THEME_MATE_DEPTHS = {
    "No_Theme": 3,
    "Albino": 2,
    "Amazon": 6,
    "Crusader": 5,
    "Dark_Doings": 2,
    "Durbar": 5,
    "Excelsior": 5,
    "Kluver_9": 4,
    "Knight_wheel": 2,
    "Oktet": 4,
    "Troitsky": 3
}