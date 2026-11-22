from collections.abc import Callable

import pytest
from playwright.sync_api import expect

from pages.todo_page import TODO_URL, TodoPage


def test_tc01_add_todos_in_order(
    capture_step: Callable[[str], None],
    todo: TodoPage,
) -> None:
    todo.add("Buy train tickets")
    expect(todo.titles).to_have_text(["Buy train tickets"])
    expect(todo.counter).to_have_text("1 item left")
    expect(todo.new_todo).to_have_value("")
    expect(todo.checkbox("Buy train tickets")).not_to_be_checked()
    capture_step("First item added")

    todo.add("Pack a lunch")
    expect(todo.titles).to_have_text(["Buy train tickets", "Pack a lunch"])
    expect(todo.counter).to_have_text("2 items left")
    capture_step("Second item added")


@pytest.mark.parametrize(
    "invalid_title", ["", "   "], ids=["empty", "whitespace"]
)
def test_tc02_reject_blank_todo(
    capture_step: Callable[[str], None],
    todo: TodoPage, invalid_title: str,
) -> None:
    todo.add("Pack a lunch")
    expect(todo.titles).to_have_text(["Pack a lunch"])
    capture_step("Before blank submission")

    todo.add(invalid_title)

    expect(todo.titles).to_have_text(["Pack a lunch"])
    expect(todo.counter).to_have_text("1 item left")
    capture_step("Blank input rejected")


@pytest.mark.parametrize(
    ("key", "expected_title"),
    [("Enter", "Water balcony plants"), ("Escape", "Water plants")],
    ids=["save", "cancel"],
)
def test_tc03_edit_todo(
    capture_step: Callable[[str], None],
    todo: TodoPage, key: str, expected_title: str,
) -> None:
    todo.add("Water plants")
    expect(todo.titles).to_have_text(["Water plants"])
    capture_step("Original todo before editing")
    editor = todo.begin_edit("Water plants")
    expect(editor).to_have_value("Water plants")
    editor.fill("Water balcony plants")
    capture_step("Draft title in editor")
    editor.press(key)

    expect(todo.items.get_by_role("textbox")).to_have_count(0)
    expect(todo.titles).to_have_text([expected_title])
    expect(todo.counter).to_have_text("1 item left")
    capture_step(f"Edit result after {key}")


def test_tc04_complete_and_reopen_todo(
    capture_step: Callable[[str], None],
    todo: TodoPage,
) -> None:
    todo.add("Organize desk")
    todo.add("Print boarding pass")
    target = todo.checkbox("Organize desk")
    other = todo.checkbox("Print boarding pass")

    target.check()
    expect(target).to_be_checked()
    expect(other).not_to_be_checked()
    expect(todo.counter).to_have_text("1 item left")
    capture_step("Target completed")

    target.uncheck()
    expect(target).not_to_be_checked()
    expect(todo.counter).to_have_text("2 items left")
    capture_step("Target reopened")


def test_tc05_delete_only_target(
    capture_step: Callable[[str], None],
    todo: TodoPage,
) -> None:
    todo.add("Organize desk")
    todo.add("Print boarding pass")
    capture_step("Two items before deletion")

    todo.delete("Organize desk")

    expect(todo.titles).to_have_text(["Print boarding pass"])
    expect(todo.counter).to_have_text("1 item left")
    capture_step("Only the other item remains")


@pytest.mark.parametrize(
    ("initial_filter", "filter_name", "route", "visible_titles"),
    [
        ("Active", "All", "", ["Organize desk", "Print boarding pass"]),
        ("Completed", "Active", "active", ["Print boarding pass"]),
        ("Active", "Completed", "completed", ["Organize desk"]),
    ],
    ids=["all", "active", "completed"],
)
def test_tc06_filter_by_status(
    capture_step: Callable[[str], None],
    todo: TodoPage, initial_filter: str, filter_name: str, route: str,
    visible_titles: list[str],
) -> None:
    todo.add("Organize desk")
    todo.add("Print boarding pass")
    todo.checkbox("Organize desk").check()
    expect(todo.titles).to_have_text(["Organize desk", "Print boarding pass"])
    capture_step("Unfiltered list before changing filters")
    initial_link = todo.page.get_by_role("link", name=initial_filter, exact=True)
    initial_link.click()
    expect(initial_link).to_have_class("selected")
    capture_step(f"{initial_filter} view before switching to {filter_name}")

    target_link = todo.page.get_by_role("link", name=filter_name, exact=True)
    target_link.click()
    expect(target_link).to_have_class("selected")

    expect(todo.page).to_have_url(TODO_URL + route)
    expect(todo.titles).to_have_text(visible_titles)
    expect(todo.counter).to_have_text("1 item left")
    capture_step(f"{filter_name} filter applied")


def test_tc07_toggle_all_both_directions(
    capture_step: Callable[[str], None],
    todo: TodoPage,
) -> None:
    todo.add("Organize desk")
    todo.add("Print boarding pass")
    first = todo.checkbox("Organize desk")
    second = todo.checkbox("Print boarding pass")
    first.check()

    todo.toggle_all.click()
    expect(first).to_be_checked()
    expect(second).to_be_checked()
    expect(todo.counter).to_have_text("0 items left")
    capture_step("All items completed")

    todo.toggle_all.click()
    expect(first).not_to_be_checked()
    expect(second).not_to_be_checked()
    expect(todo.counter).to_have_text("2 items left")
    capture_step("All items reopened")


def test_tc08_clear_completed_keeps_active_todo(
    capture_step: Callable[[str], None],
    todo: TodoPage,
) -> None:
    todo.add("Organize desk")
    todo.add("Print boarding pass")
    todo.add("Pack a lunch")
    todo.checkbox("Organize desk").check()
    todo.checkbox("Pack a lunch").check()
    capture_step("Before clearing completed items")

    todo.clear_completed.click()

    expect(todo.titles).to_have_text(["Print boarding pass"])
    expect(todo.checkbox("Print boarding pass")).not_to_be_checked()
    expect(todo.counter).to_have_text("1 item left")
    expect(todo.clear_completed).to_be_hidden()
    capture_step("Completed items cleared")


def test_tc09_persist_titles_and_status_after_reload(
    capture_step: Callable[[str], None],
    todo: TodoPage,
) -> None:
    todo.add("Organize desk")
    todo.add("Pack a lunch")
    todo.checkbox("Organize desk").check()
    expect(todo.counter).to_have_text("1 item left")
    capture_step("State before reload")

    todo.page.reload(wait_until="domcontentloaded")

    expect(todo.titles).to_have_text(["Organize desk", "Pack a lunch"])
    expect(todo.checkbox("Organize desk")).to_be_checked()
    expect(todo.checkbox("Pack a lunch")).not_to_be_checked()
    expect(todo.counter).to_have_text("1 item left")
    capture_step("State restored after reload")
