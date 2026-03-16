#services/caption_generator.py
import ollama
import os
import cv2
import gc


def extract_frames_memory(video_path, interval=1.5, max_frames=6):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")
    
    cap.set(cv2.CAP_PROP_POS_MSEC, 1000)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    if fps <= 0:
        fps = 24
    
    frame_interval = int(fps * interval)
    frames = []
    frame_count = 0
    saved = 0

    while True:
        ret, frame = cap.read()
        if not ret or saved >= max_frames:
            break

        if frame_count % frame_interval == 0:
            frame = cv2.resize(frame, (336, 336))
            success, buffer = cv2.imencode(
                ".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 75]
            )
            if success:
                frames.append(buffer.tobytes())
                saved += 1
            
            del frame

        frame_count += 1

    cap.release()
    return frames


def extract_caption_only(text):
    lines = text.strip().split("\n")
    for line in reversed(lines):
        if line.strip() and "#" in line:
            return line.strip().strip('"').strip("'")
    for line in reversed(lines):
        if line.strip():
            return line.strip().strip('"').strip("'")
    return text.strip().strip('"').strip("'")


def generate_caption(media_path):
    ext = os.path.splitext(media_path)[1].lower()

    image_ext = [".jpg", ".jpeg", ".png", ".webp"]
    video_ext = [".mp4", ".mov", ".avi", ".mkv"]

    if ext in image_ext:
        response = ollama.chat(
            model="qwen2.5vl:3b",
            messages=[{
                "role": "user",
                "content": """
ONLY output the caption. No analysis, no explanation, no intro text.
Do NOT wrap the caption in quotes.

Generate a catchy, human Instagram/TikTok caption.
Make it fun, emotional, add emojis.
Max 2 sentences.
""",
                "images": [media_path]
            }]
        )
        return extract_caption_only(response["message"]["content"])

    elif ext in video_ext:
        frames = extract_frames_memory(media_path)
        
        if not frames:
            raise ValueError("No frames extracted from video")
        
        print(f"Extracted {len(frames)} frames, sending to model...")

        try:
            response = ollama.chat(
                model="qwen2.5vl:3b",
                messages=[{
                    "role": "user",
                    "content": """
These images are frames extracted from the same video.

ONLY output the caption. No analysis, no explanation, no intro text.

Write a viral Instagram/TikTok caption about the main action in the video.

Rules:
- mention the action in the caption
- 1–2 sentences
- include emojis
""",
                    "images": frames
                }]
            )
        finally:
            del frames
            gc.collect()

        return extract_caption_only(response["message"]["content"])

    else:
        raise ValueError(f"Unsupported file type: {ext}")