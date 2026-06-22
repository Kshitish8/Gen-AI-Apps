from flask import Flask,render_template,request
from openai import OpenAI

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
app = Flask(__name__)
 
@app.route('/')
def hello():
    return render_template("home.html")

@app.route('/gpt',methods=['POST'])
def gpt():
    # Safely get the prompt from either 'userprompt' or 'prompt' to avoid BadRequestKeyError
    prompt = request.form.get("userprompt") or request.form.get("prompt") or ""

    # Only call the API when we actually received a prompt
    data = ""
    if prompt:
        p = prompt.strip().lower()
        # handle simple greetings locally to avoid calling the API for trivial prompts
        if p in ("hello", "hi", "hey"):
            data = "Hello! How can I help you today?"
        else:
            response = client.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt = prompt,
                max_tokens=150
            )
            data = response.choices[0].text   
    return render_template("home.html",prompt=prompt,data=data)
app.run(debug  = True)