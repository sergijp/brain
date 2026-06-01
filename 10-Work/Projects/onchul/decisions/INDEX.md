---
title: "onchul — Decisions INDEX"
date: 2026-06-01
tags: [onchul, adr, index]
category: index
project: onchul
---

# onchul — Архітектурні рішення (ADR)

- [[2026-06-01-station-time-native-time-column]] — час станцій (`time`/`time_arrival`) зберігати як нативний MySQL `TIME` + cast-обгортка `{HH,mm}`.
