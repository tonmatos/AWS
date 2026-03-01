import json
import sys
from pathlib import Path

DECK_FILES = [
    "database-advanced.json",
    "ec2.json",
    "ecs.json",
    "edge-networking.json",
    "iam.json",
    "iam-ec2.json",
    "integration.json",
    "lambda.json",
    "rds.json",
    "s3.json",
    "security-ops.json",
    "storage-advanced.json",
    "vpc.json",
    "compute-scale.json",
]

class DuplicateKeyError(ValueError):
    pass

def no_dupe_object_pairs_hook(pairs):
    obj = {}
    seen = set()
    for k, v in pairs:
        if k in seen:
            raise DuplicateKeyError(f"Duplicate key: {k}")
        seen.add(k)
        obj[k] = v
    return obj

def load_json_strict(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f, object_pairs_hook=no_dupe_object_pairs_hook)

def validate_deck(path: Path, deck: dict):
    errors = []

    if "questions" not in deck or not isinstance(deck["questions"], list):
        errors.append("Missing or invalid 'questions' array.")
        return errors

    for idx, q in enumerate(deck["questions"]):
        qid = q.get("id", f"{path.name}#idx={idx}")

        for field in ["id", "domain", "difficulty", "type", "select", "prompt", "options", "answer"]:
            if field not in q:
                errors.append(f"{qid}: missing '{field}'")

        qtype = q.get("type")
        select = q.get("select", {})
        min_sel = select.get("min")
        max_sel = select.get("max")

        if qtype not in ("single", "multi"):
            errors.append(f"{qid}: invalid type '{qtype}' (expected single|multi)")

        if not isinstance(min_sel, int) or not isinstance(max_sel, int) or min_sel < 1 or max_sel < min_sel:
            errors.append(f"{qid}: invalid select range min={min_sel} max={max_sel}")

        options = q.get("options", [])
        if not isinstance(options, list) or not options:
            errors.append(f"{qid}: options must be a non-empty list")
            continue

        opt_keys = []
        for o in options:
            if not isinstance(o, dict):
                errors.append(f"{qid}: option must be an object")
                continue
            k = o.get("key")
            t = o.get("text")
            if not isinstance(k, str) or not k.strip():
                errors.append(f"{qid}: option missing/invalid key")
            if not isinstance(t, str) or not t.strip():
                errors.append(f"{qid}: option missing/invalid text")
            opt_keys.append(k)

        if len(opt_keys) != len(set(opt_keys)):
            errors.append(f"{qid}: duplicate option keys: {opt_keys}")

        ans = q.get("answer", {}).get("keys", [])
        if not isinstance(ans, list) or not ans:
            errors.append(f"{qid}: answer.keys must be a non-empty list")
            continue

        opt_key_set = set(opt_keys)
        bad = [k for k in ans if k not in opt_key_set]
        if bad:
            errors.append(f"{qid}: answer keys not in options: {bad}")

        if qtype == "single" and len(ans) != 1:
            errors.append(f"{qid}: single-select must have exactly 1 answer key (found {len(ans)})")

        if isinstance(min_sel, int) and isinstance(max_sel, int):
            if len(ans) < min_sel or len(ans) > max_sel:
                errors.append(f"{qid}: answer count {len(ans)} not within select {min_sel}-{max_sel}")

    return errors

def main():
    root = Path(".")
    failures = 0

    for name in DECK_FILES:
        path = root / name
        if not path.exists():
            continue

        try:
            deck = load_json_strict(path)
        except DuplicateKeyError as e:
            failures += 1
            print(f"[FAIL] {name}: {e}")
            continue
        except json.JSONDecodeError as e:
            failures += 1
            print(f"[FAIL] {name}: JSON parse error: {e}")
            continue

        errs = validate_deck(path, deck)
        if errs:
            failures += 1
            print(f"[FAIL] {name}:")
            for err in errs:
                print(f"  - {err}")
        else:
            print(f"[OK]   {name}")

    if failures:
        print(f"\n{failures} file(s) failed.")
        sys.exit(1)

    print("\nAll checked files passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
