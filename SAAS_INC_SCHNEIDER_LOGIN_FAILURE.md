# SaaS INC Ticket - Schneider Community Login Failure

**Date:** February 3, 2026
**Project:** LIA
**Kayako ID:** 60297560

---

## Ticket Summary

**Title:** [schneider] Schneider Community Login Failure (HTTP 500)

---

## Issue Description

We recently experienced an issue where the Schneider Community login was down and returning an HTTP 500 error (see attached screenshot in Kayako 60297560). While the service appears to be working again, the customer requires a Root Cause Analysis to understand what caused this outage.

**Description:** Login on https://community.se.com/ was throwing an HTTP status 500 error. The issue is now resolved but the customer wants a RCA and cause of the outage.

---

## Details

### Customer Impact
- **Severity:** High
- **Customer Affected:** All Schneider Electric Community users
- **Business Impact:** Complete login failure preventing all users from accessing the community platform

### Timeframe
- **Incident Occurred:** February 3, 2026 at 13:53:49 +0100
- **Status:** Resolved (service working again)
- **Duration:** TBD (requires investigation)

### Error Evidence

**Sumologic Query:** https://service.sumologic.com/ui/#/search/create?id=hRw5dDcAOwBGVr7wj0o0Qu3GLLUKAIyN49K9Yveq

**Error Details:**
```
2026-02-03 13:53:49,522 +0100 [exec-12773] ERROR  [cid=krefy84679, tx=e7b06f20-06cf-4bd4-aa09-1104b6e82cee, rh=23.36.67.203, userId=] auth2sso_v2.OauthSsoFailureHandler - [3F7AE95C] Authentication Failed: Critical api call failed with status code:403 request: baseUrl[https://idp.se.com] methodPath[/oauth/token] parameters[[]] headers[[]] callName[OAuthRequestAccessToken] entity[[Content-Type: application/x-www-form-urlencoded; charset=UTF-8,Content-Length: 270,Chunked: false]] response:
```

**Root Cause Indicator:** OAuth authentication failure with Schneider's IDP (https://idp.se.com) returning HTTP 403 status code when requesting OAuth token.

---

## Steps to Reproduce

1. Navigate to https://community.se.com/
2. Attempt to log in with valid credentials
3. Observe HTTP 500 error returned to user
4. Backend logs show OAuth token request to idp.se.com failing with 403

---

## Expected Behavior

- Users should be able to log in successfully to the Schneider Electric Community
- OAuth token request to idp.se.com should return 200 with valid access token
- Community platform should authenticate users and grant access

---

## Actual Behavior

- Login process failed with HTTP 500 error shown to users
- Backend OAuth token request to https://idp.se.com/oauth/token failed with HTTP 403
- Authentication pipeline broke, preventing all user logins

---

## Root Cause Analysis Needed

1. **OAuth Configuration:** Why did idp.se.com start returning 403 for OAuth token requests?
2. **IDP Service Status:** Was there an outage or configuration change on the Schneider IDP side?
3. **Credentials/Permissions:** Did OAuth client credentials expire or get revoked?
4. **Timeline:** When exactly did the issue start and when was it resolved?
5. **Resolution:** What fixed the issue? Was it automatic recovery or manual intervention?
6. **Prevention:** How can we prevent this from happening again?

---

## Requested Action

1. **Investigate** Sumologic logs for the full incident timeline
2. **Identify** the root cause of the 403 error from idp.se.com
3. **Document** what resolved the issue (automatic vs manual)
4. **Provide** complete RCA to customer via Kayako 60297560
5. **Implement** monitoring/alerting to detect similar OAuth failures proactively
6. **Review** OAuth token refresh logic and error handling

---

## Additional Context

### Supporting Links

- **Kayako Ticket:** 60297560
- **Community URL:** https://community.se.com/
- **Sumologic Error Query:** https://service.sumologic.com/ui/#/search/create?id=hRw5dDcAOwBGVr7wj0o0Qu3GLLUKAIyN49K9Yveq
- **IDP Endpoint:** https://idp.se.com/oauth/token

### Technical Details

- **Error Code:** 3F7AE95C
- **Transaction ID:** e7b06f20-06cf-4bd4-aa09-1104b6e82cee
- **Client ID:** krefy84679
- **Request IP:** 23.36.67.203
- **Failed Service:** OAuthRequestAccessToken

---

## Priority Justification

**Priority:** Highest

**Rationale:**
- Complete login failure affecting all Schneider Community users
- Customer escalation requiring RCA
- Service availability issue impacting business operations
- Potential reoccurrence risk if root cause not identified
- Critical authentication infrastructure failure

---

## Recommended Labels for Jira Ticket

- `saas-inc`
- `schneider-community`
- `authentication`
- `oauth-failure`
- `http-500`
- `idp-integration`
- `outage`
- `rca-required`

---

## Next Steps

1. **File this ticket** in Jira (trilogy-eng.atlassian.net) under LIA project
2. **Assign** to SaaS support/engineering team
3. **Link** to Kayako ticket 60297560
4. **Investigate** Sumologic logs for complete incident details
5. **Coordinate** with Schneider IDP team if needed
6. **Provide** RCA to customer once investigation complete

---

**Prepared by:** Santhosh M  
**Date:** February 3, 2026  
**Priority:** Highest
