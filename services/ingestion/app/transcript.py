from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str):
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    return url


def fetch_transcript(video_id: str):
    api = YouTubeTranscriptApi()

    try:
        # ✅ Try English first
        transcript = api.fetch(video_id, languages=["en"])

    except Exception:
        try:
            # 🔥 fallback to ANY available language
            transcript_list = api.list(video_id)
            transcript = transcript_list.find_transcript(
                [t.language_code for t in transcript_list]
            ).fetch()

        except Exception as e:
            raise Exception("No transcript available for this video")

    return [
        {
            "text": t.text,
            "start": t.start,
            "end": t.start + t.duration
        }
        for t in transcript
    ]