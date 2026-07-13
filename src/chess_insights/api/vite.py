import json

with open('static/dist/.vite/manifest.json') as f:
    manifest = json.load(f)

def _collect_deps(entry_name, seen_js=None, seen_css=None):
    if seen_js is None:
        seen_js = []
    if seen_css is None:
        seen_css = []

    data = manifest[entry_name]

    # collect this chunk's CSS first
    for css_file in data.get('css', []):
        if css_file not in seen_css:
            seen_css.append(css_file)

    # recurse into imported chunks
    for imported in data.get('imports', []):
        _collect_deps(imported, seen_js, seen_css)

    # add this chunk's JS file
    if data['file'] not in seen_js:
        seen_js.append(data['file'])

    return seen_js, seen_css

def vite_asset(entry):
    js_files, css_files = _collect_deps(entry)

    tags = ''
    for css_file in css_files:
        tags += f'<link rel="stylesheet" href="/static/dist/{css_file}">\n'
    for js_file in js_files:
        tags += f'<link rel="modulepreload" href="/static/dist/{js_file}">\n'

    entry_file = manifest[entry]['file']
    tags += f'<script type="module" src="/static/dist/{entry_file}"></script>\n'

    return tags