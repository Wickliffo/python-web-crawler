import json

def write_json_report(page_data, filename="report.json"):
    # Filter out any None values (placeholders from failed requests)
    valid_pages = [p for p in page_data.values() if p is not None]
    
    # Sort the list by the "url" key for a consistent report
    pages = sorted(valid_pages, key=lambda p: p["url"])
    
    # Write to the file with 2-space indentation for readability
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(pages, f, indent=2)
    
    print(f"Report successfully written to {filename}")
