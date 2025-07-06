#!/usr/bin/env python3
import argparse, re, struct, base64, urllib.parse, sys

def extract_base_url(full_url: str) -> str:
    p = urllib.parse.urlparse(full_url)
    base = f"{p.scheme}://{p.hostname}"
    if p.port:
        base += f":{p.port}"
    # Pfad-Anteil entfernen, behalte nur Host (Kontextpfad kann nötig sein)
    return base

def extract_page_id(url: str) -> int:
    u = urllib.parse.unquote(url)
    m = re.search(r'/pages/(\d+)(?:/|$)|[?&]pageId=(\d+)', u)
    if not m:
        raise ValueError(f"Fehler: Keine pageId in URL gefunden: {url}")
    return int(m.group(1) or m.group(2))

def tiny_token(page_id: int) -> str:
    packed = struct.pack('<L', page_id)
    return base64.b64encode(packed, altchars=b'_-').rstrip(b'=').decode('ascii')

def make_tiny_link(base_url: str, full_url: str) -> str:
    pid = extract_page_id(full_url)
    token = tiny_token(pid)
    return base_url.rstrip('/') + '/x/' + token

def main():
    p = argparse.ArgumentParser(
        description="Erzeuge Tiny-Link aus Confluence-Full-URL (kein Token nötig).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    p.add_argument(
        "--base-url", "-b",
        help="Basis-URL deiner Confluence-Instanz (z. B. https://wisman.izus.uni-stuttgart.de)"
    )
    p.add_argument(
        "--full-url", "-u",
        required=True,
        help="Komplette Confluence-Seiten-URL"
    )
    args = p.parse_args()
    
    base = args.base_url or extract_base_url(args.full_url)
    try:
        tiny = make_tiny_link(base, args.full_url)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unbekannter Fehler: {e}", file=sys.stderr)
        sys.exit(2)

    print(tiny)
    sys.exit(0)

if __name__ == "__main__":
    main()