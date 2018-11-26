"""
Most code below inspired by Django crypto.py utility

https://github.com/django/django/blob/master/django/utils/crypto.py
"""
import hashlib
import random
import sys
import time

# Use the system PRNG if possible
try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    import warnings
    warnings.warn(
        'A secure pseudo-random number generator is not available '
        'on your system. Falling back to Mersenne Twister.'
    )
    using_sysrandom = False

def get_random_string(
    length=16,
    allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                  'abcdefghijklmnopqrstuvwxyz'
):
    """
    Return a securely generated random string.
    """
    if not using_sysrandom:
        random.seed(
            hashlib.sha256(
                ('{}{}'.format(random.getstate(), time.time())).encode()
            ).digest()
        )
    return ''.join(random.choice(allowed_chars) for i in range(length))

def get_secret_key():
    return get_random_string(
        length=64,
        allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    )


if __name__ == '__main__': 
    DATABASE_URL = ''.join([
        'postgres://postgres:{}'.format(get_random_string()),
        '@127.0.0.1:5432/',
        '{{ cookiecutter.project_dj_name }}{}'.format('_db')
    ])

    with open('.env', 'w') as fp:
        fp.write('SECRET_KEY={}\n'.format(get_secret_key()))
        fp.write('DEBUG={{ cookiecutter.debug }}\n')
        fp.write('ALLOWED_HOSTS=localhost,127.0.0.1,[::1]\n')
        fp.write('LANGUAGE_CODE={{ cookiecutter.language_code }}\n')
        fp.write('TIME_ZONE={{ cookiecutter.time_zone }}\n')
        {% if cookiecutter.database_engine == 'postgresql' %}
        fp.write('DATABASE_URL={}\n'.format(DATABASE_URL))
        {% endif %}

    sys.exit(0)
