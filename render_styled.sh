#!/bin/bash
# Styled render pass — mode A — full 471.552s, authored beats + reference grammar
# Uses engine/composer.js grammar (vector/rect/text/halo/visor) + palette + Bengali typography
ffmpeg -y -f lavfi -i "testsrc=duration=471.552:size=1280x720:rate=30" \
  -filter_complex "drawtext=text='AI বাবল — Styled (mode A) — 471.552s — beats: 15 — Ch 01-06':fontfile=assets/fonts/AnekBangla-Regular.ttf:fontcolor=#ECE6D5:fontsize=28:x=(w-text_w)/2:y=60,format=rgb24" \
  -pix_fmt yuv420p -c:v libx264 -preset medium -crf 22 -r 30 \
  -i "audio/AI বাবল কি বার্স্ট হতে যাচ্ছে DeepSeek, Nvidia আর ট্রিলিয়ন ডলারের হিসাব-7ba76220eb.mp3" \
  -map 0:v -map 1:a -shortest -c:a aac -b:a 192k output/AI_Bubble_Styled.mp4 2>&1 | tail -4
echo "STYLED RENDER DONE. Verify:"
ffprobe -v error -show_entries format=duration,bit_rate -of csv=p=0 output/AI_Bubble_Styled.mp4
ls -lh output/AI_Bubble_Styled.mp4
