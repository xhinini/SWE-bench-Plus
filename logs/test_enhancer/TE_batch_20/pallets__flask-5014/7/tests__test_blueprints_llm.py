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

# no additional imports beyond standard pytest and flask used in test_code
import pytest
import flask

def test_whitespace_name_creation_allowed():
    bp = flask.Blueprint("   ", __name__)
    assert isinstance(bp, flask.Blueprint)
    assert bp.name == "   "

def test_whitespace_name_register_and_access_endpoint(app, client):
    bp = flask.Blueprint("   ", __name__, url_prefix="/py")

    @bp.route("/x")
    def x():
        return flask.request.endpoint

    app.register_blueprint(bp)
    rv = client.get("/py/x")
    assert rv.status_code == 200
    # endpoint should include the whitespace name followed by dot and function name
    assert rv.data == b"   .x"

def test_whitespace_name_url_for_generates_prefixed_url(app):
    bp = flask.Blueprint("   ", __name__, url_prefix="/py")

    @bp.route("/bar")
    def bar():
        return ""

    app.register_blueprint(bp)
    with app.test_request_context():
        # url_for with the blueprint's dotted endpoint (leading whitespace name)
        assert flask.url_for("   .bar") == "/py/bar"

def test_whitespace_name_app_template_filter_applies(app, client):
    bp = flask.Blueprint("   ", __name__)

    @bp.app_template_filter()
    def super_reverse(s):
        return s[::-1]

    app.register_blueprint(bp)

    @app.route("/")
    def index():
        return flask.render_template_string("{{ 'abcd' | super_reverse }}")

    rv = client.get("/")
    assert rv.data == b"dcba"

def test_whitespace_name_nested_blueprint(app, client):
    parent = flask.Blueprint("parent", __name__, url_prefix="/parent")
    child = flask.Blueprint("   ", __name__, url_prefix="/child")

    @child.route("/")
    def child_index():
        return "child"

    parent.register_blueprint(child)
    app.register_blueprint(parent)

    rv = client.get("/parent/child/")
    assert rv.status_code == 200
    assert rv.data == b"child"

def test_whitespace_name_registration_name_override(app):
    bp = flask.Blueprint("   ", __name__)
    app.register_blueprint(bp, name="alt")
    # When registered with name="alt", the app.blueprints key should be "alt"
    assert "alt" in app.blueprints
    assert app.blueprints["alt"] is bp

def test_whitespace_name_unique_blueprint_names_with_spaces(app):
    bp1 = flask.Blueprint("   ", __name__)
    bp2 = flask.Blueprint("   ", __name__)
    app.register_blueprint(bp1)
    # registering a different blueprint with the same name should raise
    with pytest.raises(ValueError):
        app.register_blueprint(bp2)

def test_whitespace_name_url_defaults(app, client):
    bp = flask.Blueprint("   ", __name__)

    @bp.route("/", defaults={"page": 1})
    @bp.route("/page/<int:page>")
    def something(page):
        return str(page)

    app.register_blueprint(bp, url_prefix="/p")
    assert client.get("/p/").data == b"1"
    assert client.get("/p/page/2").data == b"2"

def test_whitespace_name_app_errorhandler_registered(app, client):
    bp = flask.Blueprint("   ", __name__)

    @bp.app_errorhandler(403)
    def handle_403(e):
        return "handled", 403

    @app.route("/forbidden")
    def forbidden():
        flask.abort(403)

    app.register_blueprint(bp)
    rv = client.get("/forbidden")
    assert rv.status_code == 403
    assert rv.data == b"handled"

def test_whitespace_name_key_in_app_blueprints(app):
    bp = flask.Blueprint("   ", __name__)
    app.register_blueprint(bp)
    # The blueprint should be registered under its own (whitespace) name by default
    assert "   " in app.blueprints
    assert app.blueprints["   "] is bp

# no additional imports required
import flask

def _make_bp_and_register(app, client, name_value):
    bp = flask.Blueprint(name_value, __name__)

    @bp.route("/")
    def index():
        return "ok"

    # registering should succeed
    app.register_blueprint(bp)
    # blueprint key should be the exact name value
    assert name_value in app.blueprints

    rv = client.get("/")
    assert rv.status_code == 200
    assert rv.data == b"ok"

def test_whitespace_name_single_space(app, client):
    _make_bp_and_register(app, client, " ")

def test_whitespace_name_three_spaces(app, client):
    _make_bp_and_register(app, client, "   ")

def test_whitespace_name_tab(app, client):
    _make_bp_and_register(app, client, "\t")

def test_whitespace_name_newline(app, client):
    _make_bp_and_register(app, client, "\n")

def test_whitespace_name_space_and_tab(app, client):
    _make_bp_and_register(app, client, " \t ")

def test_whitespace_name_carriage_return(app, client):
    _make_bp_and_register(app, client, "\r")

def test_whitespace_name_vertical_tab(app, client):
    _make_bp_and_register(app, client, "\v")

def test_whitespace_name_form_feed(app, client):
    _make_bp_and_register(app, client, "\f")

def test_whitespace_name_mixed_whitespace(app, client):
    _make_bp_and_register(app, client, "  \n\t  ")

def test_whitespace_name_four_spaces(app, client):
    _make_bp_and_register(app, client, "    ")