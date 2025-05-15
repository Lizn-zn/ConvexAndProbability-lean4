import os
import re

# 配置
ROOT_DIR = './'
MAX_LINES = 1000

# Lean keywords
LEAN_BLOCK_START = re.compile(r'^\s*(theorem|lemma|def|structure|class|inductive|instance|example)\b')

def find_lean_files(root):
    lean_files = []
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith('.lean'):
                lean_files.append(os.path.join(dirpath, filename))
    return lean_files

def split_lean_file(filepath, max_lines=MAX_LINES):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if len(lines) <= max_lines:
        return  

    import_lines = []
    for line in lines:
        if line.strip() == '' or line.strip().startswith('--'):
            import_lines.append(line)
            continue
        if line.lstrip().startswith('import') or line.lstrip().startswith('open'):
            import_lines.append(line)
        else:
            break

    block_starts = [i for i, line in enumerate(lines) if LEAN_BLOCK_START.match(line)]
    block_starts.append(len(lines))  

    parts = []
    current_part = []
    current_len = 0

    for i in range(len(block_starts) - 1):
        block = lines[block_starts[i]:block_starts[i+1]]
        if current_len + len(block) > max_lines and current_part:
            parts.append(current_part)
            current_part = []
            current_len = 0
        current_part.extend(block)
        current_len += len(block)
    if current_part:
        parts.append(current_part)

    base, ext = os.path.splitext(filepath)
    for idx, part in enumerate(parts, 1):
        new_path = f"{base}_part{idx}{ext}"
        with open(new_path, 'w', encoding='utf-8') as f:
            f.writelines(import_lines)
            if import_lines and import_lines[-1].strip() != '':
                f.write('\n')
            f.writelines(part)
    print(f"Split {filepath} into {len(parts)} parts.")
    # remove the original file
    os.remove(filepath)

def main():
    lean_files = find_lean_files(ROOT_DIR)
    for filepath in lean_files:
        split_lean_file(filepath)

if __name__ == '__main__':
    main()