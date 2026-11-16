"""把抓到的载具详情整合成应用用的精简数据（JS 内嵌）。"""
import json, re, sys

CLS_MAP = {
    "SUV": "suv",
    "公共事业用车": "special",
    "军用车": "military",
    "厢型车": "van",
    "商用车": "van",
    "小型汽车": "compact",
    "工业用车": "special",
    "开轮式": "super",
    "摩托车": "moto",
    "改装车": "sports",
    "服务用车": "special",
    "直升机": "heli",
    "紧急用车": "service",
    "经典跑车": "classic",
    "肌肉车": "muscle",
    "自行车": "bike",
    "船": "boat",
    "超级跑车": "super",
    "越野车": "offroad",
    "跑车": "sports",
    "轿跑车": "coupe",
    "轿车": "sedan",
    "遥控车": "special",
    "飞机": "plane",
}

def clean(s):
    if s is None:
        return ""
    s = str(s).replace("\u00a0", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s

def num(v):
    try:
        if v in (None, "", 0, "0", "0.00"):
            return None
        f = float(v)
        return round(f, 2)
    except Exception:
        return None

def main():
    rows = json.load(open("vehicles_detail.json", encoding="utf-8"))
    print(f"input {len(rows)} records", file=sys.stderr)

    out = []
    skipped = []
    for r in rows:
        en = clean(r.get("name_en"))
        sc = clean(r.get("name_sc"))
        model = clean(r.get("model_name"))
        if not en and not sc:
            skipped.append(r.get("id"))
            continue
        cls_cn = clean(r.get("class_name"))
        cat = CLS_MAP.get(cls_cn, "special")

        item = {
            "m": model,                       # 模型名（唯一键）
            "n": sc or en,                    # 简中名（主显示）
            "e": en,                          # 英文名
            "t": clean(r.get("name_tc")),     # 繁中名
            "b": clean(r.get("manufacturer_name")),   # 厂商
            "c": cat,                          # 应用分类
            "k": cls_cn,                       # 官方类别原文
        }
        # 价格
        p = num(r.get("price"))
        tp = num(r.get("trade_price"))
        if p: item["p"] = int(p)
        if tp: item["tp"] = int(tp)
        # 性能
        sp = num(r.get("stat_speed"))
        ac = num(r.get("stat_acceleration"))
        br = num(r.get("stat_braking"))
        ha = num(r.get("stat_handling"))
        if sp is not None: item["sp"] = sp
        if ac is not None: item["ac"] = ac
        if br is not None: item["br"] = br
        if ha is not None: item["ha"] = ha
        # 极速
        tst = num(r.get("top_speed_tested"))
        tsg = num(r.get("top_speed_game"))
        if tst: item["tst"] = tst
        if tsg: item["tsg"] = tsg
        # 座位 / 驱动 / 车重
        if r.get("seats"): item["s"] = r["seats"]
        dt = clean(r.get("drivetrain_name"))
        if dt: item["d"] = dt
        if r.get("weight"): item["w"] = r["weight"]
        # DLC
        dl = clean(r.get("dlc_name"))
        if dl: item["dl"] = dl
        # 获取方式
        wb = clean(r.get("where_to_buy_name"))
        if wb: item["wb"] = wb
        # 武装/改装标记
        if r.get("has_imani_upgrade"): item["im"] = 1
        if r.get("has_drift_tune"): item["dr"] = 1
        if r.get("has_hao_upgrade"): item["hw"] = 1
        if r.get("is_removed"): item["rm"] = 1
        # 介绍
        desc = clean(r.get("desc"))
        if desc: item["x"] = desc
        # 现实原型
        based = clean(r.get("based_on_sc")) or clean(r.get("based_on"))
        if based: item["o"] = based
        # 缩略图路径
        if r.get("image_url"):
            item["img"] = r["image_url"]

        out.append(item)

    out.sort(key=lambda x: (x["c"], x["n"]))
    print(f"output {len(out)} records, skipped {len(skipped)}", file=sys.stderr)

    with open("vehicles_compact.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))

    # 字段覆盖率
    tot = len(out)
    for k in ["p", "sp", "ac", "br", "ha", "tst", "x", "b", "dl", "s", "d", "o"]:
        c = sum(1 for x in out if k in x)
        print(f"  字段 {k}: {c}/{tot} ({100*c//max(tot,1)}%)", file=sys.stderr)

if __name__ == "__main__":
    main()
