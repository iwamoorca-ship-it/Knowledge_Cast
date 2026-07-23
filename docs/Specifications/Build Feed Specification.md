# Build Feed Specification

| Item | Value |
|------|-------|
| Artifact | Build Feed |
| Version | 1.0 |
| Status | Approved |
| Owner | Knowledge_Cast |
| Last Updated | 2026-07-23 |

---

# Version History

| Version | Date | Description |
|----------|------|-------------|
| 1.0 | 2026-07-23 | Initial |

---

# 1. Purpose

`build_feed.py` is responsible for generating the Podcast RSS feed (`feed.xml`) from Episode Metadata.

The script does **not** generate podcast content, audio files, or metadata.

Its sole responsibility is transforming Episode Metadata into a valid Podcast RSS feed.

---

# 2. Responsibility

## Input

Episode Metadata

```
episodes/*.json
```

## Output

```
feed.xml
```

---

# 3. Scope

## Included

- Read Episode Metadata
- Validate required fields
- Sort episodes
- Generate RSS XML
- Write `feed.xml`

## Excluded

- News collection
- AI summarization
- Script generation
- Text-to-Speech
- MP3 generation
- GitHub Push
- Git Commit

---

# 4. Input Specification

Input directory

```
episodes/
```

Input format

```
JSON
```

Each JSON represents one Podcast Episode.

Example

```
episodes/

    2026-07-23.json

    2026-07-24.json
```

---

# 5. Episode Metadata

Required fields

| Field | Description |
|--------|-------------|
| guid | Unique Episode ID |
| title | Episode Title |
| description | Episode Summary |
| publish_date | Publication Date |
| audio.path | Relative path of MP3 |
| audio.size | File size (Byte) |
| audio.mime_type | MIME Type |
| image.path | Cover image |

Optional fields

| Field |
|------|
| duration |
| author |
| language |
| topics |
| references |
| transcript |

---

# 6. Processing Flow

```
Read Episode JSON

↓

Validate Metadata

↓

Sort Episodes

↓

Generate RSS XML

↓

Write feed.xml
```

---

# 7. Validation Rules

The following fields are mandatory.

- guid
- title
- description
- publish_date
- audio.path
- audio.size
- audio.mime_type

If validation fails,

- Output error log
- Skip invalid episode
- Continue processing

---

# 8. Sorting Rule

Episodes shall be sorted by

```
publish_date
```

Descending order.

Newest episode appears first.

---

# 9. RSS Output

Generate

```
feed.xml
```

conforming to

- RSS 2.0
- Apple Podcast Specification

The following channel information shall be generated.

- title
- description
- author
- language
- category
- image
- explicit

Each Episode shall generate

- item
- title
- description
- link
- guid
- enclosure
- pubDate

---

# 10. File Output

Output

```
feed.xml
```

Location

```
Repository Root
```

Overwrite existing file.

---

# 11. Error Handling

If an Episode JSON is invalid

- Write warning
- Skip Episode
- Continue generation

If output directory is unavailable

- Abort processing

---

# 12. Dependencies

Python Standard Library

- json
- pathlib
- datetime
- xml.etree.ElementTree

External libraries are not required.

---

# 13. Non-Functional Requirements

- Deterministic Output
- Platform Independent
- UTF-8 Encoding
- Relative Path Support
- No External Network Access

---

# 14. Future Extension

Future versions may support

- Multiple Podcast Channels
- Multiple Languages
- Episode Chapters
- Transcript
- Dynamic Cover Images
- Author Profiles
- AI Generated Keywords
- AI Generated Show Notes

---

# 15. Pipeline Position

```
Episode Metadata

↓

build_feed.py

↓

feed.xml

↓

publish.py

↓

GitHub Pages

↓

Podcast Applications
```

---

# 16. Design Philosophy

The Build Feed component is a pure Publisher.

It shall not depend on AI generation, TTS, or News Collection.

All required information shall be supplied through Episode Metadata.

This design ensures complete separation between Knowledge Generation and Artifact Publication.

# 17. Assumptions

The Build Feed component assumes that:

- Episode Metadata conforms to Episode JSON Specification.
- Audio files referenced in Episode Metadata exist and are accessible.
- Cover image exists and is accessible.
- Publication timestamps are provided in ISO 8601 format.

- # References

- Episode JSON Specification
- RSS 2.0 Specification
- Apple Podcasts RSS Specification
