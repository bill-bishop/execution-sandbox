from . import auth, execute, execute_worker, read_file, read_partial, workspace, ws, write_file
from . import auth_github, healthcheck, canvas, waitlist

all_blueprints = [
    auth.bp,
    execute.bp,
    execute_worker.bp,
    read_file.bp,
    read_partial.bp,
    workspace.bp,
    write_file.bp,
    auth_github.bp,
    healthcheck.bp,
    canvas.bp,
    waitlist.bp,
]