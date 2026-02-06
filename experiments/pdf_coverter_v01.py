#!/usr/bin/env python3
"""
console script, testing pdf converter
"""

import glob
import time
from pathlib import Path

import click


def mk_doc_converter(source: str) -> tuple[str, float]:
    """Convert document of supported formats to markdown."""
    load_start = time.time()
    from docling.document_converter import DocumentConverter

    converter = DocumentConverter()
    load_time = time.time() - load_start
    click.echo(f"  ⏱️  Model loaded in {load_time:.2f}s")

    convert_start = time.time()
    result = converter.convert(source)
    markdown = result.document.export_to_markdown()
    convert_time = time.time() - convert_start

    return markdown, convert_time


@click.group()
def main():
    pass


@main.command()
@click.argument("pattern")
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(file_okay=False),
    required=True,
    help="Directory to save the converted markdown files.",
)
def convert(pattern: str, output_dir: str):
    """Convert documents matching PATTERN to Markdown.

    PATTERN: Glob pattern for source documents (e.g., '/path/f*.pdf' or 'docs/*.docx')
    """
    app_start = time.time()

    # Expand glob pattern
    files = glob.glob(pattern)

    if not files:
        click.echo(f"❌ No files found matching pattern: {pattern}", err=True)
        return

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    click.echo(f"📁 Found {len(files)} file(s) to convert\n")

    total_conversion_time = 0

    for i, source in enumerate(files, 1):
        # Generate output filename
        source_path = Path(source)
        output_file = Path(output_dir) / f"{source_path.stem}.md"

        click.echo(f"[{i}/{len(files)}] Converting: {source_path.name}")

        doc_start = time.time()
        markdown, convert_time = mk_doc_converter(source)

        with open(output_file, "w") as f:
            f.write(markdown)

        doc_total = time.time() - doc_start
        total_conversion_time += convert_time

        click.echo(f"  ⏱️  Conversion took {convert_time:.2f}s (total: {doc_total:.2f}s)")
        click.echo(f"  ✅ Saved to: {output_file}\n")

    app_total = time.time() - app_start

    click.echo("=" * 60)
    click.echo("✨ Summary:")
    click.echo(f"  • Total files converted: {len(files)}")
    click.echo(f"  • Total conversion time: {total_conversion_time:.2f}s")
    click.echo(f"  • Average per document: {total_conversion_time / len(files):.2f}s")
    click.echo(f"  • Total runtime: {app_total:.2f}s")
    click.echo("=" * 60)


if __name__ == "__main__":
    main()
