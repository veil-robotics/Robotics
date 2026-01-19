<p align="center">
  <img src="docs/assets/banner.png" alt="Veil Robotics banner" width="100%" />
</p>

<h1 align="center">Veil Robotics</h1>

<p align="center">
  <b>Privacy cleaning you can prove.</b><br/>
  A local video sanitizer + human verification loop that turns “trust me” into measurable evidence.
</p>

<p align="center">
  <a href="#why-this-exists">Why</a> •
  <a href="#what-were-building">What</a> •
  <a href="#how-it-works">How it works</a> •
  <a href="#roadmap">Roadmap</a> •
  <a href="#security--privacy">Security</a> •
  <a href="#repo-structure">Repo</a>
</p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/status-building%20MVP-blue" />
  <img alt="license" src="https://img.shields.io/badge/license-TBD-lightgrey" />
  <img alt="contributions" src="https://img.shields.io/badge/contributions-welcome-brightgreen" />
</p>

---

## Why this exists

Modern video is a privacy minefield: faces, plates, screens, badges, documents, reflections—tiny identifiers hiding in plain sight.

Most “privacy tools” stop at *processing* and skip the hard part: **proof**.

Veil Robotics is built around a simple premise:

> Sanitization without verification is a vibe.  
> Sanitization with measurable verification is infrastructure.

We pair a **local cleaner** with a **human validation loop** and produce an **auditable Privacy Receipt** for every transformation.

---

## What we’re building

**A system that lets people sanitize video locally and earn points for provable contributions.**

- **Cleaner (local):** MP4 in → detectors → blur/blackout → sanitized MP4 out
- **Privacy Receipt:** signed `receipt.json` proving what happened, with hashes + model versions + thresholds
- **Validation microtasks:** humans verify whether sanitized video still leaks identifiers
- **Trust metrics:** leak-rate estimates, detector miss categories, verification time/cost
- **Anti-gaming:** quality gates, rate limits, reputation-weighted consensus

Points are **off-chain** (fast, cheap, reversible for abuse control). Wallet connect is used for identity and portability.

---

## How it works

### 1) Clean locally
You run the cleaner on your machine.

- Input: **MP4 (MVP)**
- Detectors (v0):
  - Face → blur
  - License plate → blur
  - Screen/text region → blackout (coarse OK in v0)

Output:
- `sanitized.mp4`

### 2) Generate a Privacy Receipt
The cleaner generates a **cryptographically signed receipt**:

- Hash of input and output (integrity)
- Detector model names + versions + thresholds (reproducibility)
- Tool build hash/version (auditability)
- Timestamp (timeline)
- Signature (Ed25519 keypair generated on install)

### 3) Verify + reward
You upload the receipt to the backend:

- Backend verifies the signature and hashes
- Points are awarded
- Sanitized outputs (for public clips) seed new validation tasks

### 4) Validators measure leak-rate
Validators complete quick microtasks like:

- “Is a face visible?” (yes/no) + timestamp
- “Any license plate visible?” (yes/no) + timestamp
- “Any screen/text visible?” (yes/no) + timestamp

Scoring:
- Consensus-based voting
- “Gold” tasks with known answers mixed in
- Points reward accuracy; low-quality clicking gets penalized

Result:
- We continuously estimate leak rate and detector miss profiles.
- The system gets more trustworthy over time.

---

## The product loop (in one picture)

```
 +-----------------+          +------------------+
 |  Local Cleaner  |          |   Validators     |
 |  MP4 -> MP4     |          |  microtasks      |
 +--------+--------+          +---------+--------+
          |                             |
          | receipt.json (signed)       | votes + timestamps
          v                             v
 +-----------------+          +------------------+
 |  Receipt Verify |<---------|  Task Generator  |
 |  + Points Award |          |  sampling + gold |
 +--------+--------+          +---------+--------+
          |
          v
 +-----------------+
 | Trust Dashboard |
 | leak rate, etc. |
 +-----------------+

```

---

## Roadmap

### Phase 1 — MVP

**A) Points + Wallet backbone**
- Web app skeleton (landing + login)
- Wallet connect (choose chain; points off-chain)
- User profile + points balance
- Activity feed

**B) Basic microtask loop (validators)**
- Task format: clip/frame + yes/no questions + timestamp
- 10–30 tasks/day UI + submit
- Consensus scoring + gold tasks
- Points rules v1: accuracy rewards + click-spam penalties

**C) Admin tools (minimum)**
- Upload task batches
- Task stats (completion, accuracy, disagreement hotspots)
- Abuse controls (rate limit, ban, reset)

---

### Phase 2 — Cleaner + Privacy Receipt (prove “real work”)

**D) Cleaner v0 (local)**
- MP4 only (ROS bag later)
- 2–3 detectors: faces/plates/screens-text
- Export sanitized MP4

**E) Privacy Receipt v0**
- Generate and sign `receipt.json` (Ed25519)
- Backend endpoint verifies signature → award points

**F) Public Contribution track (safe uploads)**
- Small set of allowed public clips
- Store sanitized outputs + receipts
- Auto-generate validator tasks from outputs (sampling)

---

### Phase 3 — Make it hard to game, easy to trust

**G) Anti-sybil / anti-bot basics**
- CAPTCHA + rate limits
- Accuracy-gated points (no points below threshold)
- Progressive unlocks: higher accuracy → higher multipliers / harder tasks

**H) Quality metrics dashboard**
- Leak-rate estimate (% clips with remaining identifiers)
- Per-detector miss categories (faces vs plates vs screens/text)
- Time-to-verify + cost estimate

**I) Release packaging**
- Cleaner shipped as Docker image (fastest)
- Optional native binary later
- One-command quickstart + sample dataset

---

### Phase 4 — Auditable points + reputation

**J) Auditable points ledger**
- Immutable log for every points event
- Daily/weekly publish signed CSV snapshot **or** Merkle root (optional later)
- Public rules page (earning + abuse handling)

**K) Reputation system v1**
- Validator rep score tied to accuracy over time
- Higher-rep votes weighted more
- Higher-rep users unlock edge-case tasks with higher rewards

---

## Security & Privacy

- **Local-first cleaning:** raw video stays on your machine by default.
- **Receipts are signed:** prevents fabricated “work” claims.
- **Points are reversible:** abuse can be corrected without chain drama.
- **Public uploads are limited:** only a curated set of public clips are allowed for uploads in the “Public Contribution” track.
- **Anti-gaming baked in:** gold tasks, consensus, rate limits, and reputation weighting.

Threat model details will live in `docs/security.md` as the implementation lands.

---

## Repo structure (planned)

```

.
├── apps/
│   ├── web/                # landing, login, wallet connect, validator UI
│   └── admin/              # batch upload, stats, abuse controls
├── services/
│   └── api/                # points, tasks, scoring, receipt verification
├── cleaner/
│   ├── cli/                # MP4 -> sanitized MP4 + receipt.json
│   └── detectors/          # face/plate/screen-text
├── packages/
│   ├── schemas/            # task + receipt JSON schemas
│   └── crypto/             # Ed25519 signing/verifying helpers
├── docs/
│   ├── architecture.md
│   ├── security.md
│   └── assets/
└── README.md

```

---

## Core artifacts

### Microtask (concept)
A microtask bundles:
- clip id / frame range or timestamp
- question set:
  - face present? (y/n)
  - license plate present? (y/n)
  - screen/text visible? (y/n)
  - timestamp marker for “where”
- metadata:
  - source type (public vs user submission)
  - gold flag (known answer)
  - difficulty/category tags

### Privacy Receipt (`receipt.json`) (concept)
- input hash + output hash
- detector list:
  - model name, version, thresholds/settings
- tool build hash/version
- timestamp
- signature (Ed25519)

---

## Principles

- **Proof over promises**
- **Measure what matters** (leaks and misses, not vibes)
- **Make honesty cheaper than cheating**
- **Start simple; iterate aggressively**
- **Privacy isn’t optional** — it’s the product

---

## Contributing

We’re early, and we like collaborators who enjoy building sharp tools.

- Open an issue for feature proposals or threat-model concerns
- PRs welcome for:
  - detector improvements
  - task UX
  - scoring logic
  - dashboard metrics
  - packaging/quickstart

Contributing guidelines will be added in `CONTRIBUTING.md`.

---

## License

TBD.

---

<p align="center">
  <sub>
    Veil Robotics — turning privacy cleaning into verifiable work.
  </sub>
</p>
