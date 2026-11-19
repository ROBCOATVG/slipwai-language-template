MINOR

**`toy-plain` answers both write models, so the template passes slipwai's current conformance suite again.** A
project is now asked per service whether its truth is its log (`write-model: events`) or its current state
(`state`), and a language answers both. `write_side_files` and `read_side_files` carry a `state` block beside their
feature rows — the repository's placeholder adapters for `memory` and `postgres`, the versioned state table's
migration, and a read-tables placeholder in place of the checkpoint store — and `event_model_paths` answers
`repository`, the port a state-stored service loads and saves through. `language.json` offers `write-model: events,
state` and names the store axis `persistence` (it was `event-store`); `event_store_directory` is answered under its new
name, `persistence_directory`; and the prune rows own the new Postgres files. The template's CI proves it against
`main` of `ROBCOATVG/slipwai` again, as it did before it was pinned. The template is now the same as the toy package
slipwai's own suite tests against (`packages/toy/` in the keel).

**Catch-up.** A package made from an earlier copy of the template fails `profiles` against current slipwai with one
line per store it offers (`write_side_files answers nothing for it on the state rung`) and one for `event_model_paths`
(`with no repository`). Add a `state` block to both side layouts with your language's repository port and an adapter
per store you offer, add a `repository` key to `event_model_paths`, answer `persistence_directory` in place of
`event_store_directory`, offer `write-model` and rename `event-store` to `persistence` in `language.json`, add the new
Postgres files to your prune rows, and move your CI's `uses:` and `keel:` back to `@main` if you pinned them.
`backend.py` here shows each change in place.
