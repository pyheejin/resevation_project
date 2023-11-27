from fastapi import HTTPException

from database.models import *
from database.admin_schema import *
from config.constant import ERROR_DIC
from database.base_model import DefaultModel


def get_ticket(session, user_id):
    response = DefaultModel()

    filter_list = []
    if user_id is not None:
        filter_list.append(Ticket.user_id == user_id)

    tickets = session.query(Ticket).filter(Ticket.status == constant.STATUS_ACTIVE,
                                           *filter_list).all()
    response.result_data = {
        'tickets': ticket_list_schema.dump(tickets)
    }
    return response


def post_ticket(request, session, g):
    response = DefaultModel()

    user_id = g.result_data.get('user', None).get('id', None)

    cost = request.cost
    price = request.price
    title = request.title
    description = request.description

    ticket_check = session.query(Ticket).filter(Ticket.title == title,
                                                Ticket.status >= constant.STATUS_INACTIVE).first()
    if ticket_check is not None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_EXIST][0])

    ticket = Ticket()
    session.add(ticket)
    session.flush()

    ticket.user_id = user_id
    ticket.cost = cost
    ticket.price = price
    ticket.title = title
    ticket.description = description

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
    title = request.title
    description = request.description

    ticket_check = session.query(Ticket).filter(Ticket.title == title,
                                                Ticket.title != ticket.title,
                                                Ticket.status >= constant.STATUS_INACTIVE).first()
    if ticket_check is not None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_EXIST][0])

    ticket.cost = cost
    ticket.price = price
    ticket.title = title
    ticket.description = description

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