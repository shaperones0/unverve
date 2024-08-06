import pathlib, os, itertools


def unverve_string(input: str) -> str:
    result = []
    for line in input.splitlines():
        line_stripped = line.strip()
        if line_stripped and line_stripped.endswith(';') and not line_stripped.startswith('var'):
            result.append(line[:-1])
        else:            
            result.append(line)    # dont remove semicolon here
    return '\n'.join(result)    # keep it being LF


def main(root_dirname: str):
    root_path = pathlib.Path(root_dirname)
    scripts_path = root_path / "scripts"
    if not scripts_path.exists():
        raise FileNotFoundError("Couldn't find scripts folder in project")
    objects_path = root_path / "objects"
    if not objects_path.exists():
        raise FileNotFoundError("Couldn't find objects folder in project")
    
    for script_fname in itertools.chain(scripts_path.iterdir(), objects_path.iterdir()):
        print(f"File {script_fname} ...", end=" ")
        with script_fname.open() as fin:
            content = fin.read()
        content_unverved = unverve_string(content)
        with script_fname.open('w') as fout:
            fout.write(content_unverved)
        print(f"written.")
        

if __name__ == "__main__":
    import sys
    root_dirname = "C:\\dev\\repo\\i-wanna-recompile\\source" #sys.argv[1]
    main(root_dirname)
