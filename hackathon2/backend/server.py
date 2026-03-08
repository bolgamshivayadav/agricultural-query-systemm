from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import json
import os

app = Flask(__name__)
CORS(app)

# ===============================
# SIMPLE DATABASE (JSON FILE)
# ===============================

DB_FILE = "queries.json"

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump([], f)

def load_queries():
    with open(DB_FILE, "r") as f:
        return json.load(f)
    
    
def save_queries(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

def save_query(data):
    queries = load_queries()
    queries.append(data)
    with open(DB_FILE, "w") as f:
        json.dump(queries, f, indent=2)


# ===============================
# KNOWLEDGE BASE
# ===============================

knowledge_base = {
    "tomato_yellow": {
        "causes": [
            "Nitrogen deficiency",
            "Overwatering",
            "Root rot",
            "Pest infestation"
        ],
        "solutions": [
            "Apply nitrogen fertilizer like urea",
            "Ensure proper drainage",
            "Check roots for rot",
            "Use neem oil spray"
        ]
    },

    "wheat_fertilizer": {
        "recommended": [
            "DAP",
            "Urea",
            "MOP"
        ],
        "schedule": [
            "Basal: DAP during sowing",
            "21 days: Urea top dressing",
            "45 days: Second urea application"
        ]
    },

    "pm_kisan": {
        "benefit": "₹6000 per year",
        "installments": "₹2000 every 4 months",
        "website": "https://pmkisan.gov.in"
    }
}


# ===============================
# QUERY PROCESSOR
# ===============================

def detect_category(question):

    q = question.lower()

    if "tomato" in q or "leaf" in q or "yellow" in q:
        return "tomato"

    if "wheat" in q:
        return "wheat"

    if "scheme" in q or "pm kisan" in q:
        return "scheme"

    return "general"


def generate_answer(question):

    category = detect_category(question)

    if category == "tomato":

        data = knowledge_base["tomato_yellow"]

        response = "Tomato yellow leaves problem.\n\n"

        response += "Causes:\n"
        for c in data["causes"]:
            response += "- " + c + "\n"

        response += "\nSolutions:\n"
        for s in data["solutions"]:
            response += "- " + s + "\n"

        return response


    elif category == "wheat":

        data = knowledge_base["wheat_fertilizer"]

        response = "Fertilizer recommendation for wheat.\n\n"

        response += "Recommended fertilizers:\n"
        for f in data["recommended"]:
            response += "- " + f + "\n"

        response += "\nApplication schedule:\n"
        for s in data["schedule"]:
            response += "- " + s + "\n"

        return response


    elif category == "scheme":

        data = knowledge_base["pm_kisan"]

        response = "PM Kisan Scheme\n\n"

        response += "Benefit: " + data["benefit"] + "\n"
        response += "Installments: " + data["installments"] + "\n"
        response += "Apply: " + data["website"]

        return response


    else:

        return "Please ask about crops, fertilizers, pests, or government schemes."


# ===============================
# API ROUTES
# ===============================

@app.route("/")
def home():
    return "Farmassist Python Backend Running"


@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question")

    queries = load_queries()

    queries.append({
        "question": question,
        "time": str(datetime.datetime.now())
    })

    save_queries(queries)

    answer = "Processing your farming question..."

    return jsonify({"answer": answer})

@app.route("/history")
def history():

    queries = load_queries()

    return jsonify(queries)


# ===============================
# RUN SERVER
# ===============================

if __name__ == "__main__":
    app.run(debug=True, port=5000)