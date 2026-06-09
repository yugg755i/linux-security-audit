from checks import check_sudo_users
from reporter import print_reports

results = [check_sudo_users()]

print_reports(results)
