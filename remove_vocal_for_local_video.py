from processor import remove_vocal_for_local_video
import sys
import asyncio

local_video_path = sys.argv[1]

print(asyncio.run(remove_vocal_for_local_video(local_video_path)))
