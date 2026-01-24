import typer

import quality_cli.runner as runner
import quality_cli.impact as impact
import quality_cli.gates as gates
import quality_cli.report as report
import quality_cli.leadership as leadership
from quality_cli import scaffold

app = typer.Typer(help="Quality Engineering Platform CLI")

app.command("init")(scaffold.init)
app.command("impact")(impact.analyze)
app.command("run")(runner.run)
app.command("gate")(gates.check)
app.command("report")(report.generate)
app.command("leadership")(leadership.generate)
