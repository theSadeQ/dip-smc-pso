# TTS Tab Audio Recorder Pro - Quick Start

## 30-Second Setup

1. Install [Tampermonkey](https://www.tampermonkey.net/) browser extension
2. Click Tampermonkey icon → Create new script
3. Paste contents of `tts-tab-audio-recorder-pro.user.js`
4. Save (Ctrl+S or Cmd+S)
5. Navigate to your TTS mock page

## Recording in 3 Steps

```
1. Click "▶️ Start" → Select "Tab" → ✅ Check "Share tab audio" → Click "Share"
2. Record your audio (use ⏸️ Pause if needed)
3. Click "⏹️ Stop" → File auto-downloads
```

## Visual Guide

```
┌─────────────────────────────┐
│ 🎙️ Tab Recorder         🟢│  ← Green = Ready
├─────────────────────────────┤
│     Ready to record         │
│                             │
├─────────────────────────────┤
│ [▶️ Start]  [⏸️ Pause]     │
│                             │
│ [⚙️ Settings]               │
└─────────────────────────────┘
```

**Recording:**
```
┌─────────────────────────────┐
│ 🎙️ Tab Recorder         🔴│  ← Red pulse = Recording
├─────────────────────────────┤
│      ● REC 02:45            │  ← Duration
│       ~5.2 MB               │  ← File size
├─────────────────────────────┤
│ [⏹️ Stop]   [⏸️ Pause]     │
└─────────────────────────────┘
```

## Common Issues → Quick Fixes

| Problem | Solution |
|---------|----------|
| **Script doesn't appear** | Check URL matches `*/tts-mock*` or edit `@match` |
| **No audio captured** | ✅ Check "Share tab audio" in permission dialog |
| **"Permission denied"** | Refresh page, click Allow when prompted |
| **Poor quality** | Settings → High (256 kbps) |
| **Large files** | Settings → Low (64 kbps) or Standard (128 kbps) |

## Settings Quick Reference

**Quality (Click ⚙️ Settings):**
- **Low (64 kbps)**: ~29 MB per hour | Good for speech
- **Standard (128 kbps)**: ~58 MB per hour | Balanced (default)
- **High (256 kbps)**: ~115 MB per hour | Best quality

**Format:**
- **WebM Opus**: Recommended (best compression)
- **WebM Vorbis**: Fallback option
- Other formats: Auto-selected if needed

## Keyboard Cheat Sheet

Currently no keyboard shortcuts. Use mouse for all controls.

## Browser Permission Dialog - What to Click

### Chrome/Edge:
```
┌────────────────────────────────────┐
│ Share your screen                  │
├────────────────────────────────────┤
│ ○ Entire screen                    │
│ ● Tab                         ← Click this
│   ✅ Share tab audio          ← Check this
├────────────────────────────────────┤
│ [Cancel]              [Share] ← Click Share
└────────────────────────────────────┘
```

### Firefox:
```
┌────────────────────────────────────┐
│ Choose what to share               │
├────────────────────────────────────┤
│ ○ Screen                           │
│ ● Firefox Tab                 ← Click this
│   ✅ Share audio              ← Check this
├────────────────────────────────────┤
│ [Cancel]             [Allow]  ← Click Allow
└────────────────────────────────────┘
```

## Pro Tips

💡 **Always check "Share tab audio"** - Most common mistake
💡 **Pause instead of stop** - If you need a break
💡 **Settings persist** - Quality choice remembered
💡 **Auto-saves on close** - Safe to close tab during recording
💡 **Watch file size** - Warning at ~900MB (browser limit ~2GB)

## Error Messages Explained

| Message | Meaning |
|---------|---------|
| ✅ Saved: ... | Success! File downloaded |
| ⚠️ Approaching 1GB | Stop soon, file getting large |
| ❌ No audio track found | Forgot to check "Share tab audio" |
| ❌ Permission denied | Clicked "Cancel" - try again |
| 🛑 Recording stopped: ... | User clicked browser's stop button |

## File Naming

**Format:** `recording-02m45s-2025-01-14T10-30-45.webm`
- `recording` = prefix (customizable)
- `02m45s` = duration (2 min 45 sec)
- `2025-01-14T10-30-45` = timestamp
- `.webm` = format

## Technical Specs at a Glance

| Feature | Details |
|---------|---------|
| **Format** | WebM (Opus/Vorbis codec) |
| **Quality** | 64/128/256 kbps configurable |
| **Sample Rate** | 48kHz (browser default) |
| **Max Duration** | Unlimited (watch file size) |
| **Max File Size** | ~2GB (browser Blob limit) |
| **Browser Support** | Chrome 72+, Firefox 66+, Safari 13+ |

## 5-Minute Tutorial

**Step 1: Start Recording (30 sec)**
- Open TTS page → Click "▶️ Start"
- Browser popup appears
- Select "Tab", check "Share tab audio", click "Share"
- Red pulse appears = recording started ✅

**Step 2: During Recording (variable)**
- Timer counts up: 00:01, 00:02, 00:03...
- File size estimate updates
- Pause anytime with ⏸️
- Resume with ▶️

**Step 3: Stop & Save (10 sec)**
- Click "⏹️ Stop"
- File downloads automatically
- Green checkmark notification
- Ready for next recording ✅

**Total setup time:** < 5 minutes including installation!

## Customization Quick Tips

**Change filename prefix:**
Edit localStorage manually in Console (F12):
```javascript
let prefs = JSON.parse(localStorage.getItem('ttsRecorderPreferences'));
prefs.filenamePrefix = 'my-audio';
localStorage.setItem('ttsRecorderPreferences', JSON.stringify(prefs));
```

**Change UI position:**
Edit script lines 148-149:
```javascript
bottom: '20px',  // Distance from bottom
right: '20px',   // Distance from right
```

**Change colors:**
Edit script line 165 (gradient):
```javascript
background: 'linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%)',
```

## Getting Help

**Before asking for help, check:**
1. ✅ Is script installed and enabled in Tampermonkey?
2. ✅ Does page URL match `@match` patterns?
3. ✅ Did you check "Share tab audio" in dialog?
4. ✅ Is tab actually playing audio?
5. ✅ Browser console (F12) showing errors?

**If still stuck:**
- Read full guide: `TTS_RECORDER_GUIDE.md`
- Check Troubleshooting section
- Verify browser compatibility

## One-Liner for Experts

```bash
# Install → Edit @match if needed → Open page → Start → Select Tab + Audio → Record → Stop
```

That's it! You're ready to record. 🎉

## Next Steps

- Read full guide for advanced features
- Customize colors/position to your liking
- Configure quality presets
- Explore pause/resume workflow
- Set custom filename prefix

---

**Quick Links:**
- Full Guide: `TTS_RECORDER_GUIDE.md`
- Script File: `tts-tab-audio-recorder-pro.user.js`
- Tampermonkey: https://www.tampermonkey.net/
