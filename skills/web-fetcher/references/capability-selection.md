# Capability selection

Use source and task requirements to select an available route. A native reader or
structured connector is sufficient for ordinary text; search results locate
sources but do not establish their full content. Browser/CUA helps with dynamic
pages, visual details and interactions. Scripts remain useful for repeated
retrieval, downloads and conversions. Do not assume every host exposes all three.

When a route fails, inspect its failure and choose an independent available path.
Do not install tools or change authentication automatically. Respect source access
controls. Report blocked/partial retrieval with the remaining evidence gap.

Native tools are invoked by the host. `fetch.py` implements CLI and HTTP adapters,
not a simulation of host browser or video understanding.
