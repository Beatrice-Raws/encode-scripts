x264-x64-2901-aMod-noprof --preset ultrafast 19\19-1.avs -o NUL

x264-x64-2901-aMod-noprof --preset ultrafast 20\20-1.avs -o NUL

x264-x64-2901-aMod-noprof --preset ultrafast 21\21-1.avs -o NUL

x264-x64-2901-aMod-noprof --preset ultrafast 22\22-1.avs -o NUL

ffmpeg -i 19\19-2.avs -vcodec ffvhuff 19\19-1.avi

ffmpeg -i 20\20-2.avs -vcodec ffvhuff 20\20-1.avi

ffmpeg -i 21\21-2.avs -vcodec ffvhuff 21\21-1.avi

ffmpeg -i 22\22-2.avs -vcodec ffvhuff 22\22-1.avi

pause