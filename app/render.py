from __future__ import annotations

import html
from pathlib import Path

from app.services.schema_service import build_service

service = build_service()


def page_shell(title: str, eyebrow: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --bg: #09111d;
      --panel: #101d2f;
      --panel-2: #17263c;
      --line: #29486f;
      --ink: #f3ecde;
      --muted: #b5c2d7;
      --blue: #6db2ff;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background:
        radial-gradient(circle at top left, rgba(54, 103, 164, 0.18), transparent 30%),
        linear-gradient(180deg, #08111c 0%, #0b1522 100%);
      color: var(--ink);
      font-family: Georgia, "Times New Roman", serif;
    }}
    .frame {{
      width: 1440px;
      min-height: 920px;
      margin: 0 auto;
      padding: 48px;
    }}
    .shell {{
      background: rgba(13, 24, 39, 0.94);
      border: 1px solid var(--line);
      border-radius: 36px;
      padding: 34px 36px 36px;
    }}
    .eyebrow {{
      margin: 0 0 22px;
      font: 700 13px/1.2 "Segoe UI", sans-serif;
      letter-spacing: 0.35em;
      text-transform: uppercase;
      color: var(--blue);
    }}
    h1 {{
      margin: 0;
      font-size: 70px;
      line-height: 1.02;
      max-width: 1180px;
      letter-spacing: -0.05em;
    }}
    p.lead {{
      margin: 24px 0 0;
      max-width: 1060px;
      color: var(--muted);
      font: 400 19px/1.55 "Segoe UI", sans-serif;
    }}
    .pills {{
      display: flex;
      gap: 14px;
      flex-wrap: wrap;
      margin: 22px 0 26px;
    }}
    .pill {{
      background: #1d2d45;
      border: 1px solid #335a8d;
      color: #f5f7fb;
      padding: 10px 16px;
      border-radius: 999px;
      font: 700 15px/1 "Segoe UI", sans-serif;
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 18px;
      margin: 8px 0 34px;
    }}
    .card {{
      background: var(--panel-2);
      border: 1px solid #335885;
      border-radius: 24px;
      padding: 22px 22px 18px;
      min-height: 170px;
    }}
    .card h2 {{
      margin: 0 0 12px;
      color: #a8cbff;
      font: 700 12px/1.2 "Segoe UI", sans-serif;
      letter-spacing: 0.24em;
      text-transform: uppercase;
    }}
    .metric {{
      font-size: 58px;
      line-height: 1;
      margin: 0 0 10px;
    }}
    .card p, .card li, .table, .lane {{
      color: var(--muted);
      font: 400 18px/1.45 "Segoe UI", sans-serif;
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: 1.2fr 0.9fr;
      gap: 18px;
    }}
    .table {{
      display: grid;
      gap: 12px;
    }}
    .row {{
      display: grid;
      grid-template-columns: 1.1fr 0.75fr 0.8fr 0.95fr;
      gap: 14px;
      align-items: center;
      padding: 16px 18px;
      background: #0c1728;
      border: 1px solid #223c5d;
      border-radius: 18px;
    }}
    .row strong {{
      color: var(--ink);
      display: block;
      font: 700 24px/1.1 Georgia, serif;
    }}
    .small {{
      font-size: 15px;
      color: #87a2c7;
    }}
    .lane {{
      padding: 16px 18px;
      background: #0c1728;
      border: 1px solid #223c5d;
      border-radius: 18px;
      margin-bottom: 12px;
    }}
    .lane strong {{
      display: block;
      color: var(--ink);
      font: 700 24px/1.15 Georgia, serif;
      margin-bottom: 6px;
    }}
    pre {{
      margin: 0;
      color: #d7e8ff;
      font: 16px/1.5 Consolas, monospace;
      white-space: pre-wrap;
    }}
  </style>
</head>
<body>
  <div class="frame">
    <div class="shell">
      <p class="eyebrow">{html.escape(eyebrow)}</p>
      {body}
    </div>
  </div>
</body>
</html>"""


def render_overview() -> str:
    summary = service.summary()
    listings = service.listings()[:3]
    rows = "".join(
        f"""
        <div class="row">
          <div>
            <strong>{html.escape(item['title'])}</strong>
            <div class="small">{html.escape(item['city'])} · {html.escape(item['propertyType'])}</div>
          </div>
          <div>{item['schemaReadinessScore']}</div>
          <div>{html.escape(item['status'])}</div>
          <div>{html.escape(', '.join(item['missingSignals'][:2]) if item['missingSignals'] else 'none')}</div>
        </div>
        """
        for item in listings
    )
    body = f"""
      <h1>Turn every listing into a structured entity package AI systems and search engines can actually understand.</h1>
      <p class="lead">
        Property Schema Publisher generates listing schema, brokerage entities, FAQ-ready content signals, and AI-readable manifests
        so brokerages can improve discovery before the lead ever arrives.
      </p>
      <div class="pills">
        <div class="pill">real estate listing schema</div>
        <div class="pill">faq and entity readiness</div>
        <div class="pill">ai-readable listing manifests</div>
        <div class="pill">publish vs rewrite scoring</div>
      </div>
      <div class="stats">
        <div class="card"><h2>listings modeled</h2><div class="metric">{summary['listingCount']}</div><p>Inventory evaluated for schema and AI-readiness quality.</p></div>
        <div class="card"><h2>avg. schema score</h2><div class="metric">{summary['averageSchemaReadinessScore']}</div><p>Composite of content depth, FAQ coverage, entity links, and context quality.</p></div>
        <div class="card"><h2>publish ready</h2><div class="metric">{summary['publishReadyCount']}</div><p>Listings already strong enough for syndication into structured discovery surfaces.</p></div>
        <div class="card"><h2>rewrite needed</h2><div class="metric">{summary['rewriteCount']}</div><p>{html.escape(summary['leadRecommendation'])}</p></div>
      </div>
      <div class="grid-2">
        <div class="card"><h2>schema queue</h2><div class="table">{rows}</div></div>
        <div class="card"><h2>lead recommendation</h2><p>{html.escape(summary['leadRecommendation'])}</p></div>
      </div>
    """
    return page_shell("Property Schema Publisher", "Property Schema Publisher", body)


def render_manifest() -> str:
    listing = service.listing("lst-3003") or service.listings()[0]
    body = f"""
      <h1>Each listing can ship with a schema pack that explains the property, the place, the offer, and the agent context together.</h1>
      <p class="lead">
        Instead of thin markup blobs, the manifest ties the listing to a usable entity structure that search and AI systems can interpret more confidently.
      </p>
      <div class="card">
        <h2>{html.escape(listing['title'])}</h2>
        <pre>{html.escape(str(listing['schema']))}</pre>
      </div>
    """
    return page_shell("Listing Manifest", "Schema Manifest", body)


def render_fix_queue() -> str:
    listings = [item for item in service.listings() if item["missingSignals"]]
    cards = "".join(
        f"""
        <div class="lane">
          <strong>{html.escape(item['title'])}</strong>
          <div>Missing: {html.escape(', '.join(item['missingSignals']))}</div>
          <div class="small">{html.escape(item['nextAction'])}</div>
        </div>
        """
        for item in listings
    )
    body = f"""
      <h1>The fix queue makes weak listings obvious before they underperform in organic and AI-driven discovery.</h1>
      <p class="lead">
        Missing school context, weak FAQs, thin neighborhood coverage, and poor entity linkage are all surfaced as concrete repair work instead of buried SEO theory.
      </p>
      <div class="card">
        <h2>repair queue</h2>
        {cards}
      </div>
    """
    return page_shell("Repair Queue", "Repair Queue", body)


def render_api_summary() -> str:
    payload = service.sample_payload()
    body = f"""
      <h1>The API exposes readiness scores and manifests in a shape that listing teams and publishing systems can use immediately.</h1>
      <p class="lead">
        The dashboard summary and manifest queue stay close together so marketing and listing ops can decide what to publish, improve, or rewrite.
      </p>
      <div class="card">
        <h2>sample payload</h2>
        <pre>{html.escape(str(payload))}</pre>
      </div>
    """
    return page_shell("API Summary", "API Summary", body)


def write_static_proof_pages(output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    pages = {
        "01-overview.html": render_overview(),
        "02-manifest.html": render_manifest(),
        "03-fix-queue.html": render_fix_queue(),
        "04-api-summary.html": render_api_summary(),
    }
    written: list[Path] = []
    for name, contents in pages.items():
        path = output_dir / name
        path.write_text(contents, encoding="utf-8")
        written.append(path)
    return written
