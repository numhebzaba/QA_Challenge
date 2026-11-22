from playwright.sync_api import Locator, Page

TODO_URL = "https://demo.playwright.dev/todomvc/#/"


class TodoPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.new_todo = page.get_by_placeholder("What needs to be done?")
        self.items = page.get_by_test_id("todo-item")
        self.titles = page.get_by_test_id("todo-title")
        self.counter = page.get_by_test_id("todo-count")
        self.toggle_all = page.get_by_label("Mark all as complete", exact=True)
        self.clear_completed = page.get_by_role("button", name="Clear completed", exact=True)

    def open(self) -> None:
        self.page.goto(TODO_URL, wait_until="domcontentloaded")

    def add(self, title: str) -> None:
        self.new_todo.fill(title)
        self.new_todo.press("Enter")

    def row(self, title: str) -> Locator:
        return self.items.filter(has=self.page.get_by_text(title, exact=True))

    def checkbox(self, title: str) -> Locator:
        return self.row(title).get_by_role("checkbox", name="Toggle Todo")

    def begin_edit(self, title: str) -> Locator:
        row = self.row(title)
        row.get_by_text(title, exact=True).dblclick()
        return row.get_by_role("textbox")

    def delete(self, title: str) -> None:
        row = self.row(title)
        row.hover()
        # The hover-only delete button has no accessible name in the demo.
        row.locator("button.destroy").click()
