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
                    return {"severity": "HIGH", "message": "root ssh login enabled"}
                elif line.startswith("PermitRootLogin no"):
                    return {"severity": "INFO", "message": "root ssh login disabled"}
                elif line.startswith("PermitRootLogin prohibit-password"):
                    return {
                        "severity": "INFO",
                        "message": "root ssh login prohibit-password",
                    }

        return {"severity": "INFO", "message": "PermitRootLogin setting not found!"}
    else:
        return {"severity": "INFO", "message": "ssh config not found!"}


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
            "message": "PasswordAuthentication setting not found!",
        }
    else:
        return {"severity": "INFO", "message": "ssh config not found!"}
