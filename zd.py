import os,datetime;from openai import OpenAI
try:
 client=OpenAI(api_key=os.environ.get("AI_API_KEY"),base_url="https://api.openai.com/v1")
 response=client.chat.completions.create(model="gpt-4o-mini",messages=[{"role":"system","content":"SEO expert writer"},{"role":"user","content":"Write a 500-word SEO article about 'Paid surveys with instant PayPal payout in 2026'. Make it a markdown guide."}])
 content=response.choices[0].message.content
 today=datetime.date.today().strftime("%Y-%m-%d")
 filename=f"source/_posts/paid-survey-{today}.md"
 os.makedirs(os.path.dirname(filename),exist_ok=True)
 with open(filename,"w",encoding="utf-8") as f:
  f.write(f"---\ntitle: Instant PayPal Surveys {today}\ndate: {today}\n---\n\n{content}")
 print(f"Success: {filename}")
except Exception as e:
 print(f"Error: {e}")
