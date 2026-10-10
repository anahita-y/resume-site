import os
import shutil
import subprocess
import threading

import django
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

call_command("collectstatic", interactive=False, verbosity=0)
call_command("migrate", interactive=False, verbosity=0)

LATEX_PACKAGES = (
    "texlive-xetex texlive-lang-arabic texlive-latex-recommended "
    "texlive-latex-extra texlive-fonts-recommended"
)


def _ensure_latex():
    if shutil.which("xelatex") or os.geteuid() != 0:
        return
    print("LATEX: installing in background...", flush=True)
    env = {**os.environ, "DEBIAN_FRONTEND": "noninteractive"}
    cmd = (
        "apt-get update && "
        f"apt-get install -y --no-install-recommends {LATEX_PACKAGES}"
    )
    result = subprocess.run(cmd, shell=True, env=env)
    print(f"LATEX: install finished with code {result.returncode}", flush=True)


threading.Thread(target=_ensure_latex, daemon=True).start()

application = get_wsgi_application()