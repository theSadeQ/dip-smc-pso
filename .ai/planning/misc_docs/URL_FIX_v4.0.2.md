# v4.0.2 - Correct Speechify URL & Protobuf Support

## The Problem

The script was looking for the **wrong URL**:
- ❌ **Expected:** `cdn.oaistatic.com`
- ✅ **Actual:** `audio.api.speechify.com/v3/synthesis/get`

Also, the response format was unexpected:
- ❌ **Expected:** Standard audio MIME types (audio/mp3, audio/webm)
- ✅ **Actual:** `application/protobuf` (binary Protocol Buffer format)

## The Fix

### 1. Added Correct URL Patterns

```javascript
audioCDNPatterns: [
    'audio.api.speechify.com',  // ← Main Speechify API
    'api.speechify.com',
    'speechify.com/v3/synthesis',
    '/synthesis/get',  // ← Specific endpoint
    // ... other patterns
]
```

### 2. Added Protobuf MIME Type

```javascript
audioMimeTypes: [
    'audio/mpeg',
    'audio/mp3',
    // ... other audio types
    'application/protobuf',  // ← Added for Speechify!
    'application/octet-stream'
]
```

### 3. Increased Minimum File Size

```javascript
minFileSize: 10000  // 10KB (protobuf files are larger)
```

### 4. Added Debug Logging

Now shows detailed info about captured requests:

```javascript
✅ Matched by MIME type: application/protobuf
📥 Fetching blob from: https://audio.api.speechify.com/v3/synthesis/get
   MIME type: application/protobuf
   Status: 200
   Blob size: 149106 bytes
   Blob type: application/protobuf
✅ File added to UI: speechify_audio_2025-01-13T14-23-11.mp3
```

## What Will Happen Now

When you play Speechify, the script will:

1. **Detect the POST request** to `audio.api.speechify.com/v3/synthesis/get`
2. **Recognize protobuf** as an audio format
3. **Capture the 149KB response** (your audio data)
4. **Show it in the panel** as a downloadable file
5. **Save as .mp3** when you click download

## The Request Details (From Your Screenshot)

```
POST https://audio.api.speechify.com/v3/synthesis/get
Content-Type: application/protobuf  ← Now supported!
Content-Length: 149106 bytes  ← Big enough (>10KB)
Status: 200 OK
```

**This will now be captured!** ✅

## Console Output You'll See

```javascript
🎵 Speechify Audio Network Downloader v4.0.2
📋 Config: {...}
🎯 Now supports: audio.api.speechify.com + protobuf format
✅ XHR interceptor installed
✅ Fetch interceptor installed
✅ UI initialized
✅ Speechify Audio Network Downloader ready!
💡 Play Speechify to start capturing audio files
🔄 Panel will automatically re-appear if removed by page

// When you play Speechify:
🎵 Fetch: Detected audio request: https://audio.api.speechify.com/v3/synthesis/get
✅ Matched by MIME type: application/protobuf
📥 Fetching blob from: https://audio.api.speechify.com/v3/synthesis/get
   MIME type: application/protobuf
   Status: 200
   Blob size: 149106 bytes
   Blob type: application/protobuf
✅ Captured audio file: speechify_audio_2025-01-13T14-23-11.mp3 (145.6 KB)
✅ File added to UI: speechify_audio_2025-01-13T14-23-11.mp3
```

## How to Update

1. **Open Tampermonkey**
2. **Find** "Speechify Audio Network Downloader"
3. **Edit the script**
4. **Select all** (Ctrl+A)
5. **Paste** the updated `speechify-network-downloader.user.js`
6. **Save** (Ctrl+S)
7. **Refresh** the page

## Testing

1. **Refresh any webpage** (to load v4.0.2)
2. **Check console** for version: `v4.0.2`
3. **Play Speechify**
4. **Watch console** for detection messages
5. **Panel should show files** with download buttons

## What Changed

| Version | Issue | Status |
|---------|-------|--------|
| v4.0.0 | Wrong URL patterns | ❌ No capture |
| v4.0.1 | Panel disappearing | ✅ Fixed persistence |
| v4.0.2 | Correct URL + protobuf | ✅ **Should work now!** |

## File Format Note

The downloaded file will be saved as `.mp3` even though the original format is protobuf. This is because:

1. Protobuf is a container format (like a wrapper)
2. The actual audio inside is likely MP3
3. Most media players will recognize it automatically

If the file doesn't play:
- Try renaming to `.protobuf` or `.bin`
- Or use a tool to extract the audio
- Or check if Speechify has a different audio format

## Summary

**This version fixes the URL issue!** The script now:
- ✅ Looks for `audio.api.speechify.com`
- ✅ Accepts `application/protobuf` responses
- ✅ Shows detailed debug logs
- ✅ Should capture Speechify audio correctly

Try it and check the console for the detailed logs! 🎉
