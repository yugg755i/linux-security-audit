from checks import check_firewall
from reporter import print_reports

results = [check_firewall()]

print_reports(results)
