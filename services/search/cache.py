from retrieval import VideoIndex

video_cache = {}

def get_video_index(video_id, loader_func):
    if video_id not in video_cache:
        chunks = loader_func(video_id)

        if not chunks:
            print(f"⚠️ No chunks for video_id: {video_id}")
            return None

        try:
            video_cache[video_id] = VideoIndex(chunks)
        except Exception as e:
            print(f"❌ Index creation failed: {e}")
            return None

    return video_cache[video_id]