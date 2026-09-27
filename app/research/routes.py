"""
Kaagaz — research API.

  GET  /api/research/options      — reference data for the picker
  POST /api/research/ask          — cache-first answer, synchronous
  POST /api/research/start        — begin a job, return its id immediately
  GET  /api/research/status/<id>  — poll for progress; runs inline if the
                                    background thread did not survive
  GET  /api/research/cache        — cache stats (judges ask about this)
  GET  /api/research/entries      — what we have pre-warmed
"""

import time

from flask import Blueprint, current_app, jsonify, request

from . import agent, cache as cache_mod, jobs, refdata
from .search import SearchError

research_bp = Blueprint("research_bp", __name__)


@research_bp.route("/options")
def options():
    return jsonify({
        "banks": [{"name": n, "group": g} for n, g in refdata.bank_options()],
        "states": sorted(set(refdata.STATES.values())),
        "categories": [
            {"value": c, "label": refdata.CATEGORIES.get(c, c)}
            for c in refdata.POPULAR_CATEGORIES
        ],
        "residency": [
            {"value": k, "label": refdata.RESIDENCY[k]["label"],
             "blurb": refdata.RESIDENCY[k]["blurb"]}
            for k in refdata.RESIDENCY_ORDER
        ],
    })


@research_bp.route("/ask", methods=["POST"])
def ask():
    req = request.get_json(force=True, silent=True) or {}
    try:
        result = agent.answer(current_app._get_current_object(), req)
    except agent.ResearchFailed as exc:
        return jsonify({"error": exc.message, "kind": exc.kind,
                        "retryable": exc.retryable}), 503
    return jsonify(result)


@research_bp.route("/start", methods=["POST"])
def start():
    req = request.get_json(force=True, silent=True) or {}
    try:
        agent.parse_request(req)
    except agent.ResearchFailed as exc:
        return jsonify({"error": exc.message, "kind": exc.kind,
                        "retryable": exc.retryable}), 400

    app = current_app._get_current_object()
    job = jobs.create(req)
    jobs.run_async(app, job, _worker)
    return jsonify({"job_id": job["id"]}), 202


def _worker(app, job):
    def on_stage(label, detail=""):
        jobs.add_stage(job, label, detail)

    try:
        result = agent.answer(app, job["request"], on_stage=on_stage)
        jobs.finish(job, result)
    except agent.ResearchFailed as exc:
        jobs.fail(job, exc.message, exc.kind, exc.retryable)
    except SearchError as exc:
        jobs.fail(job, "We couldn't reach the research service just now.")


@research_bp.route("/status/<job_id>")
def status(job_id):
    app = current_app._get_current_object()
    job = jobs.get(job_id)
    if job is None:
        return jsonify({"error": "Unknown job"}), 404

    snapshot = jobs.public(job)

    # Background thread did not survive (serverless / single-threaded WSGI):
    # take the work over inline so the user still gets a real answer.
    if job["status"] == "running":
        idle = time.time() - job["touched_at"]
        if idle > jobs.JOB_DEAD_AFTER or time.time() - job["started_at"] > jobs.JOB_MAX_SECONDS:
            job["inline"] = True
            jobs.add_stage(job, "Researching on this connection", "no background worker available")
            _worker(app, job)
            snapshot = jobs.public(job)

    if job["status"] == "done":
        return jsonify({"status": "done", "result": job["result"],
                        "stages": job["stages"], "citations": job["citations"],
                        "elapsed": snapshot["elapsed"], "inline": job["inline"]})
    if job["status"] == "error":
        return jsonify({"status": "error", "error": job["error"],
                        "stages": job["stages"],
                        "elapsed": snapshot["elapsed"]}), 200

    return jsonify({"status": "running", "stages": job["stages"],
                    "latest": snapshot["latest"], "citations": job["citations"],
                    "elapsed": snapshot["elapsed"], "inline": job["inline"]})


@research_bp.route("/cache")
def cache_stats():
    return jsonify(cache_mod.stats(current_app._get_current_object()))


@research_bp.route("/entries")
def cache_entries():
    limit = request.args.get("limit", default=200, type=int)
    return jsonify(cache_mod.list_entries(
        current_app._get_current_object(), limit=min(limit, 500)))
