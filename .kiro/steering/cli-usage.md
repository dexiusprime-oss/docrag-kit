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
# No interaction needed - automatically overwrites existing database
docrag index
```

### `docrag reindex`
```bash
# No interaction needed - automatically rebuilds database
docrag reindex
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
# Use --non-interactive flag to skip confirmation prompts
docrag mcp-config --non-interactive

# Update existing MCP configuration with new tools
docrag mcp-config --update --non-interactive

# Note: This command now adds MCP config to workspace (.kiro/settings/mcp.json)
# instead of user config (~/.kiro/settings/mcp.json)
```

### `docrag update`
```bash
# Update existing projects with new features (no interaction needed)
docrag update
```

## Summary

- **Always add `--non-interactive` to `docrag init`**
- **Always add `--non-interactive` to `docrag mcp-config`**
- **Use `--update` flag with `docrag mcp-config` for existing projects**
- **`docrag index` - no flags needed, automatically overwrites**
- **`docrag reindex` - no flags needed, automatically rebuilds**
- **`docrag update` - no flags needed, updates existing projects**
- **Never use `docrag config --edit` in automated contexts**
- **Use `docrag config` (without --edit) to view configuration**
