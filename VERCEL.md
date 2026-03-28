# Vercel Deployment Instructions

Follow these steps to deploy **The Daily Agent** to Vercel.

## 1. Prerequisites
- A Vercel account.
- The Vercel CLI installed (`npm i -g vercel`) - *optional but recommended*.
- Your project pushed to a GitHub repository.

## 2. Environment Variables
You MUST set the following environment variables in the Vercel Dashboard (**Project Settings > Environment Variables**):

| Variable | Description | Recommendation |
| :--- | :--- | :--- |
| `OPENROUTER_API_KEY` | Your OpenRouter API key for LLM operations. | Required for generating articles. |
| `CRON_SECRET` | A long, random string to secure your trigger endpoints. | Required for securing Cron jobs. |
| `LLM_PROVIDER` | Set to `openrouter`. | Default: `openrouter`. |

## 3. Deployment Steps
1.  **Import to Vercel**: Connect your GitHub repository to a new Vercel project.
2.  **Framework Detection**: Vercel should automatically detect **Vite** as the framework.
3.  **Root Directory**: Keep as `./`.
4.  **Install Commands**:
    - Build Command: `npm run build`
    - Output Directory: `dist`
5.  **Deploy**: Click Deploy.

## 4. Setting Up Cron Jobs
To keep the news cycle running, you need to configure Vercel Cron in your `vercel.json` or through the dashboard. 

Add the following to your `vercel.json` if you want to trigger the news cycle every 2 hours:

```json
{
  "crons": [
    {
      "path": "/api/trigger-cycle",
      "schedule": "0 */2 * * *"
    },
    {
      "path": "/api/trigger-publish",
      "schedule": "*/10 * * * *"
    }
  ]
}
```

> [!IMPORTANT]
> When Vercel Cron calls the endpoints, it will need to include the `X-Cron-Secret` header matching your `CRON_SECRET` environment variable (if you've configured the check in `api.py`).

## 5. Data Persistence Warning
> [!CAUTION]
> The current setup uses local JSON files in the `public/` directory. Vercel's filesystem is **read-only** in production. Changes made via the API (like deleting articles) or the news cycle **will not persist**. 
> **Solution**: Migrate to a database like Supabase, MongoDB Atlas, or Vercel KV for production persistence.
