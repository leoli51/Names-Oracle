from . import get_name_info, get_available_countries
import importlib.resources

data_handle = importlib.resources.files(__package__).joinpath("data")
with data_handle as p:
    data_path = p

def remove_dataset():
    import shutil 

    if data_path.exists():
        print("Removing dataset...")
        try:
            shutil.rmtree(mydir)
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))
        print("Done.")
    else:
        print("Dataset not found, download it with: python -m names_oracle download_dataset")

def download_dataset():
    import zipfile
    from urllib.request import urlretrieve
    import os
    from os import path
    
    print("Downloading dataset ~600MB it may take some time. The dataset is only downloaded once!")
    
    data_url = "https://github.com/leoli51/Names-Oracle/releases/download/0.1/data.zip"
    data_zip_path = path.join(path.dirname(data_path), "data.zip")

    print(f"downloading: {data_url} in {data_zip_path}")
    
    urlretrieve(data_url, data_zip_path)
    
    print("Dataset downloaded!")

    with zipfile.ZipFile(data_zip_path, 'r') as zip_ref:
        zip_ref.extractall(path.dirname(data_path))

    os.remove(data_zip_path)

def test():
    if not data_path.exists():
        print("Dataset not found, download it with: python -m names_oracle download_dataset")
        return
    
    from pprint import pprint
    print("List of available countries:")
    print(get_available_countries())

    print("Data for Francesco:")
    pprint(get_name_info('Francesco', 'IT'))
    print("Data for Maria Felicita:")
    pprint(get_name_info('Maria Felicita', 'IT'))
    print("Data for random non existent name (should return None):")
    pprint(get_name_info('Mawlkenv lka', 'IT'))

    print("Splitting La Rocca Maria Felicita in first (Maria Felicita) and last (La Rocca) name:")
    print(split_name_in_first_and_last("La Rocca Maria Felicita"))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='download or test the names oracle module')
    parser.add_argument('command', type=str, help='the command to execute, can be: download_dataset, remove_dataset or test')
    args = parser.parse_args()
    # parse command either test or download 
    if args.command == "download_dataset":
        download_dataset()
    elif args.command == "test":
        test()
    elif args.command == "remove_dataset":
        remove_dataset()
    else:
        print(f"invalid command: {args.command}, use download_dataset, remove_dataset or test")