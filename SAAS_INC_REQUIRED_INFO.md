# SAAS INC - Required Information Checklist

## Essential Information (MUST HAVE)

### 1. **Basic Details**
- [ ] Customer name/identifier
- [ ] Kayako ticket number
- [ ] Brief description of the problem
- [ ] Project name (usually "LIA")

### 2. **The Problem**
- [ ] What is broken/not working?
- [ ] When did it start?
- [ ] Is it still happening? (Active/Resolved/Intermittent)

### 3. **Customer Impact**
- [ ] Severity level (Critical/High/Medium/Low)
- [ ] How many users are affected?
- [ ] What business operations are impacted?

### 4. **Evidence**
- [ ] Sumologic query link (with error logs)
- [ ] Error messages or HTTP status codes
- [ ] Community URL where issue occurs
- [ ] Timestamp when issue occurred (with timezone)

### 5. **Priority Justification**
- [ ] Why is this urgent? (outage, customer escalation, SLA risk, etc.)

---

## Nice to Have (Recommended)

### 6. **Technical Details**
- [ ] Error codes or transaction IDs
- [ ] Stack traces or console errors
- [ ] Which service/component is failing?
- [ ] Recent deployments or changes?

### 7. **Steps to Reproduce**
- [ ] How to trigger the issue
- [ ] What should happen vs. what actually happens

### 8. **Workaround**
- [ ] Is there a temporary fix?
- [ ] If not, state "No workaround available"

### 9. **Investigation Needs**
- [ ] What needs to be investigated?
- [ ] What RCA is required?
- [ ] What should be delivered to the customer?

---

## Quick Filing Guide

**Minimum to file a ticket:**
1. Customer name + Kayako ID
2. What's broken
3. Sumologic link with errors
4. Severity/Priority level
5. Customer impact statement

**Good ticket includes:**
- All of the above
- Reproduction steps
- Technical error details
- Requested actions

**Great ticket includes:**
- All of the above
- Workaround (if exists)
- Related past incidents
- Communication plan

---

## Template Locations

- **Full Template:** `SAAS_INC_TEMPLATE.md`
- **This Checklist:** `SAAS_INC_REQUIRED_INFO.md`
- **Example INC:** `SAAS_INC_SCHNEIDER_LOGIN_FAILURE.md`
- **Example CR:** `SAAS_CR_60293980_SSO_KEY.md`

---

## Quick Example

```
Title: [schneider] Community Login Returns HTTP 500
Kayako: 60297560
Problem: Users can't log in to community.se.com - getting 500 errors
Impact: High - All users blocked from logging in
Sumologic: [link to logs showing OAuth 403 errors]
Started: Feb 3, 2026 at 13:53 UTC
Priority: Highest - Complete service outage
Needs: RCA on why idp.se.com OAuth token requests failing with 403
```

---

**Pro Tip:** Start with the minimum info to file the ticket fast, then update with more details as you investigate.
