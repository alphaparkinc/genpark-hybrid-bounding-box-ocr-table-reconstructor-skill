import sys, json
from client import BoundingBoxTableReconstructor

def main():
    rec = BoundingBoxTableReconstructor()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(rec.run_benchmark_table_reconstruction(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            params = req.get("params", {})
            rid = req.get("id")

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "reconstruct_table_grid", "description": "Group raw bounding boxes into 2D rows and columns."},
                        {"name": "format_to_markdown", "description": "Render 2D grid into Markdown table."},
                        {"name": "run_benchmark_table_reconstruction", "description": "Execute deterministic table reconstruction benchmark."}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "reconstruct_table_grid":
                    out = rec.reconstruct_table_grid(args.get("bounding_boxes", []))
                elif tname == "format_to_markdown":
                    out = {"markdown": rec.format_to_markdown(args.get("grid", []))}
                elif tname == "run_benchmark_table_reconstruction":
                    out = rec.run_benchmark_table_reconstruction()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
