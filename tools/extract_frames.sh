#!/bin/sh
# Usage: extract_frames.sh video.mp4 outdir seconds_between_frames
# Makes small JPG frames so an AI can look at a video it cannot play.
mkdir -p "$2"
ffmpeg -v error -i "$1" -vf "fps=1/$3,scale=480:-1" -q:v 4 "$2/f_%04d.jpg"
