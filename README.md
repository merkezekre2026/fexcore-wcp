# fexcore-wcp

Automated FEXCore `.wcp` packages for **Winlator Bionic** forks (CMod, Ludashi, GameNative, and compatible builds).

This repository tracks upstream [FEX-Emu/FEX](https://github.com/FEX-Emu/FEX), cross-compiles the ARM64EC and WOW64 DLLs with `llvm-mingw`, and publishes installable Winlator component packages.

## What you get

Each release contains a single `.wcp` archive with:

- `profile.json` manifest (`type: FEXCore`)
- `system32/libarm64ecfex.dll`
- `system32/libwow64fex.dll`

## Install manually

1. Download the latest `FEXCore-*.wcp` from [Releases](https://github.com/merkezekre2026/fexcore-wcp/releases).
2. Open your Winlator Bionic fork.
3. Go to **Settings -> Install Content**.
4. Select the downloaded `.wcp` file.
5. Choose the new FEXCore component when creating or editing a container.

## Install via Downloadable Content URL

1. Open Winlator Bionic.
2. Go to **Settings -> Downloadable Content URL**.
3. Paste this raw index URL:

```
https://raw.githubusercontent.com/merkezekre2026/fexcore-wcp/main/contents.json
```

4. Use the in-app content browser to download and install FEXCore builds.

## Build pipeline

GitHub Actions workflow: [`.github/workflows/build-fexcore-wcp.yml`](.github/workflows/build-fexcore-wcp.yml)

Triggers:

- Daily scheduled nightly build
- Manual `workflow_dispatch`

Steps:

1. Checkout upstream FEX with submodules
2. Install build dependencies and cached `llvm-mingw`
3. Build `arm64ec` and `aarch64` targets via [`scripts/build-fexcore.sh`](scripts/build-fexcore.sh)
4. Package with [`scripts/package-wcp.sh`](scripts/package-wcp.sh)
5. Publish a GitHub release asset
6. Update [`contents.json`](contents.json) for Winlator content discovery

## Local development

Scripts are lintable without a full FEX build:

```bash
bash -n scripts/build-fexcore.sh scripts/package-wcp.sh
python3 -m py_compile scripts/update-contents-json.py
python3 -m json.tool contents.json
```

To run a full local build you need FEX sources, `llvm-mingw`, `cmake`, `ninja`, and the same Ubuntu build packages used in CI.

## Upstream

- Source: https://github.com/FEX-Emu/FEX
- FEX is licensed separately from this packaging repository; see upstream for license details.

## License

This repository is licensed under the MIT License. See [LICENSE](LICENSE).
