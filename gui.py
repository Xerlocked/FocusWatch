import sys
import subprocess
import platform
from PyQt6.QtWidgets import QMainWindow, QApplication, QListWidget, QComboBox, QGridLayout, QPushButton, QWidget, QSizePolicy, QMenu, QMessageBox, QLabel, QVBoxLayout
from PyQt6.QtGui import QAction, QIcon, QShortcut, QKeySequence
from PyQt6.QtCore import Qt, pyqtSignal, QTime, QTimer
from qt_material import apply_stylesheet
import pygetwindow as gw


class WorkerTimer(QTimer):
    update_signal = pyqtSignal(int)
    update_state_signal = pyqtSignal(bool)
    
    def __init__(self, parnet = None):
        super().__init__()
        self.parent = parnet
        self.elapsed_time = 0
        self.timeout.connect(self.on_timeout)
        self.os = platform.system()
    
    def on_clear(self):
        self.elapsed_time = 0
    
    def on_timeout(self):
        if self.parent == None:
            return
        
        active_window_title = gw.getActiveWindowTitle() if self.os == "Windows" else self.getActiveWindowTitleForMacOS()
        
        if self.parent.is_item_exists(active_window_title):
            self.elapsed_time += 1
            self.update_state_signal.emit(True)
        else:
            self.update_state_signal.emit(False)
        self.update_signal.emit(self.elapsed_time)
        
        
    def getActiveWindowTitleForMacOS(self):
        
        print('HI')
        script = '''
        tell application "System Events"
            set frontApp to name of first application process whose frontmost is true
        end tell
        tell application frontApp
            set windowTitle to name of front window
        end tell
        return windowTitle
        '''
    
        result = subprocess.run(['osascript', '-e', script], stdout=subprocess.PIPE)
        window_title = result.stdout.decode('utf-8').strip()
        return window_title


class MainPanel(QMainWindow):
    
    def __init__(self, sub_panel, worker):
        super().__init__()
        
        self.initialize(sub_panel, worker)
        
    def initialize(self, sub_panel, worker):
        
        # Sub Panel
        self.sub_panel = sub_panel
        
        # Time Worker
        self.worker = worker
        
        exitAct = QAction(QIcon(), 'Exit', self)
        
        # 플랫폼 설정(나중에 수정)
        if platform.system() == "Darwin":
            exitAct.setShortcut(QKeySequence(Qt.Modifier.META) | Qt.Key.Key_Q)
        else:
            exitAct.setShortcut('Ctrl+Q')
        
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        
        # 중앙 위젯 설정
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        # 콤보 박스
        self.combo_process_list = QComboBox(self)
        self.combo_process_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.combo_process_list.textActivated[str].connect(self.add_process)
        
        # 타이머 시작 버튼
        start_button = QPushButton(self)
        start_button.setFixedSize(64, 32)
        start_button.clicked.connect(self.command_start_timer)
        
        # 시작 아이콘
        start_icon = QIcon("play.svg")
        start_button.setIcon(start_icon)

        # 프로세스 목록 리프레시 버튼
        refresh_button = QPushButton(self)
        refresh_button.setFixedSize(48, 32)
        refresh_button.setProperty('class', 'secondary_button')
        refresh_button.clicked.connect(self.command_refresh_process)
        
        # 리프레시 아이콘
        refresh_icon = QIcon("refresh.svg")
        refresh_button.setIcon(refresh_icon)
        
        # 리스트
        self.process_list_widget = QListWidget()
        
        self.process_list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.process_list_widget.customContextMenuRequested.connect(self.show_context_menu)
        
        # 화면 그리드
        grid = QGridLayout()
        
        grid.addWidget(self.combo_process_list, 0, 0)
        grid.addWidget(start_button, 0, 1)
        grid.addWidget(refresh_button, 0, 2)
        grid.addWidget(self.process_list_widget, 1, 0, 2, 0)
        
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 0)
        grid.setColumnStretch(2, 0)
        
        grid.setRowStretch(0, 0)
        grid.setRowStretch(0, 1)
        
        central_widget.setLayout(grid)
        
        # self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')
        self.setFixedSize(350, 230)
        self.show()
        
        # 현재 실행 중인 프로세스 리스트 초기화
        self.command_refresh_process()
        
    def show_context_menu(self, pos):
        # QMenu 생성
        context_menu = QMenu(self)
        
        # QAction 생성
        action_delete = QAction("삭제", self)
        context_menu.addAction(action_delete)
        
        # QAction 이벤트 연결
        action_delete.triggered.connect(self.delete_selected_item)
        context_menu.exec(self.process_list_widget.viewport().mapToGlobal(pos))
        
        
    def delete_selected_item(self):
        # 선택된 아이템
        selected_item = self.process_list_widget.currentItem()
        
        if selected_item:
            self.process_list_widget.takeItem(self.process_list_widget.row(selected_item))
        
        
    def command_refresh_process(self):
        
        # 모든 활성화된 윈도우 창 가져오기
        windows = self.get_all_window_titles()
        
        if len(windows) > 0:
            self.combo_process_list.clear()
            self.combo_process_list.addItems(windows)


    def get_all_window_titles(self):
        os = platform.system()
        
        if os == "Windows":
            windows = gw.getAllTitles()
        
        elif os == "Darwin":
            # macOS에서 활성화된 윈도우 창 가져오기
            script = '''
            tell application "System Events"
                set window_list to ""
                set app_list to application processes
                repeat with app in app_list
                    set win_list to every window of app
                    repeat with win in win_list
                        set window_list to window_list & (name of app & " - " & name of win & linefeed)
                    end repeat
                end repeat
            end tell
            return window_list
            '''
            result = subprocess.run(['osascript', '-e', script], stdout=subprocess.PIPE)
            windows = result.stdout.decode('utf-8').strip().splitlines()
        
        else:
            windows = []
            
        windows = [title for title in windows if title]
        
        return windows

        
    def command_start_timer(self):
        if self.worker:
            self.worker.start(1000)
            
        self.hide()
        self.sub_panel.show()
        
        
    def add_process(self, process_name):
        
        if len(self.process_list_widget) == 3:
            QMessageBox.information(self, "오류", "최대 3개까지 가능합니다.\r\n기존 목록을 삭제 해주세요.")
            return
        
        if self.is_item_exists(process_name):
            return
        
        self.process_list_widget.addItem(process_name)
        
    def is_item_exists(self, item):
        
        for index in range(self.process_list_widget.count()):
            if self.process_list_widget.item(index).text() == item:
                return True
        return False

# 서브 패널
class SubPanel(QMainWindow):
    
    def __init__(self, main_panel, worker):
        super().__init__()
        
        self.main_panel = main_panel
        
        self.worker = worker
        
        self.setWindowTitle('sub window')
        self.setFixedSize(250, 80)
        
        # 윈도우 플래그 설정
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet('background-color: #000000;')
        self.setWindowOpacity(0.5) # 윈도우 투명도 조절
        
        self.timer_label = QLabel('00:00:00', self)
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet('font-size: 46px; color: #ffffff;')
        
        # 레이아웃
        layout = QVBoxLayout()
        layout.addWidget(self.timer_label)
        
        # 중앙 레이아웃
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        if platform.system() == 'Darwin':
            stop_shortcut = QShortcut(QKeySequence(Qt.Modifier.META | Qt.Key.Key_S), self)
            clear_shortcut = QShortcut(QKeySequence(Qt.Modifier.META | Qt.Key.Key_R), self)
        else:
            stop_shortcut  = QShortcut(QKeySequence("Ctrl+S"), self)
            clear_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
            
        stop_shortcut.activated.connect(self.stop_timer)
        clear_shortcut.activated.connect(self.clear_timer)
        
        # 쓰레드 연결
        self.worker.update_signal.connect(self.update_timer)
        self.worker.update_state_signal.connect(self.update_state)
        
    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()


    def mouseMoveEvent(self, event):
        self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos )
        self.dragPos = event.globalPosition().toPoint()
        event.accept()
        
        
    def update_state(self, state):
        
        if state:
            self.timer_label.setStyleSheet('font-size: 46px; color: #E11837;')
        else:
            self.timer_label.setStyleSheet('font-size: 46px; color: #ffffff;')
        
    def update_timer(self, elapsed_time):
        # 경과 시간 시,분,초로 포맷팅
        time = QTime(0, 0).addSecs(elapsed_time)
        self.timer_label.setText(time.toString("hh:mm:ss"))
        
        
    def stop_timer(self):
        self.hide()
        self.worker.stop()
        self.main_panel.show()
        
    def clear_timer(self):
        self.worker.on_clear()

def main():
    app = QApplication(sys.argv)
    
    # setup stylesheet
    apply_stylesheet(app, theme='light_red.xml', css_file='custom.css')

    worker_timer = WorkerTimer()

    mp = MainPanel(None, worker_timer)
    sp = SubPanel(mp, worker_timer)
    
    mp.sub_panel = sp
    worker_timer.parent = mp
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()