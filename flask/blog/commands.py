import click

from blog.posts import (
    get_all_posts,
    get_post_by_slug,
    update_post_by_slug,
    new_post
)

@click.group()
def post():
    """Group of commands to manage posts."""
    pass

@post.command()
@click.option("--title", prompt=True, help="Title of the post.")
@click.option("--content", prompt=True, help="Content of the post.")
def new(title, content):
    """Create a new post."""
    new_slug = new_post(title, content)
    click.echo(f"Post created successfully {new_slug}")

@post.command("list")
def _list():
    """List all posts."""
    posts = get_all_posts()
    for post in posts:
        click.echo(f"{post['title']} - {post['slug']}")

@post.command()
@click.argument("slug")
def get(slug):
    """Get a post by slug."""
    post = get_post_by_slug(slug)
    click.echo(f"{post['title']} - {post['slug']}")
    click.echo(post["content"])

@post.command()
@click.argument("slug")
@click.option("--content", default=None, type=str)
@click.option("--published", default=None, type=str)
def update(slug, content, published):
    """Update a post."""
    data = {}
    if content is not None:
        data["content"] = content
    if published is not None:
        data["published"] = published.lower() == "true"
    update_post_by_slug(slug, data)
    click.echo(f"Post {slug} updated successfully")
    
@post.command()
@click.argument("slug")
def unpublish(slug):
    """Unpublish a post by slug."""
    updated = update_post_by_slug(slug, {}, published=False)
    if updated:
        click.echo(f"Post {slug} unpublished successfully.")
    else:
        click.echo(f"No post found with slug: {slug}")

def configure(app):
    app.cli.add_command(post)
