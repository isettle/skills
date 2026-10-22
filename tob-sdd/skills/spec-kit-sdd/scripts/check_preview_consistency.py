#!/usr/bin/env python3
"""Spec Kit Preview 一致性检查（项目A 2026-09 多轮验证过的断言打包）。

用法: python3 check_preview_consistency.py <specs_root> <preview_dir>
  specs_root  = specs/ 目录（含总纲+各模块 spec.md，校验集必须覆盖全部模块文件）
  preview_dir = 线框目录（*.html + PREVIEW.md）

检查项:
  1) 每页 HTML 标签闭合（html.parser，void 清单）
  2) 死链扫描 + 全站 topnav 链接集合一致性（历史上 workbench 漏 todo 就是靠它抓的）
  3) 原型页引用的 FR-xxx 是否全部在 spec 中有定义（含跨模块）
  4) spec 全库: FR 重复定义 / NEEDS CLARIFICATION 计数 / 实现层泄漏词
     （注: 用户指定的域词如 API 路径标识 tpl_api 属合法，不进泄漏表）
  5) spec 每个模块 >200 字的非表格长行（可读性红线）

断言纪律: 存在性用 >=，只有"旧措辞清零"类否定断言用严格 0；本脚本只报事实，
命中后先 grep 原文确认是真冲突还是断言词不匹配，再决定改 spec/原型还是改断言。
"""
import os
import re
import sys
import html.parser

LEAKS = ["arrayJson", "varchar", "DDL", "外键", "关联表", "upsert", "md5"]
VOID = {"meta", "link", "br", "img", "input", "hr"}
FR_DEF = re.compile(r"- \*\*(FR-\d{3}\w*)\*\*")
FR_REF = re.compile(r"FR-\d{3}[a-z]?")


class TagCheck(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errs = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.errs.append(tag)


def main(specs_root, preview_dir):
    fails = 0
    spec_paths = []
    for root, dirs, fs in os.walk(specs_root):
        dirs[:] = [d for d in dirs if d != ".git"]
        for f in fs:
            if f == "spec.md":
                spec_paths.append(os.path.join(root, f))
    if not spec_paths:
        print(f"ERROR: {specs_root} 下未找到任何 spec.md")
        return 2

    spec_texts = {p: open(p, encoding="utf-8").read() for p in spec_paths}
    allt = "\n".join(spec_texts.values())

    # 4) spec 全库
    defs = FR_DEF.findall(allt)
    dups = {x for x in set(defs) if defs.count(x) > 1}
    nc = allt.count("NEEDS CLARIFICATION")
    def _leak_check(w):
        bad = [l for l in allt.splitlines() if w in l]
        keep = [l for l in bad if ("拍板" in l or "取代" in l or "指纹" in l
                or "排重" in l or re.search(r"B\d+", l))]
        return len(bad) - len(keep)
    leaks = {w for w in LEAKS if _leak_check(w) > 0}
    long_rows = [(p, i, len(l)) for p, x in spec_texts.items() for i, l in
                 enumerate(x.splitlines(), 1) if len(l) > 200 and not l.strip().startswith("|")]
    print(f"[spec] 定义 FR={len(set(defs))} 重复={dups or '无'} NC={nc} 泄漏={leaks or '无'} 长行={long_rows or '无'}")
    fails += bool(dups) + bool(leaks) + bool(long_rows)

    pages = sorted(f for f in os.listdir(preview_dir) if f.endswith(".html"))
    nav_sets = {}
    # 1) 标签闭合 + 3) FR 引用 + 2) 死链
    for fn in pages:
        t = open(os.path.join(preview_dir, fn), encoding="utf-8").read()
        p = TagCheck()
        p.feed(t)
        if p.errs or p.stack:
            print(f"[html] ✗ {fn}: mismatch={p.errs[:3]} unclosed={p.stack[-3:]}")
            fails += 1
        for h in set(re.findall(r'href="([\w.-]+\.html)"', t)):
            if h not in set(pages):
                print(f"[link] ✗ {fn}: 死链 {h}")
                fails += 1
        undef = sorted({x for x in FR_REF.findall(t) if x not in set(defs)} - {"FR-"})
        if undef:
            print(f"[fr]   ✗ {fn}: 引用未定义 FR {undef}")
            fails += 1
        i = t.find('<div class="topnav">')
        if i >= 0:
            seg = t[i:t.index('</div>', i)]
            nav_sets[fn] = frozenset(re.findall(r'href="([\w.-]+\.html)"', seg))
    print(f"[html] {len(pages)} 页闭合/引用/死链检查完成")

    # 2) 导航集合一致性
    if nav_sets:
        allp = {f for f in pages}
        vers = set(nav_sets.values())
        if len(vers) > 1:
            print(f"[nav]  ⚠ topnav 存在 {len(vers)} 个版本（可能新增页未全站插入口）")
            for fn, s in sorted(nav_sets.items()):
                miss = allp - s - {fn}
                if miss:
                    print(f"       {fn} 缺: {sorted(miss)}")
            fails += 1
        else:
            print(f"[nav]  ✓ 全站一致，每页 {len(next(iter(vers)))} 链接 / 共 {len(pages)} 页")

    print("RESULT:", "PASS ✅" if fails == 0 else f"{fails} 项待人工确认（先 grep 原文再定夺）")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
