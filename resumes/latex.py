import shutil
import subprocess
import tempfile
from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.template.loader import render_to_string


def build_resume_pdf(resume):
    base = Path(__file__).resolve().parent / "static" / "resumes"
    context = {
        "resume": resume,
        "font_dir": (base / "fonts").as_posix() + "/",
        "logo_uni_arg": "{" + (base / "img" / "logo_university.jpg").as_posix() + "}",
        "logo_assoc_arg": "{" + (base / "img" / "logo_association.jpg").as_posix() + "}",
    }
    source = render_to_string("resumes/resume.tex", context)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        (tmp_dir / "resume.tex").write_text(source, encoding="utf-8")

        proc = subprocess.run(
            ["xelatex", "-interaction=nonstopmode", "-halt-on-error", "resume.tex"],
            cwd=tmp, capture_output=True, text=True, timeout=180,
        )
        pdf_path = tmp_dir / "resume.pdf"

        if proc.returncode != 0 or not pdf_path.exists():
            debug = Path(settings.MEDIA_ROOT) / "latex_debug"
            debug.mkdir(parents=True, exist_ok=True)
            for name in ("resume.tex", "resume.log"):
                if (tmp_dir / name).exists():
                    shutil.copy(tmp_dir / name, debug / f"{resume.pk}_{name}")
            raise RuntimeError(f"کامپایل لاتکس ناموفق بود. فایل‌های بررسی در {debug} ذخیره شد.")

        if resume.pdf:
            resume.pdf.delete(save=False)
        resume.pdf.save(f"resume_{resume.pk}.pdf", ContentFile(pdf_path.read_bytes()), save=True)