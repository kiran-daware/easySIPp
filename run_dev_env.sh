#!/bin/sh
set -eu

for cmd in python3 curl sha256sum; do
    command -v "$cmd" >/dev/null 2>&1 || {
        echo "Error: '$cmd' is required. Try: sudo apt-get install -y python3 python3-venv python3-pip curl coreutils libcap2-bin" >&2
        exit 1
    }
done

APP_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
VENV="$APP_DIR/venv"
SIPP_URL=${SIPP_URL:-"https://github.com/SIPp/sipp/releases/download/v3.7.3/sipp"}
SIPP_BIN="$APP_DIR/easySIPp/sipp"
HOST=${HOST:-127.0.0.1}
PORT=${PORT:-8080}
mkdir -p "$APP_DIR/easySIPp/xml/tmp"

# (Re)install deps when venv is missing or requirements.txt changed
REQ_HASH=$(sha256sum "$APP_DIR/requirements.txt" | cut -d' ' -f1)
STAMP="$VENV/.req_hash"
if [ ! -x "$VENV/bin/python" ] || [ "$(cat "$STAMP" 2>/dev/null)" != "$REQ_HASH" ]; then
    echo "Setting up virtualenv..."
    [ -x "$VENV/bin/python" ] || python3 -m venv "$VENV"
    "$VENV/bin/python" -m pip install --upgrade pip
    "$VENV/bin/pip" install -r "$APP_DIR/requirements.txt"
    echo "$REQ_HASH" > "$STAMP"
fi

# Download SIPp atomically (temp file, then move into place)
if [ ! -x "$SIPP_BIN" ]; then
    echo "Downloading SIPp..."
    TMP=$(mktemp "$APP_DIR/easySIPp/sipp.XXXXXX")
    trap 'rm -f "$TMP"' EXIT
    curl --fail --location --retry 3 --output "$TMP" "$SIPP_URL"
    chmod 755 "$TMP"
    mv "$TMP" "$SIPP_BIN"
    trap - EXIT
fi

# Grant raw-socket capability only if not already present
if command -v setcap >/dev/null 2>&1 && command -v getcap >/dev/null 2>&1; then
    if ! getcap "$SIPP_BIN" | grep -q cap_net_raw; then
        sudo setcap cap_net_raw+eip "$SIPP_BIN" ||
            echo "Warning: setcap failed on $SIPP_BIN; some SIPp modes may need sudo" >&2
    fi
fi

export DJANGO_ENV="development"

"$VENV/bin/python" "$APP_DIR/manage.py" migrate --noinput
exec "$VENV/bin/python" -m uvicorn easySIPp_project.asgi:application --host "$HOST" --port "$PORT"