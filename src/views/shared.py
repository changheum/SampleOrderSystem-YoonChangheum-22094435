_COL_ID    = 10
_COL_NAME  = 20
_COL_TIME  = 14
_COL_YIELD = 8


def render_sample_table(entries: list[dict]) -> None:
    print(f"{'ID':<{_COL_ID}} {'이름':<{_COL_NAME}} {'생산시간(분)':<{_COL_TIME}} {'수율':<{_COL_YIELD}} {'재고'}")
    print("-" * 60)
    for entry in entries:
        s = entry["sample"]
        print(f"{s.sample_id:<{_COL_ID}} {s.name:<{_COL_NAME}} {s.avg_production_time:<{_COL_TIME}} {s.yield_rate:<{_COL_YIELD}} {entry['stock_quantity']}")
