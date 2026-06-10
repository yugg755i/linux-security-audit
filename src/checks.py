import subprocess
from pathlib import Path


def check_ssh_root_login():
    config = Path("/etc/ssh/sshd_config")
    if config.exists():
        with config.open() as ssh_config:
            for line in ssh_config:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("PermitRootLogin yes"):
                    return {"severity": "HIGH", "message": "Root SSH login enabled"}
                elif line.startswith("PermitRootLogin no"):
                    return {"severity": "INFO", "message": "Root SSH login disabled"}
                elif line.startswith("PermitRootLogin prohibit-password"):
                    return {
                        "severity": "INFO",
                        "message": "Root SSH login prohibit-password",
                    }

        return {"severity": "INFO", "message": "PermitRootLogin setting not found"}
    else:
        return {"severity": "INFO", "message": "SSH config not found"}


def check_pass_auth():
    config = Path("/etc/ssh/sshd_config")
    if config.exists():
        with config.open() as ssh_config:
            for line in ssh_config:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("PasswordAuthentication yes"):
                    return {
                        "severity": "MEDIUM",
                        "message": "Password Authentication Enabled",
                    }
                elif line.startswith("PasswordAuthentication no"):
                    return {
                        "severity": "INFO",
                        "message": "Password Authentication Disabled",
                    }

        return {
            "severity": "INFO",
            "message": "PasswordAuthentication setting not found",
        }
    else:
        return {"severity": "INFO", "message": "ssh config not found"}


def check_firewall():
    for service in ["ufw", "firewalld", "nftables"]:
        result = subprocess.run(
            ["systemctl", "is-active", service], capture_output=True, text=True
        )
        if result.stdout.strip() == "active":
            return {"severity": "INFO", "message": f"Firewall active ({service})"}
    return {"severity": "MEDIUM", "message": "Firewall inactive"}


def check_sudo_users():
    result = subprocess.run(
        ["getent", "group", "wheel"], capture_output=True, text=True
    )

    if result.returncode != 0:
        return {"severity": "INFO", "message": "no wheel group found"}
    group_info = result.stdout.strip()

    if not group_info:
        return {"severity": "INFO", "message": "no wheel group found"}

    user_info = group_info.split(":")[-1]

    if not user_info:
        return {"severity": "INFO", "message": "0 sudo users found"}

    users = user_info.split(",")
    user_count = len(users)

    return {
        "severity": "INFO",
        "message": f"{user_count} sudo users found: {', '.join(users)}",
    }


def check_world_writable_files():
    result = subprocess.run(
        [
            "find",
            "/",
            "-type",
            "f",
            "-perm",
            "-002",
            "-not",
            "-path",
            "/proc/*",
            "-not",
            "-path",
            "/sys/*",
            "-not",
            "-path",
            "/dev/*",
            "-not",
            "-path",
            "/run/*",
        ],
        capture_output=True,
        text=True,
    )
    files = result.stdout.strip().splitlines()
    count = len(files)
    if count == 0:
        severity = "INFO"
    else:
        severity = "MEDIUM"
    return {"severity": severity, "message": f"{count} world-writable files found"}


def check_open_ports():
    result = subprocess.run(["ss", "-tuln"], capture_output=True, text=True)

    ports = set()

    for line in result.stdout.splitlines()[1:]:
        parts = line.split()

        if len(parts) < 5:
            continue

        address = parts[4]
        port = address.split(":")[-1]
        ports.add(port)

    return {
        "severity": "INFO",
        "message": f"{len(ports)} open ports: {','.join(sorted(ports, key=int))}",
    }


def check_executable_files():
    result = subprocess.run(
        [
            "find",
            "/",
            "-type",
            "f",
            "-executable",
            "-not",
            "-path",
            "/proc/*",
            "-not",
            "-path",
            "/sys/*",
            "-not",
            "-path",
            "/dev/*",
            "-not",
            "-path",
            "/run/*",
        ],
        capture_output=True,
        text=True,
    )
    files = result.stdout.splitlines()
    count = len(files)

    return {"severity": "INFO", "message": f"{count} executable files found"}


def check_dir(path):

    result_write = subprocess.run(
        [
            "find",
            path,
            "-type",
            "f",
            "-perm",
            "-002",
            "-not",
            "-path",
            "/proc/*",
            "-not",
            "-path",
            "/sys/*",
            "-not",
            "-path",
            "/dev/*",
            "-not",
            "-path",
            "/run/*",
        ],
        capture_output=True,
        text=True,
    )
    write_files = result_write.stdout.strip().splitlines()
    write_count = len(write_files)

    result_exe = subprocess.run(
        [
            "find",
            path,
            "-type",
            "f",
            "-executable",
            "-not",
            "-path",
            "/proc/*",
            "-not",
            "-path",
            "/sys/*",
            "-not",
            "-path",
            "/dev/*",
            "-not",
            "-path",
            "/run/*",
        ],
        capture_output=True,
        text=True,
    )
    exe_files = result_exe.stdout.splitlines()
    exe_count = len(exe_files)

    return {
        "severity": "INFO",
        "path": path,
        "world_writable_count": write_count,
        "world_writable_files": write_files,
        "executable_count": exe_count,
        "executable_files": exe_files,
    }
