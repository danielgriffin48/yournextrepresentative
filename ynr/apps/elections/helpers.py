from functools import update_wrapper
from django.utils import timezone

from candidates.models import Ballot


class ElectionIDSwitcher:
    def __init__(self, ballot_view, election_view, **initkwargs):
        self.election_id_kwarg = initkwargs.get("election_id_kwarg", "election")
        self.ballot_view = ballot_view
        self.election_view = election_view

    def __call__(self, request, *args, **kwargs):
        ballot_qs = Ballot.objects.filter(
            ballot_paper_id=kwargs[self.election_id_kwarg]
        )

        if ballot_qs.exists():
            # This is a ballot paper ID
            view_cls = self.ballot_view
        else:
            # Assume this is an election ID, or let the election_view
            # deal with the 404
            view_cls = self.election_view

        view = view_cls.as_view()

        view.view_class = view_cls
        # take name and docstring from class
        update_wrapper(view, view_cls, updated=())
        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, view_cls.dispatch, assigned=())

        self.__name__ = self.__qualname__ = view.__name__
        return view(request, *args, **kwargs)


def four_weeks_before_election_date(election):
    """
    Takes an election object and a datetime object four weeks prior to the
    election date.
    Used in data migrations where we want to set a realistic created timestamp
    on old objects.
    """
    election_date = election.election_date - timezone.timedelta(weeks=4)
    return timezone.datetime(
        election_date.year,
        election_date.month,
        election_date.day,
        tzinfo=timezone.utc,
    )
