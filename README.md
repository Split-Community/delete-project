# Split Project Cleanup Script

A utility script for completely removing all resources from a Split.io project workspace.

**NOTE: This will not work for migrated environments that are accessed from app.harness.io.** 
You will probably want to remove the project deletion code in that case.

## Overview

This script systematically deletes all resources associated with a specific workspace in Split.io, including:

1. **Environment-level resources**:
   - Splits
   - Segments (standard, rule-based, and large segments)

2. **Project-level resources**:
   - Splits
   - Segments (all types)
   - Traffic Types
   - Flag Sets

3. **Infrastructure**:
   - SDK Keys/API Keys
   - Environments
   - The workspace itself

## Prerequisites

- Python 3.x
- Split API Client library (`splitapiclient`)
- Admin-level API key with permissions to delete all resources

## Configuration

Before running the script, configure the following parameters:

1. `projectName`: Name of the workspace/project to delete
2. `thisApiKey`: Your Split admin API key
3. `environmentNameToSDKKeyMap`: Dictionary mapping environment names to their SDK keys

Example:
```python
projectName = 'YOUR_PROJECT_NAME'
thisApiKey = 'your-admin-api-key'
```

## Usage

Simply run the script with Python:

```bash
python delete_all.py
```

## Error Handling

The script may fail with the following errors:

- `'NoneType' object has no attribute 'id'`: This occurs if the workspace specified in `projectName` cannot be found. Verify the workspace name is correct and that your API key has access to it.
- API permission errors: Ensure your API key has sufficient permissions to delete all resource types.
- Because the API does not have access to metric configurations, the script will not delete them. This also means that traffic types will not be deleted if they are used in a metric and this will result in errors.

## Warning

**⚠️ USE WITH CAUTION ⚠️**

This script performs irreversible deletion of data. Once executed, all specified resources will be permanently removed. It is recommended to:

1. Verify the `projectName` carefully before running
2. Back up any important configuration before deletion
3. Use in non-production environments first to understand the behavior

## Dependencies

```
splitapiclient
```

Install using:

```bash
pip install splitapiclient
```
