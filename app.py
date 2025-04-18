from flask import Flask, request, jsonify
from datetime import datetime
import pytz

app = Flask(__name__)

# Secret token for API access
API_TOKEN = "supersecrettoken123"

# Dictionary mapping capital cities to timezones
capital_timezones = {
    "London": "Europe/London",
    "Paris": "Europe/Paris",
    "Berlin": "Europe/Berlin",
    "New Delhi": "Asia/Kolkata",
    "Tokyo": "Asia/Tokyo",
    "Canberra": "Australia/Sydney",
    "Washington": "America/New_York",
    "Ottawa": "America/Toronto",
    "Brasilia": "America/Sao_Paulo",
    "Cairo": "Africa/Cairo",
    "Beijing": "Asia/Shanghai",
    "Moscow": "Europe/Moscow"
}

# Token required decorator
def token_required(f):
    def decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            if token == API_TOKEN:
                return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized. Provide a valid Bearer token."}), 401
    decorator.__name__ = f.__name__
    return decorator

# Route to get time and UTC offset for a capital
@app.route('/api/time', methods=['GET'])
@token_required
def get_city_time():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Missing 'city' parameter in query string."}), 400

    timezone_str = capital_timezones.get(city)
    if timezone_str is None:
        return jsonify({"error": f"City '{city}' is not in our database."}), 404

    tz = pytz.timezone(timezone_str)
    now = datetime.now(tz)
    offset = now.strftime('%z')  # Like +0530
    utc_offset = f"UTC{offset[:3]}:{offset[3:]}"  # Convert to UTC+05:30

    return jsonify({
        "city": city,
        "local_time": now.strftime('%Y-%m-%d %H:%M:%S'),
        "utc_offset": utc_offset
    })

# Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
