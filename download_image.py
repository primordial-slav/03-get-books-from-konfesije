import requests
import os

def read_config(filepath):
    """Read URL and cookies from a file and return them."""
    config = {'cookies': {}}
    with open(filepath, 'r') as file:
        for line in file:
            key, value = line.strip().split('=', 1)
            if key == 'URL':
                config['url_template'] = value
            else:
                config['cookies'][key] = value
    return config

def download_image(pg_seq,folder,year, url_template, cookies, download_folder):
    """Download a single image using the provided cookies and URL template and save to specified folder."""
    formatted_pg_seq = format(pg_seq, '03')
    url = url_template.format(pg_seq=formatted_pg_seq,year=year,key=folder)
    response = requests.get(url, cookies=cookies)
    if response.status_code == 200 and 'image' in response.headers['Content-Type']:
        
        filename = f'{year}_{formatted_pg_seq}.jpg'
        file_path = os.path.join(folder, filename)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Image {formatted_pg_seq} downloaded and saved as {file_path}.")
        return True
    else:
        print(f"Failed to download image {formatted_pg_seq} or incorrect content type received.")
        return False

def create_download_folder(folder_name):
    """Ensure the download folder exists."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

def main():
    config_path = './dummy_config.txt'  # Path to the config file
    config = read_config(config_path)

    # Create and use a 'temp' folder in the current directory for downloads
    download_folder = create_download_folder('temp')

    url_template = config['url_template']
    cookies = config['cookies']
    
    folders = ['vencani', 'krsteni', 'umrli']
    years = list(range(1872, 1896))
    
    
    for folder in folders:
        for year in years:
            pg_seq = 1
            while True:
                success = download_image(pg_seq,folder,year ,url_template, cookies, download_folder)
                if not success:
                    print(f"Stopping download at page {pg_seq}, assuming no more images.")
                    break
                pg_seq += 1

if __name__ == "__main__":
    main()
