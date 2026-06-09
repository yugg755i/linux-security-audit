import json


def print_reports(results):
    for result in results:
        print(f"[{result['severity']}] {result['message']}")


def save_reports_txt(results, filename):
    with open(filename, "w") as f:
        for result in results:
            f.write(f"[{result['severity']}] {result['message']}\n")


def save_reports_json(results, filename):
    with open(filename, "w") as f:
        json.dump(results, f, indent=4)
