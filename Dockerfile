FROM python:3.11-slim

# 作業ディレクトリ
WORKDIR /usr/src/app

# 依存関係を先にコピー
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリコードをコピー
COPY project/app/ ./app
COPY project/data/ ./data

# 実行コマンド
CMD ["sleep", "infinity"]
