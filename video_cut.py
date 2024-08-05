import subprocess

def split_video(input_file, segments):
    for i, segment in enumerate(segments):
        start_time = segment['start']
        duration = segment['duration']
        output_file = f"output_part_{i+1}.mp4"
        
        command = [
            'ffmpeg',
            '-i', input_file,
            '-ss', start_time,
            '-t', duration,
            '-c', 'copy',
            output_file
        ]
        
        subprocess.run(command, check=True)
        print(f"Generated {output_file}")

# 定义要切片的时间段
segments = [
    {'start': '00:00:00', 'duration': '00:00:10'},
    {'start': '00:00:10', 'duration': '00:00:20'},
    {'start': '00:00:30', 'duration': '00:00:15'}
]

# 输入文件路径
input_file = r'一口气看完李白一生，大唐有你才真的了不起_2.mp4'

# 调用函数进行切片
split_video(input_file, segments)
