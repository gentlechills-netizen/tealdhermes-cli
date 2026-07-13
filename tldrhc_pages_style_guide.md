# tldrhc — Style guide

tldrhc pages follow the [official tldr format](https://github.com/tldr-pages/tldr/blob/main/contributing-guides/style-guide.md)
with Hermes CLI-specific conventions.

## Template

```markdown
# hc-command

> Short description (imperative, one line).
> Syntax: hermes command [options]

- Do something specific:

`hermes command {{arg}}`

- Do something else:

`hermes command --option`
```

## Sections (in order)

### Title — `# hc-command`
One line. Matches the page filename prefix.

### Description — `> text`
Description from descriptions.yaml (`long` field, falls back to `short`).
One line, imperative, no punctuation at end.

### Syntax — `> Syntax: hermes command [options]`
Always present. Shows the base command syntax.

### Examples

#### Format
Each example is a pair: description line + command line, separated by a blank line.

```markdown
- Do something specific:

`hermes command {{arg}}`

- Next example:

`hermes command --option {{value}}`
```

#### Rules
- **Imperative mood.** "Back up Hermes configuration:" not "Backs up Hermes configuration" / "Backing up Hermes configuration".
- **At most 5 examples.**
- **Use backticks** for the command.
- **No bold, no italics** in descriptions.
- **No sudo** — Hermes commands don't need it.

### Placeholders
Use `{{placeholder}}` syntax for values the user must provide.

| Pattern | Example |
|---------|---------|
| Single value | `{{name}}`, `{{number}}` |
| Path/file | `{{path/to/directory}}` |
| Mutually exclusive | `{{on/off}}`, `{{here/global}}` |
| Descriptive | `{{what to learn}}`, `{{authentication topic}}` |

Only use placeholders when the user MUST replace the value.
If the example works as-is (e.g. `hermes backup --quick`), keep it literal.

## Editing examples
Examples live in `examples.yaml`. Each entry:

```yaml
command-name:
  - desc: "Do something:"
    cmd: "hermes command {{arg}}"
  - desc: "Do something else:"
    cmd: "hermes command --option"
```

Add, edit, or remove entries here, then run `./update.sh`.
