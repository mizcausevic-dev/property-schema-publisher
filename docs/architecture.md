# Architecture

Property Schema Publisher treats listing discoverability as a structured-data and content-readiness problem.

## Inputs

- Listing title and URL
- City and address
- Price and property type
- Description quality
- FAQ count
- Neighborhood, school, and transit context
- Image count
- Entity linkage depth

## Core idea

Brokerages often publish listings with inconsistent schema and thin answer surfaces. This repo improves that by keeping three decisions visible:

- what schema can be published now
- what content needs repair before syndication
- which listings are strong enough for AI-facing entity packaging

## Outputs

- Brokerage schema
- Listing schema manifests
- Publish / improve / rewrite scoring
- Repair queue
- API payloads for listing ops and publishing systems
