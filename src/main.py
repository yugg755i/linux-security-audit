import argparse
from pathlib import Path

from checks import (
    check_firewall,
    check_pass_auth,
    check_ssh_root_login,
    check_sudo_users,
    check_world_writable_files,
)
from reporter import print_reports, save_reports_json, save_reports_txt


def main():
    Path("reports").mkdir(exist_ok=True)

    parser = argparse.ArgumentParser(description="linux security auditing tool")
    parser.add_argument(
        "--save-txt", action="store_true", help="save report to TXT file"
    )
    parser.add_argument(
        "--save-json", action="store_true", help="save report to JSON file"
    )

    args = parser.parse_args()

    results = [
        check_ssh_root_login(),
        check_pass_auth(),
        check_firewall(),
        check_sudo_users(),
        check_world_writable_files(),
    ]
    if args.save_txt:
        save_reports_txt(results, "reports/report.txt")
    if args.save_json:
        save_reports_json(results, "reports/report.json")

    print_reports(results)


if __name__ == "__main__":
    main()
