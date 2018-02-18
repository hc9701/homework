from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, AnyOf, Length, EqualTo, Email


class LoginForm(FlaskForm):
    username = StringField(
        validators=[
            DataRequired("用户名不能为空"),
        ],
    )
    password = PasswordField(
        validators=[
            DataRequired("密码不能为空")
        ],
    )
    identity = SelectField(
        '', choices=[(0, '普通用户'), (1, '管理员')],
        validators=[
            AnyOf([0, 1], '请以合法身份登录')
        ],
        render_kw={
            'data-select-like-alignement': 'never'
        },
        coerce=int,
    )
    submit = SubmitField('')


class RegisterForm(FlaskForm):
    username = StringField(
        validators=[
            Length(6,20,'用户名长度应在6-20位之间'),
        ]
    )
    password = PasswordField(
        validators=[
            Length(6,20,'密码长度应在6-20位之间'),
        ]
    )
    email=EmailField(
        validators=[
            Email('请输入合法邮箱')
        ]
    )
    confirm = PasswordField(
        validators=[
            EqualTo(password,'两次密码不一致')
        ]
    )
