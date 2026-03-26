# Common errors

## During package load

Errors that may occur when executing `import iesopt`.

- _"Exception: no version of Julia is compatible with =x.y.z - perhaps you need to update JuliaUp"_: Open a terminal and execute `juliaup update`. If it still reports the same error afterwards, checkout the specific version that it fails to find, and manually install that.

- Julia Version Confilict on Windows:
  ```console
  Exception: 'julia' compat entries have empty intersection:
  - '=1.12.5' at ...\\.venv\lib\site-packages\iesopt\juliapkg.json
  - '1.0.0 - 1.11' at ...\\.venv\lib\site-packages\juliacall\juliapkg.json (OpenSSL_jll)
  ```
  Try installing Python via `uv` instead of the standard [Python Installer](https://www.python.org/downloads/release/pymanager-260/); this can be done, e.g., by running `uv python install 3.14 --force`. Currently, versions published directly by CPython come with an outdated `OpenSSL` version.
