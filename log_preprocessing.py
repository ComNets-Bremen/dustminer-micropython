import json
import csv

def parse_line(line):
    
    ## Parse a single line of the log file.
    ## log format: JSON or a custom format
    try:
        event = json.loads(line.strip())
        return {
            "NodeId": event["eventId"],
            "EventType": event["data"].get("status", ""),
            "Timestamp": event["timestamp"],
            "Attributes": event["data"]
        }
    except json.JSONDecodeError:
        print(f"Error parsing line: {line}")
        return None

def parse_logs(raw_log_file):
    ## Parse the entire log file into a structured format.
    parsed_logs = []
    with open(raw_log_file, 'r') as file:
        for line in file:
            event = parse_line(line)
            if event:
                parsed_logs.append(event)
    return parsed_logs

def label_logs(parsed_logs, predicate):
    ## Label logs as 'good' or 'bad' based on a predicate function.
    labeled_data = []
    for log in parsed_logs:
        label = predicate(log)
        labeled_data.append({"Log": log, "Label": label})
    return labeled_data

def convert_to_csv(labeled_data, output_file):
    ## Convert labeled logs into a CSV file for analysis.
    with open(output_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["NodeId", "EventType", "Timestamp", "Attributes", "Label"])
        writer.writeheader()
        for item in labeled_data:
            row = item["Log"]
            row["Label"] = item["Label"]
            writer.writerow(row)

def convert_to_json(labeled_data, output_file):
    ## Convert labeled logs into a JSON file for analysis.
    with open(output_file, 'w') as file:
        json.dump(labeled_data, file, indent=4)

def example_predicate(log):
    if log["EventType"] == "Error":
        return "bad"
    return "good"

if __name__ == "__main__":
    # File paths
    raw_log_file = "raw_logs.txt"  
    csv_output_file = "labeled_logs.csv"
    json_output_file = "labeled_logs.json"

    # Step 1: Parse logs
    parsed_logs = parse_logs(raw_log_file)
    print(f"Parsed Logs: {parsed_logs}")

    # Step 2: Label logs using the example predicate
    labeled_logs = label_logs(parsed_logs, example_predicate)
    print(f"Labeled Logs: {labeled_logs}")

    # Step 3: Convert to CSV
    convert_to_csv(labeled_logs, csv_output_file)
    print(f"Logs saved to {csv_output_file}")

    # Step 4: Convert to JSON
    convert_to_json(labeled_logs, json_output_file)
    print(f"Logs saved to {json_output_file}")
