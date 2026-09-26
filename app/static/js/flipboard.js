/**
 * Kaagaz — flipboard.js
 * Split-flap / departure-board animation engine.
 * No external dependencies. Exposes window.KaagazFlip.
 */
(function (global) {
  'use strict';

  /* ═══════════════════════════════════════════════════
     FlipNumber
     Animates a numeric element through random interim
     values before landing on a target, like an airport
     departure board.
  ═══════════════════════════════════════════════════ */
  function FlipNumber(el) {
    if (!el) throw new Error('FlipNumber: element is required');
    this.el    = el;
    this.value = parseInt(el.dataset.value || el.textContent || '0', 10);
    this._timer = null;
  }

  FlipNumber.prototype.animateTo = function (newValue) {
    var self   = this;
    var steps  = 7;  // number of random flicker frames
    var step   = 0;
    var delay  = 60; // ms per frame

    // Clear any in-flight animation
    if (self._timer) clearInterval(self._timer);

    self._timer = setInterval(function () {
      if (step < steps - 1) {
        // Show a random value, biased towards plausible range
        self.el.textContent = Math.floor(Math.random() * (Math.max(newValue, 20) + 1));
        step++;
      } else {
        self.el.textContent = newValue;
        self.value          = newValue;
        clearInterval(self._timer);
        self._timer = null;
      }
    }, delay);
  };

  /* ═══════════════════════════════════════════════════
     FlipStatus
     Animates a status badge through a CSS 3D flip when
     the state changes.
  ═══════════════════════════════════════════════════ */
  var STATUS_LABELS = {
    pending:     'PENDING',
    in_progress: 'IN PROGRESS',
    done:        'DONE'
  };

  function FlipStatus(el) {
    if (!el) throw new Error('FlipStatus: element is required');
    this.el    = el;
    this.state = el.dataset.state || 'pending';
  }

  FlipStatus.prototype.transitionTo = function (newState) {
    var self = this;
    self.el.classList.add('flipping');
    setTimeout(function () {
      self.el.dataset.state = newState;
      self.el.textContent   = STATUS_LABELS[newState] || newState;
      self.state            = newState;
      self.el.classList.remove('flipping');
    }, 200);
  };

  /* ═══════════════════════════════════════════════════
     Registry — keep one instance per DOM id
  ═══════════════════════════════════════════════════ */
  var _flipNumbers = {};  // id → FlipNumber instance
  var _flipStatuses = {}; // item-id → FlipStatus instance

  function getOrCreateFlipNumber(id) {
    if (!_flipNumbers[id]) {
      var el = document.getElementById(id);
      if (!el) return null;
      _flipNumbers[id] = new FlipNumber(el);
    }
    return _flipNumbers[id];
  }

  function getOrCreateFlipStatus(itemId) {
    if (!_flipStatuses[itemId]) {
      var el = document.querySelector('.flip-status[data-item-id="' + itemId + '"]');
      if (!el) return null;
      _flipStatuses[itemId] = new FlipStatus(el);
    }
    return _flipStatuses[itemId];
  }

  /* ═══════════════════════════════════════════════════
     Public API — window.KaagazFlip
  ═══════════════════════════════════════════════════ */
  var KaagazFlip = {
    /**
     * Animate a flip-number element to a new value.
     * @param {string} id        — DOM element id (e.g. 'doneCount')
     * @param {number} newValue
     */
    animateNumber: function (id, newValue) {
      var fn = getOrCreateFlipNumber(id);
      if (fn) fn.animateTo(newValue);
    },

    /**
     * Transition a status badge element.
     * @param {Element|string} elOrItemId — element or data-item-id value
     * @param {string}         newState   — 'pending' | 'in_progress' | 'done'
     */
    transitionStatus: function (elOrItemId, newState) {
      if (typeof elOrItemId === 'string') {
        var fs = getOrCreateFlipStatus(elOrItemId);
        if (fs) fs.transitionTo(newState);
      } else if (elOrItemId && elOrItemId.nodeType) {
        // Element passed directly
        var itemId = elOrItemId.dataset.itemId;
        if (itemId && !_flipStatuses[itemId]) {
          _flipStatuses[itemId] = new FlipStatus(elOrItemId);
        }
        var instance = itemId ? _flipStatuses[itemId] : new FlipStatus(elOrItemId);
        instance.transitionTo(newState);
      }
    },

    /* Expose constructors for advanced use */
    FlipNumber: FlipNumber,
    FlipStatus: FlipStatus
  };

  /* ═══════════════════════════════════════════════════
     DOM-ready initialisation
     (checklist.html also wires up its own handlers;
      flipboard.js handles only the animation layer)
  ═══════════════════════════════════════════════════ */
  function onReady(fn) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', fn);
    } else {
      fn();
    }
  }

  onReady(function () {

    /* 1. Animate the total counter on page load (checklist page only) */
    var totalEl = document.getElementById('totalCount');
    if (totalEl) {
      var totalValue = parseInt(totalEl.dataset.value || totalEl.textContent || '0', 10);
      // Small delay so the user sees it "tick in"
      setTimeout(function () {
        KaagazFlip.animateNumber('totalCount', totalValue);
      }, 300);
    }

    /* 2. Wire up mark-done buttons for flip-board progress
          NOTE: checklist.html has its own state-machine for cycling
          pending → in_progress → done → pending.
          flipboard.js does NOT duplicate that logic — it only
          provides animation helpers that checklist.html calls via
          window.KaagazFlip.
    */

    /* 3. Details-panel toggles
          Also handled in checklist.html inline script, but we add
          a fallback here in case flipboard.js is loaded on other pages.
    */
    var detailToggles = document.querySelectorAll('.details-toggle');
    detailToggles.forEach(function (btn) {
      if (btn.dataset.fbInitialised) return; // already wired by page script
      btn.dataset.fbInitialised = '1';
      btn.addEventListener('click', function () {
        var targetId = btn.dataset.target;
        var panel    = targetId ? document.getElementById(targetId) : null;
        if (!panel) return;
        var expanded = panel.classList.toggle('expanded');
        btn.setAttribute('aria-expanded', expanded ? 'true' : 'false');
        btn.textContent = expanded ? 'Hide details ▴' : 'Show details ▾';
      });
    });

    /* 4. AI Explainer toggle
          Also handled in checklist.html, but provided as fallback.
    */
    var explainBtns = document.querySelectorAll('.explain-btn');
    explainBtns.forEach(function (btn) {
      if (btn.dataset.fbInitialised) return;
      btn.dataset.fbInitialised = '1';

      btn.addEventListener('click', function () {
        var id        = btn.dataset.itemId;
        var term      = btn.dataset.term;
        var txType    = btn.dataset.txType;
        var box       = id ? document.getElementById('explainer-' + id) : null;
        if (!box) return;

        var noteEl    = document.getElementById('explainer-note-' + id);
        var contentEl = box.querySelector('.ai-explainer__content');

        if (box.classList.contains('visible')) {
          box.classList.remove('visible');
          btn.textContent = 'What is this?';
          return;
        }

        box.classList.remove('loaded');
        box.classList.add('visible', 'loading');
        if (contentEl) contentEl.textContent = 'Consulting the Kaagaz knowledge base\u2026';
        if (noteEl)    noteEl.textContent     = '';
        btn.textContent = 'Hide explanation';

        fetch('/api/ai/explain', {
          method:  'POST',
          headers: { 'Content-Type': 'application/json' },
          body:    JSON.stringify({ term: term, transaction_type: txType })
        })
        .then(function (res) {
          if (!res.ok) throw new Error('HTTP ' + res.status);
          return res.json();
        })
        .then(function (data) {
          box.classList.remove('loading');
          box.classList.add('loaded');
          if (contentEl) contentEl.textContent = data.explanation || 'No explanation available.';
          if (noteEl) {
            noteEl.textContent = data.source === 'static_fallback'
              ? 'Live AI explanation temporarily unavailable \u2014 showing database entry.'
              : '';
          }
        })
        .catch(function () {
          box.classList.remove('loading');
          if (contentEl) contentEl.textContent = 'Unable to load explanation. Please try again.';
          if (noteEl)    noteEl.textContent     = '';
        });
      });
    });

  }); // end onReady

  /* ═══════════════════════════════════════════════════
     Export
  ═══════════════════════════════════════════════════ */
  global.KaagazFlip = KaagazFlip;

}(window));
