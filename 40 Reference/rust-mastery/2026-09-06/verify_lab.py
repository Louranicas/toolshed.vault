"""Capture bounded validation; no timing claim is made by this script."""
import hashlib
import json
from datetime import date
from pathlib import Path
import shutil
import subprocess

root = Path(__file__).resolve().parent
lab = root / "lab"
evidence = root / "evidence"
evidence.mkdir(exist_ok=True)
receipt = {"date": date.today().isoformat(), "scope": "Educational fixture; not a production performance result", "checks": [], "profiles": []}

def run(argv, cwd=lab, name=None):
    result = subprocess.run(argv, cwd=cwd, text=True, capture_output=True)
    if name:
        (evidence / f"{name}.log").write_text(result.stdout + result.stderr)
    receipt["checks"].append({"command": argv, "exit_code": result.returncode, "log": f"{name}.log" if name else None})
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result

receipt["rustc"] = run(["rustc", "-Vv"]).stdout.strip()
receipt["cargo"] = run(["cargo", "-V"]).stdout.strip()
receipt["tools_on_current_path"] = {x: shutil.which(x) for x in ["perf", "valgrind", "hyperfine", "samply", "heaptrack"]}
run(["cargo", "test", "--release", "--locked", "--offline"], name="semantic-tests")
run(["cargo", "bench", "--bench", "allocations", "--locked", "--offline", "--", "--test"], name="criterion-smoke")
run(["cargo", "build", "--profile", "profiling", "--features", "dhat-heap", "--locked", "--offline"], name="profile-build")
binary = lab / "target/profiling/rust-mastery-lab"
receipt["profile_binary_sha256"] = hashlib.sha256(binary.read_bytes()).hexdigest()
for fixture, content in {
    "repeated": "same value\n" * 10_000,
    "unique": "".join(f"value-{i:08}\n" for i in range(10_000)),
}.items():
    data_path = evidence / f"{fixture}.txt"
    data_path.write_text(content)
    for mode in ["owned", "reused"]:
        name = f"{fixture}-{mode}"
        result = run([str(binary), mode, str(data_path)], cwd=evidence, name=name)
        profile = evidence / "dhat-heap.json"
        profile.rename(evidence / f"{name}.dhat.json")
        receipt["profiles"].append({
            "fixture": fixture, "mode": mode, "input_bytes": len(content.encode()),
            "input_sha256": hashlib.sha256(content.encode()).hexdigest(),
            "output": result.stdout.strip(), "dhat_summary": result.stderr.strip(),
            "profile": f"{name}.dhat.json",
        })
receipt["lab_sources"] = {
    str(p.relative_to(lab)): hashlib.sha256(p.read_bytes()).hexdigest()
    for p in sorted(lab.rglob("*"))
    if p.is_file() and "target" not in p.relative_to(lab).parts
}
(evidence / "verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps({"checks": len(receipt["checks"]), "profiles": receipt["profiles"]}, indent=2))
