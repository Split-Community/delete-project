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
    })


workspace = client.workspaces.find(projectName)

environments = client.environments.list(workspace.id)

# delete environment level data
for environment in environments:
    splitDefs = client.split_definitions.list(environment.id, workspace.id)
    print(f"Deleting splits for environment: {environment.name}")
    for splitDef in splitDefs:
        client.splits.remove_from_environment(splitDef.name, environment.id, '', '', workspace.id)

    segmentDefs = client.segment_definitions.list(environment.id, workspace.id)
    print(f"Deleting segments for environment: {environment.name}")
    for segDef in segmentDefs:
        segDef.import_keys_from_json(True, {'keys':[]})
        client.segments.remove_from_environment(segDef.name, environment.id)

    rbsDefs = client.rule_based_segment_definitions.list(environment.id, workspace.id)
    print(f"Deleting rule based segments for environment: {environment.name}")
    for rbsDef in rbsDefs:
        client.rule_based_segments.remove_from_environment(rbsDef.name, environment.id)
    
    largeSegmentDefs = client.large_segment_definitions.list(environment.id, workspace.id)
    print(f"Deleting large segments for environment: {environment.name}")
    for lsDef in largeSegmentDefs:
        client.rule_based_segments.remove_from_environment(lsDef.name, environment.id)


# delete project level data
for split in client.splits.list(workspace.id):
    print(f"Deleting split: {split.name}")
    client.splits.delete(split.name, workspace.id)

for segment in client.segments.list(workspace.id):
    print(f"Deleting segment: {segment.name}")
    client.segments.delete(segment.name, workspace.id)

for rbs in client.rule_based_segments.list(workspace.id):
    print(f"Deleting rule based segment: {rbs.name}")
    client.rule_based_segments.delete(rbs.name, workspace.id)

for ls in client.large_segments.list(workspace.id):
    print(f"Deleting large segment: {ls.name}")
    client.large_segments.delete(ls.name, workspace.id)


# delete traffic types
for trafficType in client.traffic_types.list(workspace.id):
    print(f"Deleting traffic type: {trafficType.name}")
    client.traffic_types.delete(trafficType.id)


# delete flag Sets
for flagSet in client.flag_sets.list(workspace.id):
    print(f"Deleting flag set: {flagSet.name}")
    client.flag_sets.delete(flagSet.id)

# delete environments
for environment in environments:
    # delete api keys
    sdkKeys = environmentNameToSDKKeyMap.get(environment.name)
    if sdkKeys:
        for key in sdkKeys:
            client.apikeys.delete_apikey(key)
    
    print(f"Deleting environment: {environment.name}")
    client.environments.delete(environment.id, workspace.id )

# delete workspace
print(f"Deleting workspace: {workspace.name}")
client.workspaces.delete(workspace.id)
