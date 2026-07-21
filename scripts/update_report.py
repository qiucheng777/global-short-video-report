from pathlib import Path
import json
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "data" / "latest.json"
data = json.loads(path.read_text(encoding="utf-8"))
turkey = timezone(timedelta(hours=3))
data["updated_at"] = datetime.now(turkey).strftime("%Y-%m-%d %H:%M")
# 这里只更新时间戳，不伪造平台排名。
# 接入合法、稳定的数据源后，可在这里替换 global_top10/china_top10。
path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("Updated:", data["updated_at"])
