#!/bin/bash
# Reproduces the enforcement layers behind flet-dev/flet#4543 without any
# Apple Developer account, using only ad-hoc code signing.
#
# Layer A — Library Validation (kernel/AMFI): main executable signed with the
#   hardened-runtime flag and no disable-library-validation entitlement may only
#   load Apple libraries or libraries signed with the SAME Team ID. pip-wheel
#   .so files are "adhoc,linker-signed" with TeamIdentifier=not set, so they
#   can never pass. Error: "... different Team IDs".
# Layer B — Gatekeeper/syspolicyd: a com.apple.quarantine xattr on the library
#   (e.g. acquired when a sandboxed app extracts files, as old serious_python
#   did) is rejected independently of Layer A. Error: "library load disallowed
#   by system policy" — the verbatim string from issue #4543.
#
# Exit code: number of failed assertions (0 = full repro confirmed).
set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
WORK="$(mktemp -d /tmp/lv-repro-4543.XXXXXX)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"

PASS=0; FAIL=0; SKIP=0
ROWS="| # | case | expected | result |
|---|------|----------|--------|"

run_case() { # <name> <expected-regex> <cmd...>
    local name="$1" expect="$2"; shift 2
    local out; out="$("$@" 2>&1)"
    if grep -qE "$expect" <<<"$out"; then
        PASS=$((PASS+1)); ROWS+=$'\n'"| $((PASS+FAIL)) | $name | \`$expect\` | ✅ PASS |"
        printf '✅ %s\n' "$name"
    else
        FAIL=$((FAIL+1)); ROWS+=$'\n'"| $((PASS+FAIL)) | $name | \`$expect\` | ❌ FAIL |"
        printf '❌ %s\n   expected /%s/\n   got: %s\n' "$name" "$expect" "$out"
    fi
}

echo "== environment =="
sw_vers
csrutil status || true
GK="$(spctl --status 2>&1 || true)"; echo "spctl: $GK"

echo; echo "== build fixtures =="
clang -o harness "$HERE/harness.c"
printf 'int toy_fn(void){return 42;}\n' > toy.c
clang -shared -o libtoy.dylib toy.c

python3 -m pip download pydantic-core --only-binary=:all: --dest wheels -q
unzip -q -o wheels/pydantic_core-*.whl -d wheel
EXT="$(find "$WORK/wheel" -name '*.so' | head -1)"
cp "$EXT" ext.so
echo "wheel extension: $(basename "$EXT")"
codesign -dvv ext.so 2>&1 | grep -E 'flags|TeamIdentifier'
codesign -dvv ext.so 2>&1 | grep -q 'TeamIdentifier=not set' \
    || { echo 'FATAL: wheel .so unexpectedly has a Team ID'; exit 1; }

TOY="$WORK/libtoy.dylib"; SO="$WORK/ext.so"

echo; echo "== Row 1: ad-hoc, NO hardened runtime (flet build macos default) =="
codesign -f -s - harness
run_case "plain + local dylib loads"            '^DLOPEN_OK'                    ./harness "$TOY"
# non-Python host: failure occurs at symbol binding => signature was ACCEPTED
run_case "plain + wheel .so passes signature"   'symbol not found'              ./harness "$SO"

echo; echo "== Row 2: ad-hoc + hardened runtime (TestFlight/App Store-equivalent LV) =="
codesign -f -s - -o runtime harness
run_case "hardened rejects local dylib (LV)"    'different Team IDs'            ./harness "$TOY"
run_case "hardened rejects wheel .so (LV)"      'different Team IDs'            ./harness "$SO"

echo; echo "== Row 3: hardened + disable-library-validation (control) =="
codesign -f -s - -o runtime --entitlements "$HERE/disable-lv.plist" harness
run_case "disable-LV loads local dylib"         '^DLOPEN_OK'                    ./harness "$TOY"
run_case "disable-LV re-admits wheel .so"       'symbol not found'              ./harness "$SO"

echo; echo "== Row 4: quarantined libraries (Gatekeeper layer — issue's verbatim error) =="
if [[ "$GK" == *enabled* ]]; then
    cp libtoy.dylib libtoy_q.dylib; cp ext.so ext_q.so
    xattr -w com.apple.quarantine "0083;00000000;flet-lv-test;" libtoy_q.dylib
    xattr -w com.apple.quarantine "0083;00000000;flet-lv-test;" ext_q.so
    # disable-LV signing still active from Row 3: quarantine blocks anyway
    run_case "quarantine beats disable-LV (toy)"      'disallowed by system policy' ./harness "$WORK/libtoy_q.dylib"
    run_case "quarantine beats disable-LV (wheel)"    'disallowed by system policy' ./harness "$WORK/ext_q.so"
    codesign -f -s - harness   # no hardened runtime at all
    run_case "quarantine blocks even plain process"   'disallowed by system policy' ./harness "$WORK/libtoy_q.dylib"
else
    SKIP=3; echo "Gatekeeper assessments disabled on this machine — skipping Row 4"
    ROWS+=$'\n'"| - | Row 4 (quarantine) | - | ⏭️ SKIPPED (spctl disabled) |"
fi

echo; echo "== summary: $PASS passed, $FAIL failed, $SKIP skipped =="
if [[ -n "${GITHUB_STEP_SUMMARY:-}" ]]; then
    { echo "## flet#4543 enforcement matrix — $PASS passed, $FAIL failed, $SKIP skipped"
      echo; echo "$ROWS"; } >> "$GITHUB_STEP_SUMMARY"
fi
exit "$FAIL"
