---
name: seo-geo
description: Apply search and AI discovery strategy to content intended to rank and be cited. Load this skill when a piece needs keyword targeting, search intent alignment, topic cluster positioning, or GEO optimization for AI engine retrieval. 
---

# SEO / GEO

This is a craft skill. It is the canonical source for SEO and GEO guidance in the content system. The copywriting skill handles content structure and output format. This skill handles how the piece gets found: keyword selection, search intent alignment, topic cluster positioning, and GEO optimization for AI engine retrieval. Load it whenever a piece has a search or AI discovery objective.

## Messaging System Reference

This skill operates against a MESSAGE.md-conformant messaging system. System architecture and progressive loading rules are documented in `CLAUDE.md`. The skill assumes MESSAGE.md is loaded and provides company attributes, glossary, brand guardrails, scenarios vocabulary, and the catalog of pillars, collections, and assets. The skill references content by name (e.g., "the position pillar," "the CISO persona"). If the messaging system is missing or non-conformant, the skill cannot operate; the agent should prompt for `/bootstrap` or `/run health`.

---

## Keyword Research Before Writing

The single most expensive SEO mistake is writing strong content against the wrong keyword. The type guides tell you to put the keyword in the H1. This skill tells you how to pick the keyword.

**Start with the reader's language, not yours.**
Internal product vocabulary rarely matches search behavior. Your product team calls it "asset correlation." Practitioners search for "find unmanaged devices" or "cloud asset inventory." Search the problem, not the solution. If you're writing a topic page, search the problem your product solves. If you're writing a comparison page, search the decision your buyer is in the middle of making.

**Evaluate keyword fit on three dimensions:**

| Dimension | Question | What you want |
|---|---|---|
| Relevance | Does ranking for this term bring the right reader? | High — a reader who found this page should be a plausible buyer or user |
| Volume | Is anyone actually searching for this? | Enough to be worth the investment — exact numbers vary by market size |
| Attainability | Can this page realistically compete in this SERP? | Look at who's currently ranking — if it's Wikipedia, HubSpot, and Gartner for a generic term, you need a more specific angle |

For B2B technical buyers, low-volume + high-relevance terms almost always outperform high-volume + low-relevance terms. A 200-search/month query from a CISO in-market is more valuable than a 10,000-search/month query from a student writing a paper.

**Primary keyword vs. secondary keywords:**

Every piece of content should have one primary keyword — the term the URL, H1, and meta description optimize for. Secondary keywords are related terms that appear naturally in the body copy, headers, and FAQ sections. They catch related queries without diluting the primary focus.

Primary keyword selection rule: one piece, one primary query. If two queries both seem important, that's two pieces of content.

**Use the research tools available:**
When web search is available, use it to evaluate keyword difficulty in context — look at who currently ranks for the primary keyword, how long those pages are, and what content format dominates the SERP (articles vs. tools vs. forum threads vs. product pages). That SERP analysis tells you what type of content search engines have decided best serves this query — and whether your format matches.

---

## Reading Search Intent

Search intent is the actual goal behind a query. A page that matches the keyword but mismatches the intent will not rank regardless of how well-written it is.

There are four intent types. Identify which one the primary keyword serves before writing a word:

**Informational intent** — The searcher wants to understand something.
- Query signals: "what is," "how does," "guide to," "explained," "vs."
- SERP signals: Articles, definitions, educational content, Wikipedia
- Content response: Topic pages, use case deep dives, research papers, blog explanations
- Conversion expectation: Low and indirect — the reader is not buying today, they're learning

**Commercial intent** — The searcher is evaluating options before deciding.
- Query signals: "best," "alternatives to," "vs.," "review," "compare," "[vendor] pricing"
- SERP signals: Comparison pages, review sites (G2, Gartner), vendor comparison guides
- Content response: Comparison pages, solution pages for high-consideration categories, evaluation guides
- Conversion expectation: Medium — the reader is building a shortlist

**Transactional intent** — The searcher is ready to act.
- Query signals: "buy," "pricing," "demo," "free trial," "[product name]"
- SERP signals: Product pages, pricing pages, conversion-focused landing pages
- Content response: Product pages, pricing pages, direct CTA pages
- Conversion expectation: High — the reader wants to move

**Navigational intent** — The searcher is looking for a specific destination.
- Query signals: Brand name + product, "[company] login," "[product] documentation"
- SERP signals: The brand's own pages dominate
- Content response: Owned pages that should rank for the brand name

**Intent mismatch is the most common SEO failure mode.** Writing a long educational blog post for a transactional query. Building a product page for an informational query. The fix isn't optimization — it's reconceiving the content format.

When the primary keyword has mixed intent signals (some informational, some commercial), the content should lead with education and close with the commercial frame. Lead with what the SERP expects; earn the commercial consideration.

---

## Topic Clusters and Content Architecture

Individual pages don't rank in isolation. Search engines evaluate topical authority — how much of a topic does a site credibly cover? A single well-written page on "attack surface management" will outrank a competitor's equally good page if the site also has three related blog posts, two use case pages, and a research paper that all link together and establish depth.

**The hub-and-spoke model:**

Every topic cluster has a hub (the pillar/topic page) and spokes (supporting content). The hub targets the broad keyword and provides comprehensive coverage. The spokes target specific subtopics, related queries, and long-tail variants. Every spoke links back to the hub; the hub links to the spokes.

When creating any piece of content, identify:
1. **Which hub does this belong to?** If a hub doesn't exist yet, flag that the hub should be created first — or that this piece will function as the hub.
2. **Which other pieces support the same hub?** These are the internal linking opportunities.
3. **What query gap does this fill?** If the hub already exists, the spoke should target a specific subtopic the hub doesn't go deep on.

**Internal linking isn't maintenance — it's architecture.**
Internal links serve two purposes: they tell search engines which pages are related and which are authoritative (link equity), and they route readers to the next logical piece of content (engagement). Both matter. The convention: every piece of content should link to its hub, should link to 2-3 relevant spokes or siblings, and should link to the most relevant product or solution page. Do this in-line, not in a "related reading" footer block — contextual links carry more signal than link lists.

**Content freshness matters unevenly.**
Topic pages and comparison pages age faster than research papers and use case guides. A comparison page that references a competitor who has materially changed their product is a liability, not an asset. Flag content by type when freshness is a ranking factor — and note in the piece's metadata when it was last reviewed.

---

## GEO: Optimizing for AI Engine Retrieval

GEO (Generative Engine Optimization) is the practice of structuring content so that AI engines — ChatGPT, Perplexity, Google AI Overviews, Claude, and others — cite it accurately and favorably in response to relevant queries.

Traditional SEO gets a page to rank. GEO gets a passage within the page to be cited. The unit of optimization has shifted from the page to the quotable chunk.

**How LLM-era search engines decide what to cite:**

AI engines retrieve content by evaluating passage relevance, factual specificity, structural clarity, and source credibility. A passage gets cited when it:
- Directly answers a specific question with a specific answer
- Contains verifiable facts (numbers, named entities, concrete claims)
- Is written in a format the engine can excerpt without losing meaning
- Comes from a source that demonstrates expertise on this topic

Vague, hedged, or overly promotional content does not get cited. Content that leads with "At [Company], we believe that..." is never what an AI engine quotes when a user asks a question.

**The quotable chunk rule:**

Every H2 section of a piece intended for GEO should be independently quotable — if an AI engine excerpted only that section, it would make sense and provide value on its own. This means:
- Lead each section with the answer or conclusion, not the setup
- State the key claim in the first sentence of the section
- Use specific numbers, named frameworks, and concrete examples — not generalizations
- Define terms inline the first time they appear in a section, not just at the top of the article

**Definition blocks are GEO anchors.**
AI engines heavily cite definitions. When a piece introduces or defines a key concept, write the definition as a standalone 2-3 sentence block that answers the question directly. Structure it so that if an AI engine receives the query "what is [term]", the definition block is the exact answer.

Example of a GEO-optimized definition:
> **Attack surface management** is the continuous practice of discovering, inventorying, and monitoring all assets — hardware, software, cloud instances, and credentials — that an attacker could use as an entry point into an organization's environment. Effective attack surface management provides security teams with a real-time, comprehensive inventory that updates as infrastructure changes, rather than a point-in-time snapshot from periodic scans.

**The question-answer format for GEO:**
For any section of a topic page or deep-dive that answers a predictable question, write the H2 header as the question ("How does attack surface management work?") and begin the section with a direct answer. This matches the AI engine's retrieval pattern exactly — it has a user question, it finds content structured as question → answer.

**AI overview optimization differs from featured snippet optimization:**
Featured snippets (traditional Google) favor 40-60 word answers to specific questions. AI overviews (Google SGE, Perplexity) synthesize multiple sources and cite 2-5 passages. For AI overviews, you're optimizing for being one of the cited sources — which means multiple quotable passages per page, not one optimized snippet. Distribute citation-ready paragraphs throughout the piece, not just at the top.

**Entity clarity builds retrieval confidence:**
AI engines organize knowledge around entities — named companies, products, people, frameworks, and concepts. Content that clearly establishes entity relationships ranks higher in AI retrieval. Name your product consistently. Reference frameworks by their official names (NIST CSF, MITRE ATT&CK). When mentioning third parties, name them explicitly rather than using pronouns or vague references. The engine's confidence in a citation increases when entities are unambiguous.

---

## Meta Content as Conversion Copy

The type guides cover meta description character counts. This covers what the meta description actually needs to do.

**The meta description is ad copy, not a summary.**
Its job is not to describe the page — it's to earn the click from a search results page where competing results are one line above and below. Write it to the reader who has already seen the headline and is deciding whether to click.

Effective pattern: `[What the reader gets] + [why this page specifically] + [one credibility signal or specific hook]`

Weak: "Learn about attack surface management in our comprehensive guide."
Strong: "Attack surface management explained for security teams — what it is, how it differs from traditional asset management, and why 73% of breaches involve an unknown asset."

The second version answers the search query, signals depth, and includes a specific number that creates credibility and curiosity.

**Page titles are SEO + click-through rate:**
The page title (HTML `<title>` tag) serves two masters. For search ranking, the primary keyword should appear early — ideally in the first 3-4 words. For click-through rate, the title should signal relevance and create enough interest to earn the click. The compromise: keyword first, benefit or specificity second.

Formula: `[Primary Keyword]: [Specific Benefit or Angle] | [Brand Name]`
Example: `Attack Surface Management: The Complete Guide for Security Teams | [Company]`

---

## Invocation

Load this skill before drafting any content with a search or AI discovery objective. It runs before the type guide's structure is applied — keyword and intent decisions must be resolved first, or the structure gets built around the wrong target.

**Where it applies:**

| Content Type | When to load |
|---|---|
| Web — topic page | Always — topic pages are SEO assets by definition |
| Web — comparison page | Always — comparison pages target commercial-intent queries |
| Web — product page | When targeting a specific search term beyond the product name |
| Web — solution page | When targeting a problem-space search query |
| Blog — thought leadership | When the post has a named search target |
| Blog — use case, data study, event recap, predictions | When search is a distribution channel for this piece |
| Paper — all types | For GEO optimization — quotable passage structure and citation targeting |
| Story — customer story | When the story lives on the website and is intended to rank |

**Where it does not apply:** Email, enablement, briefs, assessments, social posts. These are distributed, not discovered.

**Sequencing:** Load this skill first, resolve the keyword and intent, then load the copywriting skill and apply its structure. Don't draft first and optimize after — content written without a keyword target rarely adapts cleanly to one.