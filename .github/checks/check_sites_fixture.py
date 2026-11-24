"""Read-only test fixture validation; never publishes content."""
import json
from pathlib import Path
p=Path(__file__).resolve().parents[2]/".sites-test"/"article.json"
a=json.loads(p.read_text())
assert set(a)=={"title","body","force_failure"}, "Unexpected fields"
assert isinstance(a["title"],str) and 1<=len(a["title"])<=160
assert isinstance(a["body"],str) and 1<=len(a["body"])<=40000
assert isinstance(a["force_failure"],bool)
assert not a["force_failure"], "Intentional Sites test failure"
print("PASS: isolated Sites fixture")
