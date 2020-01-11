from py.srv.database import db_session
from py.srv.notifications import NotificationMdl


@db_session
def get_notifications(session, args, acl):
    limit = 50
    if 'limit' in args.keys():
        limit = args['limit']
    items = NotificationMdl.get_all(session=session, limit=limit)
    items = [x for x in items if x.acl <= acl]

    if 'skip' in args.keys():
        return items[args['skip']:]
    return items
