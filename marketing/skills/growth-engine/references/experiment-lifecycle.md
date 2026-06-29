# Experiment Lifecycle

## States

```
created → running → trending → keep (winner auto-promoted to playbook)
                             → discard (loser)
```

## The Autoresearch Loop

```
1. HYPOTHESIZE
   "Thread posts get 2x impressions vs single posts"
           │
           ▼
2. EXPERIMENT
   Run variants, collect data points after each publish
           │
           ▼
3. ANALYZE
   Bootstrap CI + Mann-Whitney U
   p < 0.05 + lift ≥ 15% = winner
           │
           ▼
4. PROMOTE or DISCARD
   Winner → playbook (auto)
   Loser  → discard pile (learned)
           │
           ▼
5. SUGGEST NEXT
   System identifies untested variables
   └──────────── loops back to 1 ─────┘
```

## Testable Categories by Channel

| Channel | Variables to test |
|---------|------------------|
| `content` | hook_style, post_format, cta_type, post_time, thread_length, emoji_usage, data_vs_narrative |
| `email` | subject_line_style, opener_type, email_length, personalization_depth, cta_style, send_time |
| `linkedin` | inmail_opener, role_framing, company_pitch, personalization_level, follow_up_cadence |
| `blog` | headline_style, content_format, platform_priority, visual_style, posting_time, content_length |
| `seo` | title_tag_format, meta_description_style, content_structure, internal_linking, heading_format |

## Playbook-First Rule

Always run `playbook --agent <name>` before creating new content. Playbook rules are empirically proven — they reflect real data, not assumptions. Apply all relevant rules to the new piece before it goes live.

## Data Directory Layout

```
data/experiments/
├── content/
│   ├── experiments.json   # Full experiment records + data points
│   ├── playbook.json      # Promoted winners
│   └── active.json        # Currently running experiment index
├── email/
├── linkedin/
└── ...
```

The `data/` directory is auto-created on first use. It should be gitignored (experiment data is local to the marketing environment).
