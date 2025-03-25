import pandas as pd
from datetime import datetime

# 📌 파일 경로 상수
LOG_FILE = "idle_log.csv"
FEATURE_FILE = "features.csv"
LABEL_FILE = "labels.csv"

print(f"📌 전처리 실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 로그 로드
try:
    df = pd.read_csv(LOG_FILE)
except FileNotFoundError as e:
    print(f"❌ 로그 파일을 찾을 수 없습니다: {e}")
    exit()

if df.empty:
    print("⚠ 로그 파일은 있지만 비어 있습니다.")
    exit()

# 요일/시간 추출
df["Weekday_Num"] = pd.to_datetime(df["Date"]).dt.weekday
df["Hour"] = pd.to_datetime(df["Time"]).dt.hour

# Feature / Label 생성
X = df[["Weekday_Num", "Hour", "CPU_Usage", "Disk_Activity_KB"]]
y = df["Idle"]

print("✅ Feature 샘플:")
print(X.head())

print("\n✅ Label 샘플:")
print(y.head())

# 저장
X.to_csv(FEATURE_FILE, index=False)
y.to_csv(LABEL_FILE, index=False)
print("✅ 전처리 완료 → features.csv, labels.csv 저장됨.")
