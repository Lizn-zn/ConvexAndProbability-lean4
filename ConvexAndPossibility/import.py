import os

def find_lean_files(root):
    lean_files = []
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith('.lean'):
                lean_files.append(os.path.join(dirpath, filename))
    return lean_files

def to_import_path(filepath):
    if filepath.startswith('./'):
        filepath = filepath[2:]
    if filepath.endswith('.lean'):
        filepath = filepath[:-5]
    return 'import ' + filepath.replace('/', '.')

def main():
    root = 'ConvexAndPossibility'
    lean_files = find_lean_files(root)
    lean_files = [f for f in lean_files]
    import_lines = [to_import_path(f) for f in sorted(lean_files)]
    for line in import_lines:
        print(line)

if __name__ == '__main__':
    main()
