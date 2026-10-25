"""Validate the non-public CMS fixture; optionally verify a Jekyll output."""

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]


def validate():
    entries = sorted((ROOT / '.cms-test' / 'entries').glob('*.json'))
    if not entries:
        raise ValueError('Missing CMS verification fixture')
    for path in entries:
        data = json.loads(path.read_text(encoding='utf-8'))
        if set(data) != {'title', 'body', 'force_failure'}:
            raise ValueError(f'{path.name}: unexpected fields')
        for key in ('title', 'body'):
            if not isinstance(data[key], str) or not data[key].strip():
                raise ValueError(f'{path.name}: {key} must be non-empty text')
        if type(data['force_failure']) is not bool:
            raise ValueError(f'{path.name}: force_failure must be boolean')
        if data['force_failure']:
            raise ValueError(f'{path.name}: intentional CMS publication block')
    if len(sys.argv) == 2:
        output = Path(sys.argv[1])
        if not (output / 'index.html').is_file():
            raise ValueError('Missing built homepage')
        if (output / '.cms-test').exists():
            raise ValueError('CMS test files leaked into public build')
        fixture_bytes = [path.read_bytes() for path in entries]
        for path in output.rglob('*'):
            if path.is_file() and path.suffix in ('.html', '.json', '.yml', '.yaml'):
                content = path.read_bytes()
                if b'REPLACE_WITH_TURBO_SITE_ID' in content or any(
                    value in content for value in fixture_bytes
                ):
                    raise ValueError(f'CMS fixture leaked into {path}')
    print(f'PASS: {len(entries)} CMS fixtures; intentional failure is off')


if __name__ == '__main__':
    try:
        validate()
    except (ValueError, OSError) as error:
        raise SystemExit(str(error))
