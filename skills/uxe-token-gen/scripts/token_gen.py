#!/usr/bin/env python3
"""
uxe-token-gen — Generate a complete design token system from a brand color.
Part of the uxe-team Claude agent toolkit.

Usage:
    python3 token_gen.py <hex_color> [style] [format]

    hex_color : Brand primary color in hex (e.g. #0066CC or 0066CC)
    style     : modern | classic | playful  (default: modern)
    format    : css | scss | js | tailwind | style-dictionary | summary  (default: css)

Examples:
    python3 token_gen.py "#0066CC" modern css
    python3 token_gen.py "#FF6B6B" playful tailwind
    python3 token_gen.py "#2D3748" classic style-dictionary
    python3 token_gen.py "#0066CC" modern summary
"""

import sys
import json
import colorsys
from typing import Dict, Any


# ── Color Utilities ────────────────────────────────────────────────────────────

def hex_to_rgb(hex_color: str) -> tuple:
    h = hex_color.lstrip('#')
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def rgb_to_hex(r, g, b) -> str:
    return '#{:02X}{:02X}{:02X}'.format(
        max(0, min(255, round(r))),
        max(0, min(255, round(g))),
        max(0, min(255, round(b))),
    )


def hex_to_hsl(hex_color: str) -> tuple:
    r, g, b = hex_to_rgb(hex_color)
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    return h * 360, s * 100, l * 100


def hsl_to_hex(h: float, s: float, l: float) -> str:
    h = h % 360
    r, g, b = colorsys.hls_to_rgb(h / 360, max(0, min(100, l)) / 100, max(0, min(100, s)) / 100)
    return rgb_to_hex(r * 255, g * 255, b * 255)


def relative_luminance(hex_color: str) -> float:
    r, g, b = hex_to_rgb(hex_color)
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def wcag_contrast(hex1: str, hex2: str) -> float:
    l1 = relative_luminance(hex1)
    l2 = relative_luminance(hex2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


# ── Style Presets ──────────────────────────────────────────────────────────────

STYLES = {
    'modern': {
        'font_sans':       '"Inter", "system-ui", "-apple-system", sans-serif',
        'font_mono':       '"Fira Code", "JetBrains Mono", monospace',
        'radius_sm':       '4px',
        'radius_default':  '8px',
        'radius_lg':       '12px',
        'radius_xl':       '20px',
        'radius_2xl':      '28px',
    },
    'classic': {
        'font_sans':       '"Helvetica Neue", "Arial", sans-serif',
        'font_mono':       '"Courier New", monospace',
        'radius_sm':       '2px',
        'radius_default':  '4px',
        'radius_lg':       '6px',
        'radius_xl':       '8px',
        'radius_2xl':      '12px',
    },
    'playful': {
        'font_sans':       '"Poppins", "Nunito", sans-serif',
        'font_mono':       '"Source Code Pro", monospace',
        'radius_sm':       '8px',
        'radius_default':  '16px',
        'radius_lg':       '24px',
        'radius_xl':       '32px',
        'radius_2xl':      '40px',
    },
}


# ── Token Generation ───────────────────────────────────────────────────────────

def color_scale(hex_color: str) -> Dict[str, str]:
    h, s, l = hex_to_hsl(hex_color)
    base = hex_color.upper() if hex_color.startswith('#') else f'#{hex_color.upper()}'
    return {
        '50':  hsl_to_hex(h, max(s * 0.20,  8), 97),
        '100': hsl_to_hex(h, max(s * 0.30, 12), 94),
        '200': hsl_to_hex(h, max(s * 0.45, 18), 88),
        '300': hsl_to_hex(h, s * 0.65, 76),
        '400': hsl_to_hex(h, s * 0.82, 63),
        '500': base,
        '600': hsl_to_hex(h, min(s * 1.05, 100), l * 0.84),
        '700': hsl_to_hex(h, min(s * 1.10, 100), l * 0.68),
        '800': hsl_to_hex(h, min(s * 1.10, 100), l * 0.48),
        '900': hsl_to_hex(h, min(s * 1.10, 100), l * 0.30),
        '950': hsl_to_hex(h, min(s * 1.10, 100), l * 0.18),
    }


def neutral_scale(hex_color: str) -> Dict[str, str]:
    h, s, _ = hex_to_hsl(hex_color)
    ns = min(s * 0.08, 6)  # nearly desaturated, brand-tinted
    return {
        '50':  hsl_to_hex(h, ns, 98),
        '100': hsl_to_hex(h, ns, 95),
        '200': hsl_to_hex(h, ns, 90),
        '300': hsl_to_hex(h, ns, 80),
        '400': hsl_to_hex(h, ns, 64),
        '500': hsl_to_hex(h, ns, 46),
        '600': hsl_to_hex(h, ns, 34),
        '700': hsl_to_hex(h, ns, 24),
        '800': hsl_to_hex(h, ns, 16),
        '900': hsl_to_hex(h, ns, 10),
        '950': hsl_to_hex(h, ns,  5),
    }


def secondary_scale(hex_color: str) -> Dict[str, str]:
    h, s, l = hex_to_hsl(hex_color)
    sec_h = (h + 150) % 360
    sec_base = hsl_to_hex(sec_h, s * 0.85, l)
    return color_scale(sec_base)


def generate_tokens(hex_color: str, style: str = 'modern') -> Dict[str, Any]:
    if not hex_color.startswith('#'):
        hex_color = '#' + hex_color
    hex_color = hex_color.upper()

    s = STYLES.get(style, STYLES['modern'])
    primary   = color_scale(hex_color)
    secondary = secondary_scale(hex_color)
    neutral   = neutral_scale(hex_color)

    # Determine best text color on primary-500 (WCAG AA)
    on_primary = '#FFFFFF' if wcag_contrast(primary['500'], '#FFFFFF') >= 4.5 else '#111111'

    return {
        'color': {
            'primary':   primary,
            'secondary': secondary,
            'neutral':   neutral,
            'semantic': {
                'success-50':  '#F0FDF4',
                'success-500': '#22C55E',
                'success-700': '#15803D',
                'warning-50':  '#FFFBEB',
                'warning-500': '#F59E0B',
                'warning-700': '#B45309',
                'error-50':    '#FEF2F2',
                'error-500':   '#EF4444',
                'error-700':   '#B91C1C',
                'info-50':     primary['50'],
                'info-500':    primary['500'],
                'info-700':    primary['700'],
            },
            'surface': {
                'default':  neutral['50'],
                'raised':   '#FFFFFF',
                'overlay':  neutral['100'],
                'sunken':   neutral['200'],
                'inverse':  neutral['900'],
            },
            'text': {
                'primary':    neutral['900'],
                'secondary':  neutral['600'],
                'tertiary':   neutral['400'],
                'disabled':   neutral['300'],
                'inverse':    neutral['50'],
                'on-primary': on_primary,
                'link':       primary['600'],
                'link-hover': primary['800'],
            },
            'border': {
                'default': neutral['200'],
                'strong':  neutral['400'],
                'focus':   primary['500'],
                'error':   '#EF4444',
            },
        },
        'typography': {
            'font-family': {
                'sans': s['font_sans'],
                'mono': s['font_mono'],
            },
            'font-size': {
                'xs':   '0.625rem',
                'sm':   '0.8125rem',
                'base': '1rem',
                'lg':   '1.25rem',
                'xl':   '1.5625rem',
                '2xl':  '1.9375rem',
                '3xl':  '2.4375rem',
                '4xl':  '3.0625rem',
                '5xl':  '3.8125rem',
            },
            'font-weight': {
                'regular':  '400',
                'medium':   '500',
                'semibold': '600',
                'bold':     '700',
            },
            'line-height': {
                'none':    '1',
                'tight':   '1.25',
                'snug':    '1.375',
                'normal':  '1.5',
                'relaxed': '1.625',
                'loose':   '2',
            },
            'letter-spacing': {
                'tight':   '-0.025em',
                'normal':  '0',
                'wide':    '0.025em',
                'wider':   '0.05em',
                'widest':  '0.1em',
            },
        },
        'spacing': {
            '0':   '0',
            '0.5': '2px',
            '1':   '4px',
            '1.5': '6px',
            '2':   '8px',
            '2.5': '10px',
            '3':   '12px',
            '3.5': '14px',
            '4':   '16px',
            '5':   '20px',
            '6':   '24px',
            '7':   '28px',
            '8':   '32px',
            '9':   '36px',
            '10':  '40px',
            '11':  '44px',
            '12':  '48px',
            '14':  '56px',
            '16':  '64px',
            '20':  '80px',
            '24':  '96px',
            '28':  '112px',
            '32':  '128px',
        },
        'border-radius': {
            'none':    '0',
            'sm':      s['radius_sm'],
            'default': s['radius_default'],
            'lg':      s['radius_lg'],
            'xl':      s['radius_xl'],
            '2xl':     s['radius_2xl'],
            'full':    '9999px',
        },
        'shadow': {
            'none':  'none',
            'xs':    '0 1px 2px 0 rgb(0 0 0 / 0.05)',
            'sm':    '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
            'md':    '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
            'lg':    '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
            'xl':    '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
            '2xl':   '0 25px 50px -12px rgb(0 0 0 / 0.25)',
            'inner': 'inset 0 2px 4px 0 rgb(0 0 0 / 0.05)',
        },
        'animation': {
            'duration': {
                'instant': '50ms',
                'fast':    '100ms',
                'normal':  '200ms',
                'slow':    '300ms',
                'slower':  '500ms',
            },
            'easing': {
                'default': 'cubic-bezier(0.4, 0, 0.2, 1)',
                'in':      'cubic-bezier(0.4, 0, 1, 1)',
                'out':     'cubic-bezier(0, 0, 0.2, 1)',
                'in-out':  'cubic-bezier(0.4, 0, 0.2, 1)',
                'bounce':  'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
                'spring':  'cubic-bezier(0.5, 0, 0, 1.5)',
            },
        },
        'breakpoint': {
            'xs':  '0px',
            'sm':  '480px',
            'md':  '640px',
            'lg':  '768px',
            'xl':  '1024px',
            '2xl': '1280px',
            '3xl': '1536px',
        },
        'z-index': {
            'base':     '0',
            'raised':   '1',
            'dropdown': '100',
            'sticky':   '200',
            'overlay':  '300',
            'modal':    '400',
            'toast':    '500',
            'tooltip':  '600',
            'max':      '9999',
        },
    }


# ── Output Formatters ──────────────────────────────────────────────────────────

def flatten(d: Dict, prefix: str = '') -> Dict[str, str]:
    out = {}
    for k, v in d.items():
        key = f'{prefix}-{k}' if prefix else k
        if isinstance(v, dict):
            out.update(flatten(v, key))
        else:
            out[key] = str(v)
    return out


def fmt_css(tokens: Dict) -> str:
    flat = flatten(tokens)
    lines = [':root {']
    for k, v in flat.items():
        lines.append(f'  --{k}: {v};')
    lines.append('}')
    return '\n'.join(lines)


def fmt_scss(tokens: Dict) -> str:
    flat = flatten(tokens)
    return '\n'.join(f'${k}: {v};' for k, v in flat.items())


def fmt_js(tokens: Dict) -> str:
    return f'export const tokens = {json.dumps(tokens, indent=2)};\n'


def fmt_tailwind(tokens: Dict) -> str:
    c = tokens['color']
    config = {
        'theme': {
            'extend': {
                'colors': {
                    'primary':   c['primary'],
                    'secondary': c['secondary'],
                    'neutral':   c['neutral'],
                    'success': {'50': c['semantic']['success-50'], '500': c['semantic']['success-500'], '700': c['semantic']['success-700']},
                    'warning': {'50': c['semantic']['warning-50'], '500': c['semantic']['warning-500'], '700': c['semantic']['warning-700']},
                    'error':   {'50': c['semantic']['error-50'],   '500': c['semantic']['error-500'],   '700': c['semantic']['error-700']},
                },
                'spacing':                tokens['spacing'],
                'fontFamily':             tokens['typography']['font-family'],
                'fontSize':               tokens['typography']['font-size'],
                'borderRadius':           tokens['border-radius'],
                'boxShadow':              tokens['shadow'],
                'transitionDuration':     tokens['animation']['duration'],
                'transitionTimingFunction': tokens['animation']['easing'],
                'zIndex':                 tokens['z-index'],
            }
        }
    }
    return f'/** @type {{import("tailwindcss").Config}} */\nmodule.exports = {json.dumps(config, indent=2)};\n'


def fmt_style_dictionary(tokens: Dict, hex_color: str, style: str) -> str:
    """W3C Design Tokens Community Group format (compatible with Tokens Studio, Style Dictionary 4+)."""
    def wrap(d, category=''):
        out = {}
        for k, v in d.items():
            if isinstance(v, dict):
                out[k] = wrap(v, category or k)
            else:
                token_type = 'color' if 'color' in category else 'dimension'
                out[k] = {'$value': v, '$type': token_type}
        return out

    sd = {
        '$schema': 'https://tr.designtokens.org/format/',
        'meta': {'brand-color': {'$value': hex_color}, 'style': {'$value': style}, 'generator': {'$value': 'uxe-token-gen'}},
    }
    sd.update(wrap(tokens))
    return json.dumps(sd, indent=2)


def fmt_summary(tokens: Dict, hex_color: str, style: str) -> str:
    primary = tokens['color']['primary']
    on_p    = tokens['color']['text']['on-primary']
    contrast = wcag_contrast(primary['500'], on_p)
    wcag_lvl = 'AAA' if contrast >= 7 else ('AA' if contrast >= 4.5 else 'FAIL')

    lines = [
        'uxe-token-gen — Design Token Summary',
        '=' * 42,
        f'Brand color  : {hex_color}',
        f'Style        : {style}',
        f'',
        'Primary Color Scale',
        '-' * 42,
    ]
    for step, val in primary.items():
        marker = '  <-- base (500)' if step == '500' else ''
        lines.append(f'  primary-{step:3s}  {val}{marker}')

    lines += [
        '',
        f'Text on primary-500  : {on_p}',
        f'Contrast ratio       : {contrast:.2f}:1  ({wcag_lvl})',
        '',
        'Semantic Colors',
        '-' * 42,
    ]
    for k, v in tokens['color']['semantic'].items():
        lines.append(f'  {k:20s}  {v}')

    lines += [
        '',
        'Typography',
        '-' * 42,
        f"  Sans  : {tokens['typography']['font-family']['sans']}",
        f"  Mono  : {tokens['typography']['font-family']['mono']}",
        '',
        'Border Radius',
        '-' * 42,
    ]
    for k, v in tokens['border-radius'].items():
        lines.append(f'  radius-{k:8s}  {v}')

    flat = flatten(tokens)
    lines += ['', f'Total tokens generated: {len(flat)}']
    return '\n'.join(lines)


# ── Main ───────────────────────────────────────────────────────────────────────

FORMATS = {'css', 'scss', 'js', 'tailwind', 'style-dictionary', 'summary'}

def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print(__doc__)
        sys.exit(0)

    hex_color = args[0].lstrip('#')
    if len(hex_color) != 6 or not all(c in '0123456789ABCDEFabcdef' for c in hex_color):
        print(f'Error: Invalid hex color "{args[0]}". Use a 6-digit hex like #0066CC', file=sys.stderr)
        sys.exit(1)
    hex_color = '#' + hex_color.upper()

    style  = args[1] if len(args) > 1 else 'modern'
    fmt    = args[2] if len(args) > 2 else 'css'

    if style not in STYLES:
        print(f'Error: Unknown style "{style}". Choose: modern | classic | playful', file=sys.stderr)
        sys.exit(1)
    if fmt not in FORMATS:
        print(f'Error: Unknown format "{fmt}". Choose: {" | ".join(sorted(FORMATS))}', file=sys.stderr)
        sys.exit(1)

    tokens = generate_tokens(hex_color, style)

    formatters = {
        'css':              lambda: fmt_css(tokens),
        'scss':             lambda: fmt_scss(tokens),
        'js':               lambda: fmt_js(tokens),
        'tailwind':         lambda: fmt_tailwind(tokens),
        'style-dictionary': lambda: fmt_style_dictionary(tokens, hex_color, style),
        'summary':          lambda: fmt_summary(tokens, hex_color, style),
    }
    print(formatters[fmt]())


if __name__ == '__main__':
    main()
