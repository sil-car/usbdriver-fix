import psutil

from pathlib import Path


def fix():
    # Service to stop:
    # - MSBuild.exe
    msbuild_procs = [p for p in psutil.process_iter(attrs=["name"]) if p.name() == 'MSBuild.EXE']  # noqa: E501
    for p in msbuild_procs:
        try:
            p.kill()
        except Exception as e:
            return f"Échec d'arrêt de service de Windows : {e}"

    # Files to remove:
    # - C:\Users\Public\Library\MSBuild.exe
    # - C:\Users\Public\Library\Version.dll
    for n in ['MSBuild.exe', 'Version.dll']:
        f = Path("C:/Users/Public/Library") / n
        if f.is_file():
            try:
                f.unlink()
            except Exception as e:
                return f"Échec de suppression de fichier : {e}"
