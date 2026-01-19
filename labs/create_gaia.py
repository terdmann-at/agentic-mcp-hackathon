import pandas as pd
from datasets import load_dataset
from huggingface_hub import snapshot_download
import os

def create_gaia_dataset():
    """
    Downloads the GAIA validation set, filters for text-only tasks (no multimedia/files),
    and saves the top 15 rows to 'gaia_validation_level1.csv'.
    """
    print("Downloading dataset from HuggingFace...")
    data_dir = snapshot_download(repo_id="gaia-benchmark/GAIA", repo_type="dataset")
    dataset = load_dataset(data_dir, "2023_level1", split="validation")

    # Convert to Pandas
    df = dataset.to_pandas()

    # Filter dataset (exclude multimedia tools and file uploads for this text-only agent)
    # Conditions:
    # A. Annotator Metadata does NOT contain video/image/youtube
    # B. file_name is empty or null
    mask_no_multimedia = ~df["Annotator Metadata"].astype(str).str.lower().str.contains(
        "video|image|youtube", regex=True
    )
    mask_no_file = df["file_name"].isnull() | (df["file_name"] == "")

    # Select top 15 rows
    filtered_df = df[mask_no_multimedia & mask_no_file].head(15).copy()

    output_file = "gaia_validation_level1.csv"
    
    # Save to the parent directory (labs/) if running from src, or current if running from root
    # We'll just save to current working directory for simplicity of use
    print(f"Saving filtered dataset ({len(filtered_df)} rows) to {output_file}...")
    filtered_df.to_csv(output_file, index=False)
    print("Done.")

if __name__ == "__main__":
    create_gaia_dataset()
