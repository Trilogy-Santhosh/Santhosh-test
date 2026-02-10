# SaaS Change Request - Generate Lithium SSO Key for SANE Stage

**Date:** February 6, 2026  
**Project:** LIA  
**Kayako ID:** 60293980  
**Type:** Change Request

---

## Title/Summary

**[sane] Generate lithium SSO key for stage**

---

## Change Description

Customer (SANE Solutions) is currently working through setting up Khoros SSO to work with Microsoft Azure and requires clarification on which SSO provisioning details need to be provided by Khoros.

The customer is asking if the following details need to be provisioned by Khoros:

1. **SSO Encryption Key**
2. **SSO Client ID**
3. **SSO Client Domain**
4. **SSO Server ID**

**Reference Documentation:**  
https://developer.khoros.com/khoroscommunitydevdocs/docs/lithiumsso-token#lithiumsso-token-generation-example

---

## Business Justification

Customer is implementing Microsoft Azure SSO integration with their Khoros Community stage environment and needs to understand:
- Which SSO configuration values must be provisioned by Khoros
- Which values they need to configure on their Azure/customer side
- The complete setup process for LithiumSSO token-based authentication with Azure

Without this information, the customer cannot complete their SSO implementation and may face delays in their deployment timeline.

---

## Change Type

**Configuration Provisioning / Customer Support**
- Generate/provide SSO encryption keys
- Configure SSO client credentials
- Document SSO setup requirements for Azure integration

---

## Risk Assessment

**Risk Level:** Low

**Rationale:**
- Stage environment only (no production impact)
- Standard SSO provisioning procedure
- Well-documented integration type
- No system downtime required
- Configuration-only change

**Potential Risks:**
- Incorrect key generation could delay customer implementation
- Misconfigured SSO parameters could cause authentication failures in stage

---

## Impact Analysis

### Affected Environment
- **Customer:** SANE Solutions
- **Environment:** Stage only
- **Instance:** Stage community instance
- **SSO Provider:** Microsoft Azure
- **Integration Type:** LithiumSSO Token-based authentication

### Customer Impact
- **Severity:** Medium (blocking customer SSO implementation)
- **Users Affected:** Stage environment only (no production users impacted)
- **Business Impact:** Customer cannot proceed with SSO testing until provisioning complete
- **Downtime Required:** None

### Expected Outcome
Customer receives necessary SSO configuration details to complete Azure SSO integration on their stage environment.

---

## Implementation Details

### Step 1: Review Customer Requirements
- Analyze customer's Azure SSO setup
- Identify which parameters Khoros must provision
- Determine which parameters customer configures

### Step 2: Generate SSO Keys/Credentials
- Generate SSO Encryption Key (if Khoros-managed)
- Provision SSO Client ID (if required)
- Configure SSO Client Domain
- Set up SSO Server ID

### Step 3: Document Configuration
- Provide complete list of Khoros-provisioned values
- Document customer-side configuration requirements
- Include step-by-step Azure integration guide
- Reference official documentation

### Step 4: Deliver to Customer
- Securely provide generated keys/credentials via Kayako
- Include configuration instructions
- Offer to assist with integration testing

---

## Testing/Validation Plan

### Pre-Change Verification
- [ ] Review customer's Azure SSO configuration requirements
- [ ] Confirm stage environment access
- [ ] Validate SSO documentation is current

### Post-Change Validation
- [ ] Verify generated keys are properly formatted
- [ ] Confirm customer received all required credentials
- [ ] Test SSO authentication flow in stage environment
- [ ] Validate token generation example works with provided keys
- [ ] Document any Azure-specific configuration notes

### Success Criteria
- [ ] Customer has all Khoros-provisioned SSO values
- [ ] Customer understands which values they must configure
- [ ] SSO test authentication succeeds in stage environment
- [ ] Customer confirms they can proceed with implementation

---

## Rollback Plan

**N/A** - This is a provisioning/configuration change with no system modifications.

If keys are incorrect:
1. Generate new SSO keys
2. Update customer with corrected values
3. Customer updates their Azure configuration
4. Re-test authentication

**Recovery Time:** < 1 hour (regenerate and provide new keys)

---

## Schedule Information

### Timeline
- **Start Date:** February 7, 2026
- **End Date:** February 20, 2026
- **Due Date:** February 20, 2026

### Maintenance Window
- **Requires Maintenance Window:** NO
- **Reason:** Configuration provisioning only, no system changes

### Duration Estimate
- **Provisioning:** 1-2 hours
- **Customer configuration:** (Customer-side activity)
- **Testing:** 1-2 hours

---

## Priority/Severity

**Priority:** Highest

**Justification:**
- Blocking customer SSO implementation
- Time-sensitive customer requirement
- Quick win with clear resolution path
- Stage environment (lower risk than production)

---

## Contact Information

### Requestor
- **Name:** Santhosh M
- **Email:** santhosh.m@trilogy.com
- **Role:** Customer Support Engineer

### Technical Contact
- **Team:** SaaSOps
- **Escalation:** Customer Support

### Customer Contact
- **Organization:** SANE Solutions
- **Environment:** Stage
- **Kayako Ticket:** 60293980

---

## Related Information

### Supporting Links
- **Kayako Ticket:** https://khoros.kayako.com/agent/tickets/60293980
- **Documentation:** https://developer.khoros.com/khoroscommunitydevdocs/docs/lithiumsso-token#lithiumsso-token-generation-example
- **SSO Integration Guide:** [To be provided]

### Technical Details
- **SSO Type:** LithiumSSO Token-based
- **Identity Provider:** Microsoft Azure
- **Authentication Method:** Token generation
- **Environment:** Stage (non-production)

### Related Documentation
- LithiumSSO Token Generation: https://developer.khoros.com/khoroscommunitydevdocs/docs/lithiumsso-token
- Azure SSO Integration Guide: [Internal documentation]
- SSO Best Practices: [Internal knowledge base]

---

## Recommended Jira Labels

```
saas-cr
sso-provisioning
lithiumsso
azure-sso
stage-environment
customer-support
sane-solutions
configuration-change
```

---

## Additional Context

### Customer Question Summary
The customer needs to understand the division of responsibility for SSO configuration:

**Khoros-Provided (likely):**
- SSO Encryption Key (generated by Khoros)
- SSO Server ID (Khoros community instance identifier)

**Customer-Configured (likely):**
- SSO Client ID (Azure application ID)
- SSO Client Domain (customer's domain)

**Action Required:**
Confirm the above assumptions and provide the customer with:
1. The generated SSO Encryption Key for their stage instance
2. The SSO Server ID for their stage community
3. Clear documentation on configuring Azure-side parameters
4. Any additional setup steps specific to Azure integration

---

## Change Implementer

**Primary:** SaaSOps Team  
**Secondary:** Customer Support (coordination and communication)

---

## Change Requester

**Customer Support** on behalf of SANE Solutions

---

## Cost Impact

**Unable to Determine**

**Rationale:**
- Standard provisioning activity (no additional infrastructure cost)
- Part of existing customer support operations
- No third-party service costs
- Labor cost within normal operations budget

---

## Impact Amount

**0** (Zero)

**Explanation:**
- No communities affected by the provisioning itself
- Stage environment only (no production user impact)
- Configuration generation has no customer-facing changes
- Testing isolated to customer's stage instance

---

## Requested Action

1. **Review** the customer's SSO integration requirements for Microsoft Azure
2. **Generate** necessary SSO keys and credentials for SANE stage environment
3. **Document** which values Khoros provides vs. customer configures
4. **Provide** the generated keys securely via Kayako ticket 60293980
5. **Include** step-by-step Azure SSO integration instructions
6. **Offer** assistance with testing and validation
7. **Update** Kayako ticket with resolution and documentation

---

## Next Steps

### Immediate Actions
1. **File this CR** in Jira (trilogy-eng.atlassian.net) under LIA project
2. **Assign** to SaaSOps team
3. **Link** to Kayako ticket 60293980
4. **Generate** SSO encryption key for SANE stage instance
5. **Document** complete SSO setup requirements

### Follow-up Actions
1. **Deliver** SSO credentials to customer via secure method
2. **Schedule** testing session with customer if needed
3. **Validate** SSO authentication in stage environment
4. **Document** any Azure-specific configuration notes
5. **Close** CR and Kayako ticket once complete

---

## Resolution Tracking

### Status
- **Current Status:** Open - Awaiting provisioning
- **Jira Ticket:** [To be created]
- **Kayako Ticket:** 60293980
- **Target Completion:** February 20, 2026

### Resolution Notes
[To be filled when resolved]

---

**Prepared by:** Santhosh M  
**Date:** February 6, 2026  
**Priority:** Highest  
**Change Type:** Configuration Provisioning  
**Maintenance Window Required:** NO
