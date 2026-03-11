Invoke the bootstrap agent to build a complete messaging system.

Before invoking the agent, gather initial context from the user to personalize the messaging guidance.

**Step 1: Check for input materials.** Read `input/` — if files exist, summarize what you found. If empty, note that no input materials were provided.

**Step 2: Gather profile context.** Use AskUserQuestion with these 4 select menus in a single call:

| Question | Header | Options |
|----------|--------|---------|
| What is your role? | Role | Product Marketer, Founder, Marketing Leader, Growth / Demand Gen, Other (Input) |
| What stage is your company at? | Stage | Emerging, Growth, Established, Other (Input) |
| What type of business? | Type | B2B, B2C, B2B2C, Services |
| What market space? | Market | Security, Developer Tools & Infrastructure, Data & AI, Business Software, Other (Input) |

**Step 3: Gather company basics.** Use AskUserQuestion with a text question:
- "Tell me about your company — name, what you do, your website URL, and anything else that helps the agent start researching."

**Step 4: Invoke the agent.** Pass all gathered context (profile answers + company info + input file summary + any user-provided arguments) to the agent:

/agents bootstrap $ARGUMENTS
