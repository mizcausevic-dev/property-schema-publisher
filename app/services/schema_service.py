from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any


def _clamp(value: float, low: int = 0, high: int = 100) -> int:
    return max(low, min(high, round(value)))


@dataclass(slots=True)
class PropertySchemaService:
    source_path: Path

    def load(self) -> dict[str, Any]:
        return json.loads(self.source_path.read_text(encoding="utf-8"))

    def brokerage_schema(self) -> dict[str, Any]:
        data = self.load()["brokerage"]
        return {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": data["name"],
            "url": data["url"],
            "telephone": data["phone"],
            "logo": data["logo"],
            "sameAs": data["same_as"],
        }

    def listing_schema(self, item: dict[str, Any]) -> dict[str, Any]:
        return {
            "@context": "https://schema.org",
            "@type": "RealEstateListing",
            "name": item["title"],
            "url": item["url"],
            "datePosted": "2026-05-12",
            "offers": {
                "@type": "Offer",
                "price": item["price"],
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock",
            },
            "mainEntity": {
                "@type": item["property_type"],
                "name": item["title"],
                "numberOfRooms": item["bedrooms"],
                "floorSize": {
                    "@type": "QuantitativeValue",
                    "value": item["sqft"],
                    "unitCode": "FTK"
                },
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": item["address"],
                    "addressLocality": item["city"],
                    "addressRegion": item["state"],
                    "postalCode": item["postal_code"],
                    "addressCountry": "US"
                }
            },
            "provider": {
                "@type": "RealEstateAgent",
                "name": item["agent_name"],
            }
        }

    def score_listing(self, item: dict[str, Any]) -> dict[str, Any]:
        schema_score = _clamp(
            item["description_quality"] * 0.24
            + item["faq_count"] * 5.2
            + item["entity_links"] * 4.0
            + item["image_count"] * 0.75
            + (9 if item["neighborhood_guide"] else 0)
            + (7 if item["school_info"] else 0)
            + (5 if item["transit_info"] else 0)
        )
        readiness = (
            "publish"
            if schema_score >= 78
            else "improve"
            if schema_score >= 56
            else "rewrite"
        )
        missing = []
        if item["faq_count"] < 3:
            missing.append("faq coverage")
        if not item["school_info"]:
            missing.append("school context")
        if not item["neighborhood_guide"]:
            missing.append("neighborhood guide")
        if item["entity_links"] < 4:
            missing.append("entity linkage")
        if item["image_count"] < 12:
            missing.append("image depth")

        next_action = (
            "Publish the schema pack now and syndicate the listing manifest into AI-readable discovery surfaces."
            if readiness == "publish"
            else "Add missing context blocks and rebuild the FAQ and entity layer before republishing."
            if readiness == "improve"
            else "Rewrite the page with a fuller neighborhood, school, and intent-answer structure before trusting it in AI search."
        )

        return {
            "listingId": item["listing_id"],
            "title": item["title"],
            "city": item["city"],
            "price": item["price"],
            "propertyType": item["property_type"],
            "schemaReadinessScore": schema_score,
            "status": readiness,
            "missingSignals": missing,
            "nextAction": next_action,
            "schema": self.listing_schema(item),
        }

    def listings(self) -> list[dict[str, Any]]:
        return sorted(
            [self.score_listing(item) for item in self.load()["properties"]],
            key=lambda item: (-item["schemaReadinessScore"], item["title"]),
        )

    def listing(self, listing_id: str) -> dict[str, Any] | None:
        for item in self.listings():
            if item["listingId"] == listing_id:
                return item
        return None

    def summary(self) -> dict[str, Any]:
        data = self.load()
        listings = self.listings()
        avg_score = mean(item["schemaReadinessScore"] for item in listings)
        publish = [item for item in listings if item["status"] == "publish"]
        rewrite = [item for item in listings if item["status"] == "rewrite"]
        return {
            "brokerage": data["brokerage"]["name"],
            "listingCount": len(listings),
            "averageSchemaReadinessScore": round(avg_score, 1),
            "publishReadyCount": len(publish),
            "rewriteCount": len(rewrite),
            "leadRecommendation": (
                "Push the strongest Cambridge and Newton listings into AI-facing schema packs now, then repair thin FAQ and entity coverage on the lower-signal inventory before syndication."
            ),
        }

    def sample_payload(self) -> dict[str, Any]:
        listings = self.listings()
        return {
            "dashboard": self.summary(),
            "manifests": [
                {
                    "listingId": item["listingId"],
                    "title": item["title"],
                    "schemaReadinessScore": item["schemaReadinessScore"],
                    "status": item["status"],
                    "missingSignals": item["missingSignals"],
                }
                for item in listings[:3]
            ],
        }


def build_service(root: Path | None = None) -> PropertySchemaService:
    base = root or Path(__file__).resolve().parents[2]
    return PropertySchemaService(base / "app" / "data" / "sample_properties.json")
