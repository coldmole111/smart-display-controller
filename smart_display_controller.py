import tkinter as tk
from tkinter import ttk
import platform
import ctypes

if platform.system() == "Windows":
    import winreg

class RealDisplayControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("디스플레이 및 밝기 (실제 작동 제어)")
        self.root.geometry("420x530")
        self.root.configure(bg="#f2f2f7")  # 아이폰 설정창 배경 색상
        
        style = ttk.Style()
        style.theme_use('clam')
        
        # 상단 타이틀
        title_frame = tk.Frame(root, bg="#f2f2f7")
        title_frame.pack(fill="x", padx=20, pady=20)
        tk.Label(title_frame, text="디스플레이 및 밝기", font=("Malgun Gothic", 18, "bold"), bg="#f2f2f7", fg="#000000").pack(anchor="w")
        
        # 메인 그룹 박스
        main_box = tk.Frame(root, bg="#ffffff", bd=0, highlightthickness=0)
        main_box.pack(fill="both", expand=True, padx=20, pady=5)
        
        # 1. 다크 모드 (실제 윈도우 테마 전환)
        dark_frame = tk.Frame(main_box, bg="#ffffff", pady=12, padx=15)
        dark_frame.pack(fill="x")
        
        tk.Label(dark_frame, text="🌙 다크 모드", font=("Malgun Gothic", 11, "bold"), bg="#ffffff", fg="#000000").pack(side="left")
        self.dark_var = tk.BooleanVar(value=False)
        self.dark_toggle = ttk.Checkbutton(dark_frame, text="켬/끔", variable=self.dark_var, command=self.toggle_dark_mode)
        self.dark_toggle.pack(side="right")
        
        tk.Label(main_box, text=" 윈도우 시스템 전체 테마를 어둡게 전환합니다.", font=("Malgun Gothic", 8), bg="#ffffff", fg="#8e8e93").pack(anchor="w", padx=15, pady=(0, 5))
        
        ttk.Separator(main_box, orient="horizontal").pack(fill="x", padx=15, pady=5)
        
        # 2. True Tone (실제 미세 화이트 밸런스 보정)
        truetone_frame = tk.Frame(main_box, bg="#ffffff", pady=12, padx=15)
        truetone_frame.pack(fill="x")
        
        tk.Label(truetone_frame, text="🎨 True Tone 모드", font=("Malgun Gothic", 11, "bold"), bg="#ffffff", fg="#000000").pack(side="left")
        self.truetone_var = tk.BooleanVar(value=False)
        self.truetone_toggle = ttk.Checkbutton(truetone_frame, text="켬/끔", variable=self.truetone_var, command=self.apply_display_settings)
        self.truetone_toggle.pack(side="right")
        
        tk.Label(main_box, text=" 화면의 색감을 자연스럽고 편안한 톤으로 미세 보정합니다.", font=("Malgun Gothic", 8), bg="#ffffff", fg="#8e8e93").pack(anchor="w", padx=15, pady=(0, 5))
        
        ttk.Separator(main_box, orient="horizontal").pack(fill="x", padx=15, pady=5)
        
        # 3. Night Shift (실제 블루라이트 차단 및 색온도 조절)
        night_frame = tk.Frame(main_box, bg="#ffffff", pady=12, padx=15)
        night_frame.pack(fill="x")
        
        tk.Label(night_frame, text="🌅 Night Shift (블루라이트)", font=("Malgun Gothic", 11, "bold"), bg="#ffffff", fg="#000000").pack(side="left")
        self.night_var = tk.BooleanVar(value=False)
        self.night_toggle = ttk.Checkbutton(night_frame, text="켬/끔", variable=self.night_var, command=self.toggle_night_shift)
        self.night_toggle.pack(side="right")
        
        tk.Label(main_box, text=" 화면의 푸른빛을 줄여 따뜻한 색감으로 눈의 피로를 낮춥니다.", font=("Malgun Gothic", 8), bg="#ffffff", fg="#8e8e93").pack(anchor="w", padx=15, pady=(0, 5))
        
        # 색온도 강도 조절 슬라이더
        slider_frame = tk.Frame(main_box, bg="#ffffff", pady=8, padx=15)
        slider_frame.pack(fill="x")
        
        tk.Label(slider_frame, text="덜 따뜻함", font=("Malgun Gothic", 8), bg="#ffffff", fg="#3a3a3c").pack(side="left")
        tk.Label(slider_frame, text="더 따뜻함", font=("Malgun Gothic", 8), bg="#ffffff", fg="#3a3a3c").pack(side="right")
        
        self.temp_slider = ttk.Scale(main_box, from_=0, to=100, orient="horizontal", command=self.on_slider_move)
        self.temp_slider.set(0)
        self.temp_slider.pack(fill="x", padx=15, pady=(0, 15))
        
        # 하단 상태 바
        self.status_label = tk.Label(root, text="디스플레이 제어 대기 중...", font=("Malgun Gothic", 9), bg="#f2f2f7", fg="#555555")
        self.status_label.pack(pady=15)

        # 프로그램 종료 시 화면 색감 원래대로 복구 등록
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def set_screen_color(self, red_scale, green_scale, blue_scale):
        """윈도우 GDI API를 이용해 실제 모니터 감마 램프(색온도)를 조작하는 핵심 함수"""
        if platform.system() != "Windows":
            return
        try:
            hdc = ctypes.windll.user32.GetDC(0)
            ramp = (ctypes.c_ushort * 768)()
            for i in range(256):
                val = i * 256
                r = int(min(65535, val * red_scale))
                g = int(min(65535, val * green_scale))
                b = int(min(65535, val * blue_scale))
                
                ramp[i] = r          # Red 채널
                ramp[256 + i] = g    # Green 채널
                ramp[512 + i] = b    # Blue 채널 (블루라이트 조절 핵심)
                
            ctypes.windll.gdi32.SetDeviceGammaRamp(hdc, ctypes.byref(ramp))
            ctypes.windll.user32.ReleaseDC(0, hdc)
        except Exception as e:
            print("색온도 적용 오류:", e)

    def apply_display_settings(self):
        """토글 상태와 슬라이더 값에 따라 실제 화면 색감을 연산하여 적용"""
        r_scale = 1.0
        g_scale = 1.0
        b_scale = 1.0
        
        # True Tone 적용 시 (약간의 자연스러운 온백색 보정)
        if self.truetone_var.get():
            g_scale *= 0.98
            b_scale *= 0.92
            
        # Night Shift 적용 시 (슬라이더 강도에 따라 블루라이트 대폭 차단 및 붉은기 추가)
        if self.night_var.get():
            strength = self.temp_slider.get() / 100.0  # 0.0 ~ 1.0
            # 파란색을 강제로 깎고(최대 50% 차단), 초록색도 일부 줄여 따뜻한 톤 연출
            b_scale *= (1.0 - (strength * 0.55))
            g_scale *= (1.0 - (strength * 0.20))
            r_scale *= (1.0 + (strength * 0.05)) # 붉은빛 미세 증가
            
        self.set_screen_color(r_scale, g_scale, b_scale)

    def toggle_dark_mode(self):
        is_dark = self.dark_var.get()
        if platform.system() == "Windows":
            try:
                registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
                key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
                key = winreg.OpenKey(registry, key_path, 0, winreg.KEY_SET_VALUE)
                val = 0 if is_dark else 1 
                winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, val)
                winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, val)
                winreg.CloseKey(key)
                mode_str = "다크 모드" if is_dark else "라이트 모드"
                self.status_label.config(text=f"시스템 테마: {mode_str} 전환 완료")
            except Exception as e:
                self.status_label.config(text="레지스트리 권한 오류 발생")

    def toggle_truetone(self):
        self.apply_display_settings()
        status = "켜짐" if self.truetone_var.get() else "꺼짐"
        self.status_label.config(text=f"True Tone 모드: {status}")

    def toggle_night_shift(self):
        is_on = self.night_var.get()
        if is_on and self.temp_slider.get() == 0:
            self.temp_slider.set(50)  # 켜면 기본 50%로 세팅
        elif not is_on:
            self.temp_slider.set(0)   # 끄면 0%로 초기화
            
        self.apply_display_settings()
        status = "활성화" if is_on else "비활성화"
        self.status_label.config(text=f"Night Shift: {status}")

    def on_slider_move(self, val):
        strength = int(float(val))
        if strength > 0 and not self.night_var.get():
            self.night_var.set(True) # 슬라이더 건드리면 자동으로 Night Shift 켜지게 연동
        elif strength == 0 and self.night_var.get():
            self.night_var.set(False)
            
        self.apply_display_settings()
        self.status_label.config(text=f"Night Shift 따뜻한 정도: {strength}% (실시간 적용 중)")

    def on_closing(self):
        """프로그램을 끌 때 모니터 색감을 원래 상태(기본값)로 안전하게 되돌림"""
        self.set_screen_color(1.0, 1.0, 1.0)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RealDisplayControlApp(root)
    root.mainloop()