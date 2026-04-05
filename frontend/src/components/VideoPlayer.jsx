import { useEffect, useRef } from "react";

export default function VideoPlayer({ url, seekTo }) {
  const iframeRef = useRef(null);

  const getVideoId = (url) => {
    try {
      const parsed = new URL(url);
      return parsed.searchParams.get("v");
    } catch {
      return null;
    }
  };

  const videoId = getVideoId(url);

  useEffect(() => {
    if (iframeRef.current && seekTo !== null && videoId) {
      iframeRef.current.src = `https://www.youtube.com/embed/${videoId}?start=${Math.floor(
        seekTo
      )}&autoplay=1`;
    }
  }, [seekTo, videoId]);

  return (
    <div>
      {videoId ? (
        <iframe
          ref={iframeRef}
          width="100%"
          height="400"
          src={`https://www.youtube.com/embed/${videoId}`}
          allowFullScreen
        />
      ) : (
        <p>No video</p>
      )}
    </div>
  );
}