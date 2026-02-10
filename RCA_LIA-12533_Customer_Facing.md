# RCA - Intuit TurboTax Community Service Disruption (LIA-12533)

**Incident Period:** January 13-14, 2026  
**Incident Reference:** https://trilogy-eng.atlassian.net/browse/LIA-12533  
**Affected Service:** Khoros Community Classic (ttlc.intuit.com)

---

## What Happened

Starting on January 13, 2026, your TurboTax community platform experienced a service disruption that affected several core features. Community members encountered errors when trying to use key functions like the "Load More" button, the "Help Others" section, profile Posts tabs, and Bulk Action tools. We received your report on January 14, 2026, and our team worked to fully resolve the issue by 9:30 PM UTC the same day. We understand how important these features are to your community experience, and we sincerely apologize for any inconvenience this caused.

---

## Root Cause

We identified that a customization deployment made on Monday, January 13, 2026, contained an error in the endpoint configuration. This configuration error prevented the system from properly processing API requests, which resulted in errors (403 Forbidden and 500 Internal Server responses) when community members attempted to use the affected features.

---

## What We Did

- **Identified the problematic deployment** that was executed on Monday, January 13, 2026
- **Rolled back the recent changes** to restore service functionality
- **Analyzed the endpoint configuration error** that caused the API failures
- **Corrected the configuration error** in the endpoint setup
- **Executed a runtime configuration (RC) update** to deploy the corrected configuration and restore all affected functionalities

---

## What We're Doing Long-Term

- **Enhanced deployment validation procedures** to detect endpoint configuration errors before production deployment
- **Implementing additional automated testing** for critical API endpoints to catch configuration issues earlier
- **Improving monitoring and alerting** for API error rates to reduce detection time for similar incidents
- **Documenting endpoint configuration best practices** to prevent similar configuration errors in future deployments


