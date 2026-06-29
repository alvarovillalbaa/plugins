# Gmail Workflows

Use this reference when the user wants the message turned into a mailbox draft, when an existing email thread matters, or when using the `gws` CLI for Gmail or Calendar operations.

## Core principle

Prefer `read → draft → review → send` over writing blind or sending immediately.

## gws CLI commands (Google Workspace CLI)

When the `gws` tool is available, use these helper commands:

| Command | When to use |
|---------|-------------|
| `gws gmail +triage` | Summarize unread inbox — sender, subject, date |
| `gws gmail +read` | Extract message body and headers before replying |
| `gws gmail +reply` | Respond to a message with automatic threading |
| `gws gmail +reply-all` | Reply to all recipients; use only when every recipient should stay in the loop |
| `gws gmail +forward` | Redirect a message to new recipients |
| `gws gmail +send` | Compose and send a new message |
| `gws gmail +watch` | Stream incoming emails in real-time (NDJSON) |

Inspect available parameters before use: `gws gmail --help` or `gws schema gmail.<resource>.<method>`.

**Use helper commands first.** Fall back to lower-level API methods only when a helper cannot do the job.

## Calendar commands (for scheduling CTAs)

When the CTA is to book a call or check availability:

| Command | When to use |
|---------|-------------|
| `gws calendar +agenda` | Show upcoming events across all calendars |
| `gws calendar +insert` | Create a new event |
| `gws calendar freebusy.query` | Check free/busy availability before proposing a time |

Before proposing a specific meeting time in outreach copy, check availability with `gws calendar +agenda` or `freebusy.query` if the user's calendar is connected. Proposing a time that is already blocked looks careless.

## Safe workflow

1. Identify whether this is a new outbound, reply, forward, or follow-up.
2. If replying or following up, run `gws gmail +read` on the latest thread content first.
3. Confirm the sender, recipients, and thread context.
4. Draft the message body in plain text.
5. Create a draft when tooling supports drafts; do not send immediately.
6. Send only if the user explicitly asks to send.

## Inbox triage workflow

When the user asks to review their inbox before drafting:

1. Run `gws gmail +triage` to surface unread messages.
2. Classify each message (Urgent / Needs Response / FYI / Archive) — see `references/follow-up-triage.md`.
3. Draft responses for Urgent and Needs Response items first.
4. Archive FYI and noise items — never delete.

## Threading rules

- Reply on-thread when context continuity matters.
- Start a new thread when the topic materially changed or the old thread is noisy.
- Do not strip away important customer or prospect context when drafting a response.

## Draft status to report back

When mailbox tooling is involved, report one of:

- `Draft created`
- `Reply draft created on existing thread`
- `Ready to copy into email client`
- `Need missing recipient or thread context before drafting`
