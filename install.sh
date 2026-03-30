#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# matcha (mmt-attacker) Installer
# Usage: curl -sSL https://raw.githubusercontent.com/Montimage/mmt-attacker/main/install.sh | bash
#   or:  wget -qO- https://raw.githubusercontent.com/Montimage/mmt-attacker/main/install.sh | bash
# ============================================================================

TOOL_NAME="matcha"
REPO_OWNER="Montimage"
REPO_NAME="mmt-attacker"
DEFAULT_BRANCH="main"
MIN_PYTHON_MAJOR=3
MIN_PYTHON_MINOR=8

# --- Color Output ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info()  { printf "${BLUE}[INFO]${NC}  %s\n" "$*"; }
ok()    { printf "${GREEN}[ OK ]${NC}  %s\n" "$*"; }
warn()  { printf "${YELLOW}[WARN]${NC}  %s\n" "$*"; }
err()   { printf "${RED}[ERR ]${NC}  %s\n" "$*" >&2; }
die()   { err "$@"; exit 1; }

# --- OS / Arch Detection ---
detect_os() {
    local os
    os="$(uname -s | tr '[:upper:]' '[:lower:]')"
    case "$os" in
        linux*)  echo "linux" ;;
        darwin*) echo "macos" ;;
        *)       die "Unsupported operating system: $os. matcha requires Linux or macOS." ;;
    esac
}

detect_package_manager() {
    if command -v apt-get &>/dev/null; then echo "apt"
    elif command -v dnf &>/dev/null;    then echo "dnf"
    elif command -v yum &>/dev/null;    then echo "yum"
    elif command -v pacman &>/dev/null; then echo "pacman"
    elif command -v zypper &>/dev/null; then echo "zypper"
    elif command -v brew &>/dev/null;   then echo "brew"
    else echo "unknown"
    fi
}

need_sudo() {
    if [ "$(id -u)" -ne 0 ]; then
        if command -v sudo &>/dev/null; then
            echo "sudo"
        else
            die "Root privileges are required to install system dependencies. Please run as root or install sudo."
        fi
    else
        echo ""
    fi
}

# --- Python Check ---
find_python() {
    local py=""
    for candidate in python3 python python3.12 python3.11 python3.10 python3.9 python3.8; do
        if command -v "$candidate" &>/dev/null; then
            local ver
            ver="$("$candidate" -c 'import sys; print(sys.version_info.major, sys.version_info.minor)')"
            local major minor
            read -r major minor <<< "$ver"
            if [ "$major" -ge "$MIN_PYTHON_MAJOR" ] && [ "$minor" -ge "$MIN_PYTHON_MINOR" ]; then
                echo "$candidate"
                return
            fi
        fi
    done
    die "Python ${MIN_PYTHON_MAJOR}.${MIN_PYTHON_MINOR}+ is required but was not found. Please install it first."
}

# --- System Dependencies (for scapy / raw sockets) ---
install_system_deps() {
    local pm="$1"
    local sudo_cmd="$2"

    info "Installing system dependencies (libpcap)..."
    case "$pm" in
        apt)
            $sudo_cmd apt-get update -qq
            $sudo_cmd apt-get install -y -qq libpcap-dev python3-pip python3-dev
            ;;
        dnf)
            $sudo_cmd dnf install -y -q libpcap-devel python3-pip python3-devel
            ;;
        yum)
            $sudo_cmd yum install -y -q libpcap-devel python3-pip python3-devel
            ;;
        pacman)
            $sudo_cmd pacman -Sy --noconfirm libpcap python-pip
            ;;
        zypper)
            $sudo_cmd zypper install -y libpcap-devel python3-pip python3-devel
            ;;
        brew)
            # libpcap is provided by macOS SDK; brew formula exists but usually not needed
            if ! brew list libpcap &>/dev/null 2>&1; then
                brew install libpcap 2>/dev/null || true
            fi
            ;;
        *)
            warn "Unknown package manager — skipping system dependency installation."
            warn "If the install fails, manually install: libpcap-dev (or equivalent)"
            ;;
    esac
    ok "System dependencies ready"
}

# --- pip Bootstrap ---
ensure_pip() {
    local python="$1"
    if ! "$python" -m pip --version &>/dev/null 2>&1; then
        info "pip not found — bootstrapping via ensurepip..."
        "$python" -m ensurepip --upgrade 2>/dev/null || \
            die "Could not bootstrap pip. Please install pip for $python manually."
    fi
}

# --- Main Installation ---
install_matcha() {
    local python="$1"

    info "Installing ${TOOL_NAME} from GitHub (${REPO_OWNER}/${REPO_NAME})..."

    # Upgrade pip first to avoid legacy resolver issues
    "$python" -m pip install --upgrade pip --quiet

    # Install the package directly from GitHub
    "$python" -m pip install \
        --quiet \
        "git+https://github.com/${REPO_OWNER}/${REPO_NAME}.git@${DEFAULT_BRANCH}#egg=${REPO_NAME}"

    ok "${TOOL_NAME} installed"
}

# --- Verification ---
verify_installation() {
    local python="$1"

    info "Verifying installation..."

    # The CLI entry point may be in ~/.local/bin (user install) or /usr/local/bin
    # Try direct command first, then locate via python -m
    if command -v "$TOOL_NAME" &>/dev/null; then
        local ver
        ver="$("$TOOL_NAME" --version 2>/dev/null || echo 'unknown')"
        ok "${TOOL_NAME} is available at $(command -v "$TOOL_NAME") (${ver})"
    else
        # Try finding it via the python environment
        local script_dir
        script_dir="$("$python" -c 'import sysconfig; print(sysconfig.get_path("scripts"))')"
        if [ -f "${script_dir}/${TOOL_NAME}" ]; then
            ok "${TOOL_NAME} installed at ${script_dir}/${TOOL_NAME}"
            warn "Add ${script_dir} to your PATH to use '${TOOL_NAME}' directly."
            warn "  echo 'export PATH=\"${script_dir}:\$PATH\"' >> ~/.bashrc && source ~/.bashrc"
        else
            die "${TOOL_NAME} installation could not be verified. Check pip output above for errors."
        fi
    fi
}

# --- Entry Point ---
main() {
    info "============================================"
    info "  Installing ${TOOL_NAME} (${REPO_OWNER}/${REPO_NAME})"
    info "============================================"

    local os pm sudo_cmd python
    os="$(detect_os)"
    pm="$(detect_package_manager)"
    sudo_cmd="$(need_sudo)"

    info "OS: ${os} | Package Manager: ${pm}"

    # Step 1: Install system deps (libpcap for scapy)
    if [ "$os" = "linux" ] || [ "$os" = "macos" ]; then
        install_system_deps "$pm" "$sudo_cmd"
    fi

    # Step 2: Locate Python 3.8+
    python="$(find_python)"
    ok "Using Python: ${python} ($("$python" --version))"

    # Step 3: Ensure pip
    ensure_pip "$python"

    # Step 4: Install matcha
    install_matcha "$python"

    # Step 5: Verify
    verify_installation "$python"

    info "============================================"
    ok "Installation complete!"
    info ""
    info "Get started:"
    info "  ${TOOL_NAME} --help         # show all commands"
    info "  ${TOOL_NAME} list           # list all available attacks"
    info ""
    warn "Note: executing attacks requires root/sudo privileges (raw sockets)."
    warn "  sudo ${TOOL_NAME} syn-flood --target-ip 192.168.1.1 --target-port 80"
    info "============================================"
}

main "$@"
