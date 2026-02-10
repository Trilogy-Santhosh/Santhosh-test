# Bug Report Format

## Bug Title
**Show More Button Not Expanding Messages in Thread with Default Sorting**

---

## Summary
The "Show More" button in thread replies fails to load additional replies when using default sorting/ordering. Changing the sorting option to any other filter (e.g., newest, oldest) temporarily resolves the issue.

---

## Environment Details

### Instance Information
- **Product:** Khoros Community Aurora
- **Version:** 25.12
- **Instance URL:** https://communityforums.atmeta.com
- **Internal Instance ID:** fboculus.prod
- **Maintenance Window:** AMER

### Browser/Client Information
- **Browser:** [Specify: Chrome/Firefox/Safari/Edge]
- **Browser Version:** [e.g., Chrome 120.0.6099.129]
- **OS:** [e.g., Windows 11, macOS Sonoma, etc.]
- **Device Type:** [Desktop/Mobile/Tablet]

---

## Reproduction Steps

### Prerequisites
- Access to affected community instance
- Thread with multiple replies (4+ replies for visibility)
- Thread with default sorting applied

### Steps to Reproduce
1. Navigate to affected thread: `https://communityforums.atmeta.com/discussions/GamesApps/updates-broke-my-device-cannot-revert/1361154`
2. Observe the "Show More" button in the replies section
3. Click on "Show More" button
4. **Expected:** Additional replies should load and display
5. **Actual:** No additional replies load; button does not expand content

### Alternative Test Cases
- Test Case 2: https://community.altera.com/discussions/nios-system/address-space/348954?topicRepliesSort=postTimeDesc
- Core QA Environment: https://lia2512-release-aurora.qa.lithium.com/discussions/pam-forum/test-post-made-at-430-ist/88

---

## Actual Behavior

### What Happens
- Clicking "Show More" button produces no visible change in the UI
- Additional replies remain hidden
- Console errors are present (see Console Errors section below)
- Default sorting parameter appears to cause the issue

### Visual Evidence
- [Attach screenshot showing "Show More" button]
- [Attach screenshot showing console errors]
- [Attach video recording of clicking the button with no response, if possible]

---

## Expected Behavior
- Clicking "Show More" should load and display all remaining replies in the thread
- Replies should appear seamlessly below already loaded content
- No console errors should be present
- Behavior should be consistent regardless of sorting option selected

---

## Console Errors/Logs

### Browser Console Errors
```
[Paste actual console error messages here]
```

### Network Tab Observations
- [HTTP status codes if relevant]
- [Failed API calls, if any]
- [Response payloads showing errors]

### Server Logs (if available)
```
[Any relevant server-side errors]
```

---

## Workaround

### Current Workaround Discovered
1. Change the sorting option from default to any other option (e.g., "Newest" or "Oldest")
2. URL parameter changes to: `?topicRepliesSort=postTimeDesc`
3. All replies become visible immediately
4. Example working URL: https://communityforums.atmeta.com/discussions/GamesApps/updates-broke-my-device-cannot-revert/1361154?topicRepliesSort=postTimeDesc

### Implications
- Issue is specifically tied to default sorting logic/parameter
- Other sorting options work correctly
- Suggests a backend or API issue with default sort handling

---

## Impact Assessment

### Severity
**High** - User-facing functionality broken on production

### Impact Scope
- **Affected Users:** Community members viewing threads with multiple replies
- **Frequency:** Reproducible consistently on affected threads
- **First Observed:** Wednesday, January 7, 2026
- **Reporter:** Superuser in the community (independently verified)

### Business Impact
- Users cannot view all replies in discussions
- Community engagement disrupted
- User experience degraded
- Content accessibility compromised

---

## Root Cause Hypothesis
The default sorting/ordering mechanism appears to have a bug in:
- API endpoint for fetching paginated replies with default sort
- Frontend logic handling "Show More" click events with default sort parameter
- Query parameter handling when no explicit sort is specified

---

## Reproducibility
- **Consistently Reproducible:** Yes
- **Conditions Required:** Thread must be using default sorting (no sort parameter in URL)
- **Environments Affected:** 
  - ✅ Production (fboculus.prod - Meta Community)
  - ✅ Production (Altera Community)
  - ✅ QA Environment (lia2512-release-aurora.qa.lithium.com)

---

## Investigation Progress

### Tests Completed
1. ✅ Reproduced on production instances (Meta, Altera)
2. ✅ Reproduced on QA core environment
3. ✅ Verified workaround (changing sort parameter)
4. ✅ Confirmed console errors present
5. ✅ Validated user report from superuser

### Next Steps
- [ ] File GitHub Issue (GHI) with engineering team
- [ ] Provide console error details
- [ ] Attach HAR file for network analysis
- [ ] Test fix in lower environments before production deployment

---

## Related Information

### Related Tickets
- **Kayako Ticket:** #60281786
- **Reporter:** Kevin Burns (burnskevin@meta.com)
- **Organization:** [Khoros] - Meta Platforms, Inc.

### Related Documentation
- [Link to API documentation for reply pagination]
- [Link to sorting mechanism documentation]

### Similar Issues
- [Reference any similar past issues if applicable]

---

## Priority and Assignment

### Priority
**High** - Production issue affecting user experience

### Component
**Aurora Issues** - Thread Replies / Pagination / Sorting

### Suggested Route
**L2 → Engineering (GHI)**

### Assigned To
[Engineering Team / Component Owner]

---

## Additional Notes

### Community Feedback
- Issue first reported by superuser on January 7, 2026
- Multiple community instances affected
- User expectation is for seamless reply viewing

### Technical Observations
- Sorting parameter in URL: `?topicRepliesSort=postTimeDesc` works correctly
- Default state (no sort parameter) breaks functionality
- Suggests backend may not handle null/default sort parameter correctly

---

## Attachments Checklist
- [ ] Screenshots of issue
- [ ] Console error logs
- [ ] HAR file (network capture)
- [ ] Video recording of issue
- [ ] Browser and OS details
- [ ] Timeline of when issue started

---

## Resolution Tracking

### Status
- **Current Status:** Open - Investigation in progress
- **GHI Filed:** [Link to GitHub issue]
- **Target Fix Version:** [To be determined]
- **ETA:** [To be determined]

### Resolution Notes
[To be filled when resolved]

---

**Report Created By:** Santhosh M (santhosh.m@trilogy.com)  
**Date Created:** January 13, 2026  
**Last Updated:** January 13, 2026


