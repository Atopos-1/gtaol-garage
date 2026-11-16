"""抓取 antwen.cn GTA数据库 全部载具列表（57 页），合并为一个 JSON。"""
import urllib.request, json, re, time, sys, os

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

BASE = "https://www.antwen.cn/vehicles"

def fetch(url, tries=4):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            last = e
            time.sleep(2 + i * 2)
    raise last

def extract_next(html):
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        return None
    return json.loads(m.group(1))

def main():
    all_rows = []
    meta = {}
    page = 1
    total_pages = 1
    while page <= total_pages:
        url = BASE if page == 1 else f"{BASE}?page={page}"
        html = fetch(url)
        data = extract_next(html)
        if data is None:
            print(f"page {page}: NO NEXT_DATA", file=sys.stderr)
            break
        pp = data["props"]["pageProps"]
        total_pages = pp.get("totalPages") or total_pages
        vs = pp.get("vehicles") or []
        all_rows.extend(vs)
        if page == 1:
            meta = {k: pp.get(k) for k in
                    ["manufacturers", "classes", "dlcs", "drivetrains", "dealers",
                     "seats", "gears", "storage", "delivery", "modShops",
                     "raceAvailability", "armor", "totalCount"]}
        print(f"page {page}/{total_pages}: +{len(vs)} (total {len(all_rows)})")
        page += 1
        time.sleep(0.4)

    # 去重（按 id）
    seen = set()
    uniq = []
    for r in all_rows:
        rid = r.get("id")
        if rid in seen:
            continue
        seen.add(rid)
        uniq.append(r)

    out = {"meta": meta, "count": len(uniq), "vehicles": uniq}
    with open("vehicles_full.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"DONE: {len(uniq)} unique vehicles -> vehicles_full.json")

if __name__ == "__main__":
    main()
