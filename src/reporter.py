def print_reports(results):
    for result in results:
        print(f"[{result['severity']}] {result['message']}")
