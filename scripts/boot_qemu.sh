#!/usr/bin/env bash
# ==============================================================================
# SynapseOS QEMU Boot Script
# Launches SynapseOS Lite or Full ISO in QEMU with SDL display & VNC fallback.
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
LITE_ISO="${PROJECT_ROOT}/iso/SynapseOS-Lite-x86_64.iso"
FULL_ISO="${PROJECT_ROOT}/output/SynapseOS-Debian12-Potato-x86_64.iso"

# Prefer Full ISO if present, otherwise Lite ISO
if [ -f "${FULL_ISO}" ]; then
    TARGET_ISO="${FULL_ISO}"
    RAM="4096"
    echo "[*] Booting Full LLM ISO: ${TARGET_ISO}"
elif [ -f "${LITE_ISO}" ]; then
    TARGET_ISO="${LITE_ISO}"
    RAM="2048"
    echo "[*] Booting Lite ISO: ${TARGET_ISO}"
else
    echo "[!] No ISO found in iso/ or output/. Run iso/decompress_iso.sh first!"
    exit 1
fi

KVM_ARGS=""
if [ -w /dev/kvm ]; then
    KVM_ARGS="-enable-kvm -cpu host"
else
    KVM_ARGS="-cpu max"
fi

echo "======================================================================"
echo " Starting SynapseOS in QEMU"
echo "  RAM:     ${RAM} MB"
echo "  CPUs:    2 Cores"
echo "  ISO:     ${TARGET_ISO}"
echo "  Display: SDL (Native Window) + VNC Server at 127.0.0.1:5900"
echo "======================================================================"

# Attempt with SDL + VNC first; fallback to headless VNC if no GUI environment
if qemu-system-x86_64 \
    ${KVM_ARGS} \
    -m "${RAM}" \
    -smp 2 \
    -cdrom "${TARGET_ISO}" \
    -vga std \
    -display sdl,gl=off \
    -vnc 0.0.0.0:0 \
    -net nic,model=virtio \
    -net user \
    -boot d; then
    exit 0
else
    echo "[!] SDL display unavailable. Falling back to headless VNC (localhost:5900)..."
    exec qemu-system-x86_64 \
        ${KVM_ARGS} \
        -m "${RAM}" \
        -smp 2 \
        -cdrom "${TARGET_ISO}" \
        -vga std \
        -display none \
        -vnc 0.0.0.0:0 \
        -net nic,model=virtio \
        -net user \
        -boot d
fi
