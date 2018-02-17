from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, AnyOf


class LoginForm(FlaskForm):
    username = StringField(
        validators=[
            DataRequired(message="用户名不能为空"),
        ],
    )
    password = PasswordField(
        validators=[
            DataRequired(message="密码不能为空")
        ],
    )
    identity = SelectField(
        '', choices=[(0, '普通用户'), (1, '管理员')],
        validators=[
            AnyOf([0, 1], message='请以合法身份登录')
        ],
        render_kw={
            'data-select-like-alignement': 'never'
        },
        coerce=int,
    )
    submit = SubmitField('')
