# -*- coding: utf-8 -*-

from suds.sudsobject import asdict
from datetime import timedelta, date, datetime
import json
import unicodedata



def recursive_asdict(d):
    """Convierte un objeto Suds en uno serializable"""
    out = {}
    for k, v in asdict(d).iteritems():
        if hasattr(v, '__keylist__'):
            out[k] = recursive_asdict(v)
        elif isinstance(v, list):
            out[k] = []
            for item in v:
                if hasattr(item, '__keylist__'):
                    out[k].append(recursive_asdict(item))
                else:
                    out[k].append(item)
        else:
            out[k] = v
    return out

def suds_to_json(data):
    return json.dumps(recursive_asdict(data))

def remover_acentos(input_str):
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

def rangodefecha(fechainicio, fechafin):
    for n in range(int ((fechafin - fechainicio).days)):
        yield fechainicio + timedelta(n)