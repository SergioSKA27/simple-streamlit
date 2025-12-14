from jinja2 import Environment, BaseLoader
from typing import List

from ...core.build.cstparser import StreamlitComponentParser

# Entorno global con filtro predefinido
GLOBAL_ENV = Environment(loader=BaseLoader(), autoescape=False) # nosec B701
GLOBAL_ENV.filters['to_code'] = lambda x: repr(x) if isinstance(x, str) else str(x)

def get_component_template(renderable: StreamlitComponentParser) -> str:
    """
    Ahora devuelve un template que SÍ puede renderizarse
    porque usa el entorno global con el filtro registrado
    """
    return GLOBAL_ENV.from_string("""

{% if effects %}
if result_{{base_component}}_{{unique_id}} := st.{{ base_component }}(
    {% for arg in args %}{{ arg | to_code }}, {% endfor %}
    {% for key, value in kwargs.items() %}
    {{ key }}={{ value | to_code }},
    {% endfor %}
):
    res = result_{{base_component}}_{{unique_id}}
    # Effects
    {% for effect in effects %}
    try:
        {{ effect | to_code }}
    except Exception as e:
        st.error(f"Error en efecto: {e}")
    {% endfor %}
{% endif %}
{% if not effects %}
st.{{ base_component }}(
    {% for arg in args %}{{ arg | to_code }}, {% endfor %}
    {% for key, value in kwargs.items() %}
    {{ key }}={{ value | to_code }},
    {% endfor %}
)
{% endif %}
""")


def merge_templates(components: List[StreamlitComponentParser]) -> str:
    base_template = GLOBAL_ENV.from_string("""
import streamlit as st
st.set_page_config(layout="wide")

{% for component in components %}
{{ component }}
{% endfor %}
""")
    
    processed = []
    for comp in components:
        data = comp.ast_serialize()
        data['effects'] = [f"lambda res: {e.__name__}(res)" for e in comp._effects]
        
        # Renderiza con el entorno global (donde SÍ existe to_code)
        rendered_component = get_component_template(comp).render(**data)
        processed.append(rendered_component)
    
    return base_template.render(components=processed)