x264-x64-2901-aMod-noprof --preset ultrafast 23\23-1.avs -o NUL

x264-x64-2901-aMod-noprof --preset ultrafast 24\24-1.avs -o NUL

x264-x64-2901-aMod-noprof --preset ultrafast 25\25-1.avs -o NUL

x264-x64-2901-aMod-noprof --preset ultrafast 26\26-1.avs -o NUL

ffmpeg -i 23\23-2.avs -vcodec ffvhuff 23\23-1.avi

ffmpeg -i 24\24-2.avs -vcodec ffvhuff 24\24-1.avi

ffmpeg -i 25\25-2.avs -vcodec ffvhuff 25\25-1.avi

ffmpeg -i 26\26-2.avs -vcodec ffvhuff 26\26-1.avi

pause