import os
import logging
import json

# 设置日志配置
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def load_srt_files_from_directory(base_path='Data/Srt_temp'):
    srt_data = {}
    # 遍历 base_path 目录中的所有子文件夹
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        if os.path.isdir(folder_path):
            srt_contents = []
            # 遍历子文件夹中的所有文件
            for file in os.listdir(folder_path):
                if file.endswith('.srt'):
                    file_path = os.path.join(folder_path, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            srt_content = f.read()
                        # 只保存前 100 个字符
                        srt_contents.append(srt_content[:100])
                    except Exception as e:
                        logging.error(f"Error reading file {file_path}: {e}")
            if srt_contents:
                srt_data[folder] = srt_contents
    return srt_data

def save_to_json(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"Error writing JSON file {file_path}: {e}")

# 示例用法
if __name__ == "__main__":
    base_path = 'Data/Srt_temp'
    srt_data = load_srt_files_from_directory(base_path)
    json_file_path = 'srt_data.json'
    save_to_json(srt_data, json_file_path)
    print(f"Data has been saved to {json_file_path}")
