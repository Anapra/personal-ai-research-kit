from google.cloud import bigquery

def setup_bigquery_schema():
    client = bigquery.Client()
    dataset_id = "research"
    table_id = "scored_signals"
    
    # Create Dataset if not exists
    dataset = bigquery.Dataset(f"{client.project}.{dataset_id}")
    dataset.location = "US"
    try:
        client.create_dataset(dataset, exists_ok=True)
        print(f"Dataset {dataset_id} is ready.")
    except Exception as e:
        print(f"Error creating dataset: {e}")

    # Define Schema
    schema = [
        bigquery.SchemaField("signal_id", "STRING", mode="REQUIRED", description="MD5 hash of the source URL"),
        bigquery.SchemaField("source", "STRING", mode="NULLABLE", description="Data source (LinkedIn, Reddit, ArXiv)"),
        bigquery.SchemaField("title", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("relevance_score", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("technical_significance", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("pii_detected", "BOOLEAN", mode="NULLABLE"),
        bigquery.SchemaField("tags", "STRING", mode="REPEATED"),
        bigquery.SchemaField("executive_summary", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("url", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("ingested_at", "TIMESTAMP", mode="REQUIRED", default_value_expression="CURRENT_TIMESTAMP")
    ]
    
    # Partitioning & Clustering for Performance/Cost (PDE Exam Focus)
    table_full_id = f"{client.project}.{dataset_id}.{table_id}"
    table = bigquery.Table(table_full_id, schema=schema)
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="ingested_at"
    )
    table.clustering_fields = ["source", "relevance_score"]
    
    try:
        client.create_table(table)
        print(f"Created partitioned & clustered table {table_full_id}")
    except Exception as e:
        print(f"Table already exists or error: {e}")

if __name__ == "__main__":
    setup_bigquery_schema()
