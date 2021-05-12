def group_by_owners(files):
    new_files = {}
    value_list = []
    for key, value in files.items():
        if value not in value_list:
            value_list.append(value)
        new_files.setdefault(value, []).append(key)
    return new_files


files = {
    'Input.txt': 'Randy',
    'Code.py': 'Stan',
    'Output.txt': 'Randy'
}
print(group_by_owners(files))
# should print {'Randy': ['Input.txt', 'Output.txt'], 'Stan': ['Code.py']}
