# 백엔드용 Dockerfile
FROM python:3.9-slim

WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 포트 노출
EXPOSE 8080

# 테스트 데이터 생성 및 서버 시작
CMD ["sh", "-c", "python create_test_data.py && python main.py"]
