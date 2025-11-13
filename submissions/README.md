# Submissions Directory

This directory stores ad submissions from the public submission form (`submit_ad.py`).

## Structure

Each submission creates two files:

1. **Ad file:** `YYYYMMDD_HHMMSS_BrandName.{ext}`
   - The actual image or video file
   - Extension: jpg, png, mp4, mov, etc.

2. **Metadata:** `YYYYMMDD_HHMMSS_BrandName_metadata.json`
   - Submission details
   - Contact information
   - Ad context
   - Analysis status

## Example

```
submissions/
├── 20250113_143022_EcoThreads.jpg
├── 20250113_143022_EcoThreads_metadata.json
├── 20250113_150534_Oatly.mp4
└── 20250113_150534_Oatly_metadata.json
```

## Metadata Format

### File Upload Submission

```json
{
  "submission_id": "20250113_143022_EcoThreads",
  "timestamp": "2025-01-13T14:30:22.123456",
  "contact": {
    "name": "John Doe",
    "email": "john@example.com"
  },
  "advertiser": {
    "name": "EcoThreads",
    "industry": "Fashion & Apparel",
    "product": "Sustainable Denim"
  },
  "ad": {
    "type": "image",
    "language": "English",
    "tone": "Serious / Informative",
    "intent": "Promote sustainable fashion alternatives",
    "copy": "Buy less. Wear longer. Repair forever.",
    "input_method": "upload_file",
    "file_path": "submissions/20250113_143022_EcoThreads.jpg",
    "url": null
  },
  "submission": {
    "purpose": "Pre-launch review",
    "make_public": true,
    "share_learnings": true
  },
  "status": "pending",
  "analysis_results": null
}
```

### URL Submission

```json
{
  "submission_id": "20250113_150534_Oatly",
  "timestamp": "2025-01-13T15:05:34.789012",
  "contact": {
    "name": "Jane Smith",
    "email": "jane@example.com"
  },
  "advertiser": {
    "name": "Oatly",
    "industry": "Food & Beverage",
    "product": "Oat Milk"
  },
  "ad": {
    "type": "video",
    "language": "English",
    "tone": "Satirical / Ironic",
    "intent": "Mock traditional dairy advertising while promoting plant-based alternatives",
    "copy": null,
    "input_method": "share_url",
    "file_path": null,
    "url": "https://www.youtube.com/watch?v=j4IFNKYmLa8"
  },
  "submission": {
    "purpose": "Competitive benchmarking",
    "make_public": false,
    "share_learnings": true
  },
  "status": "pending",
  "analysis_results": null
}
```

## Status Values

- `pending` - Submitted, waiting for analysis
- `analyzing` - Currently being processed
- `completed` - Analysis done, results available
- `failed` - Analysis failed, needs review
- `archived` - Old submission, kept for records

## Processing Queue

Submissions should be processed in order of timestamp (FIFO).

To view pending submissions:
```bash
ls -t submissions/*_metadata.json | xargs grep '"status": "pending"'
```

## Analysis Workflow

### For File Uploads

1. **Submission** → User uploads file, creates files here
2. **Queue** → Admin or automated process picks up pending submissions
3. **Analysis** → Run through RAI (image or video analysis)
4. **Results** → Update metadata with analysis_results
5. **Notification** → Email results to submitter
6. **Archive** → Optional: Move old submissions to archive folder

### For URL Submissions

1. **Submission** → User provides URL, metadata saved
2. **Download** → Use `download_ads.py` or automated scraper to fetch ad
3. **Save** → Store downloaded file in submissions/ directory
4. **Update** → Update metadata with file_path
5. **Analysis** → Run through RAI (same as file uploads)
6. **Results** → Update metadata with analysis_results
7. **Notification** → Email results to submitter

**Processing URL submissions:**
```bash
# Manual processing
python3 download_ads.py "https://www.youtube.com/watch?v=..."

# Then run analysis via main app
./start.sh
```

## Privacy & Security

**IMPORTANT:**
- This directory may contain sensitive information
- Do NOT commit to public git repositories
- Add to .gitignore
- Implement access controls in production
- Comply with GDPR/data protection laws
- Delete submissions after retention period

## .gitignore

Already configured in project root:
```
submissions/*.jpg
submissions/*.jpeg
submissions/*.png
submissions/*.mp4
submissions/*.mov
submissions/*.json
```

Only this README is tracked in git.

## Future Enhancements

### Automated Processing
Create a background job that:
1. Monitors this directory for new submissions
2. Runs RAI analysis automatically
3. Updates metadata with results
4. Sends email notifications
5. Moves to archive after 30 days

### Database Integration
When implementing database (Supabase/PostgreSQL):
- Store metadata in database instead of JSON files
- Keep only file paths here
- Enable better querying and analytics

### Cloud Storage
For production, consider:
- Moving files to Cloud Storage / S3
- Keep only metadata locally
- Better scalability and backups

---

**Setup Date:** 2025-01-13
**Purpose:** Ad submission queue for RAI analysis
