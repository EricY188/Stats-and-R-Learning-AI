import subprocess, tempfile, textwrap, os, shutil

def run_r_code_safe(code: str, timeout: int = 30):
    tmp_dir = tempfile.mkdtemp(prefix="rtutor_")
    r_path = shutil.which("Rscript")
    if not r_path:
        return {"error": "Rscript not found"}
    script = textwrap.dedent(f"""            png("plot.png")
    tryCatch({{
      {code}
    }}, error=function(e) {{
      cat("R_ERROR:", e$message, file=stderr())
    }})
    dev.off()
    """)
    script_file = os.path.join(tmp_dir, "script.R")
    with open(script_file, "w") as f:
        f.write(script)
    try:
        res = subprocess.run(
            [r_path, script_file],
            cwd=tmp_dir,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {"error": "Execution timed out"}
    out = {"stdout": res.stdout, "stderr": res.stderr}
    plot_file = os.path.join(tmp_dir, "plot.png")
    if os.path.exists(plot_file):
        out["plot_png_b64"] = open(plot_file, "rb").read().hex()
    return out
