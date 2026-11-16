"""下载所有载具缩略图到 assets/img/，文件名用 model_name，保持离线可用。"""
import json, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

OUT_DIR = "assets/img"
DATA = "vehicles_full.json"

def fetch(v):
    url = v.get("thumb_url")
    model = v.get("model_name") or v.get("model") or ""
    if not url or not model:
        return None
    # model 可能含特殊字符，安全化文件名
    safe = "".join(c for c in model if c.isalnum() or c in "-_")
    if not safe:
        safe = str(v.get("id"))
    path = os.path.join(OUT_DIR, safe + ".webp")
    if os.path.exists(path):
        return "exists"
    for i in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                b = r.read()
            if len(b) < 500:
                return None  # 太小，多半是错误页
            with open(path, "wb") as f:
                f.write(b)
            return "ok"
        except Exception as e:
            if i == 2:
                return f"err:{type(e).__name__}"
            time.sleep(1 + i)

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    data = json.load(open(DATA, encoding="utf-8"))
    vs = data["vehicles"]
    print(f"downloading {len(vs)} thumbnails ...", flush=True)

    ok = err = skip = 0
    done = 0
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(fetch, v): v for v in vs}
        for f in as_completed(futs):
            r = f.result()
            done += 1
            if r == "ok": ok += 1
            elif r == "exists": skip += 1
            elif r is None: err += 1
            else: err += 1
            if done % 100 == 0:
                print(f"  {done}/{len(vs)} ok={ok} err={err}", flush=True)
    print(f"DONE ok={ok} exists={skip} err={err}")

if __name__ == "__main__":
    main()
