# xy2_'s site
This is the source code of my personal site.

An instance can be found at https://xy2.dev/.

## Deployment

1. (Optionally) Create psite/settings.py with your own settings.
2. (If you use nginx) Symlink the nginx config in /enabled-sites/ in the nginx directory.
3. Install the packages: `pipenv install`.
4. Run gunicorn with the included configs with `gunicorn_django -D -c gunicorn.conf.py`.

All feedback is appreciated : issues and PRs welcome.
