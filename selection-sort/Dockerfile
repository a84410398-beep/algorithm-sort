# Python 공식 슬림 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 코드 복사
COPY . .

# Cloud Run 기본 포트 지정 (8080)
ENV PORT=8080
EXPOSE 8080

# Gunicorn 서버를 이용해 앱 실행
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
