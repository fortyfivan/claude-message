Process real-world feedback and propose messaging system changes.

Full feedback mode: feedback [input]
Log-only mode: feedback --log [input]

The feedback agent parses input for the signal, source, and confidence. It reads the messaging house and traces every doc the feedback impacts. It proposes specific changes with current → proposed text and reasoning, presents the full impact analysis, and waits for user approval before making any changes. Appends a journal entry after execution.

In log-only mode (--log), the observation is recorded in the journal without proposing changes.

/agents feedback $ARGUMENTS
