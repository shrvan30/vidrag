#  Frontend Architecture

## Tech Stack

* React + Vite
* TailwindCSS

## Components

| Component   | Role                |
| ----------- | ------------------- |
| UrlInput    | Accepts YouTube URL |
| VideoPlayer | Displays video      |
| SearchBar   | Query input         |
| ResultsList | Search results      |
| ChatBox     | RAG interaction     |

## Features

* Timestamp-based navigation
* Chat-based Q&A
* Real-time UX

## Video Design

* YouTube iframe embed
* Uses `?start=seconds`
* Avoids ReactPlayer for stability
