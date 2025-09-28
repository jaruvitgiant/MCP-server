
import google.generativeai as genai

genai.configure(api_key="//")

model = genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content("สวัสดี Gemini!")
print(response.text)