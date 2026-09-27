/**
 * Kaagaz — flipboard.js
 *
 * The signature component. Two jobs:
 *
 *   1. Render a number as fixed-width split-flap digit cells. The cells are
 *      sized in `ch` units off a monospace face, so 1 and 8 occupy exactly the
 *      same width and the board cannot shift when a value goes 9 -> 10 -> 11.
 *      This is the whole anti-jitter mechanism and it is why the digit width is
 *      NOT set in px.
 *
 *   2. Drive the "researching" face of the board from real pipeline progress.
 *      Stage names and source URLs are what the server actually produced; the
 *      board never invents a message to fill a wait.
 *
 * No dependencies. Exposes window.KaagazFlip.
 */
(function (global) {
  'use strict';

  var REDUCED = global.matchMedia &&
                global.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ══════════════════════════════════════════════════════════════
     FlipNumber
     ══════════════════════════════════════════════════════════════ */
  function FlipNumber(el, opts) {
    opts = opts || {};
    this.el       = el;
    this.minWidth = opts.minWidth || 1;   // always render at least one cell
    this.cells    = [];
    this._build();
  }

  FlipNumber.prototype._build = function () {
    this.el.classList.add('flip');
    this.el.textContent = '';
    this.el.setAttribute('aria-hidden', 'true');
  };

  /** Ensure exactly n cells exist; reuse them so the DOM is never churned. */
  FlipNumber.prototype._ensureCells = function (n) {
    while (this.cells.length < n) {
      var c = document.createElement('span');
      c.className = 'flip__cell';
      this.el.appendChild(c);
      this.cells.push(c);
    }
    while (this.cells.length > n) {
      this.el.removeChild(this.cells.pop());
    }
  };

  /**
   * Render a value. Pads with spaces so the board does not change width when
   * the digit count changes — the cell count is pinned to the widest value the
   * board has ever been asked to show.
   */
  FlipNumber.prototype.set = function (value, opts) {
    opts = opts || {};
    var text = String(value == null ? '' : value);

    // Empty slot for a number we do not have yet (e.g. total before load).
    if (text === '') text = ' ';

    this.minWidth = Math.max(this.minWidth, text.length);
    var padded = text.padStart(this.minWidth, ' ');

    this._ensureCells(padded.length);
    for (var i = 0; i < padded.length; i++) {
      var ch = padded.charAt(i);
      var cell = this.cells[i];
      var next = ch === ' ' ? ' ' : ch;
      if (cell.textContent === next) continue;
      cell.textContent = next;
      cell.setAttribute('data-empty', ch === ' ' ? 'true' : 'false');
      if (!REDUCED && !opts.silent) {
        cell.classList.remove('is-flipping');
        // Force reflow so the animation restarts on a repeated digit.
        void cell.offsetWidth;
        cell.classList.add('is-flipping');
      }
    }
  };

  /** Pad the board out to a known width so it never grows mid-demo. */
  FlipNumber.prototype.reserve = function (digits) {
    this.minWidth = Math.max(this.minWidth, digits);
    this.set('', { silent: true });
  };

  /* ══════════════════════════════════════════════════════════════
     StatusBadge
     Fixed width (CSS min-width) so a badge going PENDING -> DONE
     cannot reflow the row it sits in.
     ══════════════════════════════════════════════════════════════ */
  var STATUS_LABELS = {
    pending:     'Pending',
    in_progress: 'In progress',
    done:        'Done'
  };

  function StatusBadge(el) {
    this.el    = el;
    this.state = el.getAttribute('data-state') || 'pending';
  }

  StatusBadge.prototype.set = function (next) {
    if (!STATUS_LABELS[next]) return;
    var self = this;
    var apply = function () {
      self.el.setAttribute('data-state', next);
      self.el.textContent = STATUS_LABELS[next];
      self.state = next;
      self.el.classList.remove('is-flipping');
    };
    if (REDUCED) { apply(); return; }
    self.el.classList.add('is-flipping');
    setTimeout(apply, 150);
  };

  /* ══════════════════════════════════════════════════════════════
     Ticker — the researching face
     ══════════════════════════════════════════════════════════════ */
  function Ticker(root) {
    this.root    = root;
    this.textEl  = root.querySelector('[data-ticker-text]');
    this.foundEl = root.querySelector('[data-ticker-found]');
    this._seen    = {};
    this._pills   = {};
  }

  Ticker.prototype.say = function (label, detail) {
    if (!this.textEl) return;
    var text = detail ? (label + ' — ' + detail) : label;
    if (text === this.textEl.textContent) return;
    this.textEl.textContent = text;
    if (!REDUCED) {
      this.textEl.classList.remove('is-entering');
      void this.textEl.offsetWidth;
      this.textEl.classList.add('is-entering');
    }
  };

  /** Reveal a source host as the search step actually returns it. */
  Ticker.prototype.found = function (urls) {
    if (!this.foundEl || !urls || !urls.length) return;
    for (var i = 0; i < urls.length; i++) {
      var url = urls[i];
      if (!url || this._seen[url]) continue;
      this._seen[url] = true;

      var host = '';
      try { host = new URL(url).hostname.replace(/^www\./, ''); }
      catch (e) { host = url.slice(0, 28); }

      var pill = document.createElement('span');
      pill.className = 'found__pill';
      pill.appendChild(document.createTextNode(host));
      this.foundEl.appendChild(pill);
      this._pills[url] = pill;
    }
  };

  Ticker.prototype.clear = function () {
    this._seen = {};
    if (this.foundEl) this.foundEl.textContent = '';
  };

  /* ══════════════════════════════════════════════════════════════
     Research driver
     Starts a job, polls for real progress, resolves with the answer.
     ══════════════════════════════════════════════════════════════ */
  function Research(onProgress) {
    this.onProgress = onProgress || function () {};
    this.jobId = null;
    this.timer = null;
    this.pollMs = 600;
    this.elapsedTimer = null;
  }

  Research.prototype._emit = function (payload) {
    try { this.onProgress(payload); } catch (e) { /* never let a callback break polling */ }
  };

  Research.prototype.start = function (request) {
    var self = this;
    this.stop();
    this._emit({ phase: 'starting' });

    return fetch('/api/research/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request)
    })
      .then(function (res) {
        return res.json().then(function (body) {
          if (!res.ok) throw new Error(body.error || 'Could not start research.');
          return body;
        });
      })
      .then(function (body) {
        self.jobId = body.job_id;
        self._emit({ phase: 'running', job_id: body.job_id });
        self.elapsedTimer = setInterval(function () {
          self._emit({ phase: 'tick' });
        }, 1000);
        return self._poll();
      });
  };

  Research.prototype._poll = function () {
    var self = this;
    return fetch('/api/research/status/' + this.jobId, {
      headers: { 'Accept': 'application/json' }
    })
      .then(function (res) { return res.json(); })
      .then(function (body) {
        if (body.status === 'done') {
          self.stop();
          return body.result;
        }
        if (body.status === 'error') {
          self.stop();
          var err = new Error((body.error && body.error.message) ||
                              'Research could not be completed.');
          err.kind = body.error && body.error.kind;
          err.retryable = !body.error || body.error.retryable !== false;
          throw err;
        }
        // still working — report what is genuinely true, then poll again
        var stages = body.stages || [];
        var latest = body.latest ||
                     (stages.length ? stages[stages.length - 1] : null);
        self._emit({
          phase: 'running',
          stage: latest ? latest.label : 'Researching',
          detail: latest ? latest.detail : '',
          stages: stages,
          citations: body.citations || [],
          elapsed: body.elapsed
        });
        if (body.citations && body.citations.length) {
          self._emit({ phase: 'citations', citations: body.citations });
        }
        return new Promise(function (resolve) {
          self.timer = setTimeout(function () { resolve(self._poll()); }, self.pollMs);
        });
      })
      .catch(function (err) {
        self.stop();
        throw err;
      });
  };

  Research.prototype.stop = function () {
    if (this.timer) { clearTimeout(this.timer); this.timer = null; }
    if (this.elapsedTimer) { clearInterval(this.elapsedTimer); this.elapsedTimer = null; }
  };

  /* ══════════════════════════════════════════════════════════════
     Registry + public API
     ══════════════════════════════════════════════════════════════ */
  var _numbers = {};

  function flipNumber(id) {
    if (!_numbers[id]) {
      var el = document.getElementById(id);
      if (!el) return null;
      _numbers[id] = new FlipNumber(el, { minWidth: parseInt(el.getAttribute('data-min'), 10) || 1 });
    }
    return _numbers[id];
  }

  var KaagazFlip = {
    FlipNumber: FlipNumber,
    StatusBadge: StatusBadge,
    Ticker: Ticker,
    Research: Research,

    /** @param {string} id @param {number|string} value */
    setNumber: function (id, value, opts) {
      var fn = flipNumber(id);
      if (fn) fn.set(value, opts);
    },

    /** Pin a board's width so it never grows mid-interaction. */
    reserve: function (id, digits) {
      var fn = flipNumber(id);
      if (fn) fn.reserve(digits);
    },

    setStatus: function (el, next) {
      if (typeof el === 'string') {
        el = document.querySelector('.status[data-item-id="' + el + '"]');
      }
      if (el) new StatusBadge(el).set(next);
    },

    ticker: function (root) {
      root = typeof root === 'string' ? document.querySelector(root) : root;
      return root ? new Ticker(root) : null;
    },

    research: function (onProgress) {
      return new Research(onProgress);
    }
  };

  global.KaagazFlip = KaagazFlip;

}(window));
