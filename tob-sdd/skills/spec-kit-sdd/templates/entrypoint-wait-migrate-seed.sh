#!/bin/sh
# 容器入口铁三角：等外部库 → 迁移 → seed → 起服务（幂等可重跑）
# 凭据由 podman run --env-file 注入（镜像内零凭据）
set -e

cd /app/backend

# 外部托管 DB 可能间歇性超时：启动时等待端口可达（24×5s ≈ 2 分钟）
echo "[entrypoint] waiting for mysql ${DB_HOST}:${DB_PORT:-3306} ..."
i=0
until python - <<'PY'
import os, socket
host = os.environ.get("DB_HOST", "")
port = int(os.environ.get("DB_PORT", "3306"))
s = socket.create_connection((host, port), timeout=5)
s.close()
PY
do
  i=$((i + 1))
  if [ "$i" -ge 24 ]; then
    echo "[entrypoint] mysql 仍不可达（24 次尝试），放弃启动" >&2
    exit 1
  fi
  echo "[entrypoint] mysql 未就绪，5 秒后重试（$i/24）..."
  sleep 5
done

echo "[entrypoint] alembic upgrade head ..."
python -m alembic upgrade head

echo "[entrypoint] seed builtin data ..."
python -m app.seed.builtin_tpl_api   # 改成项目的 seed 模块；seed 必须幂等（按唯一键 upsert）

echo "[entrypoint] starting uvicorn on :8000 ..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
