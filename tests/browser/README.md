# Browser tests

Two gates that cannot be expressed in the Python suite, because both are claims
about rendered geometry rather than about application logic.

They drive real Chrome over CDP via `puppeteer-core` (no browser download
needed — they attach to the Chrome already installed on the machine).

## Running

```sh
# 1. start the app on the test port
FLASK_APP=wsgi:app python -c "
from app import create_app
create_app().run(host='127.0.0.1', port=5099, threaded=True)
" &

# 2. one-time
npm install puppeteer-core

# 3. run the gates
node tests/browser/responsive_audit.js    # 375 / 768 / 1280, all pages
node tests/browser/jitter_test.js         # flip-board geometric stability
```

Both exit non-zero on failure, so they drop straight into CI.

## What they assert

### `responsive_audit.js`
The brief makes responsive behaviour a hard gate. For every page at 375, 768 and
1280px it checks:

- no horizontal overflow (`scrollWidth` must not exceed the viewport)
- no element wider than the viewport
- nothing bleeding off either edge
- no content clipped inside its own box (excluding deliberately scrollable and
  ellipsized elements)
- every interactive control at least 24px tall (WCAG 2.5.8)
- body text contrast at or above WCAG AA, measured live from computed styles
- no uncaught JavaScript errors

Writes a screenshot per page-width to `shots/`.

### `jitter_test.js`
The brief requires the flip-board to be pixel-perfect with no layout shift when
digits change length. That rots silently, so it is measured:

- the board, its left module, the counter and the right module must not move or
  resize as the done-count steps through every value 0..N
- every digit cell must be exactly the same width at every value
- the status badge must not resize between "Pending" / "In progress" / "Done"
  (a 112px min-width is required to hold the longest label)
- the board must not move while the 3D flip animation runs

### `demo_links_test.js`

Clicks every example chip on the ask page and asserts each one lands on a
rendered checklist with steps, source links and the research record — i.e. that
it was served from cache rather than falling through to the researching view.
This exists because a seed once drifted out of sync with the link that
advertises it (the education-loan chip asked for `education loan` while the
seed was keyed `education loan (study abroad)`), which would have put a cold
research call in the middle of a recorded demo.

The Python suite asserts the same property at the data layer
(`TestDemoIsPreWarmed`); this one asserts it through the real UI.
