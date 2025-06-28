# 프론트엔드용 Dockerfile
FROM node:18-alpine

WORKDIR /app

# 의존성 설치
COPY package*.json ./
RUN npm ci --only=production

# 애플리케이션 코드 복사
COPY . .

# 빌드
RUN npm run build

# 포트 노출
EXPOSE 3000

# 개발 서버 시작 (또는 프로덕션 빌드 서빙)
CMD ["npm", "run", "dev", "--", "--port", "3000", "--host", "0.0.0.0"]
