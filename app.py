from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import EditProfileForm, AddUserForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


@app.route('/edit_profile/<int:user_id>', methods=['GET', 'POST'])
def edit_profile(user_id):
    user = User.query.get_or_404(user_id)
    form = EditProfileForm(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data  # В реальном приложении пароли должны быть захэшированы
        db.session.commit()
        flash('Профиль успешно обновлён!', 'success')
        return redirect(url_for('edit_profile', user_id=user.id))

    return render_template('edit_profile.html', form=form)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    form = AddUserForm()

    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data  # В реальном приложении пароли должны быть захэшированы
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Пользователь успешно добавлен!', 'success')
        return redirect(url_for('add_user'))  # Перенаправление на ту же страницу после добавления

    return render_template('add_user.html', form=form)

if __name__ == '__main__':
    with app.app_context():  # Создаем контекст приложения
        db.create_all()  # Создание базы данных и таблиц
    app.run(debug=True)