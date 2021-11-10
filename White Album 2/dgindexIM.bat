@echo off
for %%m in (%*) do (
	C:\encoder\dgdecim\DGIndexIM.exe -i %%m -o "%%~nm.dgi" -e 
	echo Indexed "%%~nxm".
)
pause