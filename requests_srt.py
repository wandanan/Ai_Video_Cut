import requests
import yaml
import json
import logging

# 设置日志配置
logging.basicConfig(filename='api_requests.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def extract_video_url(file_path):
    """从指定的 YAML 文件中提取视频信息并返回 URL 列表."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    urls = []
    for video in data['videos']:
        urls.append(video['url'])
    
    return urls

def save_json_response(response, index):
    """将 JSON 响应保存到以索引命名的文件中."""
    file_name = f'..\Data\Srt_Json\{index + 1}.json'
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(response, json_file, ensure_ascii=False, indent=4)

def main(yaml_file):
    urls = extract_video_url(yaml_file)
    api_url = "https://bibigpt.co/api/open/rotkwCD0Wyt5/subtitle"

    for index, video_url in enumerate(urls):
        data = {
            "url": video_url,
            "includeDetail": 'false'
        }

        try:
            response = requests.post(api_url, data=data)
            response.raise_for_status()  # 如果请求失败，抛出异常

            save_json_response(response.json(), index)
            logging.info(f'成功保存 {video_url} 的响应数据。')
            print(f'成功保存 {video_url} 的响应数据。')

        except requests.exceptions.RequestException as e:
            logging.error(f'请求失败，视频 URL: {video_url}，错误: {e}')
            print(f'请求失败，视频 URL: {video_url}，错误: {e}')

if __name__ == "__main__":
    main('video_url.yaml')  # 替换为你的实际 YAML 文件路径