import subprocess, os
from pathlib import Path

sound_path = Path(__file__).parent.resolve()
input_path = sound_path.joinpath('input')
output_path = sound_path.joinpath('output')

episode_range = (1, 12)
special_range = (1, 10)

def run_convert(prefix: str = 'EP', _range: tuple = (1, 1)) -> None:
    for i in range(_range[0], _range[1]+1):
        pcm24_file = input_path.joinpath(f'{prefix}{i:02d}.wav')
        pcm16_file = input_path.joinpath(f'{prefix}{i:02d}_16.wav')
        flac_file = output_path.joinpath(f'{prefix}{i:02d}.flac')
    
        convert_to_pcm16 = f'ffmpeg -i "{str(pcm24_file)}" -acodec pcm_s16le "{str(pcm16_file)}"'
        convert_to_flac = f'flaccl.bat -11 --lax --fast-gpu -o "{str(flac_file)}" "{str(pcm16_file)}"'
        
        subprocess.run(convert_to_pcm16)
        subprocess.run(convert_to_flac)

        Path.unlink(pcm24_file)
        Path.unlink(pcm16_file)

run_convert(prefix='EP', _range=episode_range)
run_convert(prefix='SP', _range=special_range)

os.system('pause')
