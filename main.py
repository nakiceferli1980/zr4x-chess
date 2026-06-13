# main.py
import chess
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Line
from kivy.clock import Clock
from kivy.uix.popup import Popup

from engine import ChessEngine

Window.size = (520, 750)

# Kivy Stilləri birbaşa kodun içinə inteqrasiya olundu
Builder.load_string('''
<SplashScreen>:
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 0.1, 0.1, 0.15, 1
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: "ZR4X GAMES"
            font_size: '40sp'
            bold: True
            color: 1, 1, 1, 1
            halign: 'center'

<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: [20, 40, 20, 40]
        spacing: 15
        canvas.before:
            Color:
                rgba: 0.95, 0.95, 0.95, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: "ŞAHMAT"
            font_size: '36sp'
            bold: True
            color: 0.1, 0.1, 0.2, 1
            size_hint_y: None
            height: '60dp'

        Button:
            text: "İnsan vs İnsan (PvP)"
            font_size: '18sp'
            bold: True
            size_hint_y: None
            height: '50dp'
            background_color: 0.2, 0.4, 0.8, 1
            on_release: root.start_pvp()

        Button:
            text: "Robota Qarşı (PvE)"
            font_size: '18sp'
            bold: True
            size_hint_y: None
            height: '50dp'
            background_color: 0.2, 0.6, 0.4, 1
            on_release: root.show_difficulty_modes()

        BoxLayout:
            id: difficulty_box
            orientation: 'vertical'
            spacing: 5
            size_hint_y: None
            height: 0
            opacity: 0
            disabled: True
            Button:
                text: "Asan"
                bold: True
                background_color: 0.4, 0.7, 0.4, 1
                on_release: root.start_pve(1)
            Button:
                text: "Orta"
                bold: True
                background_color: 0.8, 0.6, 0.2, 1
                on_release: root.start_pve(2)
            Button:
                text: "Çətin"
                bold: True
                background_color: 0.8, 0.2, 0.2, 1
                on_release: root.start_pve(3)

        Button:
            text: "Mat Tapmacaları"
            font_size: '18sp'
            bold: True
            size_hint_y: None
            height: '50dp'
            background_color: 0.5, 0.3, 0.7, 1
            on_release: root.go_to_puzzles()

<PuzzleMenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 15
        spacing: 10
        canvas.before:
            Color:
                rgba: 0.95, 0.95, 0.95, 1
            Rectangle:
                pos: self.pos
                size: self.size

        BoxLayout:
            size_hint_y: None
            height: '50dp'
            spacing: 10
            Button:
                text: "↩ Geri"
                bold: True
                size_hint_x: None
                width: '80dp'
                on_release: root.go_back()
            Label:
                text: "Şahmat Tapmacaları"
                font_size: '20sp'
                bold: True
                color: 0, 0, 0, 1

        Label:
            text: "1 Gedişdə Mat"
            bold: True
            color: 0.2, 0.5, 0.2, 1
            size_hint_y: None
            height: '30dp'

        GridLayout:
            id: grid_1_move
            cols: 5
            spacing: 5
            size_hint_y: None
            height: '100dp'

        Label:
            text: "2 Gedişdə Mat"
            bold: True
            color: 0.7, 0.2, 0.2, 1
            size_hint_y: None
            height: '30dp'

        GridLayout:
            id: grid_2_move
            cols: 5
            spacing: 5
            size_hint_y: None
            height: '100dp'
        
        Widget:

<GameScreen>:
    canvas.before:
        Color:
            rgba: 0.9, 0.9, 0.9, 1
        Rectangle:
            pos: self.pos
            size: self.size
''')

COLORS = {
    'light_square': (1, 1, 1, 1),           
    'dark_square': (0.75, 0.75, 0.75, 1),    
    'text_coords': (0.2, 0.2, 0.2, 1),       
    'select_highlight': (0.3, 0.8, 0.3, 0.6), 
    'legal_move': (0.4, 0.9, 0.4, 0.5),      
    'legal_capture': (0.9, 0.2, 0.2, 0.6),   
    'check_king': (1, 0, 0, 0.8),            
}

UNICODE_PIECES = {
    'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 
    'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚'  
}

chess_engine = ChessEngine()

class SplashScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.switch_to_menu, 3.0)
    def switch_to_menu(self, dt):
        self.manager.current = 'menu'

class MenuScreen(Screen):
    def show_difficulty_modes(self):
        box = self.ids.difficulty_box
        if box.opacity == 0:
            box.height = '120dp'; box.opacity = 1; box.disabled = False
        else:
            box.height = 0; box.opacity = 0; box.disabled = True

    def start_pvp(self):
        chess_engine.reset_game()
        chess_engine.game_mode = "PvP"
        self.manager.current = 'game'

    def start_pve(self, level):
        chess_engine.reset_game()
        chess_engine.game_mode = "PvE"
        chess_engine.difficulty = level
        self.manager.current = 'game'

    def go_to_puzzles(self):
        self.manager.current = 'puzzle_menu'

class PuzzleMenuScreen(Screen):
    def on_enter(self):
        self.ids.grid_1_move.clear_widgets()
        for i in range(10):
            btn = Button(text=str(i+1), bold=True, background_color=(0.2, 0.6, 0.2, 1))
            btn.bind(on_release=lambda instance, idx=i: self.start_puzzle(1, idx))
            self.ids.grid_1_move.add_widget(btn)

        self.ids.grid_2_move.clear_widgets()
        for i in range(10):
            btn = Button(text=str(i+1), bold=True, background_color=(0.6, 0.2, 0.2, 1))
            btn.bind(on_release=lambda instance, idx=i: self.start_puzzle(2, idx))
            self.ids.grid_2_move.add_widget(btn)

    def start_puzzle(self, p_type, index):
        chess_engine.load_puzzle(p_type, index)
        self.manager.current = 'game'

    def go_back(self):
        self.manager.current = 'menu'

class GameScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        main_layout = BoxLayout(orientation='vertical')
        
        top_bar = BoxLayout(size_hint_y=None, height='50dp', padding=[10, 5], spacing=10)
        with top_bar.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Line(rectangle=(top_bar.x, top_bar.y, top_bar.width, top_bar.height), width=1)

        back_text = "↩ Menyu" if chess_engine.game_mode != "Puzzle" else "↩ Tapmacalar"
        back_btn = Button(text=back_text, size_hint_x=None, width='100dp', bold=True)
        back_btn.bind(on_release=self.go_back)
        
        if chess_engine.game_mode == "Puzzle":
            mode_text = f"{chess_engine.current_puzzle_type} Gedişli Mat - Səviyyə {chess_engine.current_puzzle_index + 1}"
        else:
            mode_text = "Robot" if chess_engine.game_mode == "PvE" else "İnsan vs İnsan"
            
        self.status_label = Label(text=mode_text, bold=True, color=(0, 0, 0, 1))
        
        top_bar.add_widget(back_btn)
        top_bar.add_widget(self.status_label)
        main_layout.add_widget(top_bar)
        
        self.board_container = FloatLayout()
        self.visual_board = VisualBoardGrid(status_label=self.status_label)
        self.board_container.add_widget(self.visual_board)
        
        main_layout.add_widget(self.board_container)
        self.add_widget(main_layout)
        
        Clock.schedule_once(self.sync_coordinates, 0.05)

    def sync_coordinates(self, dt):
        b_x, b_y = self.visual_board.pos
        b_w, b_h = self.visual_board.size
        cell = b_w / 8

        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        ranks = ['1', '2', '3', '4', '5', '6', '7', '8']

        for i, file_char in enumerate(files):
            lbl = Label(text=file_char, font_size='13sp', color=COLORS['text_coords'],
                        size_hint=(None, None), size=(cell, 20),
                        x=b_x + (i * cell), y=b_y - 22)
            self.board_container.add_widget(lbl)

        for i, rank_char in enumerate(ranks):
            lbl = Label(text=rank_char, font_size='13sp', color=COLORS['text_coords'],
                        size_hint=(None, None), size=(20, cell),
                        x=b_x - 22, y=b_y + ((7 - i) * cell))
            self.board_container.add_widget(lbl)

    def go_back(self, instance):
        if chess_engine.game_mode == "Puzzle":
            self.manager.current = 'puzzle_menu'
        else:
            self.manager.current = 'menu'

class VisualBoardGrid(GridLayout):
    def __init__(self, status_label, **kwargs):
        super().__init__(**kwargs)
        self.cols = 8
        self.rows = 8
        self.spacing = 0 
        self.size_hint = (None, None) 
        
        self.engine = chess_engine
        self.status_label = status_label
        self.selected_square = None
        self.grid_buttons = {}
        
        self.ensure_square_squares()
        Window.bind(on_resize=self.ensure_square_squares)
        
        self.render_board()

    def ensure_square_squares(self, *args):
        side = min(Window.width - 60, Window.height - 180)
        self.size = (side, side)
        self.pos = ((Window.width - side) / 2, (Window.height - side) / 2 + 10)

    def render_board(self):
        self.clear_widgets()
        for row in reversed(range(8)):
            for col in range(8):
                square = chess.square(col, row)
                symbol, is_white = self.engine.get_piece_at(square)
                bg_color = COLORS['light_square'] if (row + col) % 2 == 0 else COLORS['dark_square']
                
                btn = Button(
                    text="",
                    font_size='32sp',
                    font_name='DejaVuSans.ttf',  
                    background_normal='',
                    background_disabled_normal='',
                    halign='center',
                    valign='middle'
                )
                btn.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
                
                if symbol:
                    btn.text = UNICODE_PIECES.get(symbol, '')
                    btn.color = (0.1, 0.3, 0.6, 1) if is_white else (0, 0, 0, 1)
                
                btn.background_color = bg_color
                btn.custom_bg = bg_color
                btn.bind(on_release=lambda instance, s=square: self.tile_clicked(s))
                self.add_widget(btn)
                self.grid_buttons[square] = btn
        
        self.highlight_check_if_any()

    def tile_clicked(self, square):
        if self.engine.board.is_game_over(): return

        if self.selected_square is None:
            symbol, is_white = self.engine.get_piece_at(square)
            if symbol:
                self.selected_square = square
                self.show_legal_moves(square)
        else:
            if self.selected_square == square:
                self.selected_square = None
                self.refresh_graphics()
                return

            move_str = chess.square_name(self.selected_square) + chess.square_name(square)
            success, checkmate = self.engine.make_move(self.selected_square, square)
            
            if success:
                if self.engine.game_mode == "Puzzle":
                    if self.engine.check_puzzle_move(move_str):
                        self.status_label.text = "TEBRİKLER! DÜZGÜN GƏDİŞ!"
                        self.status_label.color = (0, 0.6, 0, 1)
                        App.get_running_app().trigger_game_finished()
                    else:
                        self.status_label.text = "SƏHV GƏDİŞ! YENİDƏN CƏHD ET."
                        self.status_label.color = (1, 0, 0, 1)
                        self.engine.board.pop() 
                else:
                    self.update_status(checkmate)
                    # Robotun növbəsidirsə, gedişi başladırıq
                    if self.engine.game_mode == "PvE" and not self.engine.board.is_game_over():
                        Clock.schedule_once(self.robot_turn, 0.2)

                self.selected_square = None
                self.refresh_graphics()
            else:
                symbol, is_white = self.engine.get_piece_at(square)
                if symbol and (self.engine.board.turn == chess.WHITE if is_white else chess.BLACK):
                    self.selected_square = square
                    self.show_legal_moves(square)
                else:
                    self.selected_square = None
                    self.refresh_graphics()

    def show_legal_moves(self, from_square):
        self.refresh_graphics() 
        self.grid_buttons[from_square].background_color = COLORS['select_highlight']
        for move in self.engine.board.legal_moves:
            if move.from_square == from_square:
                to_square = move.to_square
                if self.engine.board.is_capture(move):
                    self.grid_buttons[to_square].background_color = COLORS['legal_capture']
                else:
                    self.grid_buttons[to_square].background_color = COLORS['legal_move']

    def robot_turn(self, dt):
        """Robotun hesablama aparıb gediş etməsi və ekranı yeniləməsi"""
        robot_move = self.engine.get_robot_move()
        if robot_move:
            self.engine.board.push(robot_move)
            self.update_status(self.engine.board.is_checkmate())
            self.refresh_graphics()  # Robotun gedişi artıq vizual olaraq yenilənir!

    def highlight_check_if_any(self):
        if self.engine.board.is_check():
            king_square = self.engine.board.king(self.engine.board.turn)
            if king_square is not None:
                self.grid_buttons[king_square].background_color = COLORS['check_king']

    def update_status(self, checkmate):
        if checkmate:
            self.status_label.text = "MAT! OYUN BİTDİ."
            self.status_label.color = (1, 0, 0, 1)
            App.get_running_app().trigger_game_finished()
        elif self.engine.board.is_game_over():
            self.status_label.text = "BƏRABƏRƏ!"
            self.status_label.color = (0.5, 0.5, 0.5, 1)
            App.get_running_app().trigger_game_finished()
        else:
            turn = "Ağlar" if self.engine.board.turn == chess.WHITE else "Qaralar"
            self.status_label.text = f"Növbə: {turn}"
            self.status_label.color = (0, 0, 0, 1)

    def refresh_graphics(self):
        for square in chess.SQUARES:
            symbol, is_white = self.engine.get_piece_at(square)
            btn = self.grid_buttons[square]
            if symbol:
                btn.text = UNICODE_PIECES.get(symbol, '')
                btn.color = (0.1, 0.3, 0.6, 1) if is_white else (0, 0, 0, 1)
            else:
                btn.text = ''
            btn.background_color = btn.custom_bg
        self.highlight_check_if_any()

class ChessApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_counter = 0  

    def build(self):
        Window.bind(on_request_close=self.confirm_exit)
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(PuzzleMenuScreen(name='puzzle_menu'))
        sm.add_widget(GameScreen(name='game'))
        return sm

    def trigger_game_finished(self):
        self.game_counter += 1
        print(f"[REKLAM SİSTEMİ] Tur bitdi. Cari sayğac: {self.game_counter}/3")
        if self.game_counter >= 3:
            self.show_interstitial_ad()
            self.game_counter = 0  

    def show_interstitial_ad(self):
        print("[REKLAM SİSTEMİ] 3 tur tamamlandı! Tam ekran reklam göstərilir...")

    def confirm_exit(self, *args):
        content = BoxLayout(orientation='vertical', padding=15, spacing=15)
        msg = Label(text="Oyundan çıxmaq istəyirsiniz?", font_size='16sp', bold=True)
        content.add_widget(msg)
        
        btn_box = BoxLayout(spacing=15, size_hint_y=None, height='45dp')
        yes_btn = Button(text="Bəli", bold=True, background_color=(0.7, 0.1, 0.1, 1))
        no_btn = Button(text="Xeyr", bold=True, background_color=(0.2, 0.2, 0.2, 1))
        
        btn_box.add_widget(yes_btn)
        btn_box.add_widget(no_btn)
        content.add_widget(btn_box)
        
        self.exit_popup = Popup(
            title="ZR4X GAMES", 
            content=content, 
            size_hint=(None, None), 
            size=('320dp', '180dp'),
            auto_dismiss=False
        )
        
        yes_btn.bind(on_release=self.exit_app)
        no_btn.bind(on_release=self.exit_popup.dismiss)
        
        self.exit_popup.open()
        return True 

    def exit_app(self, instance):
        self.exit_popup.dismiss()
        self.stop()

if __name__ == '__main__':
    ChessApp().run()
