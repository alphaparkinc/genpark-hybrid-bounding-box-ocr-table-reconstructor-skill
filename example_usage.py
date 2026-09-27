import sys, json
from client import BoundingBoxTableReconstructor

def main():
    print("Testing BoundingBoxTableReconstructor...")
    rec = BoundingBoxTableReconstructor()
    res = rec.run_benchmark_table_reconstruction()
    print(json.dumps(res, indent=2))
    assert res["benchmark_status"] == "PASSED"
    assert res["num_rows"] == 3
    assert res["num_cols"] == 3
    assert "| Q1 2026 |" in res["markdown_table"]
    print("All Bounding Box Table Reconstructor tests passed successfully!")

if __name__ == "__main__":
    main()
