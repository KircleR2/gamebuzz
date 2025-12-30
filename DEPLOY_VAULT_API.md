# 🚀 Deploy Vault API Changes to DigitalOcean Production

> **Platform:** DigitalOcean App Platform  
> **Live Site:** https://passclub.online  
> **Dashboard:** https://cloud.digitalocean.com/apps

## ✅ Local Testing Results

All critical tests passed locally:
- ✅ Database schema with vault fields works
- ✅ CustomerVaultProfile model works
- ✅ SavedPaymentMethod model works
- ✅ Order model accepts vault_customer_id, used_saved_card, saved_card_token

## ⚠️ Current Issue

**Error on production:** `column "vault_customer_id" of relation "events_order" does not exist`

**Root cause:** Migration `0009_order_saved_card_token_order_used_saved_card_and_more` exists in codebase but hasn't been applied to production database.

## 🔧 Solution: Deploy to Apply Migrations

### Option 1: Run Migrations via DigitalOcean Console (Fastest - 2 min) ⭐ RECOMMENDED

This runs the migration immediately without rebuilding your app:

1. **Go to Apps Dashboard:**
   - Visit: https://cloud.digitalocean.com/apps
   - Click on your **gamebuzz** app (the one running passclub.online)

2. **Open Console:**
   - You'll see your app components (web service, database, etc.)
   - Click on your **web component** (usually named `gamebuzz` or `web`)
   - In the top navigation, click the **"Console"** tab
   - Wait for console to connect (~5-10 seconds)

3. **Run Migration:**
   ```bash
   python manage.py migrate events
   ```
   
   You should see:
   ```
   Operations to perform:
     Apply all migrations: events
   Running migrations:
     Applying events.0009_order_saved_card_token_order_used_saved_card_and_more... OK
   ```

4. **Verify Migration Applied:**
   ```bash
   python manage.py showmigrations events
   ```
   
   Expected output should show `[X]` next to 0009:
   ```
   events
    [X] 0001_initial
    [X] 0002_remove_event_timezone_remove_event_zip_code
    ...
    [X] 0009_order_saved_card_token_order_used_saved_card_and_more  ✅
   ```

5. **Test immediately!**
   - Go to https://passclub.online/e/evento-test-1/checkout/
   - The error should be gone!

### Option 2: Redeploy on DigitalOcean (Full rebuild - 5-10 min)

For a clean deployment with all changes:

1. Go to: https://cloud.digitalocean.com/apps
2. Click on your **gamebuzz** app
3. Go to **"Settings"** tab → Click **"gamebuzz"** component
4. Click **"Actions"** dropdown → Select **"Force Rebuild and Deploy"**
5. Wait for build to complete (~5-10 minutes)
6. Migrations will run automatically via `build.sh` line 49

**Expected build log:**
```bash
Running migrations...
Operations to perform:
  Apply all migrations: events, ...
Running migrations:
  Applying events.0009_order_saved_card_token_order_used_saved_card_and_more... OK
```

### Option 3: Git Push (If Auto-Deploy Enabled)

If you have auto-deploy from GitHub enabled:

1. Make sure all changes are committed and pushed
2. Push to your main branch:
```bash
git push origin main
```
3. DigitalOcean will automatically detect and deploy
4. Migrations run during build phase

## 🧪 Testing After Deployment

Once deployed, test with card **4111111111111111** (confirmed working with OTP `123456`):

### Test 1: New Card WITHOUT Saving
1. Go to: https://passclub.online/e/evento-test-1/checkout/
2. Fill in details:
   - Email: `test1@example.com`
   - Card: `4111111111111111`
   - Exp: `12/25`
   - CVV: `123`
   - Name: `TEST USER`
3. **DO NOT** check "Save this card"
4. Complete purchase
5. Enter OTP: `123456` when prompted
6. ✅ Should complete successfully
7. ✅ Card should NOT be saved

### Test 2: New Card WITH Saving (CRITICAL TEST)
1. Go to checkout
2. Fill in details:
   - Email: `test2@example.com`
   - Card: `4111111111111111`
   - Exp: `12/25`
   - CVV: `123`
   - Name: `TEST USER TWO`
3. **✅ CHECK** "Guardar esta tarjeta para compras futuras"
4. Complete purchase
5. Enter OTP: `123456`
6. ✅ Should complete AND save card
7. ✅ Check logs: should see "Tokenizing new card" and "Card tokenized successfully"

### Test 3: Use Saved Card (VERIFY IT WORKS)
1. Go to checkout again with a NEW incognito/private window
2. Enter email: `test2@example.com`
3. Wait 2-3 seconds for cards to load
4. ✅ Saved card should appear: "Visa •••• 1111"
5. Select the saved card radio button
6. ✅ Card entry fields should disappear
7. Complete purchase (no card entry needed!)
8. Enter OTP: `123456` (still required for security)
9. ✅ Should complete with saved card
10. ✅ Check logs: should see "Processing payment with saved card token"

## 🔐 How Card Saving Works (Post-Fix)

**FIXED ISSUE:** Cards were not being saved when 3DS challenge was involved.

**NEW WORKFLOW (Correct):**
1. User checks "Save this card" ✅
2. System **tokenizes card FIRST** (creates vault customer + stores card) 🔒
3. System **pays with the token** (not raw card data) 💳
4. 3DS challenge appears → User enters OTP 🔑
5. Payment completes via webhook 📡
6. **Card is ALREADY saved** (from step 2) ✅

**OLD WORKFLOW (Broken):**
1. User checks "Save this card"
2. System pays with raw card data
3. 3DS challenge appears → User enters OTP
4. Payment completes via webhook
5. ❌ Card data not available in webhook → **CARD NOT SAVED**

**Why the fix works:**
- Tokenization happens BEFORE 3DS challenge
- Card is saved immediately, regardless of 3DS outcome
- Follows Vault API best practices
- Secure: card data never stored in our database

## 📊 Verify in Database (Optional)

After testing, verify data was saved:

```sql
-- Check vault profiles created
SELECT customer_email, vault_customer_id, vault_reference 
FROM events_customervaultprofile;

-- Check saved cards
SELECT cvp.customer_email, spm.last_four, spm.card_brand, spm.is_default
FROM events_savedpaymentmethod spm
JOIN events_customervaultprofile cvp ON spm.customer_profile_id = cvp.id;

-- Check orders using saved cards
SELECT order_number, customer_email, used_saved_card, vault_customer_id
FROM events_order 
WHERE used_saved_card = TRUE;
```

## 🔍 Troubleshooting

### If migration fails during build:

**Error:** `django.db.utils.OperationalError: permission denied`
- **Fix:** Check database user has CREATE TABLE permissions

**Error:** `django.db.utils.ProgrammingError: relation already exists`
- **Fix:** Run `python manage.py migrate events --fake 0009` then redeploy

### If checkout still shows error after deploy:

1. Verify migration ran via Console:
```bash
python manage.py showmigrations events
```

2. Check production logs for errors:
   - In DigitalOcean dashboard → Your App → **"Runtime Logs"** tab
   - Look for migration errors during build
   - Check both Build Logs and Runtime Logs

3. Verify environment variables are set:
   - Go to App → Settings → Component (gamebuzz) → Environment Variables
   - Check `DATABASE_URL` is configured (should be auto-set by managed database)
   - Verify `COBALT_CLIENT_ID` and `COBALT_CLIENT_SECRET` are set
   - Verify `COBALT_WEBHOOK_TOKEN` is set

## 📝 What Changed

### Database:
- ✅ Added `vault_customer_id` to Order table (nullable integer)
- ✅ Added `used_saved_card` to Order table (boolean, default False)
- ✅ Added `saved_card_token` to Order table (varchar 255)
- ✅ Created `events_customervaultprofile` table
- ✅ Created `events_savedpaymentmethod` table

### Code (already deployed):
- ✅ Extended `CobaltPaymentGateway` with Vault API methods
- ✅ Updated `EventCheckoutView` to support saved cards
- ✅ Added `CustomerSavedCardsView` endpoint
- ✅ Updated checkout.html with saved card UI

### What's NOT Changed:
- ✅ Existing payment flow still works (backward compatible)
- ✅ 3DS implementation unchanged
- ✅ Non-saved card payments work exactly as before

## ✨ Success Criteria

After deployment, you should be able to:
- ✅ Complete checkout without saving card (old flow)
- ✅ Complete checkout WITH saving card (new flow)
- ✅ See saved cards when returning customer enters email
- ✅ Pay using saved card (with 3DS challenge)
- ✅ No database errors about missing columns

---

## 🔗 Quick Links for DigitalOcean

- **Apps Dashboard:** https://cloud.digitalocean.com/apps
- **Your App Console:** Apps → gamebuzz → Console tab
- **Runtime Logs:** Apps → gamebuzz → Runtime Logs tab  
- **Environment Variables:** Apps → gamebuzz → Settings → gamebuzz component → Edit
- **Database:** Apps → gamebuzz → Settings → gamebuzz-db (connection info)

## 💡 Pro Tips

**After running migration in Console:**
- Changes are immediate - no rebuild needed!
- Your app keeps running - zero downtime
- Perfect for quick database schema fixes

**If you prefer a full redeploy:**
- Good for ensuring everything is fresh
- Takes longer (~5-10 min) but more thorough
- Use "Force Rebuild and Deploy" option

---

**🎯 Ready to deploy?** 

**Recommended:** Use **Option 1 (Console)** for fastest fix - only 2 minutes!

Then test on https://passclub.online/e/evento-test-1/checkout/ with card `4111111111111111` and OTP `123456`

