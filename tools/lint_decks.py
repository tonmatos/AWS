#!/usr/bin/env python3
import json
import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # tools/ -> project root
QUESTIONS_DIR = ROOT / "questions"
MANIFEST_PATH = QUESTIONS_DIR / "index.json"

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

def validate_deck_file(path: Path, doc: dict):
    errors = []

    if str(doc.get("schemaVersion", "")) != "1.0":
        errors.append(f"{path.name}: schemaVersion must be '1.0'")

    qs = doc.get("questions")
    if not isinstance(qs, list):
        errors.append(f"{path.name}: questions must be an array")
        return errors

    for idx, q in enumerate(qs):
        qid = q.get("id", f"{path.name}#idx={idx}")

        for field in ["id", "domain", "difficulty", "type", "select", "prompt", "options", "answer"]:
            if field not in q:
                errors.append(f"{path.name}:{qid} missing '{field}'")

        qtype = q.get("type")
        if qtype not in ("single", "multi"):
            errors.append(f"{path.name}:{qid} invalid type '{qtype}'")

        sel = q.get("select", {})
        mn = sel.get("min")
        mx = sel.get("max")
        if not isinstance(mn, int) or not isinstance(mx, int) or mn < 1 or mx < mn:
            errors.append(f"{path.name}:{qid} invalid select min={mn} max={mx}")

        opts = q.get("options", [])
        if not isinstance(opts, list) or len(opts) == 0:
            errors.append(f"{path.name}:{qid} options must be a non-empty array")
            continue

        keys = []
        for o in opts:
            if not isinstance(o, dict):
                errors.append(f"{path.name}:{qid} option must be an object")
                continue
            k = o.get("key")
            t = o.get("text")
            if not isinstance(k, str) or not k.strip():
                errors.append(f"{path.name}:{qid} option missing/invalid key")
            if not isinstance(t, str) or not t.strip():
                errors.append(f"{path.name}:{qid} option missing/invalid text")
            keys.append(k)

        if len(keys) != len(set(keys)):
            errors.append(f"{path.name}:{qid} duplicate option keys: {keys}")

        ans = (q.get("answer") or {}).get("keys")
        if not isinstance(ans, list) or len(ans) == 0:
            errors.append(f"{path.name}:{qid} answer.keys must be a non-empty array")
            continue

        bad = [k for k in ans if k not in set(keys)]
        if bad:
            errors.append(f"{path.name}:{qid} answer keys not in options: {bad}")

        if qtype == "single" and len(ans) != 1:
            errors.append(f"{path.name}:{qid} single must have exactly 1 answer key")

        if isinstance(mn, int) and isinstance(mx, int):
            if len(ans) < mn or len(ans) > mx:
                errors.append(f"{path.name}:{qid} answer count {len(ans)} not within select {mn}-{mx}")

    return errors

def main():
    if not MANIFEST_PATH.exists():
        print(f"[FAIL] Missing manifest: {MANIFEST_PATH}")
        sys.exit(1)

    try:
        manifest = load_json_strict(MANIFEST_PATH)
    except Exception as e:
        print(f"[FAIL] Manifest JSON error in {MANIFEST_PATH.name}: {e}")
        sys.exit(1)

    if str(manifest.get("schemaVersion", "")) != "1.0":
        print("[FAIL] questions/index.json schemaVersion must be '1.0'")
        sys.exit(1)

    files = manifest.get("files")
    if not isinstance(files, list) or len(files) == 0:
        print("[FAIL] questions/index.json must have a non-empty files[]")
        sys.exit(1)

    all_ids = set()
    failures = 0

    for fname in files:
        if not isinstance(fname, str) or not fname.strip():
            failures += 1
            print("[FAIL] Invalid entry in files[] (must be a filename string)")
            continue

        path = QUESTIONS_DIR / fname
        if not path.exists():
            failures += 1
            print(f"[FAIL] Missing deck file: questions/{fname}")
            continue

        try:
            doc = load_json_strict(path)
        except DuplicateKeyError as e:
            failures += 1
            print(f"[FAIL] questions/{fname}: {e}")
            continue
        except json.JSONDecodeError as e:
            failures += 1
            print(f"[FAIL] questions/{fname}: JSON parse error: {e}")
            continue

        errs = validate_deck_file(path, doc)
        if errs:
            failures += 1
            print(f"[FAIL] questions/{fname}:")
            for x in errs:
                print(f"  - {x}")
            continue

        # cross-file unique IDs
        for q in doc.get("questions", []):
            qid = q.get("id")
            if qid in all_ids:
                failures += 1
                print(f"[FAIL] Duplicate question id across files: {qid}")
            all_ids.add(qid)

        print(f"[OK]   questions/{fname}")

    if failures:
        print(f"\n{failures} problem(s) found.")
        sys.exit(1)

    print("\nAll decks OK.")
    sys.exit(0)

if __name__ == "__main__":
    main()
