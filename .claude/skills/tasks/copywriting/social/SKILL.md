---
name: social
description: Create authentic, high-engagement social content for LinkedIn and Twitter/X including posts, threads, articles, and newsletters. Optimized for platform algorithms and differentiated from generic AI-generated content.
---

[Note for the user: tune this skill and the asset types to your requirements - this is a generic example as a starting point]

# Social Copywriting

## Instructions

1. **Identify Platform & Format:** Determine LinkedIn or Twitter/X, and specific format (post, thread, article, newsletter)
2. **Load Format Guide:** Read the corresponding file from `types/`
3. **Review the Brief:** Session should include messaging brief with objective, audience, and key message
4. **Reference Messaging House:** Extract relevant context from `/messaging`
5. **Draft Content:** Apply platform-specific guidelines and format requirements
6. **Self-Assess:** Review against quality signals

## Post Type Guides

After identifying the platform and format, load the corresponding guide:

**LinkedIn:**
- **Short-Form Post:** See `types/linkedin-post.md`
- **Article/Newsletter:** See `types/linkedin-article.md`

**Twitter/X:**
- **Single Post:** See `types/x-post.md`
- **Thread:** See `types/x-thread.md`

## Messaging House Context

| Context Type       | What to Extract                              | Source Files                 |
|--------------------|----------------------------------------------|------------------------------|
| Persona & Audience | Target reader, pain points, technical level  | people.md                  |
| Voice & POV        | Brand voice, personal narrative, tone        | profile.md (voice section)   |
| Value Framework    | Key insights, differentiation, outcomes      | position.md, portfolio.md       |
| Market Perspective | Industry tensions, trends, contrarian views  | position.md                     |
| Evidence           | Data points, customer stories, proof         | proof.md                     |
| Strategic Context  | Campaign themes, current initiatives         | play.md                   |

## Platform Guidelines

### LinkedIn

**Algorithm priorities:**
- Native content (no external links in post body)
- Early engagement (first 60-90 minutes critical)
- Replies and meaningful comments weighted heavily
- Posts with recognizable AI patterns get 47% less reach

**Content that performs:**
- Thought leadership with unique POV (2-3x higher engagement)
- Personal stories with professional insight
- Data-driven observations with clear takeaways
- Carousels for frameworks and educational content (6.6% engagement rate)

**Format constraints:**
- 3,000 character limit
- Hook must land in first 210 characters (before "See more")
- Line breaks improve readability
- 1-3 hashtags maximum (at end, not inline)

### Twitter/X

**Algorithm priorities:**
- Replies weighted 27x more than likes
- Video content gets 2x organic reach
- External links throttled significantly (270% fewer views)
- First hour engagement determines distribution

**Content that performs:**
- Threads for thought leadership (5-7 posts optimal)
- Questions and opinion-driven posts
- Real-time commentary on industry news
- 80/20 rule: 80% value, 20% promotional

**Format constraints:**
- 280 characters per post
- Threads should have strong hooks and clear progression
- 1-2 hashtags maximum
- No external links in main post (add in reply if needed)

## Authenticity Guidelines

**Avoid these AI-detectable patterns:**
- Starting with "I've been thinking about..." or "Here's the thing..."
- Numbered lists with generic headers (5 Ways to..., 3 Tips for...)
- Emoji-heavy formatting (🔥💡🚀)
- "Let me explain" or "Here's why this matters"
- Ending with "What do you think?" without genuine engagement hook
- Perfect parallel structure in every list item
- Buzzword-heavy language (leverage, synergy, game-changer)

**Instead, favor:**
- Specific observations from real experience
- Imperfect, conversational language
- Contrarian or nuanced takes
- Concrete examples over abstract principles
- Questions that invite genuine debate
- Vulnerability or admission of uncertainty where authentic

## Quality Signals

Quality signals for this content type. Use during generation as a compass; the reader agent evaluates against these during review.

```
Social Quality Signals:
- [ ] Platform-native: No external links in body, follows format constraints
- [ ] Hook strength: First line earns the scroll-stop
- [ ] Authenticity: Doesn't match common AI patterns
- [ ] Specificity: Concrete examples, not generic advice
- [ ] Voice alignment: Matches brand tone from profile.md
- [ ] Engagement design: Natural conversation starter, not forced CTA
- [ ] Altitude match: Technical depth appropriate for audience
```

## Output Format

```markdown
## Social Brief
**Platform:** [LinkedIn / Twitter/X]
**Format:** [Post / Thread / Article / Newsletter]
**Objective:** [Awareness / Engagement / Traffic / Conversion]
**Target Audience:** [Persona and context]
**Key Message:** [Core point to land]

## Content

[Platform-formatted content with line breaks preserved]

## Posting Notes
**Optimal timing:** [Suggested post time]
**Engagement strategy:** [How to respond to comments]
**Repurpose opportunity:** [Other formats this could become]

## Self-Assessment
- Hook strength: [Notes on grounding and context strength]
- Authenticity: [Notes on grounding and context strength]
- Platform fit: [Notes on grounding and context strength]
```

## Writing Guidelines

- Lead with tension, insight, or unexpected observation
- Write like you talk, not like you write
- One idea per post (threads can layer, but each post should stand alone)
- Specificity beats generality every time
- Your experience and POV are the differentiator
- If you wouldn't say it in a conversation, don't post it
- Genuine engagement > manufactured virality
