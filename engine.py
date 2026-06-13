# engine.py
import chess
import random

class ChessEngine:
    def __init__(self):
        self.board = chess.Board()
        self.game_mode = "PvP"  # "PvP", "PvE", "Puzzle"
        self.difficulty = 1     # 1: Asan, 2: Orta, 3: Çətin
        
        # Test üçün daxili mat tapmacaları datası
        self.puzzles = {
            1: [  # 1 gedişlik matlar
                {"fen": "k7/8/1Q6/8/8/8/8/4K3 w - - 0 1", "move": "b6b7"},
                {"fen": "2k5/8/2K5/5R2/8/8/8/8 w - - 0 1", "move": "f5f8"}
            ],
            2: [  # 2 gedişlik matlar
                {"fen": "k7/8/2K5/5Q2/8/8/8/8 w - - 0 1", "move": "f5c8"}
            ]
        }
        self.current_puzzle_type = 1
        self.current_puzzle_index = 0

    def reset_game(self):
        self.board = chess.Board()

    def get_piece_at(self, square):
        piece = self.board.piece_at(square)
        if piece:
            return piece.symbol(), piece.color == chess.WHITE
        return None, None

    def make_move(self, from_square, to_square):
        """Oyunçunun gedişini yoxlayır və icra edir"""
        move = chess.Move(from_square, to_square)
        
        # Piyadanın vəzirə çevrilməsi (Promotion) yoxlanışı
        piece = self.board.piece_at(from_square)
        if piece and piece.piece_type == chess.PAWN:
            if (piece.color == chess.WHITE and chess.square_rank(to_square) == 7) or \
               (piece.color == chess.BLACK and chess.square_rank(to_square) == 0):
                move = chess.Move(from_square, to_square, promotion=chess.QUEEN)

        if move in self.board.legal_moves:
            self.board.push(move)
            return True, self.board.is_checkmate()
        return False, False

    def get_robot_move(self):
        """Robotun çətinlik dərəcəsinə görə gediş seçməsi"""
        legal_moves = list(self.board.legal_moves)
        if not legal_moves:
            return None

        # 1. Əgər bir gedişdə mat varsa, robot bunu mütləq etsin (Bütün səviyyələr üçün)
        for move in legal_moves:
            self.board.push(move)
            if self.board.is_checkmate():
                self.board.pop()
                return move
            self.board.pop()

        # 2. Əgər rəqibin fiqurunu vurmaq mümkündürsə, "Uduş" gedişlərini yığ
        captures = [m for m in legal_moves if self.board.is_capture(m)]

        # SƏVİYYƏ 1: Asan (Tamamilə təsadüfi gedişlər edir)
        if self.difficulty == 1:
            return random.choice(legal_moves)

        # SƏVİYYƏ 2: Orta (%50 ehtimalla ağıllı gediş/daş vurma, %50 təsadüfi)
        elif self.difficulty == 2:
            if captures and random.random() < 0.5:
                return random.choice(captures)
            return random.choice(legal_moves)

        # SƏVİYYƏ 3: Çətin (Həmişə daş vurmağa və ya ən yaxşı mövqeyə can atır)
        else:
            if captures:
                return random.choice(captures)
            return random.choice(legal_moves)

    def load_puzzle(self, puzzle_type, index):
        """Tapmacanı yükləyir"""
        self.game_mode = "Puzzle"
        self.current_puzzle_type = puzzle_type
        self.current_puzzle_index = index
        
        puzzle_list = self.puzzles.get(puzzle_type, self.puzzles[1])
        if index >= len(puzzle_list):
            index = 0
            self.current_puzzle_index = 0
            
        puzzle = puzzle_list[index]
        self.board = chess.Board(puzzle["fen"])

    def check_puzzle_move(self, move_str):
        """Tapmaca rejimində edilən gedişin doğruluğunu yoxlayır"""
        puzzle_list = self.puzzles.get(self.current_puzzle_type, self.puzzles[1])
        correct_move = puzzle_list[self.current_puzzle_index]["move"]
        return move_str.startswith(correct_move)
