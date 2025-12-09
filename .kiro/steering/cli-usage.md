# CLI Usage Rules for Agents

When working with DocRAG Kit CLI commands, follow these rules to avoid interactive prompts:

## Non-Interactive Flags

Always use non-interactive flags when running CLI commands programmatically:

### `docrag init`
```bash
# Use --non-interactive flag to skip prompts
docrag init --non-interactive --template general

# Available templates: general, symfony, ios
```

### `docrag index`
```bash
# Use --force to skip confirmation prompts
docrag index --force
```

### `docrag reindex`
```bash
# Use --force to skip confirmation prompts
docrag reindex --force
```

### `docrag config`
```bash
# View config (no interaction needed)
docrag config

# DO NOT use --edit flag in automated contexts
# It opens an interactive editor
```

### `docrag mcp-config`
```bash
# Safe to use - no interaction needed
docrag mcp-config
```

## Summary

- **Always add `--non-interactive` to `docrag init`**
- **Always add `--force` to `docrag index` and `docrag reindex`**
- **Never use `docrag config --edit` in automated contexts**
- **Use `docrag config` (without --edit) to view configuration**
