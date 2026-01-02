# Bug Report: LIA-11649 - Bulk Archive Search Failure

**JIRA Issue:** [LIA-11649](https://trilogy-eng.atlassian.net/browse/LIA-11649)  
**Status:** In Queue  
**Priority:** Highest  
**Created:** December 16, 2025  
**Last Updated:** December 22, 2025  

---

## Executive Summary

Multiple customers across the EUW1 region are experiencing a critical failure in the **Bulk Archival Tool**. When attempting to initiate bulk archive search jobs, the operation fails silently with no user feedback. Backend logs reveal a database constraint violation: `SQLIntegrityConstraintViolationException: Column 'row_version' cannot be null` during the insertion into the `bulk_archive_search_jobs` table.

**Root Cause:** The `row_version` column in the `bulk_archive_search_jobs` table is not being properly initialized during job creation, violating a NOT NULL constraint.

**Impact:** Core moderation functionality is completely broken for affected customers. Moderators must resort to manual per-thread archival, significantly impacting productivity.

---

## Affected Customers

### 1. **Orange FR (Instance: bdffx42837.prod)**
### 2. **eBay UK (Instance: ebay04)**
### 3. **eBay Germany (Instance: ebay07)**

**Common Factor:** All affected instances are hosted in the **EUW1 region**.

---

## Customer-Specific Analysis

### 🔴 Customer 1: Orange France (bdffx42837.prod)

#### Environment Details
- **Customer:** Orange
- **Community URL:** https://communaute.orange.fr
- **Instance ID:** bdffx42837.prod
- **Region:** EUW1
- **Kayako Ticket:** 60259649
- **Reporter:** Ibtiseme Boumaiza (ibtiseme.boumaiza@orange.com)
- **User ID:** 14685270 (Ibtisseme_B)
- **Escalation Status:** Escalated as "core_functionality_defect" after 1 week without resolution

#### Problem Description
The bulk archive search feature on the Content Archivals "Contributions" page fails silently when submitted. No error message is displayed to the user, and no job is created in the system.

#### Reproduction Steps
1. Log in to https://communaute.orange.fr as user Ibtisseme_B (userId 14685270) with moderation rights
2. Navigate to: Content Archivals → Contributions (`/t5/contentarchivals/contentbulkarchivalsearchpage`)
3. Configure a bulk archive search with the following parameters:
   - `locationType=Forum`
   - `location=category:forum` or `category:Internet`
   - `createdRangeTime=3y`
   - `noRepliesRangeTime=1M`
4. Submit the bulk archive search (triggers `/t5/contentarchivals/contentbulkarchivalsearchpage.bulkarchivalsearch:listrerender`)
5. **Observe:** No job appears in the UI, no feedback provided

#### Technical Details
**Sumo Logic Error Logs:**
```
Source: /home/lithium/customer/bdffx42837.prod/serv/lithium.log

WARN  LoggingJdbcDriverEventListener - onQueryFailed(...):
  DefaultQueryInfo[...]
  query=INSERT INTO bulk_archive_search_jobs
    (status, job_created_time, row_version, query_location_id, query_type, ...)
  ...
  java.sql.SQLIntegrityConstraintViolationException: (conn=811042)
    Column 'row_version' cannot be null
  ...
  userEmail: ibtiseme.boumaiza@orange.com
  requestURI: /t5/contentarchivals/contentbulkarchivalsearchpage.bulkarchivalsearch:listrerender
```

#### Impact Assessment
- **Severity:** Critical - Core moderation functionality is completely unavailable
- **Workaround:** Manual per-thread archival (extremely time-consuming)
- **Business Impact:** Significantly reduces moderation productivity and efficiency
- **Customer Sentiment:** Escalated due to lack of response for 1 week

#### Evidence
- Video demonstration provided by customer showing the failure
- Screenshots showing the UI with no job creation

---

### 🔴 Customer 2: eBay UK (ebay04)

#### Environment Details
- **Customer:** eBay UK
- **Community URL:** http://community.ebay.co.uk
- **Instance ID:** ebay04
- **Region:** EUW1
- **Kayako Ticket:** 60266312
- **Sumo Logic Error Logs:** [Link](https://service.sumologic.com/ui/#/search/create?id=njf1CywWl1t9xO1QrYGJ4g5uIiMlKQYVkR0Oszpt)

#### Problem Description
Identical issue to Orange FR - the Bulk Archival Tool in the UK community cannot start new search jobs. The page remains unchanged after submission with no error messages.

#### Symptoms Observed
- **Cannot start new search jobs** - Operation appears to do nothing
- **Bulk Archival page remains unchanged** after form submission
- **No error message displayed** to the user
- **Consistent across multiple boards and browsers**
- **Cache and cookies cleared** - issue persists

#### Technical Details
- Same database constraint violation as Orange FR
- Issue occurs on the same endpoint: `/t5/contentarchivals/contentbulkarchivalsearchpage.bulkarchivalsearch:listrerender`
- Backend logs show `SQLIntegrityConstraintViolationException` related to `row_version` column

#### Confirmed Troubleshooting
- ✅ Content Archiving feature is **enabled** for the community
- ✅ Issue persists **after page refresh**
- ✅ **No jobs are created** in the jobs table
- ✅ **No job status updates** (e.g., "searching", "ready to archive") appear
- ✅ Configuration and permissions are **correct**

#### Customer Conclusion
Since the expected behavior (job creation or status update) does not occur despite correct configuration and permissions, this is confirmed to be a **UI or backend issue**, not a configuration-related problem.

---

### 🔴 Customer 3: eBay Germany (ebay07)

#### Environment Details
- **Customer:** eBay Germany
- **Community URL:** http://community.ebay.de
- **Instance ID:** ebay07
- **Region:** EUW1
- **Kayako Ticket:** 60266312 (shared with eBay UK)
- **Sumo Logic Error Logs:** [Link](https://service.sumologic.com/ui/#/search/create?id=RFrirspZUKBh4jTD7PA51MnTHPUzMRxTvWqdJxrJ)

#### Problem Description
Identical failure mode as eBay UK and Orange FR. The German community experiences the same silent failure when attempting to use the Bulk Archival Tool.

#### Example Configuration Used
**Bulk Archival Search Page URL:**
```
https://community.ebay.de/t5/contentarchivals/contentbulkarchivalsearchpage/node-id/board:729?
  createdRangeTime=3M&
  filter=createdDateRangeTime,location,locationType,noRepliesRangeTime&
  toggleableFieldGroups={}&
  searchPageName=bulkArchivalSearchPage&
  locationType=Forum&
  location=board:mkl&
  noRepliesRangeTime=1M&
  showPastEventsFilter=false&
  hideAcceptedSolutionFilter=false
```

**Affected Board Example:**
- Board: eBay Plus / eBay Punkte
- URL: https://community.ebay.de/t5/eBay-Plus-eBay-Punkte/bd-p/mkl

#### Symptoms Observed
- Identical symptom set to eBay UK
- No job creation in the jobs table
- No status updates after submission
- Silent failure with no user feedback

#### Technical Details
- Same root cause: `row_version` column NULL constraint violation
- Same backend endpoint failure
- Content Archiving feature is enabled but non-functional

---

## Technical Root Cause Analysis

### Database Issue
**Table:** `bulk_archive_search_jobs`  
**Column:** `row_version`  
**Constraint:** NOT NULL  
**Problem:** The column is not being initialized during INSERT operations

### Code Location
**Likely Location:** `SQLContentBulkArchivalDao.addSearchJob()`

### Error Flow
1. User submits bulk archive search form
2. Request is sent to `/t5/contentarchivals/contentbulkarchivalsearchpage.bulkarchivalsearch:listrerender`
3. Backend attempts to insert a new row into `bulk_archive_search_jobs`
4. INSERT fails due to `row_version` being NULL (violates NOT NULL constraint)
5. SQLException is logged but not surfaced to the user
6. No job is created, no feedback is shown
7. User sees no change in the UI (silent failure)

---

## Expected vs. Actual Behavior

### ✅ Expected Behavior
1. User submits a valid bulk archive search
2. System creates a new row in `bulk_archive_search_jobs` with all required fields populated
3. Job appears in the UI with status (e.g., "Searching", "Ready to Archive")
4. TimeBack processes the archive request
5. User receives feedback on job progress

**OR** (for invalid requests):
- Clear error message displayed to the user explaining what went wrong

### ❌ Actual Behavior
1. User submits bulk archive search
2. Database INSERT fails silently
3. No job is created
4. No error message shown to user
5. UI remains unchanged (appears to do nothing)
6. Moderators are left with no feedback

---

## Recommended Engineering Actions

### 🔧 Immediate Fix Required

1. **Investigate Database Schema**
   - Review the DDL for `bulk_archive_search_jobs` table
   - Determine how `row_version` should be populated:
     - Database default value?
     - Application-level initialization?
     - Trigger-based?

2. **Fix Code in `SQLContentBulkArchivalDao.addSearchJob()`**
   - Ensure `row_version` is explicitly set during INSERT
   - Possible solutions:
     - Add explicit value in INSERT statement (e.g., `row_version = 0` or `row_version = 1`)
     - Ensure database has a DEFAULT value for the column
     - Add proper initialization logic in the DAO layer

3. **Improve Error Handling**
   - Surface meaningful error messages to the UI when INSERT fails
   - Add validation before attempting database INSERT
   - Implement user-friendly error feedback mechanism

4. **Add Logging Improvements**
   - Ensure all constraint violations are logged with full context
   - Add debug logging for bulk archive job creation flow

### 🧪 Testing & Validation

1. **Test with Customer Scenarios**
   - Use the exact filter combinations from Orange FR:
     - `locationType=Forum`
     - `location=category:forum`, `category:Internet`
     - `createdRangeTime=3y`
     - `noRepliesRangeTime=1M`
   
2. **Test with eBay Scenarios**
   - Use board-specific searches (e.g., `location=board:mkl`)
   - Test with various time ranges (3 months, 1 month no replies)

3. **Validation Steps Post-Fix**
   - Deploy fix to bdffx42837.prod
   - Validate with customer's exact example filters
   - Confirm jobs are created and appear in UI
   - Verify TimeBack processes jobs correctly
   - Test error scenarios to ensure proper error messaging

### 📊 Regression Testing

1. **Scope Investigation**
   - Determine if this is specific to:
     - EUW1 region only?
     - Certain query filter combinations?
     - Recent code deployment regression?
   - Check if other regions (US-EAST-1, etc.) are affected

2. **Code History Review**
   - Check recent commits to `SQLContentBulkArchivalDao`
   - Review any schema changes to `bulk_archive_search_jobs` table
   - Investigate recent deployments to EUW1 region

---

## Priority Justification

**Priority: Highest** ✅ (Correctly assigned)

### Reasons:
1. **Multiple Enterprise Customers Affected** (Orange, eBay UK, eBay DE)
2. **Core Functionality Broken** - Bulk archival is essential for moderation
3. **Silent Failure** - No workaround available except manual per-thread archival
4. **Productivity Impact** - Moderators cannot efficiently manage content
5. **Customer Escalation** - Orange explicitly escalated after 1 week delay
6. **Potential Wider Impact** - May affect other EUW1 customers not yet reported

---

## Additional Notes

### Common Patterns Across All Customers
- ✅ All instances hosted in **EUW1 region**
- ✅ Same error: **`row_version` cannot be null**
- ✅ Same endpoint failure: **`bulkarchivalsearch:listrerender`**
- ✅ **Silent failure** - no user feedback
- ✅ Content Archiving feature is **enabled** but **non-functional**

### Evidence Provided
- Screenshots from eBay showing the UI state
- Video demonstration from Orange FR
- Sumo Logic error logs for all three customers
- Detailed reproduction steps

---

## Kayako Tickets
- **Orange FR:** 60259649
- **eBay UK + DE:** 60266312

---

## Next Steps for Engineering Team

1. ✅ **Assign to Backend/Database Team** - This is a database constraint violation issue
2. 🔍 **Root Cause Analysis** - Investigate why `row_version` is NULL during INSERT
3. 🛠️ **Implement Fix** - Ensure proper initialization of `row_version` column
4. 🧪 **Test with Customer Data** - Validate fix with exact customer scenarios
5. 🚀 **Deploy to EUW1** - Prioritize deployment to affected region
6. ✉️ **Customer Communication** - Update all three customers once fixed
7. 📊 **Monitor Post-Deployment** - Ensure no similar issues arise

---

**Report Generated:** December 22, 2025  
**Compiled By:** Support Engineering Team  
**Source:** JIRA LIA-11649


