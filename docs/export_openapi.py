"""
docs/export_openapi.py — Export OpenAPI Specification
Student Assignment Tracker

Generates openapi.json and openapi.yaml from the live FastAPI app.
Run from the repo root:

    python docs/export_openapi.py

Output files:
    docs/api/openapi.json
    docs/api/openapi.yaml
"""

import sys, json
sys.path.insert(0, '.')

from api.main import app

# ---------------------------------------------------------------------------
# Export JSON
# ---------------------------------------------------------------------------
schema = app.openapi()

json_path = "docs/api/openapi.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(schema, f, indent=2, default=str)
print(f"✅ Exported: {json_path}")

# ---------------------------------------------------------------------------
# Export YAML
# ---------------------------------------------------------------------------
try:
    import yaml  # type: ignore[import]
    yaml_path = "docs/api/openapi.yaml"
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(schema, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    print(f"✅ Exported: {yaml_path}")
except ImportError:
    print("⚠️  PyYAML not installed — skipping YAML export.")
    print("   Run: pip install pyyaml")