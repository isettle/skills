"""项目A-style connectivity probe: reads backend/.env, verifies MySQL + Aliyun OSS,
prints ONLY sanitized facts (never secrets). Copy into <repo>/backend/check_conn.py.
Run: backend/.venv/bin/python backend/check_conn.py
  (deps: uv pip install -p <venv>/bin/python pymysql oss2  — uv venv has no pip module)
Exit 0 = both green. On auth failure, FIRST verify file values match expected length
(creds transcribed via chat get redacted/truncated!), then suspect server-side grants.
"""
import os, socket, sys

def load_env(path):
    d = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                d[k.strip()] = v.strip()
    return d

env = load_env(os.path.join(os.path.dirname(__file__), ".env"))
ok = True

# sanity: empty secret keys = user hasn't filled .env yet — don't probe, don't guess-fill
missing = [k for k in ("DB_PASSWORD", "OSS_ACCESS_SECRET") if not env.get(k, "")]
if missing:
    print("缺值：" + ", ".join(missing) + " —— 交用户手填 backend/.env（勿凭聊天内容转录，会被脱敏截断）")
    sys.exit(2)

# --- MySQL ---
try:
    import pymysql
    host, port = env["DB_HOST"], int(env.get("DB_PORT", 3306))
    socket.create_connection((host, port), timeout=8).close()
    print(f"[mysql] TCP {host}:{port} 可达")
    conn = pymysql.connect(host=host, port=port, user=env["DB_USER"],
                           password=env["DB_PASSWORD"], database=env["DB_NAME"],
                           charset="utf8mb4", connect_timeout=8)
    with conn.cursor() as cur:
        cur.execute("SELECT VERSION(), DATABASE(), CURRENT_USER()")
        ver, db, user = cur.fetchone()
        cur.execute("SHOW TABLES"); n_tables = len(cur.fetchall())
    conn.close()
    # 打印的 ver 是真实版本：回写两份 plan 的 Storage 行（拍板名常与实际不符，如 8.0 vs 5.7.35）
    print(f"[mysql] 登录成功 server={ver} 当前库={db} 账号={user} 现有表数={n_tables}")
except Exception as e:
    ok = False
    print(f"[mysql] 失败: {type(e).__name__}: {str(e)[:180]}")

# --- OSS ---
bkt = None
try:
    import oss2
    auth = oss2.Auth(env["OSS_ACCESS_ID"], env["OSS_ACCESS_SECRET"])
    bkt = oss2.Bucket(auth, "https://" + env["OSS_ENDPOINT"], env["OSS_BUCKET"])
    it = bkt.list_objects_v2(max_keys=1)
    meta = bkt.get_bucket_info()
    print(f"[oss] 认证成功 bucket={env['OSS_BUCKET']} 区域={meta.location} 对象样本={len(it.object_list)}")
except Exception as e:
    # SignatureDoesNotMatch → 先怀疑 secret 串在聊天转录中被截断，后怀疑真错值；
    # 仅 list 403 AccessDenied → 探针写读删分化"缺权限"与"签名错"
    try:
        key = "vts-probe/conn-test.txt"
        bkt.put_object(key, b"ok"); bkt.get_object(key).read(); bkt.delete_object(key)
        print(f"[oss] list 受限({type(e).__name__})，写/读/删探针成功 → 基础读写可用")
    except Exception as e2:
        ok = False
        print(f"[oss] 失败: {type(e).__name__}: {str(e)[:150]} | 探针: {type(e2).__name__}: {str(e2)[:120]}")

sys.exit(0 if ok else 1)
