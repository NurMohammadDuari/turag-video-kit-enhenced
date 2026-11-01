"""Resolve named cast identity while keeping scene action and framing editable."""
import copy

IDENTITY = {'role', 'variant', 'color', 'legColor', 'visor'}


def resolve_cast(episode):
    result = copy.deepcopy(episode)
    cast = result.get('cast', {})
    if not isinstance(cast, dict):
        raise ValueError('cast must be an object keyed by persistent character ID')
    for name, identity in cast.items():
        if not isinstance(identity, dict) or set(identity)-IDENTITY:
            raise ValueError(f'Cast {name}: only identity fields are allowed; stage actions in the shot')
        if identity.get('role','extra') not in {'guide','extra','doctor','vendor'}:
            raise ValueError(f'Cast {name}: unknown role')
        if 'variant' in identity and (type(identity['variant']) is not int or not 0 <= identity['variant'] <= 5):
            raise ValueError(f'Cast {name}: variant must be 0..5')
    for beat in result['beats']:
        for obj in beat.get('shot', {}).get('objects', []):
            if 'castId' not in obj:
                continue
            name = obj['castId']
            if obj.get('type') != 'person' or name not in cast:
                raise ValueError(f'{beat["id"]}: unknown castId or non-person cast use: {name}')
            identity = cast[name]
            for key, value in identity.items():
                if key in obj and obj[key] != value:
                    raise ValueError(f'{beat["id"]}: {name} changes {key}; use a distinct costume identity deliberately')
                obj[key] = value
            for frame in obj.get('keyframes', []):
                if IDENTITY.intersection(frame):
                    raise ValueError(f'{beat["id"]}: identity cannot change through keyframes')
            for action in obj.get('actions', []):
                if IDENTITY.intersection(action):
                    raise ValueError(f'{beat["id"]}: identity cannot change through action tracks')
    return result
