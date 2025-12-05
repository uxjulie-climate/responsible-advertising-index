# Overnight Run Instructions

## Quick Start

```bash
# Run this and go to bed
nohup ./run_overnight.sh &

# Check it's running
tail -f overnight_run_*.log
```

**Press Ctrl+C to exit the log viewer** (the script keeps running in background)

---

## What Will Happen Tonight

### Hungarian Ads (37 remaining)
- Start from ad #10 (already did 1-10)
- ~1.5 hours (37 ads × 2.5 min/ad)
- Should get 25-30 successful (some 403 errors expected)

### Cannes Ads (250 total)
- Broken into 10 batches of 25 ads
- ~10 hours (250 ads × 2.5 min/ad)
- Delays between batches to avoid rate limiting
- Expect ~150-200 successful (some will fail)

**Total time:** ~12 hours

---

## Monitoring

### Check Progress

```bash
# See latest log line
tail overnight_run_*.log

# Watch live
tail -f overnight_run_*.log

# Count successful downloads
ls analysis_storage/ | wc -l
```

### Check in Morning

```bash
# See summary
tail -50 overnight_run_*.log

# How many succeeded?
python3 simple_pipeline.py export
cat analysis_storage/all_results_*.csv | wc -l

# Check languages detected
cat analysis_storage/all_results_*.csv | cut -d',' -f5 | sort | uniq -c
```

---

## If Something Goes Wrong

### Script Stopped
```bash
# Check if it's running
ps aux | grep run_overnight

# If not running, resume from where it left off
# Count how many already done
DONE=$(ls analysis_storage/ | wc -l)
echo "Already processed: $DONE ads"

# Resume Hungarian (if less than 47 done)
python3 simple_pipeline.py batch hungarian_ad_catalog.csv --start $DONE

# Then do Cannes
python3 simple_pipeline.py batch video_catalog_20251118_161141.csv
```

### Too Many 403 Errors
- Normal! YouTube rate limits
- The 60-second delays between batches help
- Failed ones can be retried individually later

### Mac Went to Sleep
```bash
# Check if caffeinate died
ps aux | grep caffeinate

# Restart it
caffeinate -d -i -s &
```

---

## Laptop Settings (Belt & Suspenders)

**Recommended before starting:**

1. **Battery Settings**
   - System Settings → Battery
   - Turn OFF "Put hard disks to sleep when possible"
   - Set "Turn display off after" to Never (or 3 hours)

2. **Energy Saver**
   - Set "Prevent automatic sleeping when display is off" to ON

3. **Keep Plugged In**
   - Make sure power cable connected

4. **Close Other Apps**
   - Close browser (lots of tabs = memory issues)
   - Close unnecessary apps

5. **Lid Position**
   - **Best:** Leave open
   - **OK:** Close if caffeinate running and "prevent sleep" enabled

---

## Expected Success Rates

| Dataset | Total | Expected Success | Reason |
|---------|-------|------------------|--------|
| Hungarian | 47 | ~35-40 (75%) | Some videos removed/restricted |
| Cannes | 250 | ~175-200 (70-80%) | Old videos, some unavailable |

**Total expected:** ~210-240 analyzed ads by morning

---

## What You'll Have in the Morning

1. **analysis_storage/** folder with 210+ subfolders
2. **all_results_YYYYMMDD.csv** with all scores
3. **overnight_run_YYYYMMDD.log** with full details
4. **batch_summary_*.json** files for each batch

---

## Dashboard Update

In the morning, update dashboard to load from `analysis_storage/`:

```bash
# The export CSV is dashboard-ready
cat analysis_storage/all_results_*.csv

# Can load directly into existing dashboard
# Or create new consolidated view
```

---

## Start Command

```bash
nohup ./run_overnight.sh &
```

**Then:** Close terminal or press Ctrl+C (script keeps running)

**Monitor:** `tail -f overnight_run_*.log` (optional)

**Go to bed!** 😴

Check results in the morning! ☀️
