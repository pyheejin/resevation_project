from fastapi import HTTPException

from database.models import *
from database.admin_schema import *
from config.constant import ERROR_DIC
from database.base_model import DefaultModel


def get_ticket(page, page_size, session, status):
    response = DefaultModel()

    filter_list = []
    if status is not None:
        filter_list.append(Ticket.status == status)

    ticket_query = session.query(Ticket).filter(Ticket.status >= constant.STATUS_INACTIVE)
    ticket_filter = ticket_query.filter(*filter_list)
    tickets = ticket_filter.offset(page_size * (page - 1)).limit(page_size).all()

    response.result_data = {
        'total_count': len(ticket_query.all()),
        'search_count': len(ticket_filter.all()),
        'tickets': ticket_list_schema.dump(tickets)
    }
    return response


def post_ticket(request, session, g):
    response = DefaultModel()

    user_id = g.result_data.get('user', None).get('id', None)

    cost = request.cost
    price = request.price
    count = request.count

    ticket = Ticket()
    session.add(ticket)
    session.flush()

    ticket.user_id = user_id
    ticket.cost = cost
    ticket.price = price
    ticket.count = count

    response.result_data = {
        'ticket': ticket_detail_schema.dump(ticket)
    }
    return response


def get_ticket_detail(ticket_id, session):
    response = DefaultModel()

    ticket = session.query(Ticket).filter(Ticket.id == ticket_id,
                                          Ticket.status >= constant.STATUS_INACTIVE).first()
    if ticket is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    response.result_data = {
        'ticket': ticket_detail_schema.dump(ticket)
    }
    return response


def put_ticket_detail(ticket_id, request, session):
    response = DefaultModel()

    ticket = session.query(Ticket).filter(Ticket.id == ticket_id,
                                          Ticket.status >= constant.STATUS_INACTIVE).first()
    if ticket is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    cost = request.cost
    price = request.price
    count = request.count

    ticket.cost = cost
    ticket.price = price
    ticket.count = count

    response.result_data = {
        'ticket': ticket_detail_schema.dump(ticket)
    }
    return response


def delete_ticket_detail(ticket_id, session):
    response = DefaultModel()

    ticket = session.query(Ticket).filter(Ticket.id == ticket_id,
                                          Ticket.status >= constant.STATUS_INACTIVE).first()
    if ticket is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    ticket.status = constant.STATUS_DELETED
    return response