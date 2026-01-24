import subprocess
import typer

def analyze():
    """
    Analyze git diff and suggest Radish tags.
    """
    try:
        diff = subprocess.check_output(
            ["git", "diff", "--name-only", "origin/main...HEAD"],
            text=True
        )
    except Exception:
        diff = ""

    tags = []

    if "login" in diff:
        tags.append("@owns:auth")
    if "checkout" in diff:
        tags.append("@owns:checkout")

    if not tags:
        tags.append("@smoke")

    typer.echo("🎯 Suggested tags:")
    typer.echo(" or ".join(tags))
    print("Impact analysis completed")
