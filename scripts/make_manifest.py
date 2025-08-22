#!/usr/bin/env python3
import hashlib, pathlib, json, time, subprocess

WMK_ID = "WMK_PARTH_2025"
root = pathlib.Path(__file__).resolve().parents[1]

def git(*args):
    return subprocess.check_output(["git"]+list(args), cwd=root).decode().strip()

commit = git("rev-parse", "HEAD")
tree   = git("rev-parse", "HEAD^{tree}")
ts     = int(time.time())

h = hashlib.sha256()
for p in root.rglob("*"):
    if p.is_file() and ".git" not in str(p):
        h.update(open(p,"rb").read())

manifest = {
    "watermark_id": WMK_ID,
    "commit": commit,
    "tree": tree,
    "sha256_all": h.hexdigest(),
    "timestamp": ts
}

out = root/".watermarks"/f"manifest-{commit}.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(manifest, indent=2))
print(f"Manifest written: {out}")
