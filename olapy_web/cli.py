from __future__ import absolute_import, division, print_function

import click
from .app import create_app

app = create_app()


# @app.cli.command('init', short_help='Initialize database')
# @click.pass_context
# def init(ctx):
#     # from olapy.cli import init
#     # os.environ['OLAPY_PATH'] = app.instance_path
#     # ctx.invoke(init)
#     # print('Initialized Olapy')


@app.cli.command(short_help='Run web Server')
@click.option(
    '--host', '-h', default='127.0.0.1', help='The interface to bind to.')
@click.option('--port', '-p', default=5000, help='The port to bind to.')
def run(host, port):
    app.run(host=host, port=port)


@click.group()
def cli():
    pass


# cli.add_command(initdb)
# cli.add_command(dropdb)
cli.add_command(run)
