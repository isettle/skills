#!/usr/bin/env python3
"""入库脱敏自查：扫描本仓库全部文本文件，命中敏感词/模式即退出码 1。

用法：python3 scripts/sanitize_scan.py [扫描根目录，默认仓库根]
收录 PR 前必跑，零命中才 commit（红线见根 README）。
"""
import os
import re
import sys

# 业务/公司/个人专有词：出现即违规（大小写敏感的精确子串）
TOKENS = [
    "一猫", "emao",
    "VTS", "VRS",                       # 真实内部项目代号
    "vehicle", "Vehicle",               # 真实业务域英文词
    "车辆", "租赁", "贸易", "外贸", "报关", "清关", "退税", "许可证",
    "车辆贸易", "车辆租赁",
    "iopgps", "azlmap", "azl",          # 第三方平台名
    "VIN",
    "微信", "钉钉", "dingtalk", "DingTalk",
    "ADHD", "adhd",
    "Qoder CN",
    "/Users/stone", "~/WorkSpace", "WorkSpace/Code", "WorkSpace/Doc",
    "iShot",
    "macOS 13", "mac13",
    "8.140.194.207", "101.201.51.212", "39.106.51.71",
]

# 正则模式：同样命中即违规
PATTERNS = [
    (r"(?<![\d.])\b(?:\d{1,3}\.){3}\d{1,3}\b(?![\d.])", "疑似 IP（白名单除外）"),
    (r"password\s*=\s*['\"][^'\"]{6,}", "疑似真实密码赋值"),
    (r"secret\s*=\s*['\"][A-Za-z0-9+/]{16,}", "疑似真实 secret"),
    (r"(?i)\b(sk-[A-Za-z0-9]{20,})", "疑似 API key"),
]

# 允许 IP 形态的白名单（占位/本地/文档示例）
IP_WHITELIST = {"0.0.0.0", "127.0.0.1", "192.0.2.1", "10.0.0.1", "127.0.0.53"}

# 跳过路径片段
SKIP_DIR_PARTS = {".git", "node_modules", "__pycache__", ".venv"}

SELF = os.path.abspath(__file__)


def scan_file(path):
    hits = []
    try:
        text = open(path, encoding="utf-8").read()
    except (UnicodeDecodeError, OSError):
        return hits  # 二进制跳过
    # 本脚本自身含敏感词清单，跳过
    if os.path.abspath(path) == SELF:
        return hits
    lines = text.splitlines()
    for tok in TOKENS:
        if tok in text:
            for j, ln in enumerate(lines, 1):
                if tok in ln:
                    hits.append((path, j, "TOKEN", tok, ln.strip()[:120]))
    for pat, desc in PATTERNS:
        for j, ln in enumerate(lines, 1):
            for m in re.finditer(pat, ln):
                if m.group(0) in IP_WHITELIST:
                    continue
                hits.append((path, j, "PATTERN", desc, ln.strip()[:120]))
    return hits


def main():
    root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1
                           else os.path.join(os.path.dirname(SELF), ".."))
    bad = []
    nfiles = 0
    for cur, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIR_PARTS]
        for fn in files:
            p = os.path.join(cur, fn)
            nfiles += 1
            bad.extend(scan_file(p))
    if bad:
        print(f"FAIL: {len(bad)} hits across {nfiles} files")
        for path, line, kind, what, ctx in bad:
            rel = os.path.relpath(path, root)
            print(f"  {rel}:{line} [{kind}] {what} :: {ctx}")
        sys.exit(1)
    print(f"OK: 0 hits across {nfiles} files")


if __name__ == "__main__":
    main()
