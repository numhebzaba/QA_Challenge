# QA_Challenge

bluePi QA Challenge

## Challenge 2 · TodoMVC UI automation

Python 3.12, Pytest, and Playwright. The suite runs against the [public TodoMVC demo](https://demo.playwright.dev/todomvc/#/).

### Run from the VS Code terminal on Windows

Open the repository folder in VS Code, then select **Terminal → New Terminal** and choose **PowerShell**. Run the commands from the folder containing `pytest.ini`.

#### First-time setup

Install Python 3.12 with the Windows Python launcher. Make sure your network can reach PyPI, the Playwright browser CDN, and the TodoMVC demo.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium
```

#### Run the tests

Set the alias once per PowerShell terminal to use the project's Pytest installation without running `Activate.ps1`.

```powershell
Set-Alias pytest "$PWD\.venv\Scripts\pytest.exe"
pytest tests/test_todos.py
```

This runs the 13 regular cases in Chromium. Add `--headed` to watch the browser or `-k tc06` to run only the filter cases. You can also run the file directly without setting the alias.

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_todos.py
```

#### Open the report

Pytest prints the full HTML report path at the end of the run. Open it from the same terminal.

```powershell
Invoke-Item .\test-results\report.html
```

Click a test row and use the gallery arrows to view its numbered screenshots. If a step screenshot times out, the Links column shows a warning and the test keeps its assertion outcome. Failure evidence is saved under `test-results/report-artifacts/`. To open a trace, replace the example ZIP path with the one for your failed case.

~~~powershell
.\.venv\Scripts\python.exe -m playwright show-trace ".\test-results\demo-artifacts\tests-demo-failure-py-test-tc00-intentional-counter-failure-chromium\trace.zip"
~~~

### Run from the VS Code terminal on macOS

Open the repository folder in VS Code, then select **Terminal → New Terminal**. These commands assume zsh or Bash and Python 3.12 is available as `python3.12`. Run them from the folder containing `pytest.ini`.

#### First-time setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
```

#### Run the tests and open the report

Activate the virtual environment again in each new terminal. Skip that line if it is already active.

```bash
source .venv/bin/activate
pytest tests/test_todos.py
open test-results/report.html
```

Pytest prints the full HTML report path after the run. To view a failure trace, replace the example ZIP path with the one for your case.

```bash
python -m playwright show-trace "test-results/report-artifacts/<case-folder>/trace.zip"
```

### Project layout

- `pages/todo_page.py` holds selectors and browser interactions. Tests own expected outcomes.
- `tests/conftest.py` opens the demo in the plugin's fresh browser context per case. Each test creates its own synthetic todos through the UI.
- `tests/test_todos.py` contains 9 scenarios expanded into 13 runnable cases.
- [Test design and traceability](docs/test-cases/TEST_CASES.md) records coverage, expected outcomes, and open rules.
- [Test cases workbook](docs/test-cases/TodoMVC-Test-Cases.xlsx) supports filtering by case, rule, and priority. A [CSV export](docs/test-cases/TodoMVC-Test-Cases.csv) is available for viewers that do not open XLSX. Update both exports with the test design when cases change.

### Optional failure demonstration

The normal suite discovers 13 cases. To include the intentional failure, run from the repository root:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_todos.py tests/demo_failure.py --browser chromium --output=test-results/demo-artifacts --html=test-results/failure-demo.html --self-contained-html --css=report.css
```

The demo adds one todo and deliberately expects the counter to show two. This run should report 13 passed, 1 failed and exit code 1. Open the failed row to inspect the screenshot and assertion details. The failure screenshot and trace are also saved under `test-results/demo-artifacts/`.

### Share a report with traces

The HTML embeds step screenshots. Trace ZIPs use relative paths, so send the HTML and its artifact folder together. For the failure demo, create the bundle from the repository root:

```powershell
Compress-Archive -LiteralPath 'test-results/failure-demo.html','test-results/demo-artifacts' -DestinationPath 'test-results/failure-demo-bundle.zip' -Force
```

Extract the bundle before opening the HTML. Keep the HTML and artifact folder side by side. For a regular run with failures, use `report.html` and `report-artifacts` in the same command.

### Keep a previous run

The next regular run overwrites the HTML and clears its previous failure artifacts. Run this from the repository root before rerunning if you want to keep the current report.

~~~powershell
$files = @('test-results/report.html')
if (Test-Path 'test-results/report-artifacts') {
    $files += 'test-results/report-artifacts'
}
$stamp = Get-Date -Format 'yyyyMMdd-HHmmssfff'
Compress-Archive -LiteralPath $files -DestinationPath "test-results/report-$stamp.zip"
~~~

Extract the archive before opening the saved report so its relative trace links can resolve.
