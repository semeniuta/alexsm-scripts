#!/bin/sh

timestamps_file=$1
video_file=$2
tmp_dir="$HOME/Desktop/tmp"
filelist="$tmp_dir/filelist.txt"

mkdir "$tmp_dir"

echo "Video cutting and assembling: $video_file"
echo "Timestamps file: $timestamps_file"

counter=0
echo "" > "$filelist"
commands=()

while read -r line
do
    # Make array from the line (space-separated timrstamps)
    timestamps=($line)
    
    clip_start=${timestamps[0]}
    clip_end=${timestamps[1]}

    cmd="ffmpeg -y -ss $clip_start -to $clip_end -i $video_file -c:v copy -c:a copy $tmp_dir/$counter.mp4"
    commands+=("$cmd")

    echo "file '$counter.mp4'" >> "$filelist"

    ((counter++))

done < "$timestamps_file"

for cmd in "${commands[@]}"
do
    echo "$cmd"
    eval "$cmd"
done

eval "ffmpeg -y -f concat -safe 0 -i $filelist -c copy $tmp_dir/merged.mp4"
