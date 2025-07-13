import os
import requests
import datetime

def get_openai_quota():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY not found in environment.")
        return

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    # Get subscription info (total quota)
    sub_resp = requests.get(
        "https://api.openai.com/v1/dashboard/billing/subscription",
        headers=headers
    )
    if sub_resp.status_code != 200:
        print("Failed to fetch subscription info:", sub_resp.text)
        return

    sub_data = sub_resp.json()
    total_quota = float(sub_data.get("hard_limit_usd", 0))

    # Get usage info (used quota for current month)
    now = datetime.datetime.utcnow()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start_date = start_of_month.strftime("%Y-%m-%d")
    end_date = now.strftime("%Y-%m-%d")

    usage_url = f"https://api.openai.com/v1/dashboard/billing/usage?start_date={start_date}&end_date={end_date}"
    usage_resp = requests.get(usage_url, headers=headers)
    if usage_resp.status_code != 200:
        print("Failed to fetch usage info:", usage_resp.text)
        return

    usage_data = usage_resp.json()
    used_quota = float(usage_data.get("total_usage", 0)) / 100  # OpenAI returns usage in cents

    remaining_quota = total_quota - used_quota

    print(f"Total quota (USD): ${total_quota:.2f}")
    print(f"Used this month (USD): ${used_quota:.2f}")
    print(f"Remaining free quota (USD): ${remaining_quota:.2f}")

if __name__ == "__main__":
    get_openai_quota()
