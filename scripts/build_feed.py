from pathlib import Path
import json
from datetime import datetime, timezone
from email.utils import format_datetime
import xml.etree.ElementTree as ET

# ============================================================
# Configuration
# ============================================================

BASE_URL = "https://iwamoorca-ship-it.github.io/Knowledge_Cast/"

CHANNEL = {
    "title": "Knowledge_Cast",
    "link": BASE_URL,
    "description": "AI Generated Business Knowledge Podcast",
    "language": "ja-JP",
    "author": "Iwamorca",
    "summary": "Daily AI-generated business knowledge podcast.",
    "category": "Non-Profit",
    "image": BASE_URL + "assets/cover.jpg",
    "explicit": "false",
}

EPISODE_DIR = Path("episodes")
OUTPUT_FILE = Path("feed.xml")

# ============================================================
# Helpers
# ============================================================


def to_rfc2822(iso_string: str) -> str:
    dt = datetime.fromisoformat(iso_string)
    dt = dt.astimezone(timezone.utc)
    return format_datetime(dt)


def validate(ep: dict) -> bool:
    required = [
        "guid",
        "title",
        "description",
        "publish_date",
        "audio",
        "image",
    ]

    for key in required:
        if key not in ep:
            return False

    if "path" not in ep["audio"]:
        return False

    if "size" not in ep["audio"]:
        return False

    if "mime_type" not in ep["audio"]:
        return False

    if "path" not in ep["image"]:
        return False

    return True


def load_episodes():
    episodes = []

    for file in EPISODE_DIR.glob("*.json"):
        try:
            with open(file, encoding="utf-8") as f:
                ep = json.load(f)

            if not validate(ep):
                print(f"[WARNING] Invalid metadata : {file}")
                continue

            episodes.append(ep)

        except Exception as e:
            print(f"[WARNING] Failed to load {file}: {e}")

    episodes.sort(
        key=lambda x: datetime.fromisoformat(x["publish_date"]),
        reverse=True,
    )

    return episodes


# ============================================================
# RSS Generation
# ============================================================


def build_feed(episodes):

    rss = ET.Element(
        "rss",
        {
            "version": "2.0",
            "xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
        },
    )

    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = CHANNEL["title"]
    ET.SubElement(channel, "link").text = CHANNEL["link"]
    ET.SubElement(channel, "description").text = CHANNEL["description"]
    ET.SubElement(channel, "language").text = CHANNEL["language"]

    ET.SubElement(channel, "{http://www.itunes.com/dtds/podcast-1.0.dtd}author").text = CHANNEL["author"]

    ET.SubElement(channel, "{http://www.itunes.com/dtds/podcast-1.0.dtd}summary").text = CHANNEL["summary"]

    ET.SubElement(
        channel,
        "{http://www.itunes.com/dtds/podcast-1.0.dtd}category",
        {"text": CHANNEL["category"]},
    )

    ET.SubElement(
        channel,
        "{http://www.itunes.com/dtds/podcast-1.0.dtd}image",
        {"href": CHANNEL["image"]},
    )

    ET.SubElement(channel, "{http://www.itunes.com/dtds/podcast-1.0.dtd}explicit").text = CHANNEL["explicit"]

    for ep in episodes:

        item = ET.SubElement(channel, "item")

        ET.SubElement(item, "title").text = ep["title"]
        ET.SubElement(item, "link").text = BASE_URL
        ET.SubElement(item, "description").text = ep["description"]
        ET.SubElement(item, "pubDate").text = to_rfc2822(ep["publish_date"])

        guid = BASE_URL + ep["audio"]["path"]
        ET.SubElement(item, "guid").text = guid

        ET.SubElement(
            item,
            "enclosure",
            {
                "url": guid,
                "length": str(ep["audio"]["size"]),
                "type": ep["audio"]["mime_type"],
            },
        )

    ET.indent(rss, space="    ")

    tree = ET.ElementTree(rss)

    tree.write(
        OUTPUT_FILE,
        encoding="utf-8",
        xml_declaration=True,
    )


# ============================================================
# Main
# ============================================================


def main():
    episodes = load_episodes()
    build_feed(episodes)
    print("feed.xml generated successfully.")


if __name__ == "__main__":
    main()
