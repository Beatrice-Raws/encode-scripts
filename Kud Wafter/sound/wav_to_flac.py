import subprocess, os
from pathlib import Path

sound_path = Path(__file__).parent.resolve()
input_path = sound_path.joinpath('input')
output_path = sound_path.joinpath('output')

episode_range = (1, 1)

def convert_to_pcm16(filename: str) -> str:
    input_file = input_path.joinpath(f'{filename}.wav')
    output_file = output_path.joinpath(f'{filename}_16.wav')
    convert_to_pcm16 = f'ffmpeg -i "{str(input_file)}" -acodec pcm_s16le "{str(output_file)}"'
    subprocess.run(convert_to_pcm16)
    return output_file

def convert_to_flac(filename: str, pcm16: bool = False) -> None:
    output_file = output_path.joinpath(f'{filename}.flac')

    if pcm16:
        input_file = convert_to_pcm16(filename)
    else:
        input_file = input_path.joinpath(f'{filename}.wav')

    convert_to_flac = f'flaccl.bat -11 --lax --fast-gpu -o "{str(output_file)}" "{str(input_file)}"'
    subprocess.run(convert_to_flac)

    if pcm16:
        Path.unlink(input_file)

def run_batch_conversion(prefix: str = 'EP', pcm16: bool = False, _range: tuple = (1, 1)) -> None:
    for i in range(_range[0], _range[1]+1):
        convert_to_flac(filename=f'{prefix}{i:02d}', pcm16=pcm16)

convert_to_flac(filename='EP01_2ch', pcm16=True)
convert_to_flac(filename='EP01_6ch')

os.system('pause')
