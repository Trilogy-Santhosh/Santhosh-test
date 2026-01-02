# SaaS INC Ticket - Mandatory Pre-Defined Labels Issue

**Date:** December 17, 2025
**Reference Ticket:** LIA-2377 (closed - outdated example from 2024)
**New Kayako ID:** 60264092

---

## Ticket Summary

**Title:** SaaS INC: Mandatory Pre-Defined Labels Enforced in Samsung Community Forum - December 2025 Example

---

## Issue Description

Users in the Samsung Community (Korea region) are unable to post content without selecting mandatory pre-defined labels. The system is enforcing label selection even when labels may not be relevant or appropriate for the user's post, creating a barrier to community engagement.

---

## Details

### Customer Impact
- **Severity:** Medium to High
- **Customer Affected:** Samsung Community Users (Korea region)
- **Business Impact:** Reduced user engagement, potential decrease in community activity, user frustration

### Recent Example (December 2025)

**Post Link:** https://r1.community.samsung.com/t5/기타/스포티파이-화면-안꺼지게-하는법-없을까요/m-p/36156401

**Post Title (Korean):** 스포티파이 화면 안꺼지게 하는법 없을까요
**Translation:** "Is there a way to keep the Spotify screen from turning off?"

**Forum Category:** 기타 (Others/Miscellaneous)

### Configuration Evidence

**Label Node Settings URL:** 
https://r1.community.samsung.com/t5/bizapps/bizappspage/tab/community%3Aadmin/node-display-id/forum-board:kr-community-other

This admin page shows that pre-defined labels are configured as **mandatory** for the forum board.

---

## Steps to Reproduce

1. Navigate to Samsung Community Korea forum: https://r1.community.samsung.com/t5/기타/
2. Attempt to create a new post in the "기타" (Others) category
3. Try to submit the post without selecting a pre-defined label
4. Observe that the system prevents submission or forces label selection

---

## Expected Behavior

- Users should be able to post content without being forced to select pre-defined labels, OR
- Labels should be optional/suggested rather than mandatory, OR
- The label selection should be more flexible to accommodate diverse post topics

---

## Actual Behavior

- The system enforces mandatory selection of pre-defined labels
- Users cannot submit posts without selecting from a limited set of pre-defined labels
- This creates friction in the user posting experience

---

## Root Cause Analysis Needed

1. **Configuration Review:** Why are labels set as mandatory in the forum board configuration?
2. **Business Logic:** Was this intended behavior or a misconfiguration?
3. **Regional Difference:** Is this specific to the Korea community or affecting other regions?

---

## Requested Action

1. **Investigate** the label configuration in the Samsung Community platform
2. **Review** the business requirement for mandatory labels
3. **Evaluate** if labels should be:
   - Made optional
   - Expanded to include more relevant options
   - Removed from certain categories (like "Others/Miscellaneous")
4. **Implement** appropriate fix based on business requirements
5. **Monitor** post-fix to ensure improved user experience

---

## Additional Context

### Why This Ticket vs. LIA-2377

The previous ticket (LIA-2377) was closed because it referenced an outdated example from 2024. This new ticket provides:
- **Recent evidence** from December 2025
- **Active Kayako ticket** (ID: 60264092) showing ongoing customer concern
- **Direct admin configuration link** showing the mandatory label setting

### Supporting Links

- **Kayako Ticket:** 60264092
- **Community Post:** https://r1.community.samsung.com/t5/기타/스포티파이-화면-안꺼지게-하는법-없을까요/m-p/36156401
- **Admin Configuration:** https://r1.community.samsung.com/t5/bizapps/bizappspage/tab/community%3Aadmin/node-display-id/forum-board:kr-community-other
- **Previous Related Ticket:** LIA-2377 (closed)

---

## Priority Justification

**Priority:** Medium-High

**Rationale:**
- Active customer complaint (Kayako 60264092)
- Ongoing issue (December 2025 example)
- User experience degradation
- Potential negative impact on community engagement metrics
- Repeat issue (previous LIA-2377 indicates this is a recurring concern)

---

## Recommended Labels for Jira Ticket

- `saas-inc`
- `samsung-community`
- `user-experience`
- `configuration-issue`
- `korea-region`
- `community-platform`

---

## Next Steps

1. **File this ticket** in Jira (trilogy-eng.atlassian.net)
2. **Assign** to appropriate SaaS support team
3. **Link** to Kayako ticket 60264092
4. **Reference** closed ticket LIA-2377 for historical context
5. **Monitor** for resolution and customer feedback

---

**Prepared by:** Santhosh M  
**Date:** December 17, 2025

