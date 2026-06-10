#!/usr/bin/env bash
set -euo pipefail

packet_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
html="$packet_dir/packet.html"
pdf="$packet_dir/finite_directional_observer_review_packet.pdf"
dump="${TMPDIR:-/tmp}/harlow_review_packet_layout_dump.html"

find_chrome() {
  if [[ -n "${CHROME_BIN:-}" && -x "${CHROME_BIN}" ]]; then
    printf '%s\n' "$CHROME_BIN"
    return 0
  fi

  local candidate
  for candidate in \
    "$HOME"/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell \
    "$HOME"/.cache/ms-playwright/chromium-*/chrome-linux64/chrome \
    /usr/bin/chromium /usr/bin/chromium-browser /usr/bin/google-chrome; do
    if [[ -x "$candidate" ]]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done
  return 1
}

if [[ ! -f "$html" ]]; then
  printf 'Missing packet source: %s\n' "$html" >&2
  exit 1
fi

if ! chrome="$(find_chrome)"; then
  cat >&2 <<'EOF'
No Chromium executable found. Install Playwright's headless runtime with:

  npx --yes --package @playwright/cli playwright install chromium-headless-shell

Then re-run this script, setting CHROME_BIN if the runtime is not in the
standard Playwright cache.
EOF
  exit 1
fi

url="file://$html"

"$chrome" \
  --headless \
  --no-sandbox \
  --disable-gpu \
  --disable-dev-shm-usage \
  --allow-file-access-from-files \
  --virtual-time-budget=2000 \
  --dump-dom \
  "$url" > "$dump"

if rg -q 'data-overflow="true"' "$dump"; then
  printf 'Layout overflow detected:\n' >&2
  rg -o 'data-page="[^"]+"[^>]*data-overflow="true"[^>]*' "$dump" >&2 || true
  exit 1
fi

"$chrome" \
  --headless \
  --no-sandbox \
  --disable-gpu \
  --disable-dev-shm-usage \
  --allow-file-access-from-files \
  --virtual-time-budget=2000 \
  --no-pdf-header-footer \
  --print-to-pdf="$pdf" \
  "$url"

printf 'Built %s\n' "$pdf"
