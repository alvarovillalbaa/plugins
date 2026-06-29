# X Concept Research

Two research methods for finding the right angle before writing a single word:
1. **YouTube competitive analysis** — find proven viral concepts to borrow
2. **X controversy research** — find the activating nerve to engineer distribution

---

## YouTube Competitive Analysis

Find a concept that's already proven viral on another platform and apply it to your product.

**Why YouTube:** The patterns that work on YouTube (titles, framing, emotional hooks) translate directly to X because both platforms reward similar psychological triggers — curiosity, specificity, and implied transformation.

### The Research Workflow

Run 15 keyword searches for your category across three timeframes:

| Timeframe | Purpose |
|-----------|---------|
| All time | Establishes the ceiling — the highest-ever performing concept in this space |
| Last 12 months | Current format preferences and trending structures |
| Last 30 days | What's working right now |

For each keyword, find the highest-performing video. That's your ceiling.
Collect patterns downward until there's a major drop-off in views.
The titles at the ceiling are the patterns worth stealing. The drop-off marks the floor.

### Outlier Detection

Flag any video exceeding **2x the channel average** views. These are the true outliers — the formats that broke through their normal audience to reach new people.

Extract recurring patterns from outlier titles:
- Structural phrases ("How I...", "The system behind...", "We built...")
- Emotional operators ("while you sleep", "overnight", "in 24 hours")
- Social proof constructions ("from 0 to X", "the exact system", "the framework used by")

### The Application Prompt

```
Find the top performing videos in [category] across the last 30 days, 
12 months, and all time. Identify the structural pattern behind the 
highest performing titles. What is the core concept or framing that 
made them work? Now apply that same framing to [product].
```

**Tools:** YouTube Data API v3, [1of10.com](https://1of10.com)

### Proven Title Patterns (by category)

| Category | Pattern at ceiling |
|----------|--------------------|
| AI/software | "The first X that [does Y while you Z]" |
| Productivity | "The exact system behind [famous outcome]" |
| Finance | "How I went from [before] to [after] using [mechanism]" |
| Design/creative | "[N] [things] designers [hate/love/can't ignore]" |
| Founder/startup | "We raised $[X]M. Here's [the thing we learned / what we built]" |

---

## X Controversy Research

Find the most activated nerve in your target community — then own it before critics can use it against you.

### The Mechanism

Quote tweets are a sourcing signal. Every quote tweet tells X's algorithm to show the post to more users.

When you own the core criticism upfront, people who disagree quote tweet to argue. People who agree quote tweet to validate. Both feed the algorithm. The critics distribute your content while complaining about it.

This only works when you own the criticism *genuinely* — not as spin, but as actual positioning. Moda wasn't lying when they said "anti-slop, by design." The criticism was real, and so was their answer.

### The Research Workflow

Search X for posts in your category, filtered to high engagement:

```
[category term] min_faves:1000
```

Sort by engagement. Look for posts with an unusually high **quote tweet ratio** relative to likes. High quote tweet ratio = divisive content = activated community nerve.

For each high-QT post, ask:
- What is the core tension or belief this activated?
- Who did it make angry and why?
- Who did it validate and why?
- Is this tension real in your product category?

### The Research Prompt

```
Research the top posts on X in [category] sorted by engagement using 
advanced search Min_Faves:1000. Identify the ones with the highest 
quote tweet ratio. What is the core criticism or controversy that made 
people react? Summarize the single most activating nerve in this community.
```

*Requires X API key or manual advanced search.*

### Communities That Activate Easily

| Community | Common activating nerve |
|-----------|------------------------|
| Designers | AI replacing human creativity / "taste" |
| SEO professionals | AI-generated content quality |
| Developers | No-code vs real engineering |
| Founders | VC funding vs bootstrapping |
| Finance/investing | Active vs passive management |
| UGC creators | AI vs authentic content |
| Sales teams | Automation vs human relationships |

### How to Engineer the Controversy

1. Identify the single most activating criticism of your product category
2. Acknowledge it directly and specifically in your positioning — not defensively
3. Make your product the direct answer to that criticism
4. Plant one line that the community can't help but react to
5. The more specific the line, the more it activates the right people

**Wrong:** "We're different from other AI tools"
**Right:** "The world's first design agent with taste. Anti-slop, by design."

The second line is quotable, divisive, and makes people react — both those who agree and those who want to prove it wrong.

---

## Combining Both Methods

The strongest launch angles come from intersecting YouTube concept research and X controversy research:

1. Find a proven viral concept frame (YouTube research)
2. Find the community's activating nerve (X research)
3. Combine: use the viral frame, filtered through the controversy angle

**Example:**
- YouTube concept: "The AI that [works for you while you sleep]" — proven frame in finance and productivity
- X controversy: Sales teams doubt AI can actually replace human prospecting
- Combined: "We raised $50M to build the First AI Revenue Agent. It runs New Business, Expansion, and Prospecting to close you more business while you sleep." → HockeyStack, 1.5M+ views
