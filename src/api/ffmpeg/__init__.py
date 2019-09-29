import os
from django.conf import settings

def concat_videos(video_paths, output_name):
    video_names = list()
    for video_path in video_paths:
        video_file = os.path.basename(video_path)
        video_name = os.path.splitext(video_file)[0]
        video_names.append(video_name)
        os.system(f'ffmpeg -i {settings.MEDIA_ROOT}/{video_name}.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts {settings.MEDIA_ROOT}/{video_name}.ts -y')
    concat_input = '|'.join([f'{settings.MEDIA_ROOT}/{video_name}.ts' for video_name in video_names])
    os.system(f'ffmpeg -i "concat:{concat_input}" -vf "transpose=1" -bsf:a aac_adtstoasc {settings.MEDIA_ROOT}/{output_name}.mp4 -y')
    
    return f'{output_name}.mp4'


def cut_video(video_path, start_shift, end_shift, output_name):
    duration = end_shift - start_shift
    video_file = os.path.basename(video_path)
    video_name = os.path.splitext(video_file)[0]
    os.system(f'ffmpeg -ss {start_shift} -i {settings.MEDIA_ROOT}/{video_name}.mp4 -to {duration} -c copy {settings.MEDIA_ROOT}/{output_name}.mp4 -y')

    return f'{settings.MEDIA_ROOT}/{output_name}.mp4'