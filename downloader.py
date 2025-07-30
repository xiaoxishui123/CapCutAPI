import os
import subprocess
import time
import requests
from requests.exceptions import RequestException, Timeout
from urllib.parse import urlparse, unquote

def download_video(video_url, draft_name, material_name):
    """
    Download video to specified directory
    :param video_url: Video URL
    :param draft_name: Draft name
    :param material_name: Material name
    :return: Local video path
    """
    # Ensure directory exists
    video_dir = f"{draft_name}/assets/video"
    os.makedirs(video_dir, exist_ok=True)
    
    # Generate local filename
    local_path = f"{video_dir}/{material_name}"
    
    # Check if file already exists
    if os.path.exists(local_path):
        print(f"Video file already exists: {local_path}")
        return local_path
    
    try:
        # Use ffmpeg to download video
        command = [
            'ffmpeg',
            '-i', video_url,
            '-c', 'copy',  # Direct copy, no re-encoding
            local_path
        ]
        subprocess.run(command, check=True, capture_output=True)
        return local_path
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to download video: {e.stderr.decode('utf-8')}")

def download_image(image_url, draft_name, material_name):
    """
    Download image to specified directory, and convert to PNG format
    :param image_url: Image URL
    :param draft_name: Draft name
    :param material_name: Material name
    :return: Local image path
    """
    # Ensure directory exists
    image_dir = f"{draft_name}/assets/image"
    os.makedirs(image_dir, exist_ok=True)
    
    # Uniformly use png format
    local_path = f"{image_dir}/{material_name}"
    
    # Check if file already exists
    if os.path.exists(local_path):
        print(f"Image file already exists: {local_path}")
        return local_path
    
    try:
        # Use ffmpeg to download and convert image to PNG format
        command = [
            'ffmpeg',
            '-i', image_url,
            '-vf', 'format=rgba',  # Convert to RGBA format to support transparency
            '-frames:v', '1',      # Ensure only one frame is processed
            '-y',                  # Overwrite existing files
            local_path
        ]
        subprocess.run(command, check=True, capture_output=True)
        return local_path
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to download image: {e.stderr.decode('utf-8')}")

def download_audio(audio_url, draft_name, material_name):
    """
    Download audio and transcode to MP3 format to specified directory
    :param audio_url: Audio URL
    :param draft_name: Draft name
    :param material_name: Material name
    :return: Local audio path
    """
    # Ensure directory exists
    audio_dir = f"{draft_name}/assets/audio"
    os.makedirs(audio_dir, exist_ok=True)
    
    # Generate local filename (keep .mp3 extension)
    local_path = f"{audio_dir}/{material_name}"
    
    # Check if file already exists
    if os.path.exists(local_path):
        print(f"Audio file already exists: {local_path}")
        return local_path
    
    try:
        # Use ffmpeg to download and transcode to MP3 (key modification: specify MP3 encoder)
        command = [
            'ffmpeg',
            '-i', audio_url,          # Input URL
            '-c:a', 'libmp3lame',     # Force encode audio stream to MP3
            '-q:a', '2',              # Set audio quality (0-9, 0 is best, 2 balances quality and file size)
            '-y',                     # Overwrite existing files (optional)
            local_path                # Output path
        ]
        subprocess.run(command, check=True, capture_output=True, text=True)
        return local_path
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to download audio:\n{e.stderr}")

def download_file(url:str, local_filename, max_retries=3, timeout=180):
    # Extract directory part
    directory = os.path.dirname(local_filename)

    # 检查是否是豆包OSS URL，如果是则添加特殊的HTTP头
    if 'ark-content-generation-cn-beijing.tos-cn-beijing.volces.com' in url:
        print(f"检测到豆包OSS URL，使用特殊HTTP头进行下载: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'video/mp4,video/*,*/*;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://doubao.com/',
            'Sec-Fetch-Dest': 'video',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'cross-site'
        }
    else:
        headers = {}

    retries = 0
    while retries < max_retries:
        try:
            if retries > 0:
                wait_time = 2 ** retries  # Exponential backoff strategy
                print(f"Retrying in {wait_time} seconds... (Attempt {retries+1}/{max_retries})")
                time.sleep(wait_time)
            
            print(f"Downloading file: {local_filename}")
            start_time = time.time()
            
            # Create directory (if it doesn't exist)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
                print(f"Created directory: {directory}")

            # 使用headers进行下载
            with requests.get(url, stream=True, timeout=timeout, headers=headers) as response:
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                block_size = 1024
                
                with open(local_filename, 'wb') as file:
                    bytes_written = 0
                    for chunk in response.iter_content(block_size):
                        if chunk:
                            file.write(chunk)
                            bytes_written += len(chunk)
                            
                            if total_size > 0:
                                progress = bytes_written / total_size * 100
                                # For frequently updated progress, consider using logger.debug or more granular control to avoid large log files
                                # Or only output progress to console, not write to file
                                print(f"\r[PROGRESS] {progress:.2f}% ({bytes_written/1024:.2f}KB/{total_size/1024:.2f}KB)", end='')
                                pass # Avoid printing too much progress information in log files
                
                if total_size > 0:
                    # print() # Original newline
                    pass
                print(f"Download completed in {time.time()-start_time:.2f} seconds")
                print(f"File saved as: {os.path.abspath(local_filename)}")
                return True
                
        except Timeout:
            print(f"Download timed out after {timeout} seconds")
        except RequestException as e:
            print(f"Request failed: {e}")
        except Exception as e:
            print(f"Unexpected error during download: {e}")
        
        retries += 1
    
    print(f"Download failed after {max_retries} attempts for URL: {url}")
    return False

