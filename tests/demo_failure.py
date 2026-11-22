"""Run explicitly to demonstrate failure evidence in the HTML report."""

from collections.abc import Callable

from playwright.sync_api import expect

from pages.todo_page import TodoPage


def test_tc00_intentional_counter_failure(
    todo: TodoPage,
    capture_step: Callable[[str], None],
) -> None:
    todo.add("Review failure evidence")
    expect(todo.titles).to_have_text(["Review failure evidence"])
    expect(todo.counter).to_have_text("1 item left")
    capture_step("Actual counter after adding one todo")

    expect(
        todo.counter,
        "Intentional demo failure: expect two active items after adding only one",
    ).to_have_text("2 items left", timeout=1000)
