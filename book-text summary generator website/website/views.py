from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Summary
from . import db
import json

import os
import openai

os.environ['OPENAI_API_KEY'] = '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'
openai.api_key = os.getenv("OPENAI_API_KEY")

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        bookTitle = request.form.get('bookTitle')
        content = 'Write a 300 word summary on the book ' + bookTitle
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": content}
            ]
        )
        new_summary = Summary(data=completion.choices[0].message.content, user_id=current_user.id)
        db.session.add(new_summary)
        db.session.commit()
        flash('Summary Generated!', category='success')
    return render_template('home.html', user=current_user)

@views.route('/delete-summary', methods=['POST'])
def delete_summary():
    summary = json.loads(request.data)
    summaryId = summary['summaryId']
    summary = Summary.query.get(summaryId)
    if summary:
        if summary.user_id == current_user.id:
            db.session.delete(summary)
            db.session.commit()

    return jsonify({})