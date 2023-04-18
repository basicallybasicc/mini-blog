#!/usr/bin/env python3

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request as req,
    url_for
)
from werkzeug.exceptions import abort
from flaskr.templates.__blueprints.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index ():
    db = get_db()
    posts = db.execute(
        """ 
            select
                a.*,
                b.username
            from
                posts as a
                join users as b
                on a.user_id = b.id
            order by
                a.create_ts desc
        """
    ).fetchall()

    return render_template("blog/index.html", posts = posts)

@bp.route('/create', methods = ['GET', 'POST'])
@login_required
def create ():
    if req.method == 'POST':
        title = req.form['title']
        body = req.form['body']
        error = None

        if not title:
            error = "Title is required"
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "insert into posts (title, body, user_id) values (?, ?, ?)",
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
    
    return render_template('blog/create.html')

def get_post(id, check_author = True):
    post = get_db().execute(
        """
        select
            a.*,
            b.username
        from
            posts as a
            join users as b
            on a.user_id = b.id
        where
            a.id = ?
        """,
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} does not exist")
    
    if check_author and post['user_id'] !=  g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods = ('GET', 'POST'))
@login_required
def update (id):
    post = get_post(id)

    if req.method == 'POST':
        title = req.form['title']
        body = req.form['body']
        error = None

        if not title:
            error = "Title is required"
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "update posts set title = ?, body = ? where id = ?",
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    
    return render_template('blog/update.html', post = post)

@bp.route('/<int:id>/delete', methods = ['POST'])
@login_required
def delete (id):
    get_post(id)
    get_db().execute("delete from posts where id = ?",(id,))
    get_db().commit()
    return redirect(url_for('blog.index'))

        