# Linux Security Audit

A Python-based Linux security auditing tool that scans for common misconfigurations and generates security reports.

Built to practice Linux security concepts, Python automation, and basic security assessment techniques.

## Features

* Check SSH root login status
* Check SSH password authentication status
* Check firewall status
* List sudo users
* Detect world-writable files
* Detect executable files
* List open ports
* Audit a custom directory for world-writable and executable files
* Generate terminal reports
* Export reports to TXT and JSON format

## Project Structure

```text
linux-security-audit/
├── src/
│   ├── checks.py       # security checks (SSH, firewall, sudo, ports, files)
│   ├── reporter.py     # report generation and TXT/JSON export
│   └── main.py         # CLI entry point
├── reports/            # generated audit reports
└── README.md
```

## Installation

```bash
git clone https://github.com/yugg755i/linux-security-audit.git
cd linux-security-audit
```

## Requirements

* Python 3.10+
* Linux system
* Standard Python libraries only

## Usage

Run the audit:

```bash
python src/main.py
```

Save report as TXT:

```bash
python src/main.py --save-txt
```

Save report as JSON:

```bash
python src/main.py --save-json
```

Audit a specific directory:

```bash
python src/main.py --path /var/www
```

Save both formats:

```bash
python src/main.py --save-txt --save-json
```

## Example Output

```text
[HIGH] Root SSH login enabled
[MEDIUM] Password authentication enabled
[INFO] Firewall active
[INFO] 1 sudo users found: admin
[MEDIUM] 5 world-writable files found
[INFO] 1042 executable files found
[INFO] 6 open ports: 22,80,443,3306,5432,8080
```

Findings are categorized as HIGH, MEDIUM, or INFO based on severity.

## Stack

- Python 3.10+
- Standard library only (no external dependencies)

## Screenshots

### CLI usage

![CLI help](screenshots/cli_help.png)

### Audit Output

![Audit Output](screenshots/audit_output.png)

