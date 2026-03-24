---
name: clash-split-routing
description: Use when user needs to configure, fix, or regenerate ClashX Pro split routing. Triggers include Claude going through wrong proxy, subscription refresh losing VPS rules, or needing to update airport nodes while keeping VPS routing for Claude/Anthropic traffic.
---

# ClashX Pro Split Routing

## Overview

Split routing config combining airport subscription nodes with a personal VPS node. Claude/Anthropic traffic routes through VPS (US residential IP), everything else through airport proxies.

## Architecture

```
Claude/Anthropic --> VPS_Residential (VMess+WS) --> Internet
Other foreign   --> Airport nodes (SSR/SS)      --> Internet
China traffic   --> DIRECT
```

## Key Facts

| Item | Value |
|------|-------|
| Client | ClashX Pro (macOS, Clash Premium core) |
| VPS | 98.158.29.227, US residential IP |
| VPS protocol | VMess + WebSocket (port 443, path `/9cf8d774d173e066`) |
| VPS Xray also runs | VLESS + Reality (port 443) - NOT usable by ClashX Pro |
| Airport provider | DOGESS (dddoge.xyz / xn--l5xa.net) |
| Subscription URL | `https://dddoge.xyz/dli/jkDYzFc23sE1qvU?clash=1` |
| Config directory | `~/.config/clash/` |

## Why Split Config Exists

- ClashX Pro's subscription refresh overwrites manual edits
- ClashX Pro does NOT support `proxyConfigPreprocess.js` (no preprocess menu option)
- Solution: shell script generates a standalone combined config from local subscription + VPS node

## Regenerating the Config

```bash
~/.config/clash/update_split_config.sh
```

Then in ClashX Pro: menu icon > Config > select **custom_split**

### What the script does

1. Reads latest local `~/.config/clash/Clash_*.yaml` (subscription file)
2. Extracts all airport proxy nodes
3. Appends VPS VMess+WS node
4. Creates proxy groups: `Claude`, `Proxies`, `Auto`, `Domestic`, `Others`
5. Injects Claude rules at top: `anthropic.com` and `claude.ai` -> `Claude` group
6. Appends all original airport rules (emoji group names renamed)
7. Outputs `~/.config/clash/custom_split.yaml`

### When to regenerate

- After airport subscription refreshes (new `Clash_*.yaml` appears)
- After VPS config changes
- If nodes feel outdated or unavailable

## Important Files

| File | Purpose |
|------|---------|
| `~/.config/clash/custom_split.yaml` | Generated combined config (DO NOT edit manually) |
| `~/.config/clash/update_split_config.sh` | Generator script |
| `~/.config/clash/VPS_Residential.yaml` | Standalone VPS-only profile (for testing) |
| `~/.config/clash/Clash_*.yaml` | Airport subscription configs (auto-downloaded) |
| `~/vps_clash_config.yaml` | Reference VLESS config (not used by ClashX Pro) |

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Claude not going through VPS | Check ClashX Pro is using `custom_split` profile, not a `Clash_*` profile |
| "rules disappeared after restart" | ClashX Pro switched back to subscription profile; re-select `custom_split` |
| Script fails to extract proxies | Subscription format may have changed; check `Clash_*.yaml` structure |
| VPS node not connecting | Test with standalone `VPS_Residential` profile first to isolate issue |
| Subscription URL returns HTML (captcha) | Script falls back to latest local `Clash_*.yaml` automatically |

## Protocol Constraints

- ClashX Pro (Clash Premium) does **NOT** support VLESS or Reality
- VPS must expose VMess+WS for ClashX Pro compatibility
- The VPS also runs VLESS+Reality on same port for other clients (Clash Meta / mihomo)
- If switching to Clash Verge (mihomo core), can use VLESS+Reality directly instead of VMess+WS
