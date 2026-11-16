"""抓取 antwen.cn 每个载具详情页，提取类别/性能/介绍等字段，增量落盘。"""
import urllib.request, json, re, os, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
BASE = "https://www.antwen.cn/vehicles/{}"
CACHE_DIR = "detail_cache"
OUT = "vehicles_detail.json"

KEEP = [
    "id", "model_name", "name_sc", "name_tc", "name_en",
    "manufacturer_name", "class_name", "dealer_name", "dlc_name",
    "drivetrain_name", "storage_name", "armor_name",
    "modification_shop_name", "delivery_method_name",
    "race_availability_name", "sell_method_name",
    "where_to_buy_name", "where_to_upgrade_name",
    "price", "trade_price", "sell_price", "sell_price_modded",
    "release_date", "seats", "gears", "weight",
    "stat_speed", "stat_acceleration", "stat_braking", "stat_handling",
    "top_speed_tested", "top_speed_game", "top_speed_hsw", "lap_time",
    "hash", "hex_hash", "based_on", "based_on_sc",
    "has_drift_tune", "has_hao_upgrade", "has_imani_upgrade",
    "has_missile_protection", "is_removed", "is_blacklisted",
    "has_editable_interior", "how_to_trade",
    "image_url", "thumb_url", "gta_wiki_url",
]

def fetch_one(row):
    vid = row["id"]
    cache = os.path.join(CACHE_DIR, f"{vid}.json")
    if os.path.exists(cache):
        try:
            return json.load(open(cache, encoding="utf-8"))
        except Exception:
            pass
    last = None
    for i in range(4):
        try:
            req = urllib.request.Request(BASE.format(vid),
                                         headers={"User-Agent": UA, "Accept": "text/html"})
            with urllib.request.urlopen(req, timeout=40) as r:
                html = r.read().decode("utf-8", "replace")
            m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
            if not m:
                raise ValueError("no NEXT_DATA")
            pp = json.loads(m.group(1))["props"]["pageProps"]
            v = pp.get("vehicle") or {}
            rec = {k: v.get(k) for k in KEEP if k in v}
            # 兜底补列表页已有字段
            for k in ("name_sc", "name_en", "price", "manufacturer_name", "dlc_name", "model_name"):
                if not rec.get(k):
                    rec[k] = row.get(k)
            descs = pp.get("descriptions") or []
            txt = ""
            for d in descs:
                t = (d.get("description") or "").strip()
                if t:
                    txt = t
                    break
            txt = re.sub(r"<br\s*/?>", "\n", txt)
            txt = re.sub(r"<[^>]+>", "", txt).strip()
            rec["desc"] = txt
            rec["desc_source"] = (descs[0].get("source_name") if descs else None)
            json.dump(rec, open(cache, "w", encoding="utf-8"), ensure_ascii=False)
            return rec
        except Exception as e:
            last = e
            time.sleep(1.5 + i * 1.5)
    return {"id": vid, "model_name": row.get("model_name"),
            "name_sc": row.get("name_sc"), "name_en": row.get("name_en"),
            "_error": str(last)[:120]}

def main():
    os.makedirs(CACHE_DIR, exist_ok=True)
    data = json.load(open("vehicles_full.json", encoding="utf-8"))
    rows = data["vehicles"]
    print(f"fetching {len(rows)} detail pages ...", flush=True)

    results = []
    done = 0
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(fetch_one, r): r for r in rows}
        for f in as_completed(futs):
            results.append(f.result())
            done += 1
            if done % 50 == 0:
                print(f"  {done}/{len(rows)}", flush=True)
                json.dump(results, open(OUT, "w", encoding="utf-8"),
                          ensure_ascii=False, indent=1)

    results.sort(key=lambda x: x.get("id") or 0)
    json.dump(results, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    errs = [r for r in results if r.get("_error")]
    print(f"DONE {len(results)} records, {len(errs)} errors -> {OUT}")
    if errs:
        print("failed ids:", [r["id"] for r in errs][:20])

if __name__ == "__main__":
    main()
