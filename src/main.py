from checks import check_world_writable_files
from reporter import print_reports

results = [check_world_writable_files()]

print_reports(results)
