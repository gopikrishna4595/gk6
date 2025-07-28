# Folder: gk6/
# File: cli.py

import json
import time
from datetime import datetime
from pathlib import Path

import typer

from .core import generate_env_file, generate_k6_script, list_apis

app = typer.Typer()


@app.command()
def convert(
    collection: Path = typer.Option(..., help="Path to Postman collection JSON"),
    env: Path | None = typer.Option(None, help="Path to Postman environment JSON"),
    include: str | None = typer.Option(
        None, help="Comma-separated API indices (e.g. 1,3,5)"
    ),
    all: bool = typer.Option(False, help="Include all APIs"),
):
    try:
        with collection.open("r", encoding="utf-8") as file:
            postman_collection = json.load(file)
        typer.echo("✅ Postman collection loaded.")
    except Exception as e:
        typer.secho(f"❌ Failed to load collection: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)

    apis = list_apis(postman_collection)
    typer.echo(f"📦 Found {len(apis)} APIs.")

    if env:
        try:
            with env.open("r", encoding="utf-8") as file:
                postman_env = json.load(file)
            typer.echo("✅ Environment file loaded.")
            env_content, keys = generate_env_file(postman_env)
            with open(".env", "w", encoding="utf-8") as f:
                f.write(env_content)
            typer.echo(".env file written.")
        except Exception as e:
            typer.secho(f"❌ Failed to load environment: {e}", fg=typer.colors.RED)
            raise typer.Exit(1)

    if not all and not include:
        typer.secho(
            "❌ You must provide either --all or --include.", fg=typer.colors.RED
        )
        raise typer.Exit(1)

    if all:
        selected_apis = apis
        typer.echo("✅ All APIs selected.")
    else:
        if include is None:
            typer.secho(
                "❌ --include must not be None when --all is False", fg=typer.colors.RED
            )
            raise typer.Exit(1)

        try:
            indices = [int(i.strip()) - 1 for i in include.split(",")]
            selected_apis = [apis[i] for i in indices]
            typer.echo(f"✅ Included APIs: {include}")
        except Exception as e:
            typer.secho(f"❌ Invalid --include value: {e}", fg=typer.colors.RED)
            raise typer.Exit(1)

    k6_script = generate_k6_script(selected_apis, postman_collection)

    collection_name = collection.stem.replace(" ", "")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    timezone_abbr = time.strftime("%Z")
    filename = f"{collection_name}_{timestamp}_{timezone_abbr}_k6_script.js"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(k6_script)

    typer.secho(f"\n🎯 K6 script saved as: {filename}", fg=typer.colors.GREEN)


@app.command(name="list-apis")
def list_apis_in_collection(
    collection: Path = typer.Option(..., help="Path to Postman collection JSON")
):
    try:
        with collection.open("r", encoding="utf-8") as file:
            postman_collection = json.load(file)
        apis = list_apis(postman_collection)
        typer.echo(f"\n📦 {len(apis)} APIs found:")
        for i, api in enumerate(apis, start=1):
            typer.echo(f"[{i}] {api['method']} {api['url']} → {api['name']}")
    except Exception as e:
        typer.secho(f"❌ Failed to list APIs: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)


@app.command()
def install_completion():
    """
    Installs shell auto-completion for your terminal (bash, zsh, fish, powershell).
    """
    import typer

    typer.echo("🔧 Installing shell completion...")
    typer.main.get_command(app).shell_complete()
    typer.echo("✅ Completion setup done. You may need to restart your shell.")


def main():
    app()


if __name__ == "__main__":
    main()
