# Challenge 2 test cases

The challenge PDF, section 2, requires runnable scripts, setup instructions, designed test cases, and a maintainable Git repository. It gives the target website and leaves behavior-level acceptance criteria open. This suite uses the [official Playwright TodoMVC basic operations plan](https://github.com/microsoft/playwright/blob/main/examples/todomvc/specs/basic-operations.plan.md) and the [official TodoMVC test report](https://demo.playwright.dev/reports/todomvc/) as the reference for the selected behaviors.

A user opens the demo, adds active todos, edits or toggles them, filters by status, and removes individual or completed todos. Reload should preserve titles and completion state in the same browser context.

All cases run through the UI and are automated in `tests/test_todos.py`. Each starts with an empty browser context. Pytest disposes of the context and its stored data afterwards.

| Case and rule | Priority | Technique | Data and steps | Expected observable result |
| --- | --- | --- | --- | --- |
| TC01 / R01 · Add | P0 | Count boundary 0 → 1 → 2 | Submit Buy train tickets, then Pack a lunch | First item appears active and clears the input. Both titles appear in order. Counter changes from 1 item left to 2 items left. |
| TC02 / R02 · Reject blank | P1 | Invalid equivalence classes | Seed Pack a lunch. Submit empty input or three spaces in separate runs | Only the seeded title remains and counter stays at 1 item left. |
| TC03 / R03 · Edit | P1 | State transition | Double-click Water plants, change it to Water balcony plants, press Enter or Escape in separate runs | Editor starts with the original title and closes. Enter commits the new title. Escape retains the original. Counter stays at 1 item left. |
| TC04 / R04 · Complete and reopen | P0 | State transition | Seed Organize desk and Print boarding pass. Check then uncheck Organize desk | Target changes active → completed → active. Other item remains active when target is completed. Counter changes from 1 to 2 items left. |
| TC05 / R05 · Delete | P1 | Mixed retained/deleted rows | Seed Organize desk and Print boarding pass. Hover Organize desk and click its delete control | Only Print boarding pass remains. Counter shows 1 item left. |
| TC06 / R06 · Filter | P1 | Decision table by filter and status | Complete Organize desk and leave Print boarding pass active. Navigate from another filter to All, Active, or Completed in separate runs | The destination filter is selected and the route matches it. All shows both titles in order. Active shows Print boarding pass. Completed shows Organize desk. Counter remains 1 item left. |
| TC07 / R07 · Toggle all | P1 | State transition | Start with two todos, one complete. Click Mark all as complete twice | Both are checked with 0 items left, then both are unchecked with 2 items left. |
| TC08 / R08 · Clear completed | P1 | Mixed state | Seed three todos and complete Organize desk and Pack a lunch. Click Clear completed | Only the active Print boarding pass remains with 1 item left. Clear completed is hidden. |
| TC09 / R09 · Persist | P0 | Reload transition | Seed Organize desk and Pack a lunch. Complete the first, then reload | Both titles, their order and respective checkbox states survive reload. Counter remains 1 item left. |

R01–R09 each map to the case in the same row. Case design covers the selected rules. For actual execution results, see the generated HTML report described in the [README](../../README.md#open-the-report).

| Open question | Impact | Blocking? |
| --- | --- | --- |
| What title length, duplicate-title policy, or rules for other whitespace characters should the demo enforce? | Additional boundary and equivalence cases need an expected outcome. | No |
| Which browser/device combinations are part of acceptance? | Verification scope defaults to desktop Chromium. | No |

The highest risks within scope are losing a todo or its status across reload, changing another row during a targeted action, and removing active todos during bulk cleanup. The public demo is an external dependency with no pinned deployment version. Cross-device sync, API, performance, and application security are outside this UI suite.

Report variants have distinct IDs. TC02 uses -EMPTY and -WHITESPACE, TC03 uses -SAVE and -CANCEL, and TC06 uses -ALL, -ACTIVE, and -COMPLETED.
