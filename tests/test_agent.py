"""Offline tests: tools behave, and the agent loop wires tool calls and results correctly.

    python -m pytest -q tests      (or: python tests/test_agent.py)
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))

from agent.agent import SiteAgent  # noqa: E402
from agent.tools import find_county, get_county_profile, get_live_power_price, rank_counties, run_tool  # noqa: E402
from fake_client import FakeClient, text, tool  # noqa: E402


def test_find_county_cases():
    assert find_county("Loudoun")["county_fips"] == "51107"
    assert find_county("loudoun county", "Virginia")["county_fips"] == "51107"
    assert find_county("Washington")["status"] == "ambiguous"
    assert find_county("Anchorage", "AK")["status"] == "unsupported"
    assert find_county("Gotham")["status"] == "not_found"


def test_profile_and_rank():
    p = get_county_profile("48141")["profile"]
    assert p["county"] == "El Paso" and 0 <= p["model_score"] <= 1
    r = rank_counties(state="TX", max_price_cents=7, top_n=3)
    assert r["status"] == "ok" and len(r["counties"]) == 3
    assert all(c["industrial_price_cents"] <= 7 and c["has_data_center"] == 0 for c in r["counties"])
    assert rank_counties(min_population=50_000_000)["status"] == "no_results"


def test_price_fallback_without_key(monkeypatch=None):
    os.environ.pop("EIA_API_KEY", None)
    assert get_live_power_price("VA")["status"] == "fallback"


def test_tool_errors_are_json():
    assert json.loads(run_tool("nope", {}))["status"] == "error"
    assert json.loads(run_tool("get_county_profile", {"bad": 1}))["status"] == "error"


def test_agent_loop_runs_tools_then_returns_memo():
    client = FakeClient([
        [tool("find_county", {"name": "Loudoun", "state": "VA"}, 1)],
        [tool("get_county_profile", {"county_fips": "51107"}, 2), tool("get_grid_queue", {"county_fips": "51107"}, 3)],
        [text("## Recommendation\nAdvance Loudoun.")],
    ])
    res = SiteAgent(client=client, model="claude-sonnet-5-5").run("Screen Loudoun VA")
    assert res.stopped == "done" and res.memo.startswith("## Recommendation")
    assert [s.name for s in res.tool_calls] == ["find_county", "get_county_profile", "get_grid_queue"]
    # tool results were sent back with matching ids
    msgs = client.calls[-1]["messages"]  # same list the agent kept appending to
    last_user = msgs[-2]                 # tool results for the second round, just before the final answer
    assert last_user["role"] == "user" and {r["tool_use_id"] for r in last_user["content"]} == {"tu_2", "tu_3"}
    assert res.cost_usd > 0


def test_agent_step_limit():
    client = FakeClient([[tool("find_county", {"name": "Loudoun"}, i)] for i in range(5)])
    res = SiteAgent(client=client, max_steps=3).run("loop forever")
    assert res.stopped == "max_steps"




def test_eval_checks():
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "eval"))
    from run_eval import behavior, evaluate, grounding, has_sections
    from agent.agent import Result, Step
    memo = ("## Recommendation\nAdvance El Paso.\n## Comparison\n| County | Score |\n|---|---|\n| El Paso | 0.9281 (98.0th pct), 4.9¢, 873,331 people |\n"
            "## County notes\n- x\n## Risks and unknowns\n- y\n## Next diligence steps\n- z\n## Sources\n- EIA")
    trace = [Step("tool", "get_county_profile", {}, json.dumps({"model_score": 0.9281, "score_percentile": 98.0,
                                                                 "industrial_price_cents": 4.9, "population": 873331}))]
    res = Result(memo, trace, 1, 1, 1.0, "done", "claude-sonnet-5-5")
    case = {"request": "x", "expect": "memo", "required_tools": ["get_county_profile"]}
    r = evaluate(case, res)
    assert r["behavior_ok"] and r["tools_ok"] and r["sections_ok"] and r["grounded_share"] == 1.0
    share, bad = grounding("Power is 3.2¢ and the score is 0.9281", {0.9281}, "")
    assert share == 0.5 and bad == [3.2]
    assert behavior({"expect": "clarify"}, "Which Washington County did you mean?")
    assert behavior({"expect": "decline"}, "Our data only covers the contiguous US, so I can't screen Anchorage.")
    assert not has_sections("just text")


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok ", name)
