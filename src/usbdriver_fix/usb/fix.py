import os
import shutil
from pathlib import Path


def display_unicode(data):
    return "".join([f"\\u{hex(ord(c))[2:].zfill(4)}" for c in data])


def verify_infected(basedir):
    message = "Clé non infectée"
    for f in Path(basedir).iterdir():
        if f.name == 'USB Driver.exe':
            return True
        elif f.is_dir() and is_virus_dir(f):
            return True
    return message


def is_virus_dir(dirpath):
    p = Path(dirpath).name
    if len(p) == 1 and (not p.isalnum() and p != '/'):
        return True
    else:
        return False


def remove_bad_files(basedir, app):
    message = "Échec de suppression de mauvais fichiers."

    # Remove virus directories.
    for dirpath, dirnames, filenames in os.walk(basedir):
        if is_virus_dir(dirpath):
            print(f"Removing tree: {dirpath}")
            try:
                shutil.rmtree(dirpath)
                break
            except Exception as e:
                return f"{message}: {e}"
        for d in dirnames:
            subdirpath = Path(dirpath) / d
            if is_virus_dir(subdirpath):
                print(f"Removing tree: {subdirpath}")
                try:
                    shutil.rmtree(subdirpath)
                except Exception as e:
                    return f"{message}: {e}"

    # Remove virus files.
    names = ['USB Driver.exe', 'MSBuild.exe', 'Version.dll']
    for n in names:
        for f in Path(basedir).rglob(n):
            print(f"Removing: {f}")
            try:
                f.unlink()
            except Exception as e:
                return f"{message}: {e}"

    # Remove all EXE files.
    exes = [f for f in Path(basedir).rglob('*.exe')]
    if 'win' not in app.platform:
        exes.extend([f for f in Path(basedir).rglob('*.EXE')])
    for f in exes:
        print(f"Removing: {f}")
        try:
            f.unlink()
        except Exception as e:
            return f"{message}: {e}"
    return True


def retrieve_hidden_files(basedir):
    message = "Échec de récupération de fichiers."
    all_paths = [str(p) for p in Path(basedir).rglob('*')]
    fixed_path_file_pairs = get_fixed_path_file_pairs(all_paths)
    file_pairs_to_move = [p for p in fixed_path_file_pairs if p[1] != basedir and p[0] != p[1]]  # noqa: E501
    for s, d in file_pairs_to_move:
        print(f"Moving: {s} to {d}")
        try:
            Path(d).parent.mkdir(exist_ok=True, parents=True)
            shutil.move(s, d)
        except Exception as e:
            return f"{message}: {e}"


def fix_usb(basedir, app=None):
    result = False
    r = verify_infected(basedir)
    if isinstance(r, str):
        result = True
    r = retrieve_hidden_files(basedir)
    if isinstance(r, str):
        result = r
    r = remove_bad_files(basedir, app=app)
    if isinstance(r, str):
        result = r
    app.usb_q.put(result)
    app.event_generate(app.usb_evt)


def get_fixed_path_file_pairs(file_paths):
    pairs = zip(file_paths, [fix_file_path(f) for f in file_paths])
    return [p for p in pairs if not Path(p[0]).is_dir()]


def fix_file_path(file_path):
    fp = Path(file_path)
    new_parts = []
    for p in fp.parts:
        if len(p) == 1 and (not p.isalnum() and p != '/'):
            continue
        new_parts.append(p)
    return str(Path(*new_parts))
