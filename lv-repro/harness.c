/*
 * dlopen harness for reproducing flet-dev/flet#4543
 * ("library load disallowed by system policy" when a hardened/sandboxed
 * macOS app loads pip-wheel Python C-extensions).
 *
 * The same binary is re-signed between matrix rows:
 *   codesign -f -s - harness                                    -> baseline
 *   codesign -f -s - -o runtime harness                         -> library validation ON
 *   codesign -f -s - -o runtime --entitlements disable-lv.plist -> LV disabled
 */
#include <dlfcn.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s <absolute-path-to-lib>\n", argv[0]); return 2; }
    void *h = dlopen(argv[1], RTLD_NOW);
    if (!h) { fprintf(stderr, "DLOPEN_FAIL: %s\n", dlerror()); return 1; }
    printf("DLOPEN_OK: %s\n", argv[1]);
    return 0;
}
