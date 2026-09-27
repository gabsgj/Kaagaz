/**
 * Kaagaz — checklist page behaviour.
 *
 * Progressive tracking with three states per document (pending / in progress /
 * done), persisted to localStorage so a half-finished checklist survives a
 * reload, plus a per-document "why is this needed?" explainer.
 *
 * The progress board is driven entirely through window.KaagazFlip so the
 * digit cells keep their fixed width and the board never reflows.
 */
(function (global) {
  'use strict';

  // Labels name the ACTION the button performs, not the state the item is in.
  // "In progress" as a button label read as a status and made it impossible to
  // tell whether the item had already moved on.
  var CYCLE = ['pending', 'in_progress', 'done'];
  var NEXT_LABEL = { pending: 'Start', in_progress: 'Mark done', done: 'Undo' };

  function Checklist(root) {
    this.root = root;
    this.steps = Array.prototype.slice.call(root.querySelectorAll('.step'));
    this.total = this.steps.length;
    this.key = this._storageKey();
    this.state = this._load();
  }

  Checklist.prototype._storageKey = function () {
    var r = this.root;
    return [
      'kaagaz:v2',
      r.getAttribute('data-transaction') || '',
      r.getAttribute('data-bank') || '',
      r.getAttribute('data-residency') || '',
      r.getAttribute('data-state') || ''
    ].join('|').toLowerCase();
  };

  Checklist.prototype._load = function () {
    var saved = {};
    try { saved = JSON.parse(global.localStorage.getItem(this.key) || '{}'); }
    catch (e) { saved = {}; }
    var out = {};
    for (var i = 0; i < this.steps.length; i++) {
      var id = this.steps[i].getAttribute('data-item-id');
      out[id] = CYCLE.indexOf(saved[id]) > -1 ? saved[id] : 'pending';
    }
    return out;
  };

  Checklist.prototype._save = function () {
    try { global.localStorage.setItem(this.key, JSON.stringify(this.state)); }
    catch (e) { /* private browsing — tracking still works for this page view */ }
  };

  Checklist.prototype.doneCount = function () {
    var n = 0;
    for (var k in this.state) { if (this.state[k] === 'done') n++; }
    return n;
  };

  Checklist.prototype.render = function () {
    var self = this;
    var done = this.doneCount();
    var pct = this.total > 0 ? Math.round((done / this.total) * 100) : 0;

    this.steps.forEach(function (step) {
      var id = step.getAttribute('data-item-id');
      var status = self.state[id] || 'pending';
      step.setAttribute('data-status', status);

      var badge = step.querySelector('.status');
      if (badge) {
        if (badge.getAttribute('data-state') !== status) {
          badge.setAttribute('data-state', status);
          badge.textContent = {
            pending: 'Pending', in_progress: 'In progress', done: 'Done'
          }[status];
        }
      }

      var btn = step.querySelector('.step__advance');
      if (btn) btn.textContent = NEXT_LABEL[status];
    });

    // Board. Numbers go through the flip cells; nothing else touches them.
    // Both counters are reserved to the TOTAL's digit width. Reserving only the
    // total would let the done counter grow a cell at 10 and shift the board.
    if (global.KaagazFlip) {
      var digits = String(self.total).length;
      global.KaagazFlip.reserve('doneCount', digits);
      global.KaagazFlip.reserve('totalCount', digits);
      global.KaagazFlip.setNumber('doneCount', done, { silent: true });
      global.KaagazFlip.setNumber('totalCount', self.total, { silent: true });
    }
    var pctEl = this.root.querySelector('#boardPct');
    if (pctEl) pctEl.textContent = pct + '%';
    var fill = this.root.querySelector('#boardFill');
    if (fill) fill.style.width = pct + '%';
    var caption = this.root.querySelector('#boardCaption');
    if (caption) {
      caption.textContent = done + ' of ' + self.total + ' collected';
    }

    var label = this.root.querySelector('#tallyLabel');
    if (label) label.textContent = done + ' of ' + self.total + ' ready';
    var tFill = this.root.querySelector('#tallyFill');
    if (tFill) tFill.style.width = pct + '%';
    var tPct = this.root.querySelector('#tallyPct');
    if (tPct) tPct.textContent = pct + '%';
  };

  Checklist.prototype.advance = function (id) {
    var current = this.state[id] || 'pending';
    var next = CYCLE[(CYCLE.indexOf(current) + 1) % CYCLE.length];
    this.state[id] = next;
    this._save();
    this.render();

    if (next === 'done') {
      var step = this.root.querySelector('.step[data-item-id="' + id + '"]');
      if (step) step.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  };

  /* ── Per-document explainer ─────────────────────────────────── */
  Checklist.prototype.explain = function (id) {
    var step = this.root.querySelector('.step[data-item-id="' + id + '"]');
    if (!step) return Promise.resolve();
    var btn = step.querySelector('.step__explain');
    var box = step.querySelector('.step__answer');
    if (!btn || !box) return Promise.resolve();

    if (box.dataset.open === '1') {
      box.hidden = true;
      box.dataset.open = '0';
      btn.setAttribute('aria-expanded', 'false');
      return Promise.resolve();
    }

    var term = btn.getAttribute('data-term');
    var tx = btn.getAttribute('data-tx');
    box.hidden = false;
    box.dataset.open = '1';
    btn.setAttribute('aria-expanded', 'true');
    box.innerHTML = '<span>Looking into that…</span>';

    return fetch('/api/ai/explain', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ term: term, transaction_type: tx })
    })
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      })
      .then(function (data) {
        var note = data.source === 'static_fallback'
          ? ' Live model unavailable — showing the stored entry instead.'
          : '';
        box.textContent = (data.explanation || 'No explanation available.') + note;
      })
      .catch(function () {
        box.textContent = 'Could not load an explanation just now. The rest of ' +
                         'the checklist is unaffected.';
      });
  };

  Checklist.prototype.wire = function () {
    var self = this;
    this.steps.forEach(function (step) {
      var id = step.getAttribute('data-item-id');
      var advance = step.querySelector('.step__advance');
      if (advance) {
        advance.addEventListener('click', function () { self.advance(id); });
      }
      var explain = step.querySelector('.step__explain');
      if (explain) {
        explain.addEventListener('click', function () { self.explain(id); });
      }
    });
  };

  function mount(root) {
    root = root || document.getElementById('resultRoot');
    if (!root || root.dataset.mounted === '1') return null;
    root.dataset.mounted = '1';

    var list = new Checklist(root);
    list.wire();
    list.render();

    var tally = document.getElementById('tally');
    if (tally && list.total > 0) {
      setTimeout(function () { tally.classList.add('is-visible'); }, 400);
    }

    // Keyboard: space toggles the focused document
    root.addEventListener('keydown', function (e) {
      if (e.key !== ' ' && e.key !== 'Enter') return;
      var step = e.target.closest ? e.target.closest('.step') : null;
      if (!step) return;
      if (e.target.tagName === 'BUTTON' || e.target.tagName === 'A') return;
      e.preventDefault();
      list.advance(step.getAttribute('data-item-id'));
    });

    return list;
  }

  global.KaagazInitChecklist = mount;
  global.KaagazKeyboard = wireKeyboard;
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { mount(); });
  } else {
    mount();
  }

  /* Keyboard shortcuts.
   *
   * `/` or Cmd/Ctrl-K focuses the search field, because the whole point of the
   * page is that you can ask about anything and the most likely next action is
   * typing. Escape blurs it again. Arrow keys walk the example chips and Enter
   * follows the focused one.
   *
   * Every handler is a no-op when the user is already typing, and none of them
   * steal a key from a modifier the browser or the OS needs. Arrow navigation is
   * suppressed while the search input has focus, because there the caret must
   * keep doing what the user expects.
   */
  function wireKeyboard() {
    if (document.body.dataset.keyboardWired === '1') return;
    document.body.dataset.keyboardWired = '1';

    var search = document.getElementById('transaction_type');

    document.addEventListener('keydown', function (e) {
      // True whenever the caret is in a field the user is typing into. Every
      // shortcut below defers to it, otherwise the app eats characters: pressing
      // "/" in the search box has to type a slash, not clear the box.
      var typing = isTextEntry(document.activeElement);

      // Cmd/Ctrl-K, or "/" on a US layout, jump to the search field, because
      // the whole point of the page is that you can ask about anything and the
      // most likely next action is typing. Cmd-K still works while typing,
      // since that combination is never text.
      if ((e.key === 'k' || e.key === 'K') && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        if (search) { search.focus(); search.select(); }
        return;
      }
      if (e.key === '/' && !e.metaKey && !e.ctrlKey && !e.altKey && !typing) {
        e.preventDefault();
        if (search) { search.focus(); search.select(); }
        return;
      }
      if (e.key === 'Escape' && document.activeElement === search && search) {
        search.blur();
        return;
      }

      if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp' &&
          e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      if (typing) return;                                  // let the caret move
      if (e.metaKey || e.ctrlKey || e.altKey) return;

      var chips = Array.prototype.slice.call(document.querySelectorAll('.chips .chip'));
      if (!chips.length) return;
      e.preventDefault();

      var current = chips.indexOf(document.activeElement);
      var forward = e.key === 'ArrowDown' || e.key === 'ArrowRight';
      var next = current === -1
        ? (forward ? 0 : chips.length - 1)
        : (current + (forward ? 1 : -1) + chips.length) % chips.length;
      chips[next].focus();
    });
  }

  function isTextEntry(el) {
    if (!el || !el.tagName) return false;
    var tag = el.tagName.toLowerCase();
    if (tag === 'input') {
      var type = (el.getAttribute('type') || 'text').toLowerCase();
      return ['text', 'search', 'url', 'email', 'tel', 'password', 'number']
        .indexOf(type) !== -1;
    }
    return tag === 'textarea' || tag === 'select' || el.isContentEditable === true;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', wireKeyboard);
  } else {
    wireKeyboard();
  }

}(window));
