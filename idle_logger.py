import time
import psutil
from pynput import mouse, keyboard
from datetime import datetime
import csv
import os
from pathlib import Path

# ========== 설정 ==========
IDLE_THRESHOLD = 6  # 10분
CPU_USAGE_THRESHOLD = 20.0  # CPU 사용률 기준
DISK_IO_THRESHOLD = 200  # KB 기준

PREPROCESS_INTERVAL = 21600  # 6시간
last_preprocess_time = time.time()

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# ========== 유틸 함수 ==========
def get_weekly_log_file():
    now = datetime.now()
    year, week, _ = now.isocalendar()
    return LOG_DIR / f"idle_log_{year}-W{week:02}.csv"

def init_log_file(log_path):
    if not log_path.exists():
        with open(log_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Time", "Weekday", "CPU_Usage", "Disk_Activity_KB", "Idle"])

# ========== 입력 리스너 ==========
last_input_time = time.time()

def on_input_detected(event):
    global last_input_time
    last_input_time = time.time()

mouse_listener = mouse.Listener(on_move=on_input_detected, on_click=on_input_detected, on_scroll=on_input_detected)
keyboard_listener = keyboard.Listener(on_press=on_input_detected)
mouse_listener.daemon = True
keyboard_listener.daemon = True
mouse_listener.start()
keyboard_listener.start()

# ========== 실행 ==========
print("✅ 유휴 상태 감지 시작 (Ctrl+C로 종료)")
init_log_file(get_weekly_log_file())

ran_power_log_today = False

try:
    while True:
        current_time = time.time()
        idle_time = current_time - last_input_time

        prev_io = psutil.disk_io_counters()
        time.sleep(1)
        curr_io = psutil.disk_io_counters()

        read_kb = (curr_io.read_bytes - prev_io.read_bytes) / 1024
        write_kb = (curr_io.write_bytes - prev_io.write_bytes) / 1024
        disk_activity = read_kb + write_kb

        cpu_usage = psutil.cpu_percent(interval=1.0)

        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        weekday = now.strftime("%A")

        is_idle = (
            idle_time >= IDLE_THRESHOLD and
            cpu_usage < CPU_USAGE_THRESHOLD and
            disk_activity < DISK_IO_THRESHOLD
        )

        log_file = get_weekly_log_file()
        init_log_file(log_file)

        with open(log_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                date, time_str, weekday,
                round(cpu_usage, 2), round(disk_activity, 2),
                int(is_idle)
            ])
            state = "🟡유휴" if is_idle else "🟢활성"
            print(f"{state} 상태 기록됨 ({time_str})")

        # 전처리 주기 확인
        if current_time - last_preprocess_time >= PREPROCESS_INTERVAL:
            print("⏱ 6시간 경과 → 자동 전처리 실행")
            os.system("python idle_preprocess.py >> preprocess.log")
            last_preprocess_time = current_time

        # PC 전원 로그 수집
        if now.strftime('%H:%M') == "21:54" and not ran_power_log_today:
            print("🔌 PC ON/OFF 로그 수집")
            os.system("python pc_power_log.py")
            ran_power_log_today = True

        # 자정이 지나면 초기화
        if now.strftime('%H:%M') == "00:00":
            ran_power_log_today = False

        time.sleep(5)

except KeyboardInterrupt:
    print("🛑 유휴 상태 감지 종료됨")
    mouse_listener.stop()
    keyboard_listener.stop()
