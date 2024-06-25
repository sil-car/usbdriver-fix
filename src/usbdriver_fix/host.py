import logging
import psutil

from pathlib import Path


def fix():
    # Service to stop:
    # - MSBuild.exe
    msbuild_procs = [p for p in psutil.process_iter(attrs=["name"]) if p.name() == 'MSBuild.EXE']  # noqa: E501
    for p in msbuild_procs:
        logging.info(f"Arrêt de processus : {p.name}")
        try:
            p.kill()
        except Exception as e:
            message = f"Échec d'arrêt de processus : {e}"
            logging.error(message)
            return message

    # Files to remove:
    # - C:\Users\Public\Library\MSBuild.EXE
    # - C:\Users\Public\Library\version.dll
    for n in ['MSBuild.EXE', 'version.dll']:
        f = Path("C:/Users/Public/Libraries") / n
        if f.is_file():
            logging.info(f"Supppression de fichier malveillant : {f}")
            try:
                f.unlink()
            except Exception as e:
                message = f"Échec de suppression de fichier : {e}"
                logging.error(message)
                return message
