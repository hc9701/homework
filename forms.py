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
    is_admin = SelectField(
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
            Length(6, 20, '用户名长度应在6-20位之间'),
        ],
        render_kw={
            "placeholder": "用户名",
        }
    )
    password = PasswordField(
        validators=[
            Length(6, 20, '密码长度应在6-20位之间'),
        ],
        render_kw={
            "placeholder": "密码",
        }
    )
    email = EmailField(
        validators=[
            Email('请输入合法邮箱'),
        ],
        render_kw={
            "placeholder": "邮箱",
        }
    )
    confirm = PasswordField(
        validators=[
            EqualTo('password', message='两次密码不一致')
        ],
        render_kw={
            "placeholder": "密码确认"
        }
    )
    submit = SubmitField('立即注册')


class UserCenterForm(FlaskForm):
    username = StringField(
        label='用户名',
        validators=[
            Length(6, 20, '用户名长度应在6-20位之间'),
        ],
        render_kw={
            "placeholder": "用户名",
            'readonly': True,
        }
    )
    new_password = PasswordField(
        label='新的密码',
        validators=[
            Length(6, 20, '密码长度应在6-20位之间'),
        ],
        render_kw={
            "placeholder": "密码",
        }
    )
    confirm = PasswordField(
        label='密码确认',
        validators=[
            EqualTo('new_password', message='两次密码不一致')
        ],
        render_kw={
            "placeholder": "密码确认"
        }
    )
    email = EmailField(
        label='邮箱',
        validators=[
            Email('请输入合法邮箱'),
        ],
        render_kw={
            "placeholder": "邮箱",
        }
    )
    app1 = StringField(label='你想要关注的APP1')
    app2 = StringField(label='你想要关注的APP2')
    word1 = StringField(label='你想要关注的分词1')
    word2 = StringField(label='你想要关注的分词2')

