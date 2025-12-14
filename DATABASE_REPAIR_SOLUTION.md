# DocRAG Database Repair Solution

## Problem Summary

The user is experiencing a critical issue with DocRAG where:
- **ERROR**: `attempt to write a readonly database` (SQLite error code 1032)
- **Multiple conflicting processes**: Several `docrag.mcp_server` processes running simultaneously
- **MCP service disconnected**: DocRAG service shows "Not connected" in Kiro
- **Incomplete indexing**: Only 24 old documents indexed, new documentation not processed

## Root Causes Identified

1. **Database Permission Issues**: SQLite database files have become read-only
2. **Process Conflicts**: Multiple MCP server instances causing database locks
3. **File System Locks**: Database lock files (*.db-wal, *.db-shm) preventing access
4. **Working Directory Mismatch**: MCP server and CLI using different working directories

## Comprehensive Solution

### Step 1: Immediate Fix - Use New Database Repair Command

```bash
# New command specifically designed for this issue
docrag fix-database
```

This command will:
- **Kill conflicting processes** automatically
- **Remove database lock files** (*.db-wal, *.db-shm)
- **Fix file permissions** (chmod 755 for directories, 644 for files)
- **Detect and repair readonly database issues**
- **Offer to rebuild corrupted database** with user confirmation

### Step 2: Diagnose Issues

```bash
# Comprehensive health check
docrag doctor

# Debug MCP synchronization issues
docrag debug-mcp
```

### Step 3: Complete Recovery Process

```bash
# 1. Fix database issues
docrag fix-database

# 2. Rebuild index from scratch (if database was corrupted)
docrag index

# 3. Update MCP configuration to prevent future conflicts
docrag mcp-config --update --non-interactive

# 4. Verify everything works
docrag doctor
```

## New Features Added

### 1. `docrag fix-database` Command
- **Automatic process management**: Finds and kills conflicting MCP processes
- **Permission repair**: Fixes readonly database and directory permissions
- **Lock file cleanup**: Removes SQLite WAL and SHM lock files
- **Smart recovery**: Offers database rebuild only when necessary
- **Progress reporting**: Clear feedback on what's being fixed

### 2. `docrag debug-mcp` Command
- **Path synchronization check**: Verifies CLI and MCP use same working directory
- **Process detection**: Shows running MCP server processes
- **Configuration analysis**: Checks workspace vs user MCP configs
- **Document count comparison**: Compares CLI vs MCP database access

### 3. Enhanced `docrag doctor` Command
- **Database integrity checks**: Tests SQLite database accessibility
- **Permission validation**: Verifies file and directory permissions
- **Process conflict detection**: Identifies competing MCP processes
- **Synchronization verification**: Ensures CLI and MCP see same data

## Technical Implementation

### Database Repair System (`database_repair.py`)
```python
class DatabaseRepair:
    def diagnose_issues(self) -> Tuple[List[str], List[str]]
    def find_conflicting_processes(self) -> List[dict]
    def kill_conflicting_processes(self) -> bool
    def fix_readonly_database(self) -> bool
    def remove_lock_files(self) -> bool
    def comprehensive_repair(self) -> Tuple[List[str], List[str]]
```

### Process Management
- **Cross-platform support**: Uses `psutil` when available, falls back to `pgrep`/`pkill`
- **Graceful termination**: Attempts SIGTERM first, then SIGKILL if needed
- **Safety checks**: Only targets `docrag.mcp_server` processes

### Permission Repair
- **Directory permissions**: Sets 755 (rwxr-xr-x) for directories
- **File permissions**: Sets 644 (rw-r--r--) for database files
- **Recursive fixing**: Applies to all files in vectordb directory

## Prevention Measures

### 1. Working Directory Synchronization
The MCP configuration now explicitly sets the working directory:
```json
{
  "mcpServers": {
    "docrag": {
      "command": "python",
      "args": ["-m", "docrag.mcp_server"],
      "cwd": "/path/to/your/project",
      "env": {},
      "disabled": false
    }
  }
}
```

### 2. Process Management
- **Single instance enforcement**: New processes check for existing instances
- **Proper cleanup**: MCP server handles shutdown signals gracefully
- **Lock file management**: Automatic cleanup of stale lock files

### 3. Error Recovery
- **Automatic retry**: Commands retry operations after fixing permissions
- **User guidance**: Clear instructions for manual recovery if needed
- **Status verification**: Post-repair checks confirm issues are resolved

## Usage Instructions for User

### Immediate Recovery
```bash
# Navigate to your project directory
cd /path/to/your/project

# Run the comprehensive fix
docrag fix-database

# If database was rebuilt, reindex
docrag index

# Update MCP configuration
docrag mcp-config --update --non-interactive

# Restart Kiro IDE completely

# Verify everything works
docrag doctor
```

### Verification Steps
1. **Check process count**: `docrag debug-mcp` should show no conflicting processes
2. **Verify database access**: `docrag doctor` should show no critical issues
3. **Test MCP connection**: Kiro should show DocRAG as "Connected"
4. **Test search**: Try using `search_docs` tool in Kiro

## Expected Results

After running the fix:
- ✅ **Database writable**: No more "readonly database" errors
- ✅ **Single process**: Only one MCP server instance running
- ✅ **MCP connected**: DocRAG service shows "Connected" in Kiro
- ✅ **Full index**: All documentation files properly indexed
- ✅ **Synchronized access**: CLI and MCP see same document count

## Monitoring and Maintenance

### Regular Health Checks
```bash
# Weekly health check
docrag doctor

# Before important work sessions
docrag debug-mcp
```

### Signs of Issues
- MCP service shows "Not connected"
- Search results are outdated
- CLI and MCP show different document counts
- Database errors in logs

### Quick Recovery
```bash
# For minor issues
docrag fix-database

# For major corruption
rm -rf .docrag/vectordb && docrag index
```

This solution addresses all the reported issues and provides robust tools for both immediate recovery and ongoing maintenance.