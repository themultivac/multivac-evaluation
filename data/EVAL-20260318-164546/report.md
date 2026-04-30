# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260318-164546
**Timestamp:** 2026-03-18T16:45:46.498390
**Category:** Project MiniMax
**Model Pool:** 9 minimax-optimized models

## Question

A startup has 3 engineers, $50,000 monthly budget, and 90 days to launch an MVP. They need to build: user authentication, a REST API with 12 endpoints, a React dashboard, a PostgreSQL database, CI/CD pipeline, and basic monitoring.

Round 1 — Initial Plan: Create a sprint plan. Allocate engineers to tasks. Estimate completion dates. Identify the critical path.

Round 2 — Day 30 Reality Check: Engineer #2 quits. The authentication system took twice as long as estimated. 4 of 12 API endpoints are done. The React dashboard has not started. You now have 2 engineers and 60 days. Revise the entire plan. What do you cut? What do you keep? What changes architecturally?

Round 3 — Day 60 Optimization: A competitor launches a similar product. Your CEO wants to launch in 15 days, not 30. You have 2 engineers, $20,000 remaining budget, and a half-finished product. The API has 8/12 endpoints, the dashboard is 40% done, CI/CD is not set up. Design the fastest possible path to a launchable MVP. What is the minimum viable version of each component? What can be faked, deferred, or replaced with a third-party service?

After all 3 rounds: What meta-principle did you use to make cuts in each round? How did your optimization strategy change as constraints tightened? What would a fourth round look like if the timeline compressed to 7 days?

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | MiniMax M2.7 | 7.44 | 4.40 | 8.95 | 1.67 |
| 2 | GPT-5.4 | 7.44 | 5.55 | 9.55 | 1.71 |
| 3 | MiniMax M1 | 7.31 | 4.40 | 9.00 | 1.63 |
| 4 | Claude Sonnet 4.6 | 6.76 | 3.80 | 9.00 | 1.66 |
| 5 | MiniMax-01 | 6.56 | 6.00 | 7.20 | 0.40 |
| 6 | MiniMax M2 | 6.19 | 3.85 | 8.60 | 1.59 |
| 7 | MiniMax M2.1 | 5.99 | 3.45 | 7.85 | 1.55 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 4.35 |
| 2 | MiniMax M1 | 6.27 |
| 3 | MiniMax M2.5 | 6.54 |
| 4 | MiniMax M2 | 6.83 |
| 5 | MiniMax M2.7 | 6.93 |
| 6 | MiniMax M2.1 | 7.23 |
| 7 | Claude Sonnet 4.6 | 7.72 |
| 8 | MiniMax-01 | 8.67 |

**Strictest Judge:** judge_gpt54
**Most Lenient Judge:** minimax_01
**Total Judgments:** 72
**Valid Judgments:** 49

---

## Model Pool

Models selected for **Project MiniMax** evaluation:

1. **MiniMax M2.7** (openrouter)
2. **MiniMax M2.5** (openrouter)
3. **MiniMax M2.1** (openrouter)
4. **MiniMax M2** (openrouter)
5. **MiniMax M1** (openrouter)
6. **MiniMax-01** (openrouter)
7. **Claude Sonnet 4.6** (openrouter)
8. **GPT-5.4** (openrouter)
9. **Gemini 3.1 Pro** (openrouter)

---

## Model Responses

### MiniMax M2.7

**Generation Time:** 58196ms
**Tokens:** 2403

```
# MVP Survival Plan: Three Rounds + Meta-Analysis

---

## Round 1 — Initial Sprint Plan

### Engineer Allocation

| Engineer | Primary Ownership | Secondary |
|----------|-----------------|-----------|
| Eng 1 | Auth + Database schema | CI/CD, Monitoring |
| Eng 2 | REST API (endpoints 1–6) | Auth integration, API docs |
| Eng 3 | React Dashboard | CI/CD, Dashboard API consumers |

### Sprint Breakdown (90 days = 6 sprints × 2 weeks)

```
Sprint 1 (Days 1–14): Auth system, DB schema design, API skeleton
Sprint 2 (Days 15–28): Auth complete, DB migrations, API endpoints 1–4
Sprint 3 (Days 29–42): API endpoints 5–12, dashboard scaffolding, CI/CD
Sprint 4 (Days 43–56): Dashboard core views, monitoring setup, integration
Sprint 5 (Days 57–70): Dashboard polish, hardening, load testing
Sprint 6 (Days 71–84): Beta testing, bug fixes, staging deployment
Sprint 7 (Days 85–90): Buffer + launch prep
```

### Estimated Completion Dates

| Component | Target Date | Notes |
|-----------|-------------|-------|
| Auth + DB | Day 21 | End of Sprint 2 |
| All 12 API endpoints | Day 42 | End of Sprint 3 |
| Dashboard (core) | Day 56 | End of Sprint 4 |
| CI/CD + Monitoring | Day 56 | Parallel with dashboard |
| Full MVP launch | Day 84 | Buffer through Day 90 |

### Critical Path

```
Auth (21 days) → API endpoints (parallel) → Dashboard integration (days 43–56) → Launch
       ↓
   Database schema (underpins everything)
```

**Critical path duration: 84 days** (tight against the 90-day budget). No slack.

---

## Round 2 — Day 30 Reality Check

### Situation Assessment

```
Original plan:  3 engineers × 90 days
Actual status:  2 engineers × 60 remaining days
Velocity loss:  ~40% from staffing alone
               + ~20% from auth scope overrun

Effective capacity: 2 engineers × 60 days
                    = 120 engineer-days
                    vs. 270 engineer-days originally planned
                    = 44% of original capacity
```

### What You Cut

| Component | Original Scope...
```

### MiniMax M2.5

**Generation Time:** 33808ms
**Tokens:** 2400

```

```

### MiniMax M2.1

**Generation Time:** 46303ms
**Tokens:** 2405

```
# Startup MVP Crisis Management: Three Rounds of Strategic Pivot

## Executive Overview

This document walks through the evolution of an MVP project under increasing resource constraints. Starting with a well-resourced 90-day plan, we navigate through team loss, timeline compression, and competitive pressure to extract maximum value from diminishing resources. Each round demonstrates how prioritization principles shift as constraints tighten, ultimately revealing the core meta-principle that should guide every startup decision: **maximize learning per unit of resources spent**.

---

## Round 1 — Initial Plan

### Project Parameters and Constraints

The startup begins with favorable conditions: a three-engineering team, $50,000 monthly budget ($150,000 total), and a 90-day timeline to launch. The product requirements include user authentication, a REST API with twelve endpoints, a React-based administrative dashboard, PostgreSQL database infrastructure, CI/CD pipeline implementation, and basic monitoring capabilities. These requirements represent a standard SaaS application architecture, but the timeline and team size create meaningful tension that demands careful planning.

The $50,000 monthly budget provides flexibility for third-party services, contractor support, or infrastructure costs. However, the 90-day window means every week of delay directly impacts competitive positioning and runway. Three engineers working full-time represents approximately 3,600 engineering hours over the 90-day period, assuming standard work schedules. This translates to roughly 300 hours per engineer per month, or about 75 hours per engineer per endpoint if the API work were distributed evenly across the twelve endpoints—a pace that is aggressive but achievable for experienced engineers working on well-defined requirements.

### Sprint Architecture and Engineer Allocation

The 90-day timeline divides naturally into three 30-day sprints, with each sprint having defined milestones and ...
```

### MiniMax M2

**Generation Time:** 18432ms
**Tokens:** 2384

```
# Round 1 — Initial Plan (3 engineers, $50k, 90 days)

Goal: deliver a complete, testable MVP with authentication, a 12-endpoint REST API, a React dashboard, PostgreSQL, CI/CD, and basic monitoring.

## Sprint plan (6 x 2-week sprints)

- Sprint 1 (Weeks 1–2): Foundations and scaffolding
  - Infrastructure: Postgres provisioned (RDS/Cloud SQL/Supabase), VPC/security groups, secrets management (Vault/SSM), local dev environment.
  - Database: initial schema with migrations, seed scripts, test data.
  - CI/CD: GitHub Actions or GitLab CI, lint/test/build, PR checks, deploy to dev/staging.
  - Monitoring: centralized logging (CloudWatch/Loki), health checks, minimal APM (Sentry/Datadog).
  - Authentication scaffolding: JWT strategy, password hashing, basic user model and endpoints.

- Sprint 2 (Weeks 3–4): Core authentication and first API endpoints
  - Authentication: signup, login, refresh, logout; email verification; password reset.
  - API: implement 3 core endpoints (e.g., entities CRUD).
  - Dashboard: layout, routing, authentication guard, basic nav and theme.

- Sprint 3 (Weeks 5–6): Dashboard and core data flows
  - Dashboard: CRUD screens for the 3 core endpoints; error boundaries; loading states.
  - API: 3 additional endpoints (e.g., listing/search, pagination, filtering).
  - Testing: unit/integration tests for auth and core endpoints.

- Sprint 4 (Weeks 7–8): Remaining endpoints and admin
  - API: 3 more endpoints (admin/analytics/audit).
  - Dashboard: admin views, charts, basic RBAC.
  - Monitoring: alerts for auth failures, API latency, error rates.

- Sprint 5 (Weeks 9–10): Hardening and polish
  - API: final 3 endpoints (e.g., webhooks, exports).
  - Security: rate limiting, input validation, CORS, OWASP checks.
  - Performance: query optimization, caching, pagination.
  - CI/CD: blue/green deploys, rollback hooks.

- Sprint 6 (Weeks 11–12): Pre-launch readiness
  - End-to-end tests, smoke tests, load tests.
  - Documentation: API docs (OpenAPI), use...
```

### MiniMax M1

**Generation Time:** 45260ms
**Tokens:** 2808

```
# MVP Development Crisis: Three Rounds of Replanning

## Round 1 — Initial Plan

### Sprint Plan (6 two-week sprints × 90 days)

| Sprint | Focus | Deliverables |
|--------|-------|--------------|
| 1 | Auth + Database Foundation | PostgreSQL schema, User model, JWT auth framework |
| 2 | Authentication Complete | Login, signup, password reset, token refresh, OAuth skeleton |
| 3 | API Core (Endpoints 1-6) | CRUD for primary entities, validation, error handling |
| 4 | API Completion (Endpoints 7-12) | Secondary entities, reporting endpoints, search/filter |
| 5 | Dashboard + Integration | React components, API integration, state management |
| 6 | DevOps + Polish | CI/CD pipeline, monitoring, testing, buffer |

### Engineer Allocation

- **Engineer 1** (Backend): Auth → Database → API endpoints
- **Engineer 2** (Backend/Full-stack): API endpoints → Support frontend
- **Engineer 3** (Frontend): React dashboard → CI/CD → Monitoring

### Completion Estimates

- Auth: Day 30
- API (12 endpoints): Day 60
- Dashboard: Day 75
- CI/CD + Monitoring: Day 85
- Buffer/Polish: Day 90

### Critical Path

```
Auth (Day 15-30) → Database Models → API Endpoints (Day 45-60) → Dashboard Integration (Day 70-75)
                                                      ↓
                                          CI/CD Pipeline (Day 80-85)
```

**Key risk**: Auth double-blocking everything. Backend must complete before frontend can integrate.

---

## Round 2 — Day 30 Reality Check

### Situation Assessment

| Metric | Planned | Actual | Variance |
|--------|---------|--------|----------|
| Engineers | 3 | 2 | -33% |
| Auth Progress | 100% | 50% (2x time) | -15 days |
| API Endpoints | 6 done | 4 done | -2 endpoints |
| Dashboard | Started | Not started | -15 days |
| Days Remaining | 60 | 60 | — |
| Budget Remaining | ~$33,000 | ~$33,000 | On track |

### Revised Resource Allocation

With 2 engineers over 60 days = **120 person-days** (down from 270)

### What Gets Cut

| Component | Origi...
```

### MiniMax-01

**Generation Time:** 32729ms
**Tokens:** 2458

```
### **Round 1 – Initial Plan**

#### **Sprint Plan and Task Allocation**

1. **User Authentication (Days 1-10)**
   - **Engineer #1**: Set up user authentication using a third-party service like Auth0 or AWS Cognito to save time.
   - **Engineer #2**: Integrate authentication with the backend.
   - **Engineer #3**: Implement frontend components for login and signup.

2. **REST API with 12 Endpoints (Days 11-30)**
   - **Engineer #1**: Develop 4 endpoints.
   - **Engineer #2**: Develop 4 endpoints.
   - **Engineer #3**: Develop 4 endpoints.

3. **PostgreSQL Database (Days 1-15)**
   - **Engineer #1**: Design and set up the database schema.
   - **Engineer #2**: Implement database migrations and seeding.

4. **React Dashboard (Days 16-40)**
   - **Engineer #3**: Build the initial structure and components.
   - **Engineer #1 & #2**: Assist with API integration and complex components.

5. **CI/CD Pipeline (Days 41-50)**
   - **Engineer #1**: Set up CI/CD using GitHub Actions or Jenkins.
   - **Engineer #2 & #3**: Assist with configuration and testing.

6. **Basic Monitoring (Days 51-60)**
   - **Engineer #1**: Implement basic monitoring using tools like Prometheus and Grafana.
   - **Engineer #2 & #3**: Assist with dashboard setup and alerts.

#### **Critical Path**
- **User Authentication** → **REST API** → **React Dashboard** → **CI/CD Pipeline** → **Basic Monitoring**

### **Round 2 – Day 30 Reality Check**

#### **New Constraints**
- **Engineer #2 has quit**: Only 2 engineers remain.
- **Authentication took twice as long**: Delayed by 5 days.
- **4/12 API endpoints are done**: Behind schedule.
- **React dashboard not started**: Critical path affected.

#### **Revised Plan**

1. **Cut**
   - **CI/CD Pipeline**: Defer to post-MVP launch.
   - **Basic Monitoring**: Defer to post-MVP launch.
   - **4 Remaining API Endpoints**: Prioritize the most critical 4 endpoints and defer the rest.

2. **Keep**
   - **User Authentication**: Essential for user engagement.
   - **8 T...
```

### Claude Sonnet 4.6

**Generation Time:** 40385ms
**Tokens:** 2407

```
# Startup MVP Sprint Plan: A Three-Round Constraint Optimization

---

## ROUND 1 — Initial Plan (Day 0, 90 Days, 3 Engineers, $50K/month)

### Team Allocation

| Engineer | Role | Primary Responsibilities |
|----------|------|--------------------------|
| **Eng #1** | Backend Lead | REST API, PostgreSQL schema, Auth backend |
| **Eng #2** | Frontend Lead | React dashboard, UI components, Auth frontend |
| **Eng #3** | DevOps/Fullstack | CI/CD pipeline, Monitoring, API support |

---

### Sprint Structure (2-week sprints)

#### Sprint 1 — Days 1–14: Foundation
| Task | Owner | Estimate | Notes |
|------|-------|----------|-------|
| Database schema design | Eng #1 | 3 days | Users, sessions, core entities |
| Auth system (backend) | Eng #1 | 5 days | JWT, refresh tokens, password hashing |
| Auth system (frontend) | Eng #2 | 4 days | Login, register, protected routes |
| CI/CD pipeline setup | Eng #3 | 5 days | GitHub Actions, staging environment |
| API endpoints 1–4 | Eng #1 | 6 days | Core CRUD, parallel with auth |
| React app scaffolding | Eng #2 | 3 days | Routing, state management, design system |
| Monitoring baseline | Eng #3 | 4 days | Error tracking, uptime, basic alerting |

**Sprint 1 Exit Criteria:** Auth works end-to-end, CI/CD deploys to staging, 4 API endpoints live

---

#### Sprint 2 — Days 15–28: Core Features
| Task | Owner | Estimate | Notes |
|------|-------|----------|-------|
| API endpoints 5–8 | Eng #1 | 8 days | Business logic layer |
| Dashboard core views | Eng #2 | 10 days | Main data views, navigation |
| Auth integration | Eng #2 | 4 days | Connect frontend auth to API |
| Production env setup | Eng #3 | 5 days | Prod deploy, secrets management |
| Database optimization | Eng #1 | 2 days | Indexes, query optimization |
| Component library | Eng #2 | 4 days | Reusable UI components |

**Sprint 2 Exit Criteria:** 8 API endpoints functional, dashboard renders real data

---

#### Sprint 3 — Days 29–42: Completion
| Task | Owner | Estima...
```

### GPT-5.4

**Generation Time:** 32009ms
**Tokens:** 2369

```
## Assumptions

To make this concrete, I’ll assume:

- 90 days = 3 months
- 3 engineers are full-time
- MVP means usable by early customers, not enterprise-ready
- “Basic monitoring” = uptime/error tracking/logs, not full observability
- Authentication means email/password + session/JWT + password reset, unless cut later
- React dashboard is an internal/user-facing web app for core workflows
- API endpoints are a mix of CRUD and a few business actions

I’ll label engineers:

- **E1** = strongest backend/infrastructure
- **E2** = full-stack
- **E3** = frontend/full-stack

I’ll structure this in 3 rounds.

---

# Round 1 — Initial Plan

## Goal

Launch a functional MVP in 90 days with:

- User authentication
- REST API with 12 endpoints
- React dashboard
- PostgreSQL database
- CI/CD pipeline
- Basic monitoring

## Planning principle

At this stage, optimize for:

- **parallel work**
- **risk reduction early**
- **integration by the middle, not the end**
- **shipping the thinnest acceptable version of every required system**

---

## High-level delivery strategy

Break the 90 days into 6 two-week sprints plus final stabilization.

### Sprint structure

- **Sprint 1–2:** foundations + risky systems first
- **Sprint 3–4:** core feature completion
- **Sprint 5:** integration, polish, operational readiness
- **Sprint 6:** buffer, QA, launch prep

---

## Work breakdown

### 1. Foundation and architecture
Includes:

- repo setup
- environments
- DB schema
- API skeleton
- auth approach
- deployment baseline
- coding standards

### 2. Authentication
Includes:

- signup/login
- password hashing
- sessions/JWT
- auth middleware
- role/basic access control
- password reset if in MVP

### 3. PostgreSQL database
Includes:

- schema design
- migrations
- seed data
- indexes/basic performance

### 4. REST API (12 endpoints)
Includes:

- endpoint design
- validation
- service logic
- DB integration
- error handling
- tests for core paths

### 5. React dashboard
Includes:

- routing...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*