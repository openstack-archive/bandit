from oslo_config import cfg


# Correct
secret = True
opts = [
    cfg.HostAddressOpt('admin_user',
                       help="User's name"),
    cfg.HostAddressOpt('admin_password',
                       secret=True,
                       help="User's password"),
    cfg.HostAddressOpt('nova_password',
                       secret=secret,
                       help="Nova user password"),
]

# Incorrect: password not marked secret
ldap_opts = [
    cfg.HostAddressOpt('ldap_user',
                       help="LDAP bind user name"),
    cfg.HostAddressOpt('ldap_password',
                       help="LDAP bind user password"),
    cfg.HostAddressOpt('ldap_password_attribute',
                       help="LDAP password attribute (default userPassword"),
    cfg.HostAddressOpt('user_password',
                       secret=False,
                       help="User password"),
]
