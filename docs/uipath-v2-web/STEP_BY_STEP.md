# UiPath v2 (Web Portal) - Step-by-Step Guide

## Overview

This guide provides **literal, activity-by-activity instructions** for building the UiPath v2 workflow that automates the web transaction portal for real-time compliance checking.

**Total time to build**: ~60-90 minutes  
**Difficulty**: Intermediate  
**Prerequisites**: UiPath Studio installed, Web portal running, Browser extension installed

---

## Table of Contents

1. [Project Setup](#1-project-setup)
2. [Define Variables](#2-define-variables)
3. [Open Browser and Navigate](#3-open-browser-and-navigate)
4. [Fill Transaction Form](#4-fill-transaction-form)
5. [Submit and Wait for Results](#5-submit-and-wait-for-results)
6. [Extract Results](#6-extract-results)
7. [Save Results to Excel](#7-save-results-to-excel)
8. [Take Screenshot (Optional)](#8-take-screenshot-optional)
9. [Process Multiple Transactions](#9-process-multiple-transactions)
10. [Error Handling](#10-error-handling)
11. [Close Browser](#11-close-browser)
12. [Final Testing](#12-final-testing)

---

## 1. Project Setup

### Step 1.1: Create New Project

1. Open **UiPath Studio**
2. Click **Process** (not Library or Template)
3. In the "New Blank Process" window:
   - **Name**: `ComplianceMonitoring_WebPortal`
   - **Location**: Choose your preferred folder
   - **Description**: `RPA v2 - Web browser automation for live transaction compliance monitoring`
4. Click **Create**

### Step 1.2: Install Required Packages

1. In UiPath Studio, go to **Manage Packages** (top ribbon or Ctrl+P)
2. Click **Official** tab
3. Search and install the following packages:
   - **UiPath.UIAutomation.Activities** - Install latest stable version
   - **UiPath.Excel.Activities** - Install latest stable version
   - **UiPath.System.Activities** - Install latest stable version
4. Click **Save** and wait for installation to complete

### Step 1.3: Install Browser Extension

1. Open Chrome or Edge browser
2. Go to **UiPath Extension** page:
   - Chrome: `chrome://extensions/` → Search for "UiPath Web Automation"
   - Edge: `edge://extensions/` → Search for "UiPath Web Automation"
3. Install and enable the extension
4. Restart browser

### Step 1.4: Verify Web Portal is Running

1. Open terminal in project directory
2. Activate virtual environment:
   ```bash
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate      # Windows
   ```
3. Start API server:
   ```bash
   uvicorn api.main:app --reload
   ```
4. Open browser to `http://localhost:8000/portal`
5. Verify form loads correctly

---

## 2. Define Variables

We'll define variables as we build. Here's the complete reference:

| Variable Name | Type | Scope | Default Value | Purpose |
|---------------|------|-------|---------------|---------|
| `portalUrl` | String | Main | `"http://localhost:8000/portal"` | Web portal URL |
| `browserType` | String | Main | `"Chrome"` | Browser to use (Chrome/Edge) |
| `excelOutputPath` | String | Main | `"C:\RPA\web_results.xlsx"` | Output Excel path |
| `screenshotFolder` | String | Main | `"C:\RPA\Screenshots"` | Screenshot save folder |
| `dtTransactions` | DataTable | Main | - | Input transactions |
| `dtResults` | DataTable | Main | - | Results to save |
| `currentRow` | DataRow | ForEach | - | Current transaction |
| `transactionType` | String | ForEach | - | Transaction type |
| `amount` | String | ForEach | - | Transaction amount |
| `senderCountry` | String | ForEach | - | Sender country |
| `receiverCountry` | String | ForEach | - | Receiver country |
| `beneficiaryName` | String | ForEach | - | Beneficiary name |
| `channel` | String | ForEach | - | Transaction channel |
| `riskScoreText` | String | ForEach | - | Extracted risk score |
| `riskScore` | Double | ForEach | - | Parsed risk score |
| `riskLevel` | String | ForEach | - | Extracted risk level |
| `flaggedRules` | String | ForEach | - | Extracted rules |
| `requiresReview` | String | ForEach | - | Review flag |
| `browser` | Browser | Main | - | Browser instance |

---

## 3. Open Browser and Navigate

### Step 3.1: Add Sequence Container

1. In **Main.xaml**, drag **Sequence** activity onto canvas
2. Properties:
   - **DisplayName**: `Web Portal Automation`

### Step 3.2: Initialize Variables

1. Inside Sequence, drag **Assign** activity
2. Configure:
   - **DisplayName**: `Set Portal URL`
   - **To**: `portalUrl` (Ctrl+K to create, Type: String, Scope: Main)
   - **Value**: `"http://localhost:8000/portal"`

3. Drag another **Assign**:
   - **DisplayName**: `Set Output Path`
   - **To**: `excelOutputPath` (Ctrl+K, String, Main)
   - **Value**: `"C:\RPA\web_results.xlsx"`

4. Drag another **Assign**:
   - **DisplayName**: `Set Screenshot Folder`
   - **To**: `screenshotFolder` (Ctrl+K, String, Main)
   - **Value**: `"C:\RPA\Screenshots"`

### Step 3.3: Create Screenshot Folder

1. Drag **Create Directory** activity
2. Configure:
   - **DisplayName**: `Create Screenshot Folder`
   - **Path**: `screenshotFolder`

### Step 3.4: Add Use Browser Activity

1. Search for `Use Browser` in Activities panel
2. Drag **Use Browser** activity into Sequence
3. Click **Configure browser** button in the activity
4. A browser window will open:
   - Manually navigate to `http://localhost:8000/portal`
   - Wait for page to fully load
   - Click **Confirm** in UiPath popup
5. The browser selector will be auto-configured

**Alternative manual configuration**:
- **Browser type**: Chrome or Edge
- **URL**: `portalUrl` (the variable)
- **Open**: `Always` (or `IfNotOpen` for reusing existing browser)

**Properties**:
- **DisplayName**: `Use Web Portal`
- **Browser**: Click in field, type `browser` (Ctrl+K, type: Browser, scope: Main)

### Step 3.5: Wait for Page Load

1. **Inside** the Use Browser activity's **Do** section, drag **Wait Element Vanish** or **Delay** activity
2. Use **Delay** for simplicity:
   - **Duration**: `00:00:02` (2 seconds)
   - **DisplayName**: `Wait for Page Load`

**Better approach - Wait for specific element**:
1. Drag **Element Exists** activity
2. Click **Indicate element in browser**
3. Click on the form header "New Transaction" in the portal
4. Configure:
   - **DisplayName**: `Verify Form Loaded`
   - **Output**: `formExists` (Ctrl+K, Boolean, Main)
   - **Timeout**: `10000` (10 seconds)

---

## 4. Fill Transaction Form

All activities in this section go **inside** the Use Browser's **Do** section.

### Step 4.1: Prepare Test Data

For this guide, we'll use hardcoded values. Later, we'll modify to read from CSV/Excel.

1. Drag **Assign** activity:
   - **DisplayName**: `Set Transaction Type`
   - **To**: `transactionType` (Ctrl+K, String, ForEach scope - but for now use Main)
   - **Value**: `"Transfer"`

2. Repeat for other fields:
   - `amount` = `"15000.00"`
   - `senderCountry` = `"United States"`
   - `receiverCountry` = `"Iran"`
   - `beneficiaryName` = `"John Doe"`
   - `channel` = `"Online Banking"`

### Step 4.2: Fill Transaction Type Dropdown

1. Drag **Select Item** activity
2. Click **Indicate element**
3. In the portal browser, click on the **Transaction Type** dropdown
4. UiPath will capture the selector
5. Configure properties:
   - **DisplayName**: `Select Transaction Type`
   - **Item**: `transactionType` (the variable)
   - **Selector**: Should auto-populate, verify it includes `id='transactionType'`

**Manual selector** (if needed):
```xml
<html app='chrome.exe' title='SecureBank - Transaction Portal' />
<webctrl id='transactionType' tag='SELECT' />
```

### Step 4.3: Fill Amount Field

1. Drag **Type Into** activity
2. Click **Indicate element**
3. Click on the **Amount** input field in portal
4. Configure:
   - **DisplayName**: `Enter Amount`
   - **Text**: `amount` (the variable)
   - **Options** (in Properties panel):
     - **EmptyField**: ✓ (checked) - clears field before typing
     - **DelayBetweenKeys**: `10` (milliseconds between keystrokes)
     - **SimulateType**: □ (unchecked for now, check if you have issues)

**Selector should include**: `id='amount'`

### Step 4.4: Fill Sender Country

1. Drag **Select Item** activity
2. Indicate the **Sender Country** dropdown
3. Configure:
   - **DisplayName**: `Select Sender Country`
   - **Item**: `senderCountry`
   - **Selector**: Should include `id='senderCountry'`

### Step 4.5: Fill Receiver Country

1. Drag **Select Item** activity
2. Indicate the **Receiver Country** dropdown
3. Configure:
   - **DisplayName**: `Select Receiver Country`
   - **Item**: `receiverCountry`
   - **Selector**: Should include `id='receiverCountry'`

### Step 4.6: Fill Beneficiary Name

1. Drag **Type Into** activity
2. Indicate the **Beneficiary Name** input field
3. Configure:
   - **DisplayName**: `Enter Beneficiary Name`
   - **Text**: `beneficiaryName`
   - **EmptyField**: ✓ (checked)

### Step 4.7: Fill Channel

1. Drag **Select Item** activity
2. Indicate the **Channel** dropdown
3. Configure:
   - **DisplayName**: `Select Channel`
   - **Item**: `channel`
   - **Selector**: Should include `id='channel'`

---

## 5. Submit and Wait for Results

### Step 5.1: Click Submit Button

1. Drag **Click** activity
2. Click **Indicate element**
3. Click on the **"Process Transaction & Check Compliance"** button
4. Configure:
   - **DisplayName**: `Submit Transaction`
   - **Click type**: `Single` (from dropdown)
   - **Mouse button**: `Left` (from dropdown)
   - **Selector**: Should include `id='submitBtn'` or `type='submit'`

### Step 5.2: Wait for Results to Appear

The portal shows a loading spinner, then displays results. We need to wait for results.

**Option 1: Simple Delay** (easiest)
1. Drag **Delay** activity
2. Configure:
   - **DisplayName**: `Wait for API Response`
   - **Duration**: `00:00:05` (5 seconds - adjust based on API speed)

**Option 2: Wait for Element** (more robust - recommended)
1. Drag **Wait Element** activity (not Wait Element Vanish)
2. Click **Indicate element**
3. In the portal, submit the form first manually to see results
4. Indicate the risk score element or results container
5. Configure:
   - **DisplayName**: `Wait for Results`
   - **Timeout**: `15000` (15 seconds)
   - **Selector**: Should include `id='complianceResults'`

**Option 3: Wait for Loading to Disappear**
1. Drag **Wait Element Vanish** activity
2. Indicate the loading spinner (you'll need to catch it mid-load, or use selector directly)
3. Selector:
   ```xml
   <html app='chrome.exe' title='SecureBank - Transaction Portal' />
   <webctrl id='loadingState' />
   ```
4. Configure:
   - **DisplayName**: `Wait for Loading to Complete`
   - **Timeout**: `15000`

**Use Option 2 (Wait Element) for best results.**

---

## 6. Extract Results

All extraction activities go after the "Wait for Results" activity.

### Step 6.1: Extract Risk Score

1. Drag **Get Text** activity
2. Click **Indicate element**
3. Manually submit a transaction in portal to see results
4. Click on the large risk score number (e.g., "0.85")
5. Configure:
   - **DisplayName**: `Get Risk Score`
   - **Output**: `riskScoreText` (Ctrl+K, String, Main or ForEach)
   - **Selector**: Look for the large number in results area

**Note**: The exact selector depends on HTML structure. It might be:
```xml
<html app='chrome.exe' title='SecureBank - Transaction Portal' />
<webctrl parentid='complianceResults' tag='SPAN' class='*text-6xl*' />
```

**Adjust selector as needed** - use UiPath's UI Explorer to find the correct element.

### Step 6.2: Convert Risk Score to Number

1. Drag **Assign** activity
2. Configure:
   - **DisplayName**: `Parse Risk Score`
   - **To**: `riskScore` (Ctrl+K, Double, same scope as riskScoreText)
   - **Value**: `CDbl(riskScoreText.Trim)`

### Step 6.3: Extract Risk Level

1. Drag **Get Text** activity
2. Indicate the risk level badge (e.g., "HIGH RISK")
3. Configure:
   - **DisplayName**: `Get Risk Level`
   - **Output**: `riskLevelRaw` (Ctrl+K, String)

**Selector might be**:
```xml
<html app='chrome.exe' title='SecureBank - Transaction Portal' />
<webctrl parentid='complianceResults' tag='SPAN' class='*rounded-full*' />
```

4. Parse the level (extract just HIGH/MEDIUM/LOW):
   - Drag **Assign** activity
   - **DisplayName**: `Parse Risk Level`
   - **To**: `riskLevel` (Ctrl+K, String)
   - **Value**: `riskLevelRaw.Replace(" RISK", "").Trim`

### Step 6.4: Extract Flagged Rules

This is more complex because rules are in a list.

**Simple approach - Get all text**:
1. Drag **Get Text** activity
2. Indicate the flagged rules container (the section showing rule names)
3. Configure:
   - **DisplayName**: `Get Flagged Rules`
   - **Output**: `flaggedRulesRaw` (Ctrl+K, String)

4. Clean up the text:
   - Drag **Assign**
   - **DisplayName**: `Clean Flagged Rules`
   - **To**: `flaggedRules`
   - **Value**: `flaggedRulesRaw.Replace(vbLf, ", ").Replace(vbCr, "").Trim`

**Advanced approach - Find Children** (optional):
1. Drag **Find Children** activity
2. Indicate the rules container
3. Configure:
   - **Filter**: `<webctrl tag='DIV' class='*border-l-4*' />`
   - **Output**: `ruleElements` (Ctrl+K, IEnumerable<UiElement>)
4. Loop through and extract text from each

**Use simple approach for this guide.**

### Step 6.5: Extract Review Flag

1. Drag **Get Text** activity
2. Indicate the "Review Required: YES/NO" text
3. Configure:
   - **DisplayName**: `Get Review Flag`
   - **Output**: `requiresReviewRaw` (Ctrl+K, String)

4. Parse to get YES/NO:
   - Drag **Assign**
   - **To**: `requiresReview`
   - **Value**: `If(requiresReviewRaw.Contains("YES"), "YES", "NO")`

### Step 6.6: Add Log Messages

1. Drag **Log Message** activity
2. Configure:
   - **DisplayName**: `Log Extracted Results`
   - **Level**: `Info`
   - **Message**: `"Results - Risk Score: " + riskScore.ToString + ", Level: " + riskLevel + ", Review: " + requiresReview`

---

## 7. Save Results to Excel

### Step 7.1: Initialize Results DataTable (Outside Browser)

This goes **outside** the Use Browser activity, before it.

1. Drag **Assign** activity
2. Configure:
   - **DisplayName**: `Initialize Results DataTable`
   - **To**: `dtResults` (Ctrl+K, DataTable, Main)
   - **Value**: `New DataTable`

3. Drag **Invoke Code** activity
4. Click **Edit Code**, paste:
   ```vb
   dtResults.Columns.Add("transaction_type", GetType(String))
   dtResults.Columns.Add("amount", GetType(String))
   dtResults.Columns.Add("sender_country", GetType(String))
   dtResults.Columns.Add("receiver_country", GetType(String))
   dtResults.Columns.Add("beneficiary_name", GetType(String))
   dtResults.Columns.Add("channel", GetType(String))
   dtResults.Columns.Add("risk_score", GetType(Double))
   dtResults.Columns.Add("risk_level", GetType(String))
   dtResults.Columns.Add("flagged_rules", GetType(String))
   dtResults.Columns.Add("requires_review", GetType(String))
   dtResults.Columns.Add("timestamp", GetType(String))
   ```
5. Add Argument:
   - **Name**: `dtResults`
   - **Direction**: `In/Out`
   - **Type**: `DataTable`
   - **Value**: `dtResults`

### Step 7.2: Add Row to DataTable (Inside Browser, After Extraction)

1. Drag **Add Data Row** activity (after all extraction activities)
2. Configure:
   - **DisplayName**: `Add Result Row`
   - **DataTable**: `dtResults`
   - **ArrayRow**: Click `{}` button, paste:
     ```vb
     {
         transactionType,
         amount,
         senderCountry,
         receiverCountry,
         beneficiaryName,
         channel,
         riskScore,
         riskLevel,
         flaggedRules,
         requiresReview,
         DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss")
     }
     ```

### Step 7.3: Write to Excel (Outside Browser, After Use Browser)

1. **After** Use Browser activity ends, drag **Write Range** activity
2. Configure:
   - **DisplayName**: `Write Results to Excel`
   - **Workbook path**: `excelOutputPath`
   - **Sheet name**: `"Web Results"`
   - **Data table**: `dtResults`
   - **Add headers**: ✓ (checked)
   - **Starting cell**: `"A1"`

---

## 8. Take Screenshot (Optional)

This provides audit evidence.

### Step 8.1: Take Screenshot of Results

1. **Inside** Use Browser, **after** extracting results, drag **Take Screenshot** activity
2. Configure:
   - **DisplayName**: `Capture Results Screen`
   - **Output**: `screenshotImage` (Ctrl+K, Image, Main)
   - **Target**: Can indicate specific element (results area) or leave empty for full page

### Step 8.2: Save Screenshot to File

1. Drag **Save Image** activity (after Take Screenshot)
2. Configure:
   - **DisplayName**: `Save Screenshot`
   - **Image**: `screenshotImage`
   - **File path**: `screenshotFolder + "\" + DateTime.Now.ToString("yyyyMMdd_HHmmss") + "_result.png"`

---

## 9. Process Multiple Transactions

To process multiple transactions, we'll read from Excel and loop.

### Step 9.1: Read Input Excel (Before Use Browser)

1. Drag **Read Range** activity (before Use Browser)
2. Configure:
   - **DisplayName**: `Read Input Transactions`
   - **Workbook path**: `"C:\RPA\web_input.xlsx"`
   - **Sheet name**: `"Transactions"`
   - **Data table**: `dtTransactions` (Ctrl+K, DataTable, Main)
   - **Add headers**: ✓ (checked)

**Create input Excel** (`C:\RPA\web_input.xlsx`) with columns:
- transaction_type
- amount
- sender_country
- receiver_country
- beneficiary_name
- channel

### Step 9.2: Wrap Use Browser in For Each Row

1. Drag **For Each Row** activity
2. Move the Use Browser activity **inside** the For Each Row's Body
3. Configure For Each Row:
   - **DisplayName**: `Process Each Transaction`
   - **DataTable**: `dtTransactions`
   - **For Each**: `CurrentRow` (auto-created variable)

### Step 9.3: Read Values from CurrentRow

Replace the hardcoded Assign activities (from Step 4.1) with:

1. Drag **Assign** activities:
   - **To**: `transactionType`
   - **Value**: `CurrentRow("transaction_type").ToString`

2. Repeat for each field:
   - `amount` = `CurrentRow("amount").ToString`
   - `senderCountry` = `CurrentRow("sender_country").ToString`
   - `receiverCountry` = `CurrentRow("receiver_country").ToString`
   - `beneficiaryName` = `CurrentRow("beneficiary_name").ToString`
   - `channel` = `CurrentRow("channel").ToString`

### Step 9.4: Add Row Counter

1. Before For Each Row, initialize counter:
   - **Assign**: `rowIndex` = `0` (Ctrl+K, Int32, Main)
   - **Assign**: `totalRows` = `dtTransactions.Rows.Count`

2. Inside For Each Row, at the start:
   - **Assign**: `rowIndex` = `rowIndex + 1`

3. Add Log Message:
   - **Message**: `"Processing transaction " + rowIndex.ToString + " of " + totalRows.ToString`

---

## 10. Error Handling

### Step 10.1: Add Try-Catch Around Use Browser

1. Right-click on the Use Browser activity
2. Select **Surround with** → **Try Catch**
3. The Use Browser moves inside the Try section

### Step 10.2: Configure Catch Block

1. In Catches section, click **Add new catch**
2. Select **System.Exception**
3. Inside Catch block, drag **Log Message**:
   - **DisplayName**: `Log Error`
   - **Level**: `Error`
   - **Message**: `"ERROR processing transaction: " + exception.Message`

4. Optionally, add **Continue** activity to skip to next transaction

### Step 10.3: Handle Element Not Found

For more specific error handling:

1. In Catches section, add another catch
2. Select **UiPath.Core.ElementOperationException** (element not found)
3. Inside this catch:
   - **Log Message**: `"Element not found - page may not have loaded: " + exception.Message`
   - **Take Screenshot** (for debugging)
   - **Save Image** to error folder

---

## 11. Close Browser

### Step 11.1: Add Finally Block (Optional)

If using Try-Catch:

1. In Try Catch activity, expand **Finally** section
2. Drag **Close Tab** or **Close Application** activity
3. Configure to close the browser

**Note**: Use Browser with **Close** option "Always" will auto-close, so this is optional.

### Step 11.2: Configure Use Browser Close Behavior

1. Click on Use Browser activity
2. In Properties panel:
   - **Close**: `Always` (closes browser when done)
   - Or `Never` (keeps browser open for debugging)
   - Or `IfOpenedByAppOrBrowser` (closes only if UiPath opened it)

---

## 12. Final Testing

### Step 12.1: Create Test Input Excel

Create `C:\RPA\web_input.xlsx` with sample data:

| transaction_type | amount | sender_country | receiver_country | beneficiary_name | channel |
|------------------|--------|----------------|------------------|------------------|---------|
| Transfer | 15000.00 | United States | Iran | John Doe | Online Banking |
| Deposit | 500.00 | United States | United States | Jane Smith | Branch |
| Withdrawal | 25000.00 | United States | North Korea | ACME Corp | ATM |

### Step 12.2: Validate Workflow

1. Click **Validate** (F8)
2. Check for errors in Output panel
3. Fix any validation errors

### Step 12.3: Run in Debug Mode

1. Add breakpoint after "Get Risk Score" activity
2. Press **F7** to run in Debug mode
3. Verify:
   - Browser opens
   - Form is filled correctly
   - Submit button is clicked
   - Results appear
   - Values are extracted

### Step 12.4: Run Full Workflow

1. Press **F5** to run normally
2. Observe:
   - Browser opens
   - All 3 transactions processed
   - Excel file created at `C:\RPA\web_results.xlsx`
   - Screenshots saved to `C:\RPA\Screenshots\`

### Step 12.5: Verify Output

1. Open `C:\RPA\web_results.xlsx`
2. Verify:
   - 3 rows of data (plus header)
   - Risk scores are reasonable (0.0-1.0)
   - Risk levels are LOW/MEDIUM/HIGH
   - Flagged rules are present for high-risk transactions

---

## Workflow Summary Diagram

```
START
  ↓
[Initialize Paths & DataTable]
  ↓
[Read Input Excel] → dtTransactions
  ↓
[FOR EACH ROW in dtTransactions]
  ↓
  [Open Browser] → http://localhost:8000/portal
    ↓
    [Wait for Page Load]
    ↓
    [Fill Form Fields]
      - Transaction Type
      - Amount
      - Sender Country
      - Receiver Country
      - Beneficiary Name
      - Channel
    ↓
    [Click Submit Button]
    ↓
    [Wait for Results]
    ↓
    [Extract Results]
      - Risk Score
      - Risk Level
      - Flagged Rules
      - Review Flag
    ↓
    [Take Screenshot] (optional)
    ↓
    [Add Row to dtResults]
  [Close Browser]
[END FOR EACH]
  ↓
[Write Range to Excel] → web_results.xlsx
  ↓
END
```

---

## Performance Optimization Tips

### 1. Reuse Browser Instance

Instead of opening/closing browser for each transaction:

1. Move **Use Browser** activity **outside** For Each Row loop
2. Only open browser once
3. Inside loop, just fill form and extract results
4. **Benefit**: 5x faster (no browser startup overhead each time)

**Modified structure**:
```
Use Browser
  ↓
  For Each Row
    ↓
    Fill Form → Submit → Extract
  End For Each
End Use Browser
```

### 2. Use Headless Mode (No UI)

For unattended execution:

1. In Use Browser properties:
   - **Private**: ✓ (checked)
   - **Hidden**: ✓ (checked) - browser runs in background
2. **Benefit**: Faster, less resource usage

**Note**: Some selectors may not work in headless mode - test first.

### 3. Reduce Delays

1. Replace fixed **Delay** activities with **Wait Element**
2. Set appropriate timeouts (not too long)
3. **Benefit**: Faster processing, dynamic adaptation to API speed

### 4. Parallel Processing (Advanced)

For processing 100+ transactions:

1. Use **Parallel For Each** activity (requires Orchestrator)
2. Open multiple browser instances
3. Process transactions in parallel
4. **Benefit**: 10x faster with 10 parallel browsers

---

## Troubleshooting

### Browser doesn't open

**Solution**:
1. Verify browser (Chrome/Edge) is installed
2. Install UiPath browser extension
3. Restart UiPath Studio
4. Try manual selector configuration

### Form fields not filled

**Solution**:
1. Add **Delay** (1 second) before first Type Into
2. Check **EmptyField** option is checked
3. Try **SimulateType** = True (faster)
4. Verify selectors using UI Explorer

### Submit button not clicked

**Solution**:
1. Increase delay before Click activity
2. Verify selector highlights correct button
3. Try different click type (ClickImage, etc.)
4. Ensure page is fully loaded

### Results not extracted

**Solution**:
1. Increase timeout in Wait Element (up to 30 seconds)
2. Manually verify results appear in portal
3. Check selectors using UI Explorer
4. Add screenshots before extraction to debug

### "Element not found" error

**Solution**:
1. Maximize browser window (some elements hidden when small)
2. Increase wait timeout
3. Verify page loaded completely
4. Check browser zoom is 100%

---

## Next Steps

1. **Read SELECTORS.md** for complete selector reference
2. **Read TESTING.md** for testing procedures
3. **Optimize** workflow for production (reuse browser, headless mode)
4. **Schedule** in UiPath Orchestrator for unattended runs

---

## Comparison: Single vs Batch Processing

| Approach | Open Browser | Best For |
|----------|--------------|----------|
| **Open/Close Each** | Inside For Each loop | Small batches (< 10 txns) |
| **Reuse Browser** | Outside For Each loop | Medium batches (10-100 txns) |
| **Headless Mode** | Hidden=True | Unattended runs |
| **Parallel Processing** | Multiple browsers | Large batches (100+ txns) |

---

**Document Version**: 1.0  
**Last Updated**: 2026-03-26  
**Related Documents**:
- README.md - v2 Overview
- SELECTORS.md - Web element selectors
- TESTING.md - Testing procedures
