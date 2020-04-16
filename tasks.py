from invoke import task


@task
def dev(c):
    start(c, dev=True)


@task
def start(c, dev=False):
    c.run(
        f"FLASK_ENV={'development' if dev else 'production'} pipenv run python main.py",
        echo=True,
    )
