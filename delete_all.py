# script to delete all items in a fme project
from splitapiclient.main import get_client

projectName = '<Project-Name>'

thisApiKey = '<your-api-key>' # the api key you're using for this script

# need this to be able to delete environments
environmentNameToSDKKeyMap = {
    'test': ['key1', 'key2'],
    'sit': ['key3', 'key4'],
#...
}
# you will have to update this when using in a migrated harness environment
client = get_client({
    'apikey': thisApiKey,
    #'harness_token': 'your-harness-token',
    #'harness_mode': True
    })


dryRun = False




workspace = client.workspaces.find(projectName)

environments = client.environments.list(workspace.id)

# delete environment level data
for environment in environments:
    splitDefs = client.split_definitions.list(environment.id, workspace.id)
    print(f"Deleting splits for environment: {environment.name}")
    for splitDef in splitDefs:
        if not dryRun:
            client.splits.remove_from_environment(splitDef.name, environment.id, '', '', workspace.id)

    segmentDefs = client.segment_definitions.list(environment.id, workspace.id)
    print(f"Deleting segments for environment: {environment.name}")
    for segDef in segmentDefs:
        if not dryRun:
            segDef.import_keys_from_json(True, {'keys':[]})
            client.segments.remove_from_environment(segDef.name, environment.id)

    rbsDefs = client.rule_based_segment_definitions.list(environment.id, workspace.id)
    print(f"Deleting rule based segments for environment: {environment.name}")
    for rbsDef in rbsDefs:
        if not dryRun:
            client.rule_based_segments.remove_from_environment(rbsDef.name, environment.id)
    
    largeSegmentDefs = client.large_segment_definitions.list(environment.id, workspace.id)
    print(f"Deleting large segments for environment: {environment.name}")
    for lsDef in largeSegmentDefs:
        if not dryRun:
            client.rule_based_segments.remove_from_environment(lsDef.name, environment.id)


# delete project level data
for split in client.splits.list(workspace.id):
    print(f"Deleting split: {split.name}")
    if not dryRun:
        client.splits.delete(split.name, workspace.id)

for segment in client.segments.list(workspace.id):
    print(f"Deleting segment: {segment.name}")
    if not dryRun:
        client.segments.delete(segment.name, workspace.id)

for rbs in client.rule_based_segments.list(workspace.id):
    print(f"Deleting rule based segment: {rbs.name}")
    if not dryRun:
        client.rule_based_segments.delete(rbs.name, workspace.id)

for ls in client.large_segments.list(workspace.id):
    print(f"Deleting large segment: {ls.name}")
    if not dryRun:
        client.large_segments.delete(ls.name, workspace.id)


# delete traffic types
for trafficType in client.traffic_types.list(workspace.id):
    print(f"Deleting traffic type: {trafficType.name}")
    if not dryRun:
        client.traffic_types.delete(trafficType.id)


# delete flag Sets
for flagSet in client.flag_sets.list(workspace.id):
    print(f"Deleting flag set: {flagSet.name}")
    if not dryRun:
        client.flag_sets.delete(flagSet.id)

# delete environments
for environment in environments:
    # delete api keys
    sdkKeys = environmentNameToSDKKeyMap.get(environment.name)
    if sdkKeys:
        for key in sdkKeys:
            if not dryRun:
                client.apikeys.delete_apikey(key)
    
    print(f"Deleting environment: {environment.name}")
    if not dryRun:
        client.environments.delete(environment.id, workspace.id )

# delete workspace
# when using a migrated environment (eg accessing from app.harness.io) this will no longer be possible - you'll have to delete either using the harness api or manually
print(f"Deleting workspace: {workspace.name}")
if not dryRun:
    client.workspaces.delete(workspace.id)
