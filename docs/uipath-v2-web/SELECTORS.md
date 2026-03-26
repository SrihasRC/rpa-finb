# UiPath v2 Web Element Selectors Reference

## Overview

This document provides **all web element selectors** needed for UiPath v2 browser automation. Each selector includes multiple identification methods (ID, CSS, XPath) for maximum reliability.

**Portal URL**: `http://localhost:8000/portal`

---

## Table of Contents

1. [Form Input Selectors](#1-form-input-selectors)
2. [Button Selectors](#2-button-selectors)
3. [Results Selectors](#3-results-selectors)
4. [Dashboard Metrics Selectors](#4-dashboard-metrics-selectors)
5. [History Selectors](#5-history-selectors)
6. [Selector Best Practices](#6-selector-best-practices)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Form Input Selectors

### Transaction Type (Dropdown)

**Element**: Dropdown select for transaction type  
**Location**: Main form, first field  
**Options**: "Transfer", "Deposit", "Withdrawal"

**Selectors**:
- **ID**: `transactionType`
- **CSS**: `#transactionType`
- **XPath**: `//select[@id='transactionType']`
- **UiPath Selector**:
  ```xml
  <html app='chrome.exe' title='SecureBank - Transaction Portal' />
  <webctrl id='transactionType' tag='SELECT' />
  ```

**Usage in UiPath**:
1. Activity: **Select Item**
2. Target: Use selector above
3. Item: One of: "Transfer", "Deposit", "Withdrawal"

---

### Amount (Number Input)

**Element**: Number input for transaction amount  
**Location**: Main form, second field  
**Validation**: Min 0.01, step 0.01

**Selectors**:
- **ID**: `amount`
- **CSS**: `#amount`
- **XPath**: `//input[@id='amount']`
- **UiPath Selector**:
  ```xml
  <html app='chrome.exe' title='SecureBank - Transaction Portal' />
  <webctrl id='amount' tag='INPUT' type='number' />
  ```

**Usage in UiPath**:
1. Activity: **Type Into**
2. Target: Use selector above
3. Text: Amount as string (e.g., "15000.00")
4. **Important**: Check "Empty field" before typing

---

### Sender Country (Dropdown)

**Element**: Dropdown select for sender country  
**Location**: Main form, third field  
**Options**: USA, UK, Canada, Germany, France, Japan, Singapore, UAE, Australia

**Selectors**:
- **ID**: `senderCountry`
- **CSS**: `#senderCountry`
- **XPath**: `//select[@id='senderCountry']`
- **UiPath Selector**:
  ```xml
  <html app='chrome.exe' title='SecureBank - Transaction Portal' />
  <webctrl id='senderCountry' tag='SELECT' />
  ```

**Usage in UiPath**:
1. Activity: **Select Item**
2. Target: Use selector above
3. Item: Country name (e.g., "United States")

---

### Receiver Country (Dropdown)

**Element**: Dropdown select for receiver country  
**Location**: Main form, fourth field  
**Options**: USA, UK, Canada, Germany, France, Japan, Singapore, UAE, Australia, Iran, North Korea, Syria

**Selectors**:
- **ID**: `receiverCountry`
- **CSS**: `#receiverCountry`
- **XPath**: `//select[@id='receiverCountry']`
- **UiPath Selector**:
  ```xml
  <html app='chrome.exe' title='SecureBank - Transaction Portal' />
  <webctrl id='receiverCountry' tag='SELECT' />
  ```

**Usage in UiPath**:
1. Activity: **Select Item**
2. Target: Use selector above
3. Item: Country name (e.g., "Iran" for high-risk testing)

**Note**: Iran, North Korea, Syria are high-risk countries that will trigger OFAC rules

---

### Beneficiary Name (Text Input)

**Element**: Text input for beneficiary name  
**Location**: Main form, fifth field

**Selectors**:
- **ID**: `beneficiaryName`
- **CSS**: `#beneficiaryName`
- **XPath**: `//input[@id='beneficiaryName']`
- **UiPath Selector**:
  ```xml
  <html app='chrome.exe' title='SecureBank - Transaction Portal' />
  <webctrl id='beneficiaryName' tag='INPUT' type='text' />
  ```

**Usage in UiPath**:
1. Activity: **Type Into**
2. Target: Use selector above
3. Text: Beneficiary name (e.g., "John Smith")

---

### Channel (Dropdown)

**Element**: Dropdown select for transaction channel  
**Location**: Main form, sixth field  
**Options**: "Online Banking", "Branch", "ATM"

**Selectors**:
- **ID**: `channel`
- **CSS**: `#channel`
- **XPath**: `//select[@id='channel']`
- **UiPath Selector**:
  ```xml
  <html app='chrome.exe' title='SecureBank - Transaction Portal' />
  <webctrl id='channel' tag='SELECT' />
  ```

**Usage in UiPath**:
1. Activity: **Select Item**
2. Target: Use selector above
3. Item: "Online Banking", "Branch", or "ATM"

---

## 2. Button Selectors

### Submit Button

**Element**: Main submit button to process transaction  
**Location**: Bottom of form  
**Text**: "Process Transaction & Check Compliance"

**Selectors**:
- **ID**: `submitBtn`
- **CSS**: `#submitBtn` or `button[type='submit']`
- **XPath**: `//button[@id='submitBtn']` or `//button[@type='submit']`
- **UiPath Selector**:
  ```xml
  <html app='chrome.exe' title='SecureBank - Transaction Portal' />
  <webctrl id='submitBtn' tag='BUTTON' type='submit' />
  ```

**Usage in UiPath**:
1. Activity: **Click**
2. Target: Use selector above
3. **Important**: Add "Wait for Ready" = "Complete" to ensure form is ready

---

### View History Button

**Element**: Button to toggle history view  
**Location**: Top navigation bar  
**Text**: "History"

**Selectors**:
- **ID**: `viewHistoryBtn`
- **CSS**: `#viewHistoryBtn`
- **XPath**: `//button[@id='viewHistoryBtn']`
- **UiPath Selector**:
  ```xml
  <html app='chrome.exe' title='SecureBank - Transaction Portal' />
  <webctrl id='viewHistoryBtn' tag='BUTTON' />
  ```

---

### Clear History Button

**Element**: Button to clear transaction history  
**Location**: Recent Transactions section header  
**Text**: "Clear History"

**Selectors**:
- **ID**: `clearHistoryBtn`
- **CSS**: `#clearHistoryBtn`
- **XPath**: `//button[@id='clearHistoryBtn']`
- **UiPath Selector**:
  ```xml
  <html app='chrome.exe' title='SecureBank - Transaction Portal' />
  <webctrl id='clearHistoryBtn' tag='BUTTON' />
  ```

---

## 3. Results Selectors

### Results Container

**Element**: Container div that holds compliance results  
**Location**: Right column, appears after form submission

**Selectors**:
- **ID**: `complianceResults`
- **CSS**: `#complianceResults`
- **XPath**: `//div[@id='complianceResults']`
- **UiPath Selector**:
  ```xml
  <html app='chrome.exe' title='SecureBank - Transaction Portal' />
  <webctrl id='complianceResults' tag='DIV' />
  ```

**Usage**: 
- Use "Element Exists" to check if results appeared
- Use "Wait for Element" before extracting results

---

### Risk Score

**Element**: Large risk score number displayed in results  
**Location**: Inside complianceResults div  
**Format**: "0.85" (decimal 0.0-1.0)

**Selectors**:
- **ID**: `riskScoreValue`
- **CSS**: `#riskScoreValue` or `#complianceResults .text-6xl.font-black`
- **XPath**: `//span[@id='riskScoreValue']` or `//div[@id='complianceResults']//span[@class[contains(., 'text-6xl')]]`
- **UiPath Selector**:
  ```xml
  <html app='chrome.exe' title='SecureBank - Transaction Portal' />
  <webctrl id='riskScoreValue' tag='SPAN' />
  ```

**Usage**:
1. Activity: **Get Text**
2. Target: Use selector above
3. Output: Save to variable `riskScoreText` (String)
4. Convert: `riskScore = CDbl(riskScoreText)` (Double)

**Note**: The element ID `riskScoreValue` may not be present in the actual HTML. Use CSS/XPath alternative if needed.

---

### Risk Level Badge

**Element**: Badge showing LOW/MEDIUM/HIGH risk level  
**Location**: Inside complianceResults, below risk score  
**Format**: "HIGH RISK" (with background color)

**Selectors**:
- **CSS**: `#complianceResults .px-6.py-2.rounded-full`
- **XPath**: `//div[@id='complianceResults']//span[contains(@class, 'rounded-full') and contains(text(), 'RISK')]`
- **UiPath Selector**:
  ```xml
  <html app='chrome.exe' title='SecureBank - Transaction Portal' />
  <webctrl parentid='complianceResults' tag='SPAN' class='*rounded-full*' />
  ```

**Usage**:
1. Activity: **Get Text**
2. Target: Use selector above
3. Output: "HIGH RISK", "MEDIUM RISK", or "LOW RISK"
4. Parse: Extract just the level (HIGH/MEDIUM/LOW)

---

### Flagged Rules List

**Element**: List of flagged compliance rules  
**Location**: Inside complianceResults, below risk level  
**Format**: Multiple rule items in a scrollable div

**Selectors**:
- **CSS**: `#complianceResults .space-y-2` (container) or `#complianceResults .border-l-4` (individual items)
- **XPath**: `//div[@id='complianceResults']//div[contains(@class, 'border-l-4')]`
- **UiPath Selector** (for container):
  ```xml
  <html app='chrome.exe' title='SecureBank - Transaction Portal' />
  <webctrl parentid='complianceResults' tag='DIV' class='*space-y-2*' />
  ```

**Usage**:
1. Activity: **Get Text** (for entire list)
2. Or use **Find Children** to get individual rule items
3. Output: List of rule names (e.g., "BSA_LARGE_CASH")

**Alternative - Get individual rules**:
```xml
<html app='chrome.exe' title='SecureBank - Transaction Portal' />
<webctrl parentid='complianceResults' tag='DIV' class='*border-l-4*' />
```
Then loop through and extract text from each.

---

### Review Required Badge

**Element**: Badge or text indicating if manual review is required  
**Location**: Inside complianceResults, usually near bottom

**Selectors**:
- **XPath**: `//div[@id='complianceResults']//span[contains(text(), 'Review Required') or contains(text(), 'No Review')]`
- **CSS**: `#complianceResults span:contains('Review')`
- **UiPath Selector**:
  ```xml
  <html app='chrome.exe' title='SecureBank - Transaction Portal' />
  <webctrl parentid='complianceResults' tag='SPAN' text='*Review*' />
  ```

**Usage**:
1. Activity: **Get Text**
2. Output: "Review Required: YES" or "Review Required: NO"
3. Parse: Extract YES/NO

---

### Transaction ID (in results)

**Element**: Transaction ID displayed in results  
**Location**: Top of complianceResults

**Selectors**:
- **XPath**: `//div[@id='complianceResults']//span[contains(text(), 'TXN')]`
- **CSS**: `#complianceResults .text-sm.text-gray-600`
- **UiPath Selector**:
  ```xml
  <html app='chrome.exe' title='SecureBank - Transaction Portal' />
  <webctrl parentid='complianceResults' tag='SPAN' text='TXN*' />
  ```

---

## 4. Dashboard Metrics Selectors

### Today's Transaction Count

**Element**: Number displayed in "Today's Transactions" metric card  
**Location**: Top dashboard, second card

**Selectors**:
- **ID**: `todayCount`
- **CSS**: `#todayCount`
- **XPath**: `//p[@id='todayCount']`
- **UiPath Selector**:
  ```xml
  <html app='chrome.exe' title='SecureBank - Transaction Portal' />
  <webctrl id='todayCount' tag='P' />
  ```

**Usage**: Get Text to extract count (e.g., "5")

---

### Flagged Transactions Count

**Element**: Number displayed in "Flagged Transactions" metric card  
**Location**: Top dashboard, third card

**Selectors**:
- **ID**: `flaggedCount`
- **CSS**: `#flaggedCount`
- **XPath**: `//p[@id='flaggedCount']`
- **UiPath Selector**:
  ```xml
  <html app='chrome.exe' title='SecureBank - Transaction Portal' />
  <webctrl id='flaggedCount' tag='P' />
  ```

**Usage**: Get Text to extract count (e.g., "2")

---

## 5. History Selectors

### Transaction History Container

**Element**: Container div holding recent transactions  
**Location**: Bottom section of page

**Selectors**:
- **ID**: `transactionHistory`
- **CSS**: `#transactionHistory`
- **XPath**: `//div[@id='transactionHistory']`
- **UiPath Selector**:
  ```xml
  <html app='chrome.exe' title='SecureBank - Transaction Portal' />
  <webctrl id='transactionHistory' tag='DIV' />
  ```

---

### Individual Transaction Items

**Element**: Individual transaction cards in history  
**Location**: Inside transactionHistory div

**Selectors**:
- **CSS**: `#transactionHistory .bg-white.rounded-lg.p-4`
- **XPath**: `//div[@id='transactionHistory']//div[contains(@class, 'bg-white') and contains(@class, 'rounded-lg')]`
- **UiPath Selector**:
  ```xml
  <html app='chrome.exe' title='SecureBank - Transaction Portal' />
  <webctrl parentid='transactionHistory' tag='DIV' class='*bg-white*rounded-lg*p-4*' />
  ```

**Usage**: Use Find Children to get all transaction items, then extract data from each

---

## 6. Selector Best Practices

### UiPath Selector Strategies

1. **Prefer IDs** (most reliable):
   ```xml
   <webctrl id='amount' />
   ```

2. **Use tag + id combination**:
   ```xml
   <webctrl id='submitBtn' tag='BUTTON' />
   ```

3. **Use parent-child relationships** for nested elements:
   ```xml
   <webctrl id='complianceResults' />
   <webctrl tag='SPAN' class='*text-6xl*' />
   ```

4. **Use wildcards** for dynamic classes:
   ```xml
   <webctrl class='*rounded-full*' />
   ```
   (Matches any class containing "rounded-full")

5. **Avoid absolute XPath** - use relative:
   ```
   ✓ //div[@id='complianceResults']//span
   ✗ /html/body/div[1]/div[2]/div[3]/span
   ```

---

### Selector Validation in UiPath

Before running workflow:

1. **UI Explorer**:
   - Open UI Explorer in UiPath
   - Navigate to portal in browser
   - Click "Indicate element"
   - Verify selector highlights correct element

2. **Test in Isolation**:
   - Create temporary workflow
   - Add "Get Text" activity
   - Verify it extracts expected value
   - Delete temporary workflow

3. **Use Anchor Base** (if selector is unreliable):
   - Use nearby stable element as anchor
   - Example: Use "Amount ($)" label as anchor for amount input field

---

### Dynamic Content Handling

Some elements appear/disappear dynamically:

**Loading State**:
- Wait for `loadingState` div to have class "hidden" before extracting results
- Selector: `<webctrl id='loadingState' class='*hidden*' />`

**Results Appearance**:
- Use "Wait for Element" on `complianceResults` div
- Timeout: 10 seconds (API can take 1-3 seconds)

**Empty History**:
- Check if history contains "No transactions yet" text
- If yes, skip extraction

---

## 7. Troubleshooting

### Element Not Found

**Symptom**: UiPath can't find element, throws "Element not found" error

**Solutions**:

1. **Add delay before interaction**:
   - Add "Delay" activity (1-2 seconds)
   - Or use "Wait for Element" before interacting

2. **Check browser zoom level**:
   - Set browser zoom to 100%
   - Use F11 in browser or `Ctrl+0`

3. **Verify page is fully loaded**:
   - Use "Wait for Ready" = "Complete" property
   - Or check URL matches exactly: `http://localhost:8000/portal`

4. **Maximize browser window**:
   - Use "Maximize Window" activity
   - Some elements may be hidden if window is too small

---

### Wrong Element Selected

**Symptom**: UiPath interacts with wrong field

**Solutions**:

1. **Add more specific attributes**:
   ```xml
   <!-- Less specific -->
   <webctrl tag='INPUT' />
   
   <!-- More specific -->
   <webctrl id='amount' tag='INPUT' type='number' />
   ```

2. **Use idx (index) attribute**:
   ```xml
   <webctrl tag='SELECT' idx='2' />
   ```
   (Selects the 2nd SELECT element)

3. **Use parent container**:
   ```xml
   <webctrl tag='FORM' id='transactionForm' />
   <webctrl tag='INPUT' id='amount' />
   ```

---

### Selector Works Manually but Fails in Workflow

**Symptom**: Selector validates in UI Explorer, but fails when workflow runs

**Solutions**:

1. **Add "Wait for Element" before action**:
   - Timeout: 10 seconds
   - Wait for target element to be visible

2. **Check timing issues**:
   - Previous action may not have completed
   - Add small delay (0.5-1 second) between actions

3. **Verify browser window is in focus**:
   - Use "Activate" activity on browser window
   - Ensures browser has focus before interaction

4. **Check for popups or overlays**:
   - Modal or toast notification may be blocking element
   - Add logic to close modal first

---

### Extracted Text is Empty

**Symptom**: "Get Text" activity returns empty string

**Solutions**:

1. **Check element visibility**:
   - Use "Element Exists" first to verify element is rendered
   - Element may be hidden (CSS: display:none)

2. **Wait for content to load**:
   - Results may not have populated yet
   - Add "Wait for Element" with 5-10 second timeout

3. **Try different extraction method**:
   - Instead of "Get Text", try "Get Attribute" with attribute="innerText" or "textContent"

4. **Inspect element in browser**:
   - Right-click → Inspect
   - Verify element actually contains text
   - May be in child element (span, div, etc.)

---

## Quick Reference Table

| Element | ID | Type | Purpose |
|---------|-----|------|---------|
| Transaction Type | `transactionType` | SELECT | Choose transfer/deposit/withdrawal |
| Amount | `amount` | INPUT (number) | Enter transaction amount |
| Sender Country | `senderCountry` | SELECT | Choose sender country |
| Receiver Country | `receiverCountry` | SELECT | Choose receiver country |
| Beneficiary Name | `beneficiaryName` | INPUT (text) | Enter beneficiary name |
| Channel | `channel` | SELECT | Choose online/branch/ATM |
| Submit Button | `submitBtn` | BUTTON | Submit form |
| Results Container | `complianceResults` | DIV | Contains all results |
| Risk Score | - | SPAN | Display risk score (0.0-1.0) |
| Risk Level | - | SPAN | Display LOW/MEDIUM/HIGH |
| Today Count | `todayCount` | P | Dashboard metric |
| Flagged Count | `flaggedCount` | P | Dashboard metric |
| History Container | `transactionHistory` | DIV | Contains transaction history |

---

## Testing Selectors

### Manual Test Procedure

1. Open portal: `http://localhost:8000/portal`
2. Open browser DevTools (F12)
3. Open Console tab
4. Test selector with JavaScript:

**Test ID selector**:
```javascript
document.getElementById('amount')
// Should return the amount input element
```

**Test CSS selector**:
```javascript
document.querySelector('#complianceResults .text-6xl')
// Should return risk score element after form submission
```

**Test XPath**:
```javascript
$x("//button[@id='submitBtn']")
// Should return array with submit button
```

### Automated Selector Test

Create a simple UiPath workflow:

1. **Open Browser**: `http://localhost:8000/portal`
2. **For each selector in table**:
   - Use "Element Exists" activity
   - Log result: "Selector [name] found: True/False"
3. **Close Browser**

Run workflow - all selectors should return True.

---

**Document Version**: 1.0  
**Last Updated**: 2026-03-26  
**Related Documents**:
- STEP_BY_STEP.md - Workflow building guide
- README.md - v2 overview
- TESTING.md - Testing procedures
