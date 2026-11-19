@echo off
setlocal
echo ====================================================================
echo  SynapseOS - Booting in QEMU via WSLg
echo ====================================================================
wsl bash -c "cd /mnt/c/Users/djiby/.gemini/antigravity/scratch/SynapseOS && chmod +x scripts/boot_qemu.sh && ./scripts/boot_qemu.sh"
