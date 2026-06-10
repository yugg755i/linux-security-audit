import json

from checks import check_dir


def print_reports(results):
    for result in results:
        print(f"[{result['severity']}] {result['message']}")


def print_dir_report(path):
    result = check_dir(path)

    print(f"Scanned: {result['path']}")

    print(f"\n[MEDIUM] {result['world_writable_count']} world-writable files found")

    for file in result["world_writable_files"][:10]:
        print(f" - {file}")

    print(f"\n[INFO] {result['executable_count']} executable files found")

    for file in result["executable_files"][:10]:
        print(f" - {file}")


def save_reports_txt(results, filename):
    with open(filename, "w") as f:
        for result in results:
            f.write(f"[{result['severity']}] {result['message']}\n")


def save_reports_json(results, filename):
    with open(filename, "w") as f:
        json.dump(results, f, indent=4)
