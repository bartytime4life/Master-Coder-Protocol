from polymerlab.io.schema import build_validator, iter_records
from polymerlab.io.loader import glob_files

def test_schema_validate_example():
    schema = "conf/schema/mcp_polymers.schema.yaml"
    paths = glob_files(["data/raw/example_polymer.json"])
    v = build_validator(schema)
    errs = []
    for p, rec in iter_records(paths):
        errs.extend([e for e in v.iter_errors(rec)])
    assert not errs, f"Schema errors: {errs}"
