import re, os

def test_nginx_conf_contains_user_routing():
    # Adjust path relative to project root
    conf_path = os.path.join(os.path.dirname(__file__), "../../terminal/nginx.conf")
    conf_path = os.path.abspath(conf_path)

    with open(conf_path) as f:
        conf = f.read()

    # Ensure regex-based server_name is present
    assert re.search(r"server_name ~\^\(\?<user>\.\+\)\\.dropcode\\.org\$;", conf)

    # Ensure proxy_pass points to workspace containers
    assert "proxy_pass http://workspace_$user:8080/;" in conf