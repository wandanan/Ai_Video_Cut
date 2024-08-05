import tiktoken
import re
import os

# 指定模型
enc = tiktoken.encoding_for_model("gpt-4o-2024-05-13")

# 指定文件夹路径
folder_path = r'Data\Srt_ex'  # 替换为你的文件夹路径

# 检查文件夹是否存在
if not os.path.exists(folder_path):
    raise FileNotFoundError(f"文件夹未找到: {folder_path}")

# 获取所有 .srt 文件
srt_files = [f for f in os.listdir(folder_path) if f.endswith('.srt')]

# 定义最大和最小 token 数以及重叠字符数
max_tokens = 7000
min_tokens = 5000
overlap_chars = 75

# 提取时间标记的正则表达式 (分秒格式)
timestamp_pattern = re.compile(r'^\d{2}:\d{2} --> \d{2}:\d{2} .*')

# 检查行是否符合要求
def is_valid_line(line):
    return bool(timestamp_pattern.match(line.strip()))

# 找到合适的分割点
def find_split_point(tokens, start, end):
    while end > start and len(tokens[start:end]) > max_tokens:
        end -= 1
    return end

# 检查并清理 chunk 中的时间结构
def clean_chunk(chunk_text):
    lines = chunk_text.split('\n')
    cleaned_lines = [line for line in lines if is_valid_line(line)]
    return '\n'.join(cleaned_lines)

# 处理每个 srt 文件
for srt_file in srt_files:
    file_path = os.path.join(folder_path, srt_file)
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 编码并统计 token 数
    encoded_tokens = enc.encode(content)
    num_tokens = len(encoded_tokens)

    # 拆分并处理重叠
    chunks = []
    i = 0
    while i < num_tokens:
        start = i
        end = min(i + max_tokens, num_tokens)

        # 寻找合适的分割点
        split_point = find_split_point(encoded_tokens, start, end)

        # 确保每个 chunk 至少有 min_tokens
        if split_point - start < min_tokens:
            split_point = min(start + max_tokens, num_tokens)

        chunk_tokens = encoded_tokens[start:split_point]
        chunk_text = enc.decode(chunk_tokens)

        # 添加前后重叠
        if start > 0:
            overlap_start = enc.decode(encoded_tokens[max(0, start - overlap_chars):start])
            chunk_text = overlap_start + chunk_text

        if split_point < num_tokens:
            overlap_end = enc.decode(encoded_tokens[split_point:min(split_point + overlap_chars, num_tokens)])
            chunk_text += overlap_end

        # 清理 chunk 中的时间结构
        cleaned_chunk_text = clean_chunk(chunk_text)

        # 检查最后一个 chunk 的字符数
        if len(cleaned_chunk_text) >= 300:
            chunks.append(cleaned_chunk_text)
        i = split_point

    # 创建输出文件夹
    output_folder = os.path.join(folder_path, os.path.splitext(srt_file)[0])
    os.makedirs(output_folder, exist_ok=True)

    # 输出结果
    for idx, chunk in enumerate(chunks):
        chunk_file_path = os.path.join(output_folder, f"{os.path.splitext(srt_file)[0]}_chunk_{idx + 1}.srt")
        with open(chunk_file_path, 'w', encoding='utf-8') as chunk_file:
            chunk_file.write(chunk)
        print(f"Chunk {idx + 1} saved to {chunk_file_path}")