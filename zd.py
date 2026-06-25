import os datetime;from openai import OpenAI
try:
 client=OpenAI(api_key=os.environ.get("AI_API_KEY"),base_url="https://generativelanguage.googleapis.com/v1beta/openai")
 response=client.chat.completions.create(model="gemini-1.5-flash",messages=[{"role":"system","content":"You are an expert affiliate marketer and SEO writer."},{"role":"user","content":"Write a 500-word SEO-friendly English article about 'Paid surveys with instant PayPal payout in 2026'. Use markdown format, include headings, and do not mention top famous sites like Swagbucks."}])
 content=response.choices[0].message.content
 today=datetime.date.today().strftime("%Y-%m-%d")
 filename=f"source/_posts/paid-survey-{today}.md"
 os.makedirs(os.path.dirname(filename),exist_ok=True)
 with open(filename,"w",encoding="utf-8") as f:
  f.write(f"---\ntitle: Paid Surveys with Instant PayPal Payout\ndate: {today}\ntags: [paid surveys, make money online]\n---\n\n{content}")
 print(f"Success: {filename}")
except Exception as e:
 print(f"Error: {e}")
