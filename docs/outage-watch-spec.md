# Outage Watch Spec

Profile: `lodi-msp-local-global`

## Goal

Alert on outages that are either:
- locally relevant to Philip's Lodi / Central Valley service footprint, or
- globally relevant enough to create customer impact/noise across managed clients.

Avoid duplicate spam. Re-alert only on material change.

## Local relevance

Treat an incident as local when it clearly affects:
- Lodi
- Stockton / Galt / Elk Grove / Manteca / Tracy / Modesto / Sacramento-adjacent coverage
- Central Valley / San Joaquin / Northern California service area
- local infrastructure used by managed clients (power, ISP, telecom, regional carrier)

## Global relevance

Treat an incident as global when:
- vendor confirms global / widespread / multi-region impact
- major shared platform is affected (M365, Google, AWS, Azure, Cloudflare, Okta, telecom backbone)
- issue is broad enough that clients will likely open tickets regardless of precise geography

## Client verticals to prioritize

### Property management
- AppFolio
- Buildium
- Yardi
- Rent Manager
- Propertyware
- RealPage
- Entrata
- tenant/resident portals, rent-payment, screening vendors

### CPA / accounting / tax
- QuickBooks Online / Intuit
- Lacerte
- ProSeries
- Drake Tax
- UltraTax / Thomson Reuters
- CCH / Wolters Kluwer
- Canopy
- Karbon
- e-file / tax portals / practice-management systems

## Broader MSP-critical categories

- Power / utility
- Internet / telecom / carrier
- DNS / CDN / identity
- Cloud / email / collaboration
- PSA / RMM / backup / security / VoIP

## Dedupe rules

Fingerprint each incident on:
- vendor
- service
- incident key / normalized title
- scope (`local` or `global`)
- status bucket (`investigating`, `identified`, `monitoring`, `resolved`)

Suppress exact duplicates for 180 minutes.

## Re-alert only when

- status bucket changes
- severity increases
- local issue becomes global
- global issue becomes locally relevant
- workaround appears
- resolution is posted

## Priority model

### P1
- local power / internet loss in service area
- widespread outage of M365 / Google / Azure / AWS / Cloudflare / identity
- major MSP-core vendor outage causing immediate operational impact

### P2
- major business SaaS degradation affecting property management or CPA clients
- significant regional carrier / ISP issue
- broad partial outage impacting normal workflows

### P3
- advisory, monitoring state, narrow partial outage, or awareness-only incident

## Source quality

Prefer:
1. vendor status page / official vendor advisory
2. one secondary corroborating source

Do not keep repeating the same issue every polling cycle.

## Alert lifecycle

Send:
- initial alert
- material update alert(s)
- single resolution alert
