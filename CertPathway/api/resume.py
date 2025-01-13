"""REST API for resume submission."""
import flask
import CertPathway
import pathlib
import uuid

@CertPathway.app.route('/api/v1/resume/', methods=['POST'])
def post_resume():
    """Save submitted resume"""
    data = flask.request.get_json()
    print(data)

    file = flask.request.files["file"]

    if file.filename:
        uuid_basename = gen_uuid_filename(file.filename)
        path = CertPathway.app.config["UPLOAD_FOLDER"]/uuid_basename
        file.save(path)

        # TODO: update database
        # TODO: how are we tracking email?
        # email = mlanting@umich.edu
        """ connection = CertPathway.model.get_db()
        connection.execute("PRAGMA foreign_keys = ON;")
        connection.execute(
            
            INSERT INTO
                resumes(filename, username)
                VALUES (?, ?)
            ,
            (uuid_basename, email)
        ) """
    else:
        flask.abort(400)

    return flask.jsonify(success=True), 200

def gen_uuid_filename(old_filename):
    """Generate a UUID filename given a plaintext filename."""
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(old_filename).suffix.lower()
    uuid_basename = f"{stem}{suffix}"

    return uuid_basename