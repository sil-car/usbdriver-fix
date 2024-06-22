import psutil

from pathlib import Path


def fix():
    # Service to stop:
    # - MSBuild.exe
    msbuild = psutil.win_service_get('MSBuild')
    if msbuild:
        try:
            psutil.Process(msbuild.pid()).kill()
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
