"""
Download datasets
"""
import urllib.request
import gzip
import io
from pathlib import Path
import threading

def download_and_process_file(url, out_path):
    """
    Download datasets in txt.gz format and write to txt file
    """
    if Path(out_path).exists():
        print(out_path,"already exists. Skipping.")
        return
    
    with urllib.request.urlopen(url) as response:
        gzipped_data = response.read()

    with gzip.GzipFile(fileobj=io.BytesIO(gzipped_data)) as gz:
        decompressed_content = gz.read().decode('utf-8')

    filtered_content = '\n'.join(
        line for line in decompressed_content.splitlines()
        if not line.startswith('#')
    )

    with open(out_path, 'w', encoding='utf-8') as file:
        file.write(filtered_content)

def main():
    """
    Main function
    """
    folder_name = "data"
    Path(folder_name).mkdir(parents=False,exist_ok=True)
    data_list = [("amazon0302", "amazon"),("email-Enron","enron"),("web-Google","google"),("soc-pokec-relationships","pokec")]
    threads = [threading.Thread(target=download_and_process_file,args=(f"https://snap.stanford.edu/data/{dataset_name}.txt.gz",folder_name+"/"+file_name+".txt")) for dataset_name,file_name in data_list]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

if __name__ == "__main__":
    """
    Entry point
    """
    main()