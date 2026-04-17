import time
from flask import Blueprint, request, jsonify, current_app


def create_api_blueprint() -> Blueprint:
    bp = Blueprint("api", __name__)

    @bp.route("/api/status")
    def status():
        db = current_app.config["db"]
        sm = current_app.config["state_machine"]
        rows = db.get_latest_readings(count=1)
        if rows:
            data = rows[0]
            data["state"] = sm.state.value
            return jsonify(data)
        return jsonify({"state": sm.state.value})

    @bp.route("/api/history")
    def history():
        db = current_app.config["db"]
        seconds = request.args.get("seconds", 60, type=int)
        since = time.time() - seconds
        rows = db.get_readings_since(since)
        return jsonify(rows)

    @bp.route("/api/config", methods=["GET"])
    def get_config():
        cfg = current_app.config["config_manager"]
        return jsonify(cfg.all())

    @bp.route("/api/config", methods=["POST"])
    def set_config():
        cfg = current_app.config["config_manager"]
        data = request.get_json()
        for key, value in data.items():
            cfg.set(key, value)
        return jsonify(cfg.all())

    @bp.route("/api/arm", methods=["POST"])
    def arm():
        sm = current_app.config["state_machine"]
        sm.arm()
        return jsonify({"state": sm.state.value})

    @bp.route("/api/disarm", methods=["POST"])
    def disarm():
        sm = current_app.config["state_machine"]
        sm.disarm()
        return jsonify({"state": sm.state.value})

    @bp.route("/api/calibrate", methods=["POST"])
    def calibrate():
        cfg = current_app.config["config_manager"]
        cfg.set("calibrate_requested", True)
        return jsonify({"status": "calibration requested"})

    @bp.route("/api/flights")
    def flights():
        db = current_app.config["db"]
        return jsonify(db.get_flights())

    @bp.route("/api/battery-test", methods=["GET"])
    def battery_test_status():
        db = current_app.config["db"]
        test = db.get_active_battery_test()
        if test:
            test["elapsed"] = time.time() - test["started_at"]
        return jsonify(test)

    @bp.route("/api/battery-test/start", methods=["POST"])
    def battery_test_start():
        db = current_app.config["db"]
        existing = db.get_active_battery_test()
        if existing:
            return jsonify({"error": "Test already running", "id": existing["id"]}), 409
        test_id = db.start_battery_test(time.time())
        return jsonify({"id": test_id, "state": "RUNNING"})

    @bp.route("/api/battery-test/stop", methods=["POST"])
    def battery_test_stop():
        db = current_app.config["db"]
        test = db.get_active_battery_test()
        if not test:
            return jsonify({"error": "No test running"}), 404
        db.stop_battery_test(test["id"], time.time())
        return jsonify({"id": test["id"], "state": "COMPLETED"})

    @bp.route("/api/battery-tests")
    def battery_test_history():
        db = current_app.config["db"]
        return jsonify(db.get_battery_tests())

    return bp
