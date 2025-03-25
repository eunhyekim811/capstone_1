# pc_power_log.py
import subprocess
import pandas as pd
from datetime import datetime, timedelta

# 최근 90일 기준
start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')

# PowerShell 명령어
command = (
    "powershell -Command \""
    f"$start = Get-Date '{start_date}'; "
    "Get-WinEvent -LogName System | "
    "Where-Object { ($_.Id -eq 6005) -or ($_.Id -eq 6006) } | "
    "Where-Object { $_.TimeCreated -ge $start } | "
    "Select-Object @{Name='Time';Expression={$_.TimeCreated.ToString('yyyy-MM-dd HH:mm:ss')}}, Id\""
)

# 실행
result = subprocess.run(command, capture_output=True, text=True, shell=True)
lines = result.stdout.strip().split("\n")

# 파싱
data = []
for line in lines:
    if "Time" in line or "----" in line:
        continue
    try:
        parts = line.strip().rsplit(" ", 1)
        time_str, event_id = parts
        timestamp = datetime.strptime(time_str.strip(), "%Y-%m-%d %H:%M:%S")
        event = "PC_ON" if event_id == "6005" else "PC_OFF"
        data.append({"Time": timestamp, "Event": event})
    except:
        continue

# 저장
df = pd.DataFrame(data)
df.to_csv("pc_power_log.csv", index=False)
print(f"✅ {len(df)}개의 ON/OFF 기록을 pc_power_log.csv에 저장했습니다.")
