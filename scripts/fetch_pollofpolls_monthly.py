#!/usr/bin/env python3
import argparse, datetime as dt, re, sqlite3, requests

URL_TMPL = "https://www.pollofpolls.no/?cmd=Stortinget&do=snitt&yw={yearmonth}"
HEADERS = {"User-Agent": "Mozilla/5.0"}

RGX = re.compile(
    r"Gjennomsnitt"
    r".*?([\d,]+)\s*\(\d+\)"  # Ap
    r".*?([\d,]+)\s*\(\d+\)"  # H
    r".*?([\d,]+)\s*\(\d+\)"  # Frp
    r".*?([\d,]+)\s*\(\d+\)"  # SV
    r".*?([\d,]+)\s*\(\d+\)"  # Sp
    r".*?([\d,]+)\s*\(\d+\)"  # KrF
    r".*?([\d,]+)\s*\(\d+\)"  # V
    r".*?([\d,]+)\s*\(\d+\)"  # MDG
    r".*?([\d,]+)\s*\(\d+\)"  # R
    r".*?([\d,]+)\s*\(\d+\)", # Andre
    flags=re.S
)

def fetch_month(yearmonth: str):
    url = URL_TMPL.format(yearmonth=yearmonth)
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    html = re.sub(r"\s+", " ", r.text)
    m = RGX.search(html)
    if not m:
        raise RuntimeError(f"Could not parse pollofpolls for {yearmonth}")
    nums = [float(x.replace(",", ".")) for x in m.groups()]
    return dict(ap=nums[0], h=nums[1], frp=nums[2], sv=nums[3], sp=nums[4],
                krf=nums[5], v=nums[6], mdg=nums[7], r=nums[8], andre=nums[9])

def upsert(conn, d, yearmonth: str):
    y, m = int(yearmonth[:4]), int(yearmonth[4:])
    last_day = (dt.date(y + (m == 12), 1 if m == 12 else m+1, 1) - dt.timedelta(days=1)).isoformat()
    conn.execute("""
        INSERT OR REPLACE INTO polls
        (date,pollster,ap,h,frp,sv,sp,krf,v,mdg,r)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """, (last_day, "pollofpolls_avg", d["ap"], d["h"], d["frp"], d["sv"], d["sp"],
          d["krf"], d["v"], d["mdg"], d["r"]))
    conn.commit()
    return last_day

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2025, help="Year to fetch (default: 2025)")
    args = parser.parse_args()

    conn = sqlite3.connect("data/processed/polls.sqlite")

    today = dt.date.today()
    for m in range(1, today.month + 1):
        ym = f"{args.year}{m:02d}"
        d = fetch_month(ym)
        when = upsert(conn, d, ym)
        print(f"Inserted pollofpolls monthly avg for {ym} ({when}): {d}")
