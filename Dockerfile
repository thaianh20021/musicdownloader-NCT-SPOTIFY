# Sử dụng Python 3.10 slim để nhẹ
FROM python:3.10-slim

# Cài đặt git và ffmpeg (quan trọng)
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy requirements và cài đặt
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào
COPY . .

# Tạo thư mục downloads
RUN mkdir -p MusicOutput

# Mở port 5000
EXPOSE 5000

# Lệnh chạy server
# Sử dụng gevent thay vì eventlet nếu eventlet vẫn lỗi, nhưng ta thử fix eventlet trước
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "-b", "0.0.0.0:5000", "web_app:app"]
