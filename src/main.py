from checks import check_ssh_root_login
from reporter import print_reports

results = [check_ssh_root_login()]

print_reports(results)
