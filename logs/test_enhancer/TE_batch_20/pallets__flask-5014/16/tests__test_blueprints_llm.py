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

# no new imports required beyond pytest and flask already used in test suite
import pytest
import flask

def _make_bp_and_register(app, name, url_prefix):
    bp = flask.Blueprint(name, __name__)

    @bp.route("/")
    def index():
        return "ok"

    app.register_blueprint(bp, url_prefix=url_prefix)
    return bp

def test_whitespace_name_single_space(app, client):
    bp = _make_bp_and_register(app, " ", "/ws1")
    rv = client.get("/ws1/")
    assert rv.status_code == 200
    assert rv.data == b"ok"

def test_whitespace_name_tab(app, client):
    bp = _make_bp_and_register(app, "\t", "/ws2")
    rv = client.get("/ws2/")
    assert rv.status_code == 200
    assert rv.data == b"ok"

def test_whitespace_name_newline(app, client):
    bp = _make_bp_and_register(app, "\n", "/ws3")
    rv = client.get("/ws3/")
    assert rv.status_code == 200
    assert rv.data == b"ok"

def test_whitespace_name_multiple_spaces(app, client):
    bp = _make_bp_and_register(app, "   ", "/ws4")
    rv = client.get("/ws4/")
    assert rv.status_code == 200
    assert rv.data == b"ok"

def test_registration_adds_blueprint_key(app):
    bp = flask.Blueprint(" ", __name__)
    app.register_blueprint(bp, url_prefix="/ws5")
    # The app.blueprints mapping should contain the exact name string (a single space).
    assert " " in app.blueprints
    assert app.blueprints[" "] is bp

def test_duplicate_whitespace_names_raise(app):
    bp1 = flask.Blueprint(" ", __name__)
    bp2 = flask.Blueprint(" ", __name__)
    app.register_blueprint(bp1, url_prefix="/ws6")
    # Registering a different blueprint with the same name should raise.
    with pytest.raises(ValueError):
        app.register_blueprint(bp2)

def test_override_name_allows_multiple(app):
    bp = flask.Blueprint(" ", __name__)
    app.register_blueprint(bp, url_prefix="/ws7")
    # Registering the same blueprint with a different name should be allowed.
    app.register_blueprint(bp, name="unique_ws7", url_prefix="/ws7_alt")
    assert "unique_ws7" in app.blueprints

def test_nested_blueprint_with_whitespace_name(app, client):
    parent = flask.Blueprint("parent", __name__)
    child = flask.Blueprint(" ", __name__)

    @child.route("/")
    def child_index():
        return "child"

    parent.register_blueprint(child, url_prefix="/child")
    app.register_blueprint(parent, url_prefix="/parent")

    rv = client.get("/parent/child/")
    assert rv.status_code == 200
    assert rv.data == b"child"

def test_app_errorhandler_registered_via_whitespace_named_blueprint(app, client):
    bp = flask.Blueprint(" ", __name__)

    @bp.app_errorhandler(403)
    def forbidden(e):
        return "handled", 403

    @app.route("/forbidden")
    def do_forbidden():
        flask.abort(403)

    app.register_blueprint(bp)
    rv = client.get("/forbidden")
    assert rv.status_code == 403
    assert rv.data == b"handled"

def test_add_app_template_filter_from_whitespace_named_blueprint(app):
    bp = flask.Blueprint("\t", __name__)

    @bp.app_template_filter("rev")
    def my_reverse(s):
        return s[::-1]

    app.register_blueprint(bp)

    # Ensure the filter is registered on the application's jinja environment
    assert "rev" in app.jinja_env.filters
    assert app.jinja_env.filters["rev"]("abcd") == "dcba"
    # Also verify that rendering with the filter works in an app context
    with app.test_request_context():
        rendered = flask.render_template_string("{{ 'abcd'|rev }}")
        assert rendered == "dcba"

import pytest
import flask

@pytest.mark.parametrize(
    "bp_name",
    [
        " ",        # single space
        "  ",       # multiple spaces
        "\t",       # tab
        "\n",       # newline
        "\r",       # carriage return
        "\t\n",     # tab + newline
        " \t ",     # mixed spaces and tab
        "\r\n",     # CRLF
        "\x0b",     # vertical tab
        "\x0c",     # form feed
    ],
)
def test_whitespace_only_blueprint_names_allowed(app, client, bp_name):
    # Construct a blueprint with a whitespace-only name and ensure it
    # can be registered and serves a route at "/".
    bp = flask.Blueprint(bp_name, __name__)

    @bp.route("/")
    def index():
        return "ok"

    # Should not raise with the gold patch.
    app.register_blueprint(bp)

    # The blueprint name should be present in the app's blueprints mapping.
    assert bp_name in app.blueprints

    # The registered route should be reachable.
    rv = client.get("/")
    assert rv.data == b"ok"

import flask
import flask

def _make_bp_and_get_endpoint(app, client, name, path):
    bp = flask.Blueprint(name, __name__)
    @bp.route(path)
    def view():
        return flask.request.endpoint
    app.register_blueprint(bp)
    rv = client.get(path)
    return bp, rv

def test_whitespace_single_space_allowed(app, client):
    name = " "
    bp, rv = _make_bp_and_get_endpoint(app, client, name, "/ws1")
    assert bp.name == name
    assert rv.data == (f"{name}.view").encode()

def test_whitespace_multiple_spaces_allowed(app, client):
    name = "   "
    bp, rv = _make_bp_and_get_endpoint(app, client, name, "/ws2")
    assert bp.name == name
    assert rv.data == (f"{name}.view").encode()

def test_whitespace_tab_allowed(app, client):
    name = "\t"
    bp, rv = _make_bp_and_get_endpoint(app, client, name, "/wt")
    assert bp.name == name
    assert rv.data == (f"{name}.view").encode()

def test_whitespace_newline_allowed(app, client):
    name = "\n"
    bp, rv = _make_bp_and_get_endpoint(app, client, name, "/wn")
    assert bp.name == name
    assert rv.data == (f"{name}.view").encode()

def test_whitespace_carriage_return_allowed(app, client):
    name = "\r"
    bp, rv = _make_bp_and_get_endpoint(app, client, name, "/wr")
    assert bp.name == name
    assert rv.data == (f"{name}.view").encode()

def test_whitespace_mixed_space_tab_allowed(app, client):
    name = " \t "
    bp, rv = _make_bp_and_get_endpoint(app, client, name, "/wst")
    assert bp.name == name
    assert rv.data == (f"{name}.view").encode()

def test_whitespace_multiple_newlines_allowed(app, client):
    name = "\n\n"
    bp, rv = _make_bp_and_get_endpoint(app, client, name, "/wnn")
    assert bp.name == name
    assert rv.data == (f"{name}.view").encode()

def test_whitespace_leading_trailing_spaces_allowed(app, client):
    name = "  leading_trailing  "
    bp, rv = _make_bp_and_get_endpoint(app, client, name, "/wlt")
    assert bp.name == name
    assert rv.data == (f"{name}.view").encode()

def test_whitespace_carriage_return_newline_allowed(app, client):
    name = "\r\n"
    bp, rv = _make_bp_and_get_endpoint(app, client, name, "/wcrlf")
    assert bp.name == name
    assert rv.data == (f"{name}.view").encode()

def test_whitespace_nested_blueprint_with_space_name(app, client):
    parent = flask.Blueprint("parent", __name__)
    child_name = " "
    child = flask.Blueprint(child_name, __name__)
    @child.route("/child/")
    def child_index():
        return flask.request.endpoint
    parent.register_blueprint(child, url_prefix="/child")
    app.register_blueprint(parent, url_prefix="/parent")
    rv = client.get("/parent/child/child/")
    # endpoint for child_index should include the child blueprint name
    assert rv.status_code == 200
    assert rv.data == (f"{child_name}.child_index").encode()

import flask
import pytest
import flask
import pytest


def _make_bp_with_name(name):
    bp = flask.Blueprint(name, __name__)

    @bp.route("/x")
    def index():
        # return the endpoint so tests can assert its value includes the
        # original blueprint name (which may be whitespace).
        return flask.request.endpoint

    return bp


def test_space_name_route_accessible(app, client):
    name = " "
    bp = _make_bp_with_name(name)
    app.register_blueprint(bp)
    rv = client.get("/x")
    assert rv.data == f"{name}.index".encode()


def test_multi_space_name_route_accessible(app, client):
    name = "   "
    bp = _make_bp_with_name(name)
    app.register_blueprint(bp)
    rv = client.get("/x")
    assert rv.data == f"{name}.index".encode()


def test_tab_name_route_accessible(app, client):
    name = "\t"
    bp = _make_bp_with_name(name)
    app.register_blueprint(bp)
    rv = client.get("/x")
    assert rv.data == f"{name}.index".encode()


def test_newline_name_route_accessible(app, client):
    name = "\n"
    bp = _make_bp_with_name(name)
    app.register_blueprint(bp)
    rv = client.get("/x")
    assert rv.data == f"{name}.index".encode()


def test_mixed_whitespace_name_route_accessible(app, client):
    name = " \t\n "
    bp = _make_bp_with_name(name)
    app.register_blueprint(bp)
    rv = client.get("/x")
    assert rv.data == f"{name}.index".encode()


def test_whitespace_name_appears_in_app_blueprints(app):
    name = "  "
    bp = flask.Blueprint(name, __name__)
    app.register_blueprint(bp)
    # app.blueprints should have the whitespace-only name as a key
    assert name in app.blueprints
    assert app.blueprints[name] is bp


def test_whitespace_name_request_endpoint_matches_expected(app, client):
    name = " "
    bp = _make_bp_with_name(name)
    app.register_blueprint(bp, url_prefix="/py")

    @app.route("/")
    def root():
        # ensure the app-level route still works
        return "root"

    rv = client.get("/py/x")
    assert rv.data == f"{name}.index".encode()


def test_whitespace_name_register_blueprint_with_url_prefix_access(app, client):
    name = "\t"
    bp = _make_bp_with_name(name)
    app.register_blueprint(bp, url_prefix="/pref")
    rv = client.get("/pref/x")
    assert rv.data == f"{name}.index".encode()


def test_whitespace_name_nested_blueprint_registration(app, client):
    parent_name = " "
    parent = flask.Blueprint(parent_name, __name__)
    child = flask.Blueprint("child", __name__)

    @child.route("/c/")
    def child_index():
        return "child"

    parent.register_blueprint(child, url_prefix="/c")
    app.register_blueprint(parent, url_prefix="/p")

    rv = client.get("/p/c/")
    assert rv.status_code == 200
    assert rv.data == b"child"


def test_name_with_surrounding_whitespace_allowed(app, client):
    # Control: non-empty after strip should be allowed (both candidate and gold)
    name = " a "
    bp = _make_bp_with_name(name)
    app.register_blueprint(bp)
    rv = client.get("/x")
    assert rv.data == f"{name}.index".encode()

import pytest
import flask
import pytest
import flask

def test_none_name_raises_value_error():
    # Passing None should raise ValueError (blueprint name may not be empty).
    with pytest.raises(ValueError):
        flask.Blueprint(None, __name__)  # type: ignore

def test_space_only_name_is_allowed_and_registers(app, client):
    name = "   "
    bp = flask.Blueprint(name, __name__)

    @bp.route("/hello")
    def hello():
        # Return the endpoint to assert the blueprint name is used in the endpoint.
        return flask.request.endpoint

    # Register the blueprint under a prefix so we can call it.
    app.register_blueprint(bp, url_prefix="/ws")
    # The blueprint should be present in app.blueprints with the exact name (including spaces).
    assert name in app.blueprints

    rv = client.get("/ws/hello")
    assert rv.status_code == 200
    # The endpoint should include the whitespace name as the blueprint prefix.
    assert rv.data == f"{name}.hello".encode("utf-8")

def test_tab_only_name_is_allowed_and_url_for(app):
    name = "\t"
    bp = flask.Blueprint(name, __name__)

    @bp.route("/t")
    def t():
        return "ok"

    app.register_blueprint(bp, url_prefix="/tprefix")

    with app.test_request_context():
        # url_for should accept the blueprint name with a tab character.
        url = flask.url_for(f"{name}.t")
        assert url == "/tprefix/t"

def test_newline_only_name_is_allowed_and_endpoint(app, client):
    name = "\n"
    bp = flask.Blueprint(name, __name__)

    @bp.route("/nl")
    def nl():
        return flask.request.endpoint

    app.register_blueprint(bp, url_prefix="/nlprefix")
    rv = client.get("/nlprefix/nl")
    assert rv.status_code == 200
    assert rv.data == f"{name}.nl".encode("utf-8")

def test_mixed_whitespace_only_name_is_allowed(app, client):
    name = " \t\n "
    bp = flask.Blueprint(name, __name__)

    @bp.route("/mix")
    def mix():
        return flask.request.endpoint

    app.register_blueprint(bp, url_prefix="/mixprefix")
    rv = client.get("/mixprefix/mix")
    assert rv.status_code == 200
    assert rv.data == f"{name}.mix".encode("utf-8")

def test_whitespace_name_works_with_template_url_for(app):
    name = "   "
    bp = flask.Blueprint(name, __name__)

    @bp.route("/tpl")
    def tpl():
        return "ok"

    app.register_blueprint(bp, url_prefix="/tplprefix")

    with app.test_request_context():
        # url_for with the exact blueprint name that contains spaces should resolve.
        assert flask.url_for(f"{name}.tpl") == "/tplprefix/tpl"

def test_whitespace_blueprint_registered_key_and_lookup(app):
    name = "   "
    bp = flask.Blueprint(name, __name__)
    app.register_blueprint(bp)
    # The blueprint key should be exactly the name (spaces preserved).
    assert name in app.blueprints
    assert app.blueprints[name] is bp

def test_whitespace_name_in_nested_blueprint_registration(app, client):
    parent = flask.Blueprint("parent", __name__)
    child_name = "   "
    child = flask.Blueprint(child_name, __name__)

    @child.route("/")
    def index():
        return flask.request.endpoint

    parent.register_blueprint(child, url_prefix="/child")
    app.register_blueprint(parent, url_prefix="/parent")

    rv = client.get("/parent/child/")
    assert rv.status_code == 200
    # Endpoint should include parent prefix and the whitespace child name.
    assert rv.data == f"parent.{child_name}.index".encode("utf-8")

def test_whitespace_name_url_for_after_registration(app):
    name = " \t "
    bp = flask.Blueprint(name, __name__)

    @bp.route("/a")
    def a():
        return "a"

    app.register_blueprint(bp, url_prefix="/aprefix")

    with app.test_request_context():
        # url_for should work with whitespace-only blueprint names.
        assert flask.url_for(f"{name}.a") == "/aprefix/a"

import pytest
import flask
import pytest
import flask

def test_single_space_name_allowed_creation_and_register(app, client):
    bp = flask.Blueprint(" ", __name__)
    
    @bp.route("/space")
    def space():
        return "space"
    
    app.register_blueprint(bp)
    rv = client.get("/space")
    assert rv.status_code == 200
    assert rv.data == b"space"

def test_multiple_spaces_name_allowed(app, client):
    bp = flask.Blueprint("   ", __name__)
    
    @bp.route("/many")
    def many():
        return "many"
    
    app.register_blueprint(bp)
    rv = client.get("/many")
    assert rv.status_code == 200
    assert rv.data == b"many"

def test_tab_name_allowed(app, client):
    bp = flask.Blueprint("\t", __name__)
    
    @bp.route("/tab")
    def tab():
        return "tab"
    
    app.register_blueprint(bp)
    rv = client.get("/tab")
    assert rv.status_code == 200
    assert rv.data == b"tab"

def test_newline_name_allowed(app, client):
    bp = flask.Blueprint("\n", __name__)
    
    @bp.route("/nl")
    def nl():
        return "nl"
    
    app.register_blueprint(bp)
    rv = client.get("/nl")
    assert rv.status_code == 200
    assert rv.data == b"nl"

def test_mixed_whitespace_name_allowed(app, client):
    name = " \t \n "
    bp = flask.Blueprint(name, __name__)
    
    @bp.route("/mix")
    def mix():
        return "mix"
    
    app.register_blueprint(bp)
    rv = client.get("/mix")
    assert rv.status_code == 200
    assert rv.data == b"mix"

def test_whitespace_name_preserved_in_app_blueprints_key(app):
    name = "   "
    bp = flask.Blueprint(name, __name__)
    app.register_blueprint(bp)
    # blueprint name should be stored as provided (including whitespace)
    assert name in app.blueprints
    assert app.blueprints[name] is bp

def test_whitespace_blueprint_unique_registration(app):
    name = "  "
    bp = flask.Blueprint(name, __name__)
    app.register_blueprint(bp)
    # registering the same blueprint with the same name should raise
    with pytest.raises(ValueError):
        app.register_blueprint(bp)

def test_none_name_raises_typeerror():
    # Passing None as the name should raise a TypeError when checking membership
    # (the implementation attempts to do '.' in name which errors for None).
    with pytest.raises(TypeError):
        flask.Blueprint(None, __name__)  # type: ignore

def test_dotted_name_still_disallowed():
    with pytest.raises(ValueError):
        flask.Blueprint("a.b", __name__)

def test_whitespace_named_blueprint_routes_work_after_app_routes(app, client):
    # Ensure whitespace blueprint works even if app routes are defined before
    bp = flask.Blueprint("  ", __name__)
    
    @bp.route("/after")
    def after():
        return "after"
    
    @app.route("/pre")
    def pre():
        return "pre"
    
    app.register_blueprint(bp)
    assert client.get("/pre").data == b"pre"
    assert client.get("/after").data == b"after"

# No additional imports beyond pytest and flask are required.
import pytest
import flask

# 1. None as name should raise ValueError with message about empty name.
def test_none_name_raises_value_error():
    with pytest.raises(ValueError) as exc:
        # type: ignore is used because the statically-typed signature expects str
        flask.Blueprint(None, __name__)  # type: ignore
    assert "may not be empty" in str(exc.value)

# 2. Empty string still not allowed.
def test_empty_string_raises_value_error():
    with pytest.raises(ValueError):
        flask.Blueprint("", __name__)

# 3. Whitespace-only name should be allowed to instantiate.
def test_whitespace_name_instantiation_allowed():
    bp = flask.Blueprint("   ", __name__)
    assert bp.name == "   "

# 4. Whitespace-only blueprint registers and route is accessible.
def test_whitespace_name_registers_route_and_accessible(app, client):
    bp = flask.Blueprint("   ", __name__, url_prefix="/p")

    @bp.route("/x")
    def x():
        return "ok"

    app.register_blueprint(bp)
    rv = client.get("/p/x")
    assert rv.status_code == 200
    assert rv.data == b"ok"

# 5. The endpoint name preserves the whitespace in the blueprint name.
def test_whitespace_name_endpoint_name_preserved(app, client):
    bp = flask.Blueprint("   ", __name__, url_prefix="/p")

    @bp.route("/ep")
    def ep():
        return flask.request.endpoint

    app.register_blueprint(bp)
    rv = client.get("/p/ep")
    # endpoint should be "<blueprint_name>.<viewname>" preserving spaces
    assert rv.data == b"   .ep"

# 6. Nested blueprint with whitespace-only child name registers and is reachable.
def test_nested_whitespace_child_blueprint_registration(app, client):
    parent = flask.Blueprint("parent", __name__, url_prefix="/parent")
    child = flask.Blueprint("   ", __name__, url_prefix="/child")

    @child.route("/c")
    def child_index():
        return "child-ok"

    parent.register_blueprint(child)
    app.register_blueprint(parent)

    rv = client.get("/parent/child/c")
    assert rv.status_code == 200
    assert rv.data == b"child-ok"

# 7. Registering the same whitespace-named blueprint twice without changing 'name'
#    should raise ValueError for duplicate registration (same behavior as normal names).
def test_whitespace_name_duplicate_registration_raises(app):
    bp = flask.Blueprint("   ", __name__)
    app.register_blueprint(bp)
    with pytest.raises(ValueError):
        # registering the same blueprint again without providing a different 'name'
        app.register_blueprint(bp)

# 8. Blueprint with whitespace name can be registered multiple times with different 'name' option.
def test_whitespace_name_register_multiple_with_different_name_options(app, client):
    bp = flask.Blueprint("   ", __name__, url_prefix="/a")

    @bp.route("/")
    def index():
        return flask.request.endpoint

    app.register_blueprint(bp, url_prefix="/a")
    app.register_blueprint(bp, url_prefix="/b", name="alt")

    rv1 = client.get("/a/")
    rv2 = client.get("/b/")

    assert rv1.status_code == 200
    assert rv2.status_code == 200
    # first registration endpoint uses original blueprint name (with spaces)
    assert rv1.data == b"   .index"
    # second registration uses provided 'name' option
    assert rv2.data == b"alt.index"

# 9. Whitespace-only blueprint works with url_for generation (returns path for endpoint).
def test_whitespace_name_url_for_generation(app, client):
    bp = flask.Blueprint("   ", __name__, url_prefix="/p")

    @bp.route("/")
    def index():
        # url_for for the same blueprint endpoint should produce the blueprint-prefixed URL
        return flask.url_for(".index")

    app.register_blueprint(bp)
    rv = client.get("/p/")
    assert rv.status_code == 200
    assert rv.data == b"/p/"

# 10. Template filters registered via whitespace-named blueprint are applied to the app.
def test_whitespace_name_template_filter_registration(app):
    bp = flask.Blueprint("   ", __name__)

    @bp.app_template_filter()
    def my_upper(s):
        return s.upper()

    # Should not raise when registering and the filter must be present afterwards.
    app.register_blueprint(bp)
    assert "my_upper" in app.jinja_env.filters
    assert app.jinja_env.filters["my_upper"]("a") == "A"