#!/bin/sh
path="../tmp/$1"
duration=$(ffprobe -i $path -show_format -v quiet | sed -n 's/duration=//p')
duration=${duration%.*}
echo "$1 $duration"
duration=$(($duration + 0))
if [ $duration -ge 10 ]
    then
    frame1=$(($duration*2/3 - 5))
    frame2=$(($duration*2/3 + 5))
    else 
    frame1=0
    frame2=$duration 
fi
frame1=${frame1%.*}
frame2=${frame2%.*}
fmframe1=$(printf '%02d:%02d:%02d\n' $((frame1/3600)) $((frame1%3600/60)) $((frame1%60)))
fmframe2=$(printf '%02d:%02d:%02d\n' $((frame2/3600)) $((frame2%3600/60)) $((frame2%60)))
echo "$fmframe1 $fmframe2"
ffmpeg -i $path -ss $fmframe1 -t $fmframe2 -vf "fps=10,scale=320:-1" $2