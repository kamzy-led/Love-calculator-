import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="frontend/build", static_url_path="/")
CORS(app)

# FLAMES mapping (as you specified)
FLAMES = {
    'F': 'Friend',
    'L': 'Love',
    'A': 'Admire',
    'M': 'Marriage',
    'E': 'Enemy',
    'S': 'Secret Lover'
}

def flames_result(name1: str, name2: str) -> dict:
    """
    Implements your FLAMES logic:
    - Remove common letters one-to-one between names (case-insensitive)
    - Count leftover letters
    - Use that count to eliminate letters cyclically from the sequence 'F L A M E S'
      wrapping around from 'S' back to 'F' (i.e., circular counting).
    - Continue until one letter remains.
    Returns: {'key': 'A', 'meaning': 'Admire', 'count': 3}
    """
    if name1 is None: name1 = ""
    if name2 is None: name2 = ""

    # sanitize: keep letters only, lowercase
    a = [c.lower() for c in name1 if c.isalpha()]
    b = [c.lower() for c in name2 if c.isalpha()]

    # remove common letters one-to-one
    # iterate a copy so we can remove safely
    for ch in a[:]:
        if ch in b:
            a.remove(ch)
            b.remove(ch)

    remaining_count = len(a) + len(b)

    # special-case: if zero remaining, decide default. We'll return 'S' (Secret Lover).
    if remaining_count == 0:
        return {'key': 'S', 'meaning': FLAMES['S'], 'count': 0}

    # elimination using circular counting and wrapping from S -> F
    sequence = list(FLAMES.keys())  # ['F','L','A','M','E','S']
    # we will remove at index computed by (count-1) offset from current start.
    current_index = 0
    while len(sequence) > 1:
        # compute index to remove: count is 1-based
        remove_index = (current_index + remaining_count - 1) % len(sequence)
        sequence.pop(remove_index)
        # next counting starts at the same index position (which is the next element after removed,
        # but since list shrank, that index is now the next element). If removed at end, index wraps to 0.
        current_index = remove_index % len(sequence)
    final_key = sequence[0]
    return {'key': final_key, 'meaning': FLAMES[final_key], 'count': remaining_count}

def advice_for(key):
    return {
        'F': "Be a great friend first — friendships can grow into something more.",
        'L': "Love is glowing — small, consistent gestures will help it grow.",
        'A': "Admiration is sweet — a genuine compliment might spark something.",
        'M': "Long-term vibes — think meaningful promises, not haste.",
        'E': "There might be friction — approach gently and seek understanding.",
        'S': "Secret lover — feelings are private. Consider being brave but respectful."
    }.get(key, "")

@app.route("/api/calculate", methods=["POST"])
def calculate():
    try:
        data = request.get_json() or {}
    except Exception:
        data = {}

    name1 = data.get("name1", "")
    name2 = data.get("name2", "")

    if not isinstance(name1, str) or not isinstance(name2, str):
        return jsonify({"error": "Invalid input, names must be strings."}), 400

    result = flames_result(name1, name2)

    ui = {
        "emoji": {
            'F': '😊',
            'L': '❤️',
            'A': '😍',
            'M': '💍',
            'E': '😤',
            'S': '😉'
        }.get(result['key'], '💞'),
        "advice": advice_for(result['key'])
    }
    payload = {**result, **ui}
    return jsonify(payload), 200

# Serve React build files (production)
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    # Serve static files from frontend/build. If path exists in build, serve it,
    # otherwise serve index.html (to support client-side routing).
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    index_path = os.path.join(app.static_folder, "index.html")
    if os.path.exists(index_path):
        return send_from_directory(app.static_folder, "index.html")
    # fallback (developer friendly)
    return "<h3>Frontend build not found. Run frontend build (npm run build)</h3>", 200

# Friendly JSON error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found", "message": "🥺 Love got lost. Use the calculator at /"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Server error", "message": "😵 Something went wrong. Try again later."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
