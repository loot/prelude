# About

This repository holds the masterlist prelude, a metadata file that is used to supply common metadata to all masterlists.

See [CONTRIBUTING.md](CONTRIBUTING.md) for information on how to contribute to the prelude.

### Synchronising Weblate translations

The `translations` directory holds files that are read and written by [Weblate](https://hosted.weblate.org/projects/loot/prelude/). There are a couple of scripts that can be used to keep them in sync with `prelude.yaml`.

To use the scripts, first install their dependencies in a virtual environment. On Windows, make sure Python 3 is installed, then run:

```
py -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

To regenerate the files in the `translations` directory from `prelude.yaml`, run:

```
py scripts/export-translations.py
```

It's also possible to overwrite the message text in `prelude.yaml` using the contents of the `translations` directory:

```
py scripts/import-translations.py
```

The scripts make assumptions about the formatting and layout of entries in `prelude.yaml`, so it's worth double-checking their changes.

Change that doesn't modify any relevant files.
