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
    # Make array from the line (space-separated timestamps)
    timestamps=($line)
    
    clip_start=${timestamps[0]}
    clip_end=${timestamps[1]}

    # Cut video section with slower seek & no copying of codecs
    cmd="ffmpeg -y -i $video_file -ss $clip_start -to $clip_end $tmp_dir/$counter.mp4"
    
    commands+=("$cmd")

    echo "file '$counter.mp4'" >> "$filelist"

    ((counter++))

done < "$timestamps_file"

# Execute each command for cutting video sections
for cmd in "${commands[@]}"
do
    echo "$cmd"
    eval "$cmd"
done

# Merge the clips into one file
ffmpeg -y -f concat -safe 0 -i "$filelist" -c copy "$tmp_dir/merged.mp4"