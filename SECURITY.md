# Security Policy

## Supported Versions

This is a small non-commercial project; only the latest `main` is supported.

| Version | Supported |
|---------|-----------|
| latest `main` | ✅ |

## Reporting a Vulnerability

Please report security issues **privately** — do **not** open a public issue:

- Preferred: GitHub → **Security** tab → *Report a vulnerability* (private advisory).
- Or email the maintainer: **adina.abylova@gmail.com**.

**Response:** acknowledgement within 14 days; fixes are best-effort (hobby project).

The app runs locally on the public Olist dataset — no network service, no auth, no user
data — so the realistic surface is dependency supply-chain. Dependencies are pinned in
`requirements.txt` / `requirements-dev.txt`.
