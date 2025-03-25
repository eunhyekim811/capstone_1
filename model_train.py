import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
from datetime import datetime

# 실행 로그 출력
print(f"📌 모델 학습 시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 데이터 불러오기
try:
    X = pd.read_csv("features.csv")
    y = pd.read_csv("labels.csv").values.ravel()
except FileNotFoundError:
    print("❌ features.csv 또는 labels.csv 파일이 없습니다.")
    exit()

# 데이터 분할 (학습용 80%, 테스트용 20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 모델 학습
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 평가
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"✅ 모델 정확도: {accuracy * 100:.2f}%\n")
print("📊 분류 리포트:")
print(classification_report(y_test, y_pred))

# 모델 저장
joblib.dump(model, "idle_model.pkl")
print("✅ 모델 저장 완료: idle_model.pkl")
