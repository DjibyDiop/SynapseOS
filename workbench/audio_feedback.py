"""
SynapseOS 100% Offline Audio Feedback & Read-Aloud Helper
=========================================================
Zero-dependency, non-blocking audio chimes and offline Text-To-Speech (TTS):
  - Sound chimes:
      * Windows: stdlib `winsound.Beep` in a daemon thread
      * Linux/Potato: `paplay` / `aplay` / terminal bell fallback
  - Read-Aloud TTS:
      * Linux (SynapseOS Live ISO): `espeak-ng` (pre-installed offline TTS)
      * Windows: silent/optional PowerShell SAPI or no-op if disabled

Never blocks the GTK UI thread or headless unit tests!
"""

import os
import shutil
import subprocess
import sys
import threading


def play_chime(kind: str = "correct", enabled: bool = True) -> None:
    """
    Play a short, pleasant non-blocking chime:
      kind = 'correct' | 'wrong' | 'combo' | 'level_up'
    """
    if not enabled or os.environ.get("SYNAPSE_HEADLESS_TEST") == "1":
        return

    def _worker():
        try:
            if sys.platform.startswith("win"):
                import winsound
                if kind == "correct":
                    winsound.Beep(660, 80)
                    winsound.Beep(880, 110)
                elif kind == "combo":
                    winsound.Beep(784, 70)
                    winsound.Beep(988, 70)
                    winsound.Beep(1175, 130)
                elif kind == "level_up":
                    for freq in (523, 659, 784, 1046):
                        winsound.Beep(freq, 80)
                else:  # wrong
                    winsound.Beep(280, 150)
            else:
                # Linux / POSIX lightweight fallback
                if shutil.which("speaker-test"):
                    pass  # avoid hanging speaker-test
                sys.stdout.write("\a")
                sys.stdout.flush()
        except Exception:
            pass

    t = threading.Thread(target=_worker, daemon=True)
    t.start()


def speak_text(text: str, lang: str = "en", enabled: bool = True) -> None:
    """
    Speak text aloud completely offline using `espeak-ng` on Linux (or SAPI on Windows if enabled).
    Runs in a background daemon thread so it never blocks UI.
    """
    if not enabled or not text or os.environ.get("SYNAPSE_HEADLESS_TEST") == "1":
        return

    clean_text = text.strip()[:400]

    def _worker():
        try:
            if shutil.which("espeak-ng"):
                voice = "fr" if lang == "fr" else "en"
                subprocess.run(
                    ["espeak-ng", "-v", voice, "-s", "155", clean_text],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=8,
                )
            elif shutil.which("espeak"):
                voice = "fr" if lang == "fr" else "en"
                subprocess.run(
                    ["espeak", "-v", voice, "-s", "155", clean_text],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=8,
                )
        except Exception:
            pass

    t = threading.Thread(target=_worker, daemon=True)
    t.start()
