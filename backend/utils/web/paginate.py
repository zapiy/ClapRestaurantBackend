from typing import List, TypeVar, Union
from types import GeneratorType, LambdaType
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.db.models import QuerySet, CharField
from django.db.models.functions import Concat, Lower

from .json_response import CustomJsonResponse


def paginate(
    data: Union[list, GeneratorType],
    request: HttpRequest,
    *,
    side_data: Union[bool, dict] = True,
    response: bool = True,
    serializer: LambdaType = None,
    per_page: int = 20
):
    paginator = Paginator(data, per_page)
    try:
        page = int(request.GET.get('p', 1))
    except:
        page = 1
        
    view = list(paginator.get_page(page))
    view = (view if serializer is None else serializer(view))
    
    if side_data:
        view = {
            'view': view,
            'paginator':{
                'current': (page if isinstance(page, int) and page in range(1, paginator.num_pages + 1) else 1),
                'max': paginator.num_pages,
            }
        }
        
        if isinstance(side_data, dict):
            view.update(side_data)
    
    if response:
        return CustomJsonResponse(view, status = 200)
    return view


_T = TypeVar('_T')
def wrap_search(request: HttpRequest, fields: List[str], query: QuerySet[_T]) -> QuerySet[_T]:
    search = request.GET.get('q', None)
    if not search:
        return query
    
    assert len(fields) > 0
    
    return (
        query
            .annotate(
                _query = Lower(
                (
                    Concat(*fields) 
                    if len(fields) > 1 else 
                    fields[0]
                ), output_field=CharField())
            )
            .filter(_query__contains=search.lower())
    )
