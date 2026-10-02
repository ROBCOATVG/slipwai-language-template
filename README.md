# slipwai-language-template

slipwai 2.0 language addon: slipwai-language-template.

This is `toy`, and **it is not a real language.** It is the smallest package slipwai's conformance suite accepts: a
family and a backend called `toy`, the `none` target, the in-memory and Postgres event stores, every member of the
backend protocol answered with a placeholder, and a one-line placeholder snippet for every example marker a skill
carries. A project generated with it builds nothing — its Makefile targets only `echo` what a real language would
run. It exists to be copied: rename it, then replace each placeholder with your language's own answer while the suite
stays green.

## What is here

| Path | What it is |
|---|---|
| `language.json` | The catalog fragment: the package's `name` (its directory's), the `core` schema range it loads on, `order`, `family`, and each backend's `label`, `targets` and per-axis `options` |
| `VERSION`, `CHANGELOG.md`, `changelog.d/` | The package's own version, independent of slipwai's, held to the same arithmetic (`changelog.d/README.md`) |
| `slipwai_language_toy/` | The Python: `__init__.py` exports `LANGUAGE`, the family (`family.py`) and the backend (`backend.py`) answering the protocol, and the pruning rows (`prune_rows.py`) |
| `assets/languages/toy/app/` | The files a service's directory starts with |
| `assets/languages/toy/flags/` | The feature-flag reader a service gets under a target that deploys |
| `assets/languages/toy/examples/<skill>/<id>.md` | One snippet per `{{example: <skill>/<id>}}` marker in slipwai's skills |
| `assets/backing-services/toy/` | What each event-store answer adds to a service (`write_side_files`, `read_side_files`) |
| `tests/test_conformance.py` | The conformance suite, as a `unittest` case over this package |

What every member means and the shape its answer takes is slipwai's backend-protocol contract, and how a package sits
on disk, what `language.json` holds and what is refused is its language-package contract. Both are in the slipwai
repository, under `specs/001-slipwai-2-language-addons/contracts/` (`backend-protocol.md`, `language-package.md`).

## Starting a language from it

1. Copy the repository into a directory of its own named for your language, `languages/mylang`: the package's
   directory name is its `name`, and the suite finds the package by it in the directory above.
2. Replace every `toy` the files hold with `mylang` (`git grep -l toy | xargs sed -i 's/toy/mylang/g'`), and rename
   the three things named for it: the Python package `slipwai_language_toy/` (`slipwai_language_mylang/`; a dash in
   the name becomes `_`), `assets/languages/toy/` and `assets/backing-services/toy/`. That covers `language.json`'s
   `name`, `family` and backend key, the `Family` and `Backend` in `LANGUAGE`, the paths into `assets/` and
   `package` in `tests/test_conformance.py`.
3. Run the suite (below). It passes on the rename alone; from there, replace each placeholder with your language's
   answer, one at a time, and let the suite name what is still missing.
4. Say what your package ships in a fragment under `changelog.d/`. `VERSION` stays `1.0.0.dev0` until the first
   release.

## Running the suite from this repository

The suite ships in slipwai itself as `slipwai.conformance`, so the only thing this repository needs is slipwai —
**2.0 or newer**, the first with the suite. Hold it to that floor, so an older slipwai is a resolver error rather than
a missing module:

```sh
pip install --pre "slipwai>=2.0"                  # --pre while 2.0 is a snapshot: a .dev version is skipped without it
pip install ./slipwai-<version>-py3-none-any.whl  # or a wheel `make wheel` built from a slipwai checkout
uv run --prerelease allow --with "slipwai>=2.0" python -m slipwai.conformance .. toy   # the same, through uv
```

Then, from the package's directory (`languages/toy` here, `languages/mylang` once renamed), either:

```sh
python -m slipwai.conformance .. toy                              # one line per check, then passed or failed
python -m unittest discover -s tests -p test_conformance.py       # one test per check
```

The first is the command line: `python -m slipwai.conformance <language-dir> <package>`, where the language directory
is the one holding the package — here `languages`, the directory above, which should hold nothing else: every
directory in it is read as a package, and one that is not is refused in a line of its own. It prints `ok`, `FAILED` with each finding under it, or
`not run` and why, for each of `protocol`, `markers`, `profiles`, `targets`, `prune rows` and `version`, and exits 0
when the package passed, 1 when it failed, 2 on a usage error and 3 when the suite itself could not run.

The second is `tests/test_conformance.py`, a subclass of `slipwai.conformance.ConformanceCase` that names its
`language_dir` (the directory this package sits in, `Path(__file__).resolve().parents[2]`) and its `package`.
`unittest` discovers it like any test module; each check is one test, failing with the same findings. Either way the
checks run in a fresh interpreter whose language directory is the one named, so whatever languages your own machine
has installed are never the ones checked.

## Trying it in a project

slipwai reads its languages from `~/.slipwai/languages`, or from the one directory `SLIPWAI_LANGUAGES` names instead.
Fill it from this checkout, which needs no network and no language index:

```sh
slipwai language install .          # copies this package to ~/.slipwai/languages/toy, under its name
slipwai list                        # toy, with its version
slipwai generate demo --backend toy --frontend none --skip-checks --output /tmp/toy-demo
```

Install again after each change: the installed copy is a copy. Or point slipwai at the directory holding your clone
for one command, `SLIPWAI_LANGUAGES=.. slipwai list`, and nothing is copied; `SLIPWAI_LANGUAGES` replaces
`~/.slipwai/languages` whole, so only what that directory holds is loaded. The suite run above is against that same
kind of directory, so the copy in `~/.slipwai/languages` can be checked too:
`python -m slipwai.conformance ~/.slipwai/languages toy`.

## The import surface

A package's Python may import only the slipwai modules listed under *The core modules a package imports* in
`contracts/language-package.md`, and nothing else of core. That list is the part of slipwai a package is built
against; a package that imports beyond it can break on any slipwai release. Your `tests/` are outside the rule.

The check that holds it is slipwai's own `make check-structure`, which reads the list from that page and refuses, by
file, line and module, any import outside it under `languages/*/slipwai_language_*/`. It runs in a slipwai checkout,
not from this repository: put a copy of the package there and run it.

```sh
git clone <slipwai's repository> slipwai && cd slipwai
git submodule update --init                          # the first-party packages the check reads beside yours
cp -r ../mylang languages/mylang                     # outside the copy, nothing of slipwai changes
python3 scripts/check-structure.py                   # what `make check-structure` runs
rm -rf languages/mylang
```

The template's own Python imports only `slipwai.registry`, `slipwai.assets`, `slipwai.backends`, `slipwai.selection`,
`slipwai.services`, `slipwai.tooling`, `slipwai.project.backing_services`, `slipwai.project.flags` and
`slipwai.project.renovate`, all on the list.
