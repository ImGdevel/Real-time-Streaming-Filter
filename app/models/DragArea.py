import win32api
import win32con
import tkinter as tk
from threading import Thread
from screeninfo import Monitor, get_monitors

class BlackWindow:
    def __init__(self, app):
    # 불투명한 레이어 생성
        self.overlay = tk.Toplevel(app.root)
        self.overlay.overrideredirect(1)
        #self.overlay.attributes("-fullscreen", True)
        self.overlay.configure(bg="black")
        self.overlay.attributes("-alpha", 0.5)  # 투명도 조절
        # 이벤트 바인딩: 마우스 클릭 이벤트를 무시하도록 합니다.
        self.overlay.bind("<Button-1>", lambda event: "break")
        self.canvas = tk.Canvas(self.overlay, bg="black", highlightthickness=0)

        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_x = None
        self.start_y = None
        self.rect_id = None

        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_button_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_button_motion(self, event):
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        x0, y0 = self.start_x, self.start_y
        x1, y1 = event.x, event.y
        self.rect_id = self.canvas.create_rectangle(x0, y0, x1, y1, outline="white", width=2, fill="white", stipple="gray50")

    def on_button_release(self, event):
        if self.rect_id:
            self.canvas.delete(self.rect_id)
            self.rect_id = None

class BlockClicksWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("400x300")
        self.root.title("Click Blocking Window")
        self.overlays = []
        self.clicked_coordinates = None
        self.root.withdraw()
        
    def run(self):

        self.root.mainloop()

    def start_event_handling(self):
        # 이벤트 처리를 위한 별도의 스레드 시작
        event_thread = Thread(target=self.handle_events)
        event_thread.start()

    def handle_events(self):
        # 이벤트 처리 로직을 여기에 구현
        self.clicked_coordinates = get_mouse_click(self)

    def stop(self):
        for window in self.overlays:
            window.overlay.destroy()
        self.root.quit()

def get_mouse_click(app : BlockClicksWindow):
    # 이전 상태 초기화
    prev_state = win32api.GetKeyState(win32con.VK_LBUTTON)
    while True:
        # 현재 상태 확인
        current_state = win32api.GetKeyState(win32con.VK_LBUTTON)
        
        # 이전 상태와 현재 상태를 비교하여 변화 감지
        if current_state != prev_state:
            # 버튼이 눌렸는지 확인

            if current_state < 0:
                x1, y1 = win32api.GetCursorPos()
                print(f"Mouse down at ({x1}, {y1})")

            if prev_state < 0:
                if current_state >= 0:
                    x2, y2 = win32api.GetCursorPos()
                    print(f"Mouse up at ({x2}, {y2})")
                    app.stop()
                    return x1, y1, x2, y2
                    
        
        # 현재 상태를 이전 상태로 업데이트
        prev_state = current_state

def position_window(window: tk.Tk, monitor: Monitor):
    #window_width, window_height = window.winfo_reqwidth(), window.winfo_reqheight()
    screen_width, screen_height = monitor.width, monitor.height
    #print(f"{screen_width}x{screen_height}+{monitor.x}+{monitor.y}")
    window.geometry(f"{screen_width}x{screen_height}+{monitor.x}+{monitor.y}")
    #window.attributes("-fullscreen", True)

def create_window_on_each_display(app:BlockClicksWindow):
    monitors = get_monitors()
    for i, monitor in enumerate(monitors, start=1):
        window = BlackWindow(app)
        app.overlays.append(window)
        position_window(window.overlay, monitor)


if __name__ == "__main__":

    app = BlockClicksWindow()
    create_window_on_each_display(app)
    app.start_event_handling()
    app.run()

    x1, y1, x2, y2 = app.clicked_coordinates
    print("Clicked coordinates:", x1, y1, x2, y2)

     

