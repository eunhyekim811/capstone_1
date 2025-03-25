import psutil
import time

print("💽 실시간 디스크 활동 모니터링 시작 (Ctrl+C로 종료)\n")

prev_io = psutil.disk_io_counters()

try:
    while True:
        time.sleep(1)

        curr_io = psutil.disk_io_counters()

        # 1초간의 변화량 계산 (바이트 단위 → KB 단위로 변환)
        read_diff = (curr_io.read_bytes - prev_io.read_bytes) / 1024
        write_diff = (curr_io.write_bytes - prev_io.write_bytes) / 1024
        total_diff = read_diff + write_diff

        print(f"📊 디스크 사용량: 읽기 {read_diff:.2f}KB, 쓰기 {write_diff:.2f}KB, 총 {total_diff:.2f}KB")

        prev_io = curr_io

except KeyboardInterrupt:
    print("\n🛑 모니터링 종료됨.")
