import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules


def preprocess_for_mining(labeled_data):
    ## Convert labeled logs into a format suitable for Apriori analysis.
    ## Output: One-hot encoded DataFrame for frequent pattern mining.
    records = []
    for item in labeled_data:
        log = item["Log"]
        row = {
            "NodeId": f"Node_{log['NodeId']}",
            "EventType": f"Event_{log['EventType']}",
            "Label": item["Label"]
        }
        records.append(row)

    df = pd.DataFrame(records)
    one_hot = pd.get_dummies(df.drop(columns="Label"))
    return one_hot, df["Label"]


def find_frequent_patterns(data, min_support=0.1):
    ## Finding frequent patterns in the dataset using Apriori.
    frequent_patterns = apriori(data, min_support=min_support, use_colnames=True)
    return frequent_patterns


def find_discriminative_patterns(good_data, bad_data, min_support=0.1):
    ## Finding discriminative patterns by comparing good and bad patterns.
    good_patterns = find_frequent_patterns(good_data, min_support=min_support)
    bad_patterns = find_frequent_patterns(bad_data, min_support=min_support)

    # Compare patterns for discrimination
    discriminative_patterns = pd.concat([good_patterns, bad_patterns], keys=["Good", "Bad"])
    discriminative_patterns = discriminative_patterns.reset_index(level=0).rename(columns={"level_0": "Category"})
    return discriminative_patterns


def two_stage_mining(data, labels, min_support=0.1, top_k_segments=5):
    # Combine data with labels for segment ranking
    data["Label"] = labels
    bad_segments = data[data["Label"] == "bad"]

    # Stage 1: Frequent pattern mining in bad segments
    bad_one_hot = pd.get_dummies(bad_segments.drop(columns="Label"))
    frequent_patterns = find_frequent_patterns(bad_one_hot, min_support=min_support)

    # Stage 2: Identify infrequent patterns in top K bad segments
    ranked_segments = bad_segments.head(top_k_segments)
    ranked_one_hot = pd.get_dummies(ranked_segments.drop(columns="Label"))
    infrequent_patterns = find_frequent_patterns(ranked_one_hot, min_support=0.01)

    return frequent_patterns, infrequent_patterns
