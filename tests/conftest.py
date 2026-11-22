from base64 import b64encode
from collections.abc import Callable
from html import escape
import re

import pytest
import pytest_html
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, expect

from pages.todo_page import TodoPage


@pytest.fixture
def todo(page: Page) -> TodoPage:
    app = TodoPage(page)
    app.open()
    expect(app.new_todo).to_be_editable()
    expect(app.items).to_have_count(0)
    return app


@pytest.fixture
def capture_step(
    page: Page, extras: list, pytestconfig: pytest.Config
) -> Callable[[str], None]:
    """Attach numbered screenshots to this test's HTML result."""
    step_number = 0

    def capture(label: str) -> None:
        nonlocal step_number
        if not pytestconfig.getoption("htmlpath"):
            return
        step_number += 1
        try:
            png = page.screenshot(animations="disabled", scale="css", timeout=3000)
        except PlaywrightTimeoutError:
            extras.append(pytest_html.extras.text(
                f"Screenshot for step {step_number:02d} ({label}) timed out after 3 seconds.",
                name=f"Screenshot warning · step {step_number:02d}",
            ))
            return
        content = b64encode(png).decode("ascii")
        extras.append(pytest_html.extras.png(content, name=f"{step_number:02d}. {label}"))

    return capture


@pytest.hookimpl(optionalhook=True)
def pytest_html_report_title(report) -> None:
    report.title = "TodoMVC test report"


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_row(report: pytest.TestReport, cells: list[str]) -> None:
    test_name = report.nodeid.rsplit("::", 1)[-1]
    match = re.fullmatch(r"test_(tc\d+)_([a-z0-9_]+)(?:\[([^]]+)\])?", test_name)
    if match is None:
        return

    case_id, scenario, parameters = match.groups()
    title = scenario.replace("_", " ").capitalize()
    browser, _, variant = (parameters or "").partition("-")
    execution_id = f"{case_id.upper()}-{variant.upper()}" if variant else case_id.upper()
    suffix = f" ({browser})" if browser else ""
    if report.when != "call":
        suffix += f" [{report.when}]"
    label = f"{execution_id} · {title}{suffix}"
    cells[1] = (
        f'<td class="col-testId" title="{escape(report.nodeid)}">'
        f"{escape(label)}</td>"
    )


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_html(data: list[str]) -> None:
    if data == ["No log output captured."]:
        data.clear()
