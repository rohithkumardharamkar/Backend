import google.generativeai as genai

genai.configure(api_key="AIzaSyBxmVaLo5VWvpPDQSqPAz2rm7BBKoySbCE")

model = genai.GenerativeModel("models/gemini-2.0-flash")  # or gemini-1.5-pro
def ai(content):
    response = model.generate_content(content)
    return response.text


ai('You are an chat bot for my donation manement wesite called Altrusys give reply to donation and cahrity related if asked rather than other question ask them to ask about only donationd and charity')