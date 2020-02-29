from contextlib import contextmanager


@contextmanager
def entity_resource_context_manager(resource_getter, entity_class, attrname: str):
    """
    :param resource_getter: funkcia na ziskanie zdroju, moze byt trieda (zdroj bude jej instancia)
    :param entity_class: trieda, ktorej chceme priradit zdroj
    :param attrname: nazov parametru triedy entity_class, kde sa ma ulozit zdroj
    """
    with resource_getter() as resource:
        setattr(entity_class, attrname, resource)
        try:
            yield
        finally:
            setattr(entity_class, attrname, None)


@contextmanager
def entity_simple_context_manager(value, entity_class, attrname: str):
    setattr(entity_class, attrname, value)
    try:
        yield
    finally:
        setattr(entity_class, attrname, None)
