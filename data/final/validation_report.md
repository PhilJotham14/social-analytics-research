# Step 4 Full Validation Report

**Generated:** 2026-01-05 19:03:25 UTC  
**Scope:** Full 53-week dataset  
**Coverage:** 2024-09-02 to 2025-09-01

---

## Dataset Overview

**Total Weeks:** 53  
**Total Rows:** 159 (3 platforms × 53 weeks)  
**Expected Rows:** 159  
**Status:** ✅ MATCH
---

## Platform Coverage

### GitHub
**Status:** ✅ Data Collected
- Weeks with data: 53/53
- Total repos collected: 2928
- Top trending topics: python, typescript

### X (Twitter)
**Status:** ⚠️ **Zeros per policy**

All 53 weeks set to zeros due to Recent Search API limitation (7-day window only).

**Explicit Policy Statement:**  
The X API v2 Recent Search endpoint can only access tweets from the past 7 days. Historical data for weeks in 2024-2025 cannot be retrieved. Per approved Step 1 methodology, these weeks are set to zeros with clear policy annotations.

### Reddit
**Status:** ⚠️ **Zeros per policy**

All 53 weeks set to zeros due to OAuth access denial.

**Explicit Policy Statement:**  
Reddit denied OAuth2 API access for this project. Per approved Step 1 methodology, all weeks are set to zeros with clear policy annotations.

---

## Data Quality Checks

### Completeness
- **Expected rows:** 159 (3 platforms × 53 weeks)
- **Actual rows:** 159
- **Status:** ✅ Complete
### Duplicates
- **Status:** ✅ No duplicates detected (verified by platform-week uniqueness)

### Outlier Detection (GitHub)
- **Status:** {"⚠️ " + str(outlier_count) + " potential outlier(s) detected" if outlier_count > 0 else "✅ No significant outliers"}
- **Method:** Flagged weeks with User Interactions >3 std deviations from mean

---

## Engagement Score Methodology

**Formula:**
```
raw_score = 0.3 × log1p(post_count) + 0.7 × log1p(user_interactions)
normalized_score = 100 × (raw - min) / (max - min)
```

**Normalization Window:** Full 53-week dataset (final normalization, not pilot)  
**Scope:** Per platform (GitHub, X, Reddit normalized independently)  
**Precision:** Rounded to 2 decimal places

---

## QA Artifacts Generated

1. ✅ `data_quality_status.csv` - Status per platform-week (ok/missing + notes)
2. ✅ `api_telemetry.csv` - Request counts per platform-week
3. ✅ `plausibility_checks.csv` - Evidence URLs for GitHub verification
4. ✅ `validation_report.md` - This comprehensive report

---

## Summary

**Validation Result:** ✅ Dataset complete and ready for submission
- GitHub: 53/53 weeks populated
- X and Reddit: Zeros documented per approved policy
- Engagement scores: Full-window normalized
- Row count: 159/159 ✅
---

**Report Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}  
**Status:** ✅ Ready for Step 4 submission
