---
title: "onchul — Decisions INDEX"
date: 2026-06-01
tags: [onchul, adr, index]
category: index
project: onchul
---

# onchul — Архітектурні рішення (ADR)

- [[2026-06-01-station-time-native-time-column]] — час станцій (`time`/`time_arrival`) зберігати як нативний MySQL `TIME` + cast-обгортка `{HH,mm}`.
- [[2026-07-15-transfer-return-money-on-parent]] — **відхилення від 3g #1**: повернення грошей за трансферну пару завжди на основному квитку (`returnMoneyLeg`).
- [[2026-07-15-transfer-resign-no-child-trip]] — **відхилення від 3g #2**: resign трансферу без `child_trip`; окремі Order + явний двомісний контракт.
