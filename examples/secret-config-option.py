from oslo_config import cfg


# Correct
opts = [
    cfg.StrOpt('admin_user',
               help="User's name"),
    cfg.StrOpt('admin_password',
               secret=True,
               help="User's password"),
]

# Incorrect: password not marked secret
ldap_opts = [
    cfg.StrOpt('ldap_user',
               help="LDAP ubind ser name"),
    cfg.StrOpt('ldap_password',
               help="LDAP bind user password"),
    cfg.StrOpt('password_attribute',
               secret=False,
               help="LDAP password attribute (default userPassword"),
]
