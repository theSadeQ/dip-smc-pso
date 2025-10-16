# TTS Tab Audio Recorder Pro - User Guide

## Overview

A production-ready userscript that records tab audio with professional features including pause/resume, quality settings, real-time monitoring, and comprehensive error handling.

## Features

✅ **Professional Recording**
- High-quality tab audio capture (64/128/256 kbps)
- WebM Opus/Vorbis format support with automatic fallback
- Real-time duration timer and file size estimation
- Pause/resume functionality

✅ **Smart Error Handling**
- Browser-specific permission instructions
- Graceful handling of stream interruptions
- Auto-save on page navigation
- Detailed error messages with solutions

✅ **Modern UI**
- Beautiful gradient interface with visual indicators
- Recording state indicators (green/red/yellow pulse)
- Settings panel with quality/format selection
- Toast notifications for user feedback

✅ **Production Features**
- LocalStorage preferences persistence
- Memory-efficient chunk processing
- Proper cleanup on all exit paths
- Browser compatibility detection
- Singleton pattern prevents multiple instances

## Installation

### 1. Install a Userscript Manager

Choose one of these browser extensions:

- **Chrome/Edge**: [Tampermonkey](https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo)
- **Firefox**: [Tampermonkey](https://addons.mozilla.org/en-US/firefox/addon/tampermonkey/) or [Greasemonkey](https://addons.mozilla.org/en-US/firefox/addon/greasemonkey/)
- **Safari**: [Userscripts](https://apps.apple.com/app/userscripts/id1463298887)

### 2. Install the Script

1. Open `tts-tab-audio-recorder-pro.user.js` in your text editor
2. Copy the entire contents
3. Click your userscript manager icon → "Create new script"
4. Paste the code and save

**OR**

Click the userscript manager icon → "Install from URL" and provide the script URL (if hosted).

### 3. Configure @match Patterns

The script includes these default patterns:
```javascript
// @match        *://*/tts-mock*
// @match        *://localhost:*/tts-mock*
// @match        *://127.0.0.1:*/tts-mock*
```

**Customize for your needs:**

- For specific domain: `@match https://yourdomain.com/tts-mock*`
- For any TTS page: `@match *://*/tts*`
- For all pages (not recommended): `@match *://*/*`

Edit these in your userscript manager after installation.

## Usage

### Starting a Recording

1. **Open your TTS mock page** (must match the `@match` patterns)
2. **Locate the recorder** in the bottom-right corner:
   - Purple gradient panel with "🎙️ Tab Recorder" title
   - Green indicator = Ready to record

3. **Click "▶️ Start"**
4. **Select recording source** in browser dialog:
   - Choose **"Tab"** or **"Browser Tab"** (not "Entire Screen")
   - ✅ **Check "Share tab audio"** or "Share audio" checkbox
   - Click "Share" or "Allow"

5. **Recording begins**:
   - Red pulsing indicator
   - Timer shows duration (MM:SS)
   - File size estimates in real-time

### During Recording

**Pause/Resume:**
- Click "⏸️ Pause" to pause recording
- Indicator turns yellow
- Click "▶️ Resume" to continue
- Paused time doesn't count toward duration

**Monitor Status:**
- Duration: `02:45` (2 minutes 45 seconds)
- File size: `~5.2 MB`
- Red pulse = recording active
- Yellow = paused

**Warnings:**
- File approaching 1GB → Consider stopping
- Stream interrupted → Auto-save notification

### Stopping & Saving

1. **Click "⏹️ Stop"** when finished
2. **Recording auto-downloads** as:
   ```
   recording-02m45s-2025-01-14T10-30-45.webm
   ```
   Format: `prefix-duration-timestamp.extension`

3. **Success notification** shows:
   ```
   ✅ Saved: recording-02m45s-2025-01-14T10-30-45.webm (5.2 MB)
   ```

### Settings

**Click "⚙️ Settings"** to configure:

**Quality Options:**
- **Low (64 kbps)**: Smallest file, decent quality (speech/podcasts)
- **Standard (128 kbps)**: Balanced (default, recommended)
- **High (256 kbps)**: Best quality, larger files (music)

**Format Options:**
- **WebM Opus**: Best compression, widely supported (recommended)
- **WebM Vorbis**: Alternative if Opus unavailable
- **WebM Audio/Video**: Fallback formats

**Preferences saved automatically** in localStorage.

## Browser-Specific Instructions

### Chrome/Edge
1. Click "Start" → Select **"Tab"** in picker
2. ✅ Check **"Share tab audio"**
3. Click "Share"

### Firefox
1. Click "Start" → Select **"Firefox Tab"**
2. ✅ Check **"Share audio"**
3. Click "Allow"

### Safari
1. Click "Start" → Select specific tab
2. Enable audio sharing in permission dialog
3. Click "Allow"

## Troubleshooting

### "No audio track found"
**Cause**: Forgot to enable audio sharing
**Solution**: Restart and check "Share tab audio" in permission dialog

### "Recording permission denied"
**Cause**: Clicked "Cancel" or "Block"
**Solution**: Refresh page and allow permissions when prompted

### "Cannot access audio"
**Cause**: Tab is muted or audio used by another app
**Solution**: Unmute tab, close other apps using audio, try again

### "Selected tab has no audio"
**Cause**: Wrong tab selected or tab has no audio output
**Solution**: Ensure tab is playing audio, select correct tab

### Recording stops unexpectedly
**Cause**: User clicked browser's "Stop sharing" button
**Solution**: Partial recording auto-saved. Use recorder's Stop button instead

### Script doesn't appear
**Cause**: Page doesn't match `@match` patterns
**Solution**:
1. Check if page URL matches patterns (contains `tts-mock`)
2. Edit `@match` in userscript manager to include your URL
3. Refresh page after editing

### Poor audio quality
**Cause**: Low bitrate setting
**Solution**: Open Settings → Select "High (256 kbps)"

### Large file sizes
**Cause**: High bitrate + long duration
**Solution**: Use "Low" or "Standard" quality, or split into shorter recordings

## Advanced Features

### Auto-Save on Page Close
Recording automatically saves if you navigate away or close tab during recording.

### Stream Interruption Handling
If user clicks browser's "Stop sharing", partial recording is saved automatically.

### Memory Management
- Chunks processed every second
- Proper cleanup on all exit paths
- No memory leaks from streams or timers

### Browser Compatibility Detection
Script automatically checks:
- `getDisplayMedia` API support
- `MediaRecorder` API support
- Available MIME types
Shows clear error if browser unsupported.

## Technical Details

### File Format
- **Container**: WebM
- **Codec**: Opus (primary) or Vorbis (fallback)
- **Bitrate**: 64/128/256 kbps (configurable)
- **Sample Rate**: Browser default (typically 48kHz)

### Browser Support
- ✅ Chrome/Edge 72+
- ✅ Firefox 66+
- ✅ Safari 13+
- ❌ Internet Explorer (not supported)

### Storage
- Preferences stored in `localStorage`
- Key: `ttsRecorderPreferences`
- Persists across sessions
- Reset by clearing browser data

### Performance
- Minimal CPU usage (audio-only recording)
- Video track disabled to save resources
- 1-second chunk collection interval
- Real-time file size estimation

## Keyboard Shortcuts

Currently none (future enhancement). Use mouse clicks for all controls.

## Privacy & Security

- **No data sent to servers** - all processing local
- **No tracking or analytics** - completely private
- **Permissions required**:
  - `getDisplayMedia`: Capture tab audio
  - `localStorage`: Save preferences
- **`@grant none`**: No special permissions beyond page context

## Customization

### Change Filename Prefix

Edit line 542 in the script:
```javascript
filenamePrefix: 'my-recording'  // Default: 'recording'
```

### Change UI Position

Edit lines 148-149:
```javascript
bottom: '20px',  // Distance from bottom
right: '20px',   // Distance from right
```

### Change UI Colors

Edit gradient in line 165:
```javascript
background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
```

### Add Custom Quality Preset

Edit lines 296-300:
```javascript
<option value="ultra">Ultra (320 kbps) - Maximum quality</option>
```

Then add to `qualityMap` (line 453):
```javascript
ultra: 320000
```

## Known Limitations

1. **Tab audio only** - Cannot record system audio or microphone
2. **Browser permission required** - Cannot bypass security dialogs
3. **WebM format only** - No MP3/AAC (MediaRecorder limitation)
4. **No editing** - Records raw audio only, no post-processing
5. **File size limits** - Browser Blob limit ~2GB (varies)

## FAQ

**Q: Can I record from multiple tabs simultaneously?**
A: No. Browser security allows one tab at a time. Stop current recording first.

**Q: Can I record my microphone along with tab audio?**
A: Not with this script. That requires `getUserMedia` + `getDisplayMedia` mixing.

**Q: Why WebM and not MP3?**
A: Browser MediaRecorder API supports WebM natively. MP3 requires encoding overhead.

**Q: Can I convert WebM to MP3?**
A: Yes, use FFmpeg or online converters after downloading.

**Q: Does this work on mobile?**
A: No. Mobile browsers don't support `getDisplayMedia` API.

**Q: Can I record from incognito/private mode?**
A: Yes, but preferences won't persist (localStorage cleared on close).

## Support

For issues or feature requests:
1. Check this guide's Troubleshooting section
2. Verify browser compatibility
3. Check browser console for errors (F12 → Console)
4. Report issues with browser, version, and error messages

## Version History

### v2.0.0 (2025-01-14)
- Complete rewrite with production-ready architecture
- Added pause/resume functionality
- Real-time duration timer and file size estimation
- Comprehensive error handling with browser-specific messages
- Settings panel with quality/format selection
- LocalStorage preferences persistence
- Modern UI with visual indicators
- Lifecycle management (beforeunload, stream end detection)
- Memory-efficient chunk processing
- Browser compatibility detection
- Toast notifications
- Smart filename generation with duration

### v1.0.0 (Previous)
- Basic tab audio recording
- Single button interface
- Minimal error handling

## Credits

Developed for TTS mock page audio recording needs. Built with vanilla JavaScript, no external dependencies.

## License

Free to use and modify for personal or commercial projects.
