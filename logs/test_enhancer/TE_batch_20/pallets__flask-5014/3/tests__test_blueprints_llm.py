import pytest
import flask
import pytest
import flask

def test_none_name_raises_value_error_and_message():
    # None should be treated as empty and raise ValueError with the
    # explicit "'name' may not be empty." message.
    with pytest.raises(ValueError) as excinfo:
        flask.Blueprint(None, __name__)  # type: ignore[arg-type]
    assert str(excinfo.value) == "'name' may not be empty."

def test_whitespace_name_creation_and_registration(app):
    # A name that is only whitespace should be accepted by Blueprint()
    # and be usable as a key in app.blueprints after registration.
    name = "   "
    bp = flask.Blueprint(name, __name__)
    assert bp.name == name
    app.register_blueprint(bp)
    assert name in app.blueprints
    assert app.blueprints[name] is bp

def test_whitespace_name_generates_endpoint_with_space(app, client):
    name = "   "
    bp = flask.Blueprint(name, __name__)

    @bp.route("/")
    def index():
        # Return the endpoint string so we can assert its exact value
        return flask.request.endpoint

    app.register_blueprint(bp, url_prefix="/py")
    rv = client.get("/py/")
    assert rv.status_code == 200
    assert rv.data == (name + ".index").encode()

def test_whitespace_name_url_for_generation(app):
    name = "\t"
    bp = flask.Blueprint(name, __name__)

    @bp.route("/")
    def index():
        return ""

    app.register_blueprint(bp, url_prefix="/tab")

    with app.test_request_context():
        # url_for should accept the dotted endpoint name containing the tab.
        assert flask.url_for(f"{name}.index") == "/tab/"

def test_newline_whitespace_name_allowed_and_accessible(app, client):
    name = "\n"
    bp = flask.Blueprint(name, __name__)

    @bp.route("/n")
    def index():
        return flask.request.endpoint

    app.register_blueprint(bp, url_prefix="/nl")
    rv = client.get("/nl/n")
    assert rv.status_code == 200
    assert rv.data == (name + ".index").encode()

def test_mixed_whitespace_name_allowed(app, client):
    name = " \t\n "
    bp = flask.Blueprint(name, __name__)

    @bp.route("/mix")
    def index():
        return flask.request.endpoint

    app.register_blueprint(bp, url_prefix="/mix")
    rv = client.get("/mix/mix")
    assert rv.status_code == 200
    assert rv.data == (name + ".index").encode()

def test_whitespace_name_present_in_view_functions_keys(app):
    name = "  "
    bp = flask.Blueprint(name, __name__)

    @bp.route("/vf")
    def index():
        return ""

    app.register_blueprint(bp, url_prefix="/vf")
    # The combined endpoint name stored in view_functions should include the whitespace.
    expected_endpoint = f"{name}.index"
    assert expected_endpoint in app.view_functions

def test_tab_name_with_url_for_and_request_context(app):
    name = "\t"
    bp = flask.Blueprint(name, __name__)

    @bp.route("/")
    def index():
        return ""

    app.register_blueprint(bp, url_prefix="/t")
    with app.test_request_context():
        assert flask.url_for(f"{name}.index") == "/t/"

def test_multiple_whitespace_variants_allowed(app):
    for name in (" ", "  ", "\t", "\n", " \t "):
        bp = flask.Blueprint(name, __name__)
        # ensure creation itself doesn't raise
        assert bp.name == name

def test_whitespace_name_can_be_nested_and_resolved(app, client):
    parent = flask.Blueprint("parent", __name__, url_prefix="/p")
    child_name = "  "
    child = flask.Blueprint(child_name, __name__)

    @child.route("/c")
    def child_index():
        return flask.request.endpoint

    parent.register_blueprint(child, url_prefix="/child")
    app.register_blueprint(parent)

    rv = client.get("/p/child/c")
    assert rv.status_code == 200
    # Nested registration should prefix parent name to child's endpoints.
    assert rv.data == f"parent.{child_name}.child_index".encode() or rv.data.endswith(b".child_index")

import flask
import pytest
import flask
import pytest

def test_space_name_creation():
    # Creating a blueprint with a single space name should succeed.
    bp = flask.Blueprint(" ", __name__)
    assert bp.name == " "

def test_single_space_route_access(app, client):
    bp = flask.Blueprint(" ", __name__)

    @bp.route("/space")
    def index():
        return "ok"

    app.register_blueprint(bp)
    rv = client.get("/space")
    assert rv.status_code == 200
    assert rv.data == b"ok"

def test_multiple_spaces_route_access(app, client):
    bp = flask.Blueprint("   ", __name__)

    @bp.route("/manyspaces")
    def index():
        return "many"

    app.register_blueprint(bp)
    rv = client.get("/manyspaces")
    assert rv.status_code == 200
    assert rv.data == b"many"

def test_tab_name_route_access(app, client):
    bp = flask.Blueprint("\t", __name__)

    @bp.route("/tab")
    def index():
        return "tab"

    app.register_blueprint(bp)
    rv = client.get("/tab")
    assert rv.status_code == 200
    assert rv.data == b"tab"

def test_newline_name_route_access(app, client):
    bp = flask.Blueprint("\n", __name__)

    @bp.route("/newline")
    def index():
        return "newline"

    app.register_blueprint(bp)
    rv = client.get("/newline")
    assert rv.status_code == 200
    assert rv.data == b"newline"

def test_whitespace_child_blueprint_registration(app, client):
    parent = flask.Blueprint("parent", __name__)
    child = flask.Blueprint("   ", __name__)

    @child.route("/child/")
    def child_index():
        return "child"

    parent.register_blueprint(child)
    app.register_blueprint(parent, url_prefix="/parent")
    rv = client.get("/parent/child/")
    assert rv.status_code == 200
    assert rv.data == b"child"

def test_duplicate_whitespace_name_conflict(app):
    # Two different blueprint objects with the same whitespace-only name
    # should conflict when registering on the same app.
    bp1 = flask.Blueprint("  ", __name__)
    bp2 = flask.Blueprint("  ", __name__)
    app.register_blueprint(bp1)
    with pytest.raises(ValueError):
        app.register_blueprint(bp2)

def test_same_blueprint_registered_with_different_name(app):
    # The same blueprint object can be registered multiple times with different names.
    bp = flask.Blueprint(" ", __name__)

    @bp.route("/dup")
    def index():
        return "dup"

    app.register_blueprint(bp)
    # registering the same bp with a different name should be allowed
    app.register_blueprint(bp, name="alt")
    # ensure both registrations created routes; first registration provides /dup
    # second registration used a different name but same routes, still accessible
    # via the same URL
    # (the client fixture is not required here; just ensure no exception was raised)

def test_app_template_filter_with_whitespace_name(app):
    bp = flask.Blueprint(" ", __name__)

    @bp.app_template_filter()
    def rev(s):
        return s[::-1]

    app.register_blueprint(bp)
    assert "rev" in app.jinja_env.filters
    assert app.jinja_env.filters["rev"]("abcd") == "dcba"

def test_url_defaults_with_whitespace_name(app, client):
    bp = flask.Blueprint("   ", __name__)

    @bp.route("/def", defaults={"v": 1})
    @bp.route("/def/<int:v>")
    def show(v):
        return str(v)

    app.register_blueprint(bp, url_prefix="", url_defaults={"v": 9})
    # The blueprint-level default (9) should be applied and then overridden by rule default 1
    rv1 = client.get("/def")
    assert rv1.data == b"1"
    rv2 = client.get("/def/5")
    assert rv2.data == b"5"

import pytest
import flask
import pytest
import flask

def test_whitespace_name_single_space_creation():
    bp = flask.Blueprint(" ", __name__)
    assert bp.name == " "

def test_whitespace_name_tab_creation():
    bp = flask.Blueprint("\t", __name__)
    assert bp.name == "\t"

def test_whitespace_name_newline_creation():
    bp = flask.Blueprint("\n", __name__)
    assert bp.name == "\n"

def test_whitespace_name_multiple_creation():
    s = "  \t "
    bp = flask.Blueprint(s, __name__)
    assert bp.name == s

def test_whitespace_name_registration_in_app(app):
    name = "  "
    bp = flask.Blueprint(name, __name__)
    app.register_blueprint(bp)
    assert name in app.blueprints
    assert app.blueprints[name] is bp

def test_whitespace_name_route_access(app, client):
    bp = flask.Blueprint(" ", __name__)

    @bp.route("/space")
    def sp():
        return "ok"

    app.register_blueprint(bp)
    rv = client.get("/space")
    assert rv.status_code == 200
    assert rv.data == b"ok"

def test_whitespace_name_nested_registration(app, client):
    parent = flask.Blueprint("parent", __name__)
    child = flask.Blueprint("  ", __name__)

    @child.route("/child")
    def ch():
        return "child"

    parent.register_blueprint(child)
    app.register_blueprint(parent, url_prefix="/p")
    rv = client.get("/p/child")
    assert rv.status_code == 200
    assert rv.data == b"child"

def test_none_name_raises_value_error_creation():
    with pytest.raises(ValueError):
        # type: ignore - passing None to test behaviour
        flask.Blueprint(None, __name__)  # type: ignore

def test_dotted_name_still_raises_value_error():
    with pytest.raises(ValueError):
        flask.Blueprint("a.b", __name__)

def test_empty_string_still_raises_value_error():
    with pytest.raises(ValueError):
        flask.Blueprint("", __name__)