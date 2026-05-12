## pure ai code but amazing tool 

# TOTP Authenticator

A lightweight, standalone TOTP (Time-based One-Time Password) generator built with Python and tkinter. Syncs with network time for accuracy.

## Features

- **Real-time code generation** — 6-digit TOTP codes that refresh every 30 seconds
- **Network time sync** — Automatically corrects for local clock drift using Google's servers
- **One-click copy** — Click the code or press the button to copy to clipboard
- **Visual countdown** — Timer turns red when the code is about to expire
- **Zero dependencies** — Uses only Python's standard library

## Requirements

| Dependency | Install |
|------------|---------|
| Python 3.6+ | [python.org](https://python.org) |
| tkinter | Included (Linux: `sudo apt install python3-tk`) |
| nuitka | `pip install -r requirements.txt` |

```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
   ```bash
   python totp.txt
   ```

2. Enter your TOTP secret key (Base32 format, spaces optional)

3. The 6-digit code generates automatically — click it to copy

## Getting Your Secret Key

Most services provide this when setting up 2FA:
- Look for "Can't scan?" or "Manual entry" during setup
- Copy the provided key (usually 16–32 characters, A–Z and 2–7)

## How It Works

- Implements [RFC 6238](https://datatracker.ietf.org/doc/html/rfc6238) TOTP standard
- HMAC-SHA1 with 30-second time steps
- Syncs local time with Google's server to prevent drift-related failures

## Building

To compile to a standalone executable (optional):

```bash
python -m nuitka --standalone --onefile --windows-disable-console totp.txt
```

## License

MIT
