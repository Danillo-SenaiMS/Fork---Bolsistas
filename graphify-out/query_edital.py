import json
from pathlib import Path

g = json.loads(Path('graphify-out/graph.json').read_text(encoding='utf-8'))

print("=== Edital Provisorio Nodes ===")
for n in g.get('nodes', []):
    nid = n.get('id', '')
    if 'edital_provisorio' in nid or 'edital_prov' in nid:
        print(f"  {nid}  (label: {n.get('label','')})")

print("\n=== Edges involving edital_provisorio ===")
for e in g.get('edges', []):
    s = e.get('source', '')
    t = e.get('target', '')
    if 'edital_provisorio' in s or 'edital_provisorio' in t:
        print(f"  {s} --{e.get('relationship','')}--> {t}  [{e.get('confidence','')}]")

print("\n=== Edital Provisorio models.py ===")
for n in g.get('nodes', []):
    nid = n.get('id', '')
    if 'edital_provisorio' in nid and 'model' in nid:
        print(f"  {nid}: {n.get('properties', {})}")

print("\n=== URL patterns for edital_provisorio ===")
for n in g.get('nodes', []):
    nid = n.get('id', '')
    if 'edital_provisorio_url' in nid or 'url_edital_provisorio' in nid:
        print(f"  {nid}: {n.get('properties', {})}")
