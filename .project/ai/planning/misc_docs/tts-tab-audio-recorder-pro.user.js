// ==UserScript==
// @name         TTS Tab Audio Recorder Pro
// @namespace    https://github.com/yourusername/tts-recorder
// @version      2.0.0
// @description  Professional tab audio recorder with pause/resume, quality settings, and comprehensive error handling
// @match        *://*/tts-mock*
// @match        *://localhost:*/tts-mock*
// @match        *://127.0.0.1:*/tts-mock*
// @grant        none
// @run-at       document-end
// ==/UserScript==

(function () {
  'use strict';

  // ============================================================================
  // Feature Detection & Browser Compatibility
  // ============================================================================

  const BrowserSupport = {
    hasGetDisplayMedia: () => navigator.mediaDevices && 'getDisplayMedia' in navigator.mediaDevices,
    hasMediaRecorder: () => typeof MediaRecorder !== 'undefined',

    detectBrowser: () => {
      const ua = navigator.userAgent;
      if (ua.includes('Chrome') && !ua.includes('Edg')) return 'chrome';
      if (ua.includes('Edg')) return 'edge';
      if (ua.includes('Firefox')) return 'firefox';
      if (ua.includes('Safari') && !ua.includes('Chrome')) return 'safari';
      return 'unknown';
    },

    getSupportedMimeTypes: () => {
      const types = [
        'audio/webm;codecs=opus',
        'audio/webm;codecs=vorbis',
        'audio/webm',
        'video/webm;codecs=vp8,opus',
        'video/webm'
      ];
      return types.filter(type => MediaRecorder.isTypeSupported(type));
    },

    checkCompatibility: () => {
      const issues = [];
      if (!BrowserSupport.hasGetDisplayMedia()) {
        issues.push('getDisplayMedia API not supported');
      }
      if (!BrowserSupport.hasMediaRecorder()) {
        issues.push('MediaRecorder API not supported');
      }
      const supported = BrowserSupport.getSupportedMimeTypes();
      if (supported.length === 0) {
        issues.push('No supported audio formats');
      }
      return { compatible: issues.length === 0, issues, supportedFormats: supported };
    }
  };

  // ============================================================================
  // Error Handler with Browser-Specific Messages
  // ============================================================================

  class ErrorHandler {
    constructor() {
      this.browser = BrowserSupport.detectBrowser();
    }

    getInstructions() {
      const instructions = {
        chrome: 'Select the "Tab" option and check "Share tab audio"',
        edge: 'Select the "Tab" option and check "Share tab audio"',
        firefox: 'Choose "Firefox Tab" and enable audio',
        safari: 'Select specific tab and enable audio sharing',
        unknown: 'Select the current tab and enable audio sharing'
      };
      return instructions[this.browser];
    }

    handleError(error, context = '') {
      console.error(`Recording error (${context}):`, error);

      let message = '';
      let suggestion = '';

      if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
        message = 'Recording permission denied';
        suggestion = `Please allow recording. ${this.getInstructions()}.`;
      } else if (error.name === 'NotFoundError') {
        message = 'No audio track found';
        suggestion = 'Make sure to select THIS tab and enable audio sharing.';
      } else if (error.name === 'NotReadableError') {
        message = 'Cannot access audio';
        suggestion = 'Tab might be muted or audio is in use by another application.';
      } else if (error.name === 'AbortError') {
        message = 'Recording was cancelled';
        suggestion = 'You clicked "Cancel" in the permission dialog.';
      } else if (error.message && error.message.includes('audio')) {
        message = 'Audio capture failed';
        suggestion = `Ensure you enable audio. ${this.getInstructions()}.`;
      } else {
        message = error.message || 'Unknown error occurred';
        suggestion = 'Please try again. If the problem persists, try refreshing the page.';
      }

      return { message, suggestion, error };
    }

    showError(error, context = '') {
      const { message, suggestion } = this.handleError(error, context);
      const fullMessage = `❌ ${message}\n\n💡 ${suggestion}`;
      alert(fullMessage);
    }
  }

  // ============================================================================
  // UI Components and Visual Design
  // ============================================================================

  class RecorderUI {
    constructor(onStart, onStop, onPause, onResume, onSettingsToggle) {
      this.callbacks = { onStart, onStop, onPause, onResume, onSettingsToggle };
      this.state = 'idle'; // idle, recording, paused
      this.build();
    }

    build() {
      // Main container
      this.container = this.createElement('div', {
        id: 'tts-recorder-container',
        style: {
          position: 'fixed',
          zIndex: '999999',
          bottom: '20px',
          right: '20px',
          fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif',
          fontSize: '14px'
        }
      });

      // Control panel
      this.panel = this.createElement('div', {
        style: {
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          borderRadius: '12px',
          padding: '16px',
          boxShadow: '0 8px 24px rgba(0,0,0,0.15)',
          minWidth: '280px',
          color: '#fff'
        }
      });

      // Header with title and indicator
      const header = this.createElement('div', {
        style: {
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginBottom: '12px'
        },
        innerHTML: `
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-weight: 600; font-size: 15px;">🎙️ Tab Recorder</span>
          </div>
        `
      });

      this.indicator = this.createElement('div', {
        style: {
          width: '10px',
          height: '10px',
          borderRadius: '50%',
          background: '#4ade80',
          boxShadow: '0 0 8px rgba(74, 222, 128, 0.6)'
        }
      });
      header.firstElementChild.appendChild(this.indicator);

      // Status display
      this.statusDisplay = this.createElement('div', {
        style: {
          background: 'rgba(255,255,255,0.15)',
          borderRadius: '8px',
          padding: '8px 12px',
          marginBottom: '12px',
          textAlign: 'center',
          fontSize: '13px',
          minHeight: '40px',
          display: 'flex',
          flexDirection: 'column',
          gap: '4px',
          justifyContent: 'center'
        },
        innerHTML: '<div>Ready to record</div>'
      });

      // Button container
      const buttonContainer = this.createElement('div', {
        style: {
          display: 'flex',
          gap: '8px',
          marginBottom: '8px'
        }
      });

      // Start/Stop button
      this.startStopBtn = this.createButton('▶️ Start', () => {
        if (this.state === 'idle') {
          this.callbacks.onStart();
        } else {
          this.callbacks.onStop();
        }
      }, { flex: '1' });

      // Pause/Resume button
      this.pauseResumeBtn = this.createButton('⏸️ Pause', () => {
        if (this.state === 'recording') {
          this.callbacks.onPause();
        } else if (this.state === 'paused') {
          this.callbacks.onResume();
        }
      }, { flex: '1' });
      this.pauseResumeBtn.disabled = true;
      this.pauseResumeBtn.style.opacity = '0.5';

      buttonContainer.appendChild(this.startStopBtn);
      buttonContainer.appendChild(this.pauseResumeBtn);

      // Settings button
      this.settingsBtn = this.createButton('⚙️ Settings', () => {
        this.callbacks.onSettingsToggle();
      }, { fontSize: '12px' });

      // Settings panel (initially hidden)
      this.settingsPanel = this.createElement('div', {
        style: {
          background: 'rgba(255,255,255,0.1)',
          borderRadius: '8px',
          padding: '12px',
          marginTop: '8px',
          display: 'none',
          fontSize: '12px'
        }
      });

      // Quality selector
      const qualityLabel = this.createElement('label', {
        style: { display: 'block', marginBottom: '8px', fontWeight: '500' },
        textContent: 'Quality:'
      });

      this.qualitySelect = this.createElement('select', {
        style: {
          width: '100%',
          padding: '6px',
          borderRadius: '4px',
          border: 'none',
          marginBottom: '12px',
          background: 'rgba(255,255,255,0.9)',
          color: '#333'
        },
        innerHTML: `
          <option value="low">Low (64 kbps) - Small file</option>
          <option value="standard" selected>Standard (128 kbps) - Balanced</option>
          <option value="high">High (256 kbps) - Best quality</option>
        `
      });

      // Format selector
      const formatLabel = this.createElement('label', {
        style: { display: 'block', marginBottom: '8px', fontWeight: '500' },
        textContent: 'Format:'
      });

      this.formatSelect = this.createElement('select', {
        style: {
          width: '100%',
          padding: '6px',
          borderRadius: '4px',
          border: 'none',
          background: 'rgba(255,255,255,0.9)',
          color: '#333'
        }
      });

      // Populate format options based on browser support
      const supportedFormats = BrowserSupport.getSupportedMimeTypes();
      supportedFormats.forEach((mimeType, index) => {
        const option = document.createElement('option');
        option.value = mimeType;
        const label = mimeType.includes('opus') ? 'WebM Opus (Recommended)' :
                     mimeType.includes('vorbis') ? 'WebM Vorbis' :
                     mimeType.startsWith('audio/webm') ? 'WebM Audio' :
                     'WebM Video';
        option.textContent = label;
        if (index === 0) option.selected = true;
        this.formatSelect.appendChild(option);
      });

      this.settingsPanel.appendChild(qualityLabel);
      this.settingsPanel.appendChild(this.qualitySelect);
      this.settingsPanel.appendChild(formatLabel);
      this.settingsPanel.appendChild(this.formatSelect);

      // Assemble UI
      this.panel.appendChild(header);
      this.panel.appendChild(this.statusDisplay);
      this.panel.appendChild(buttonContainer);
      this.panel.appendChild(this.settingsBtn);
      this.panel.appendChild(this.settingsPanel);
      this.container.appendChild(this.panel);

      document.body.appendChild(this.container);
    }

    createElement(tag, options = {}) {
      const el = document.createElement(tag);
      if (options.id) el.id = options.id;
      if (options.className) el.className = options.className;
      if (options.innerHTML) el.innerHTML = options.innerHTML;
      if (options.textContent) el.textContent = options.textContent;
      if (options.style) Object.assign(el.style, options.style);
      return el;
    }

    createButton(text, onClick, extraStyle = {}) {
      const btn = this.createElement('button', {
        textContent: text,
        style: {
          padding: '10px 16px',
          borderRadius: '6px',
          border: 'none',
          background: 'rgba(255,255,255,0.2)',
          color: '#fff',
          cursor: 'pointer',
          fontWeight: '500',
          fontSize: '13px',
          transition: 'all 0.2s',
          ...extraStyle
        }
      });
      btn.addEventListener('click', onClick);
      btn.addEventListener('mouseenter', () => {
        if (!btn.disabled) btn.style.background = 'rgba(255,255,255,0.3)';
      });
      btn.addEventListener('mouseleave', () => {
        btn.style.background = 'rgba(255,255,255,0.2)';
      });
      return btn;
    }

    setState(state) {
      this.state = state;

      // Update indicator
      const indicatorStyles = {
        idle: { background: '#4ade80', boxShadow: '0 0 8px rgba(74, 222, 128, 0.6)' },
        recording: { background: '#ef4444', boxShadow: '0 0 8px rgba(239, 68, 68, 0.6)', animation: 'pulse 1.5s infinite' },
        paused: { background: '#fbbf24', boxShadow: '0 0 8px rgba(251, 191, 36, 0.6)' }
      };
      Object.assign(this.indicator.style, indicatorStyles[state]);

      // Update buttons
      if (state === 'idle') {
        this.startStopBtn.textContent = '▶️ Start';
        this.pauseResumeBtn.disabled = true;
        this.pauseResumeBtn.style.opacity = '0.5';
        this.settingsBtn.disabled = false;
        this.settingsBtn.style.opacity = '1';
      } else if (state === 'recording') {
        this.startStopBtn.textContent = '⏹️ Stop';
        this.pauseResumeBtn.textContent = '⏸️ Pause';
        this.pauseResumeBtn.disabled = false;
        this.pauseResumeBtn.style.opacity = '1';
        this.settingsBtn.disabled = true;
        this.settingsBtn.style.opacity = '0.5';
      } else if (state === 'paused') {
        this.pauseResumeBtn.textContent = '▶️ Resume';
      }
    }

    updateStatus(duration, fileSize) {
      const minutes = Math.floor(duration / 60);
      const seconds = duration % 60;
      const timeStr = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
      const sizeStr = (fileSize / (1024 * 1024)).toFixed(1);

      let statusText = '';
      if (this.state === 'recording') {
        statusText = `<div style="font-weight: 600; font-size: 16px; color: #fca5a5;">● REC ${timeStr}</div>`;
      } else if (this.state === 'paused') {
        statusText = `<div style="font-weight: 600; font-size: 16px; color: #fcd34d;">⏸ PAUSED ${timeStr}</div>`;
      } else {
        statusText = '<div>Ready to record</div>';
      }

      if (this.state !== 'idle') {
        statusText += `<div style="font-size: 11px; opacity: 0.9;">~${sizeStr} MB</div>`;
      }

      this.statusDisplay.innerHTML = statusText;
    }

    toggleSettings() {
      const isHidden = this.settingsPanel.style.display === 'none';
      this.settingsPanel.style.display = isHidden ? 'block' : 'none';
      this.settingsBtn.textContent = isHidden ? '⚙️ Close Settings' : '⚙️ Settings';
    }

    getSettings() {
      const qualityMap = {
        low: 64000,
        standard: 128000,
        high: 256000
      };
      return {
        bitrate: qualityMap[this.qualitySelect.value],
        mimeType: this.formatSelect.value
      };
    }

    showNotification(message, type = 'info') {
      const notification = this.createElement('div', {
        style: {
          position: 'fixed',
          top: '20px',
          right: '20px',
          background: type === 'error' ? '#ef4444' : type === 'success' ? '#22c55e' : '#3b82f6',
          color: '#fff',
          padding: '12px 20px',
          borderRadius: '8px',
          boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
          zIndex: '1000000',
          maxWidth: '300px',
          fontSize: '13px',
          animation: 'slideIn 0.3s ease'
        },
        textContent: message
      });

      document.body.appendChild(notification);
      setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
      }, 3000);
    }

    destroy() {
      if (this.container && this.container.parentNode) {
        this.container.remove();
      }
    }
  }

  // Add pulse animation
  const style = document.createElement('style');
  style.textContent = `
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.5; }
    }
    @keyframes slideIn {
      from { transform: translateX(400px); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
      from { transform: translateX(0); opacity: 1; }
      to { transform: translateX(400px); opacity: 0; }
    }
  `;
  document.head.appendChild(style);

  // ============================================================================
  // Main Tab Audio Recorder Class
  // ============================================================================

  class TabAudioRecorder {
    constructor() {
      this.mediaStream = null;
      this.mediaRecorder = null;
      this.chunks = [];
      this.startTime = null;
      this.pausedTime = 0;
      this.lastPauseTime = null;
      this.timerInterval = null;
      this.errorHandler = new ErrorHandler();

      // Load preferences
      this.loadPreferences();

      // Initialize UI
      this.ui = new RecorderUI(
        () => this.start(),
        () => this.stop(),
        () => this.pause(),
        () => this.resume(),
        () => this.ui.toggleSettings()
      );

      // Setup lifecycle handlers
      this.setupLifecycleHandlers();

      // Apply saved settings to UI
      this.applySavedSettings();
    }

    loadPreferences() {
      const defaults = {
        quality: 'standard',
        format: 'opus',
        filenamePrefix: 'recording'
      };

      try {
        const saved = localStorage.getItem('ttsRecorderPreferences');
        this.preferences = saved ? { ...defaults, ...JSON.parse(saved) } : defaults;
      } catch (e) {
        console.warn('Failed to load preferences:', e);
        this.preferences = defaults;
      }
    }

    savePreferences() {
      try {
        localStorage.setItem('ttsRecorderPreferences', JSON.stringify(this.preferences));
      } catch (e) {
        console.warn('Failed to save preferences:', e);
      }
    }

    applySavedSettings() {
      // Apply saved quality and format to UI selects
      if (this.ui.qualitySelect) {
        this.ui.qualitySelect.value = this.preferences.quality;
      }
    }

    setupLifecycleHandlers() {
      // Handle page unload during recording
      window.addEventListener('beforeunload', (e) => {
        if (this.mediaRecorder && this.mediaRecorder.state === 'recording') {
          e.preventDefault();
          e.returnValue = 'Recording in progress. Your recording will be saved. Leave anyway?';
          // Auto-save on unload
          this.stop();
        }
      });

      // Handle visibility changes
      document.addEventListener('visibilitychange', () => {
        if (document.hidden && this.mediaRecorder && this.mediaRecorder.state === 'recording') {
          console.log('Page hidden, recording continues...');
        }
      });
    }

    async start() {
      try {
        // Get settings from UI
        const settings = this.ui.getSettings();

        // Request display media with audio
        this.mediaStream = await navigator.mediaDevices.getDisplayMedia({
          video: { mediaSource: 'tab' },
          audio: {
            echoCancellation: false,
            noiseSuppression: false,
            autoGainControl: false
          }
        });

        // Check if audio track exists
        const audioTracks = this.mediaStream.getAudioTracks();
        if (audioTracks.length === 0) {
          throw new Error('No audio track found. Please enable "Share tab audio" in the permission dialog.');
        }

        console.log('Audio tracks:', audioTracks.map(t => ({ label: t.label, enabled: t.enabled })));

        // Disable video to save resources (keep track alive but disable rendering)
        const videoTracks = this.mediaStream.getVideoTracks();
        videoTracks.forEach(track => {
          track.enabled = false;
        });

        // Setup stream end detection
        this.mediaStream.getTracks().forEach(track => {
          track.addEventListener('ended', () => {
            console.log('Track ended:', track.kind);
            this.ui.showNotification('Recording stopped: User ended screen sharing', 'info');
            this.stop();
          });
        });

        // Initialize recorder
        this.chunks = [];
        this.mediaRecorder = new MediaRecorder(this.mediaStream, {
          mimeType: settings.mimeType,
          audioBitsPerSecond: settings.bitrate
        });

        this.mediaRecorder.ondataavailable = (e) => {
          if (e.data && e.data.size > 0) {
            this.chunks.push(e.data);
          }
        };

        this.mediaRecorder.onstop = () => {
          this.saveRecording();
        };

        this.mediaRecorder.onerror = (e) => {
          console.error('MediaRecorder error:', e);
          this.errorHandler.showError(e.error || new Error('Recording error'), 'MediaRecorder');
          this.cleanup();
        };

        // Start recording
        this.mediaRecorder.start(1000); // Collect data every second
        this.startTime = Date.now();
        this.pausedTime = 0;

        // Update UI
        this.ui.setState('recording');
        this.ui.showNotification('Recording started!', 'success');

        // Start timer
        this.startTimer();

        // Save current settings as preferences
        this.preferences.quality = this.ui.qualitySelect.value;
        this.savePreferences();

      } catch (error) {
        console.error('Failed to start recording:', error);
        this.errorHandler.showError(error, 'start');
        this.cleanup();
      }
    }

    stop() {
      if (!this.mediaRecorder) return;

      if (this.mediaRecorder.state !== 'inactive') {
        this.mediaRecorder.stop();
      }

      this.stopTimer();
      this.ui.setState('idle');
    }

    pause() {
      if (!this.mediaRecorder || this.mediaRecorder.state !== 'recording') return;

      this.mediaRecorder.pause();
      this.lastPauseTime = Date.now();
      this.ui.setState('paused');
      this.ui.showNotification('Recording paused', 'info');
    }

    resume() {
      if (!this.mediaRecorder || this.mediaRecorder.state !== 'paused') return;

      this.mediaRecorder.resume();
      this.pausedTime += Date.now() - this.lastPauseTime;
      this.ui.setState('recording');
      this.ui.showNotification('Recording resumed', 'success');
    }

    startTimer() {
      this.timerInterval = setInterval(() => {
        const elapsed = Math.floor((Date.now() - this.startTime - this.pausedTime) / 1000);
        const settings = this.ui.getSettings();
        const estimatedSize = (elapsed * settings.bitrate) / 8;
        this.ui.updateStatus(elapsed, estimatedSize);

        // Warn if approaching 1GB
        if (estimatedSize > 900 * 1024 * 1024 && elapsed % 30 === 0) {
          this.ui.showNotification('⚠️ Recording size approaching 1GB. Consider stopping soon.', 'info');
        }
      }, 1000);
    }

    stopTimer() {
      if (this.timerInterval) {
        clearInterval(this.timerInterval);
        this.timerInterval = null;
      }
    }

    saveRecording() {
      try {
        if (this.chunks.length === 0) {
          this.ui.showNotification('No data recorded', 'error');
          this.cleanup();
          return;
        }

        const settings = this.ui.getSettings();
        const blob = new Blob(this.chunks, { type: settings.mimeType });
        const url = URL.createObjectURL(blob);

        // Calculate actual duration
        const duration = Math.floor((Date.now() - this.startTime - this.pausedTime) / 1000);
        const minutes = Math.floor(duration / 60);
        const seconds = duration % 60;
        const durationStr = `${minutes.toString().padStart(2, '0')}m${seconds.toString().padStart(2, '0')}s`;

        // Generate filename
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').split('.')[0];
        const extension = settings.mimeType.includes('webm') ? 'webm' : 'ogg';
        const filename = `${this.preferences.filenamePrefix}-${durationStr}-${timestamp}.${extension}`;

        // Download
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();

        // Cleanup
        setTimeout(() => {
          URL.revokeObjectURL(url);
          a.remove();
        }, 1000);

        const sizeMB = (blob.size / (1024 * 1024)).toFixed(1);
        this.ui.showNotification(`✅ Saved: ${filename} (${sizeMB} MB)`, 'success');

        this.cleanup();

      } catch (error) {
        console.error('Failed to save recording:', error);
        this.ui.showNotification('Failed to save recording', 'error');
        this.cleanup();
      }
    }

    cleanup() {
      // Stop all tracks
      if (this.mediaStream) {
        this.mediaStream.getTracks().forEach(track => {
          track.stop();
        });
        this.mediaStream = null;
      }

      // Clear recorder
      this.mediaRecorder = null;
      this.chunks = [];

      // Reset timers
      this.stopTimer();
      this.startTime = null;
      this.pausedTime = 0;
      this.lastPauseTime = null;

      // Update UI
      this.ui.setState('idle');
      this.ui.updateStatus(0, 0);
    }
  }

  // ============================================================================
  // Initialization
  // ============================================================================

  function initialize() {
    // Check for target element
    const checkElement = () => {
      if (document.getElementById('tts-mock-app') ||
          document.querySelector('[data-tts-mock]') ||
          document.title.includes('TTS Mock')) {
        return true;
      }
      return false;
    };

    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => {
        if (checkElement()) startRecorder();
      });
    } else {
      if (checkElement()) startRecorder();
    }
  }

  function startRecorder() {
    // Check browser compatibility
    const compat = BrowserSupport.checkCompatibility();

    if (!compat.compatible) {
      console.error('Browser not compatible:', compat.issues);
      alert(`❌ Tab Audio Recorder cannot run:\n\n${compat.issues.join('\n')}\n\nPlease use a modern browser (Chrome, Edge, or Firefox).`);
      return;
    }

    console.log('✅ Browser compatible. Supported formats:', compat.supportedFormats);

    // Initialize recorder
    try {
      window.tabRecorder = new TabAudioRecorder();
      console.log('🎙️ Tab Audio Recorder Pro initialized successfully');
    } catch (error) {
      console.error('Failed to initialize recorder:', error);
      alert('Failed to initialize recorder. Please refresh the page.');
    }
  }

  // Start initialization
  initialize();

})();
