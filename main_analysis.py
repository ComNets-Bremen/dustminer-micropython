from log_preprocessing import parse_logs, label_logs, example_predicate
from pattern_mining import preprocess_for_mining, find_discriminative_patterns, two_stage_mining

# Step 1: Parse logs
raw_logs = parse_logs("raw_logs.txt")

# Step 2: Label logs
labeled_logs = label_logs(raw_logs, example_predicate)

# Step 3: Preprocess for mining
one_hot_data, labels = preprocess_for_mining(labeled_logs)

# Step 4: Split data into good and bad
good_data = one_hot_data[labels == "good"]
bad_data = one_hot_data[labels == "bad"]

# Step 5: Perform pattern mining
frequent_patterns, infrequent_patterns = two_stage_mining(one_hot_data, labels, min_support=0.1, top_k_segments=5)

# Step 6: Display results
print("Frequent Patterns in Bad Segments:")
print(frequent_patterns)

print("\nInfrequent Patterns in Top-K Segments:")
print(infrequent_patterns)
