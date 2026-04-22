# Boris Cherny: Tips for Using Claude Code

> Source: https://x.com/bcherny/status/2017742741636321619
> Author: Boris Cherny (@bcherny) — Creator of Claude Code
> Date: 2026-01-31
> Stats: 9M views, 50K likes, 104K bookmarks

I'm Boris and I created Claude Code. I wanted to quickly share a few tips for using Claude Code, sourced directly from the Claude Code team. The way the team uses Claude is different than how I use it. Remember: there is no one right way to use Claude Code -- everyones' setup is different. You should experiment to see what works for you!

## 1. Do more in parallel

Spin up 3-5 git worktrees at once, each running its own Claude session in parallel. It's the single biggest productivity unlock, and the top tip from the team. Personally, I use multiple git checkouts, but most of the Claude Code team prefers worktrees -- a little easier to reason about, less cd'ing.

## 2. Start every complex task in plan mode

Pour your energy into the plan so Claude can 1-shot the implementation.

One person has one Claude write the plan, then they spin up a second Claude to review it as a staff engineer.

Another says the moment something goes sideways, they stop and go back to plan mode.

## 3. Invest in your CLAUDE.md

After every correction, end with: "Update your CLAUDE.md so you don't make that mistake again." Claude is eerily good at writing rules for itself.

Ruthlessly edit your CLAUDE.md over time. Keep iterating.

## 4. Create your own skills and commit them to git

Reuse across every project.

Tips from the team:
- If you do something more than once a day, turn it into a skill or command
- Build a /techdebt slash command and run it at the end of every session to find and kill duplicated code

## 5. Claude fixes most bugs by itself

Here's how we do it:

Enable the Slack MCP, then paste a Slack bug thread into Claude and just say "fix." Zero context switching required.

Or, just say "Go fix the failing CI tests." Don't micromanage how.

Point Claude at docker logs to debug production issues.

## 6. Level up your prompting

a. Challenge Claude. Say "Grill me on these changes and don't make a PR until I pass your test." Make Claude be your reviewer. Or, say "Prove to me this works" and have Claude diff behavior between main and your feature branch.

b. After a mediocre result, ask Claude to critique its own output and improve it.

## 7. Terminal & Environment Setup

The team loves Ghostty! Multiple people like its synchronized rendering, 24-bit color, and proper unicode support.

For easier Claude-juggling, use /statusline to customize your status bar to always show context usage and current git branch. Many team members run multiple terminal panes side by side.

## 8. Use subagents

a. Append "use subagents" to any request where you want Claude to throw more compute at the problem.

b. Offload individual tasks to subagents to keep your main agent's context window clean and focused.

c. Route permission requests to Opus 4.5 via a hook -- let it decide whether to allow or deny.

## 9. Use Claude for data & analytics

Ask Claude Code to use the "bq" CLI to pull and analyze metrics on the fly. We have a BigQuery skill checked into the codebase, and everyone on the team uses it for analytics queries directly in Claude Code. Personally, I haven't written a line of SQL in months.

## 10. Learning with Claude

a. Enable the "Explanatory" or "Learning" output style in /config to have Claude explain the *why* behind its changes.

b. Have Claude generate a visual HTML presentation explaining unfamiliar code or concepts.

## Bonus tips from replies

- Make sure Claude explores the codebase to find reusable functions as part of its plan. Also check for duplication in code review (using `claude -p` in CI).
- Claude Code does the first round of code review for every PR at Anthropic. They run Claude Agent SDK (`claude -p`) in a GitHub action as part of CI.
- Run `/permissions` to pre-allow permissions.
- Chrome MCP is a game changer.
