"""
Kaagaz — research job registry.

A cold research call takes 15-40 seconds. Section 5 of the brief requires that
latency be *shown*, not hidden behind a spinner, so the browser starts the work
and then polls for progress while the flip-board flips through real stage names
and real source URLs.

Threading note: this works on the Flask dev server and any WSGI server with
threads (gunicorn --threads, waitress). It degrades safely when it cannot —
`JOB_DEAD_AFTER` seconds after a job is created with no progress, the polling
request runs the research inline instead and returns the finished result, so a
single-threaded or serverless runtime still produces a correct answer, just
without the live progress feed.
"""

import threading
import time
import uuid

# A job with no progress at all for this long is presumed dead (thread did not
# survive, or the runtime froze the worker). The poll then runs it inline.
JOB_DEAD_AFTER = 3.0
# Hard ceiling on how long we will keep reporting "running".
JOB_MAX_SECONDS = 180

_jobs = {}
_lock = threading.Lock()


def _new_job(req):
    return {
        "id": uuid.uuid4().hex[:12],
        "request": dict(req),
        "status": "running",   # running | done | error
        "stages": [],          # [{label, detail, at}]
        "citations": [],
        "started_at": time.time(),
        "touched_at": time.time(),
        "result": None,
        "error": None,
        "inline": False,
    }


def create(req):
    job = _new_job(req)
    with _lock:
        _jobs[job["id"]] = job
    return job


def get(job_id):
    with _lock:
        return _jobs.get(job_id)


def add_stage(job, label, detail=""):
    with _lock:
        job["stages"].append(
            {"label": label, "detail": detail, "at": round(time.time() - job["started_at"], 2)}
        )
        job["touched_at"] = time.time()
        del job["stages"][:-12]  # keep the last dozen; the UI only shows a few


def set_citations(job, citations):
    with _lock:
        job["citations"] = list(citations or [])
        job["touched_at"] = time.time()


def finish(job, result):
    with _lock:
        job["result"] = result
        job["status"] = "done"
        job["touched_at"] = time.time()


def fail(job, message, kind="search_unavailable", retryable=True, suggestions=None):
    with _lock:
        job["status"] = "error"
        job["error"] = {"message": message, "kind": kind, "retryable": retryable,
                        "suggestions": suggestions or []}
        job["touched_at"] = time.time()


def public(job):
    """Snapshot for the polling endpoint. Never leaks the raw job object."""
    if job is None:
        return None
    elapsed = round(time.time() - job["started_at"], 1)
    latest = job["stages"][-1] if job["stages"] else None
    return {
        "id": job["id"],
        "status": job["status"],
        "stages": job["stages"],
        "latest": latest,
        "citations": job["citations"],
        "elapsed": elapsed,
        "inline": job["inline"],
    }


def run_async(app, job, worker):
    """Run `worker(app, job)` on a daemon thread, recording the outcome.

    A failure to even start the thread is not fatal: the job stays in
    `running`, goes stale after JOB_DEAD_AFTER, and the poller takes over.
    """

    def target():
        try:
            worker(app, job)
        except Exception as exc:  # noqa: BLE001 — must never kill the thread silently
            fail(job, f"Research failed unexpectedly ({type(exc).__name__}).")

    try:
        t = threading.Thread(target=target, daemon=True,
                             name="kaagaz-research-" + job["id"][:6])
        t.start()
    except Exception:
        pass  # poller will take over
    return job


def reap(max_age=600):
    """Drop finished jobs older than `max_age` seconds so the dict can't grow."""
    cutoff = time.time() - max_age
    with _lock:
        for job_id in [k for k, v in _jobs.items() if v["touched_at"] < cutoff]:
            del _jobs[job_id]
