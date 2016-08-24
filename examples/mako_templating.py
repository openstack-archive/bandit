from mako import template
import mako

from mako import template

template.Template("hello")

# XXX(fletcher): for some reason, bandit is missing the one below. keeping it
# in for now so that if it gets fixed inadvertitently we know.
template.Template("hern")
template.Template("hern")
