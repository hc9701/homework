from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.fields import StringField, PasswordField, SubmitField, SelectField, FileField
from wtforms.fields.html5 import EmailField, URLField
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


class AddUserForm(FlaskForm):
    username = StringField(
        label='用户名',
        validators=[
            Length(6, 20, '用户名长度应在6-20位之间'),
        ],
        render_kw={
            "placeholder": "用户名",
        }
    )
    password = PasswordField(
        label='密码',
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
            EqualTo('password', message='两次密码不一致')
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
    is_admin = SelectField(
        label='身份',
        choices=[(0, '普通用户'), (1, '管理员')],
        validators=[
            AnyOf([0, 1], '身份不合法')
        ],
        coerce=int,
    )
    submit = SubmitField('添加用户')


class LoadNetDataForm(FlaskForm):
    url = URLField(
        label='URL',
        render_kw={
            "size": "50"
        }
    )
    submit = SubmitField('导入')

class ModifyDataForm(FlaskForm):
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
    submit = SubmitField('修改资料')

class ModifyUserForm(FlaskForm):
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
    submit = SubmitField('修改资料')
    is_admin = SelectField(
        '', choices=[(0, '普通用户'), (1, '管理员')],
        validators=[
            AnyOf([0, 1], '请选择合法身份')
        ],
        coerce=int,
    )

class UploadForm(FlaskForm):
    excel = FileField(validators=[
        FileAllowed(['xls,xlsx'], u'只能上传excel！'),
        FileRequired(u'文件未选择！')])
    submit = SubmitField(u'上传')