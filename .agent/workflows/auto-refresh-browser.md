---
description: Auto-refresh browser after code changes
---

# Auto-Refresh Browser After Implementation

This workflow ensures the browser automatically refreshes after completing code changes, so the user can immediately see the results without manual F5.

## When to Use
- After editing HTML, CSS, or JavaScript files
- After completing any implementation task
- When user needs to see changes immediately

## Steps

1. **Complete the code implementation**
   - Make all necessary file edits
   - Ensure changes are saved

2. **Trigger browser refresh using browser_subagent**
   ```
   Use browser_subagent with:
   - TaskName: "Refresh Page After Changes"
   - Task: "Refresh the current page at http://localhost:8080/[page].html to show the latest changes. After refreshing, take a screenshot to confirm the page loaded successfully. Return confirmation that the page was refreshed."
   - RecordingName: "auto_refresh_[feature]"
   ```

3. **Verify the refresh**
   - Check the screenshot from browser_subagent
   - Confirm changes are visible
   - Report to user

## Example Usage

After editing `index.html`:
```
browser_subagent(
  TaskName: "Refresh Page After Button Implementation",
  Task: "Refresh the page at http://localhost:8080/index.html to show the latest changes. After refreshing, take a screenshot to confirm the page loaded successfully.",
  RecordingName: "refresh_after_button"
)
```

## Important Notes
- Always refresh after completing implementation
- This is CRITICAL for user workflow
- Without auto-refresh, changes won't be visible
- User specifically requested this as a standard procedure

## Turbo Mode
// turbo-all
This workflow can be auto-run as it only refreshes the browser.
