import json

import people.api.next.serializers
from api.next.views import ResultsSetPagination
from candidates import models as extra_models
from candidates.api.next.serializers import LoggedActionSerializer
from django.db.models import Prefetch
from django.http import Http404, HttpResponsePermanentRedirect
from people.api.next.filters import PersonFilter
from people.models import Person
from popolo.models import Membership
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.reverse import reverse


class PersonViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        queryset = (
            Person.objects.prefetch_related(
                Prefetch(
                    "memberships",
                    Membership.objects.select_related("party", "post").order_by(
                        "ballot__election__election_date"
                    ),
                ),
                "memberships__ballot__election",
                "tmp_person_identifiers",
                "other_names",
                "memberships__previous_party_affiliations",
            )
            .select_related("image", "image__uploading_user")
            .order_by("id")
        )
        return queryset

    def filter_queryset(self, queryset):
        """
        If this is a last_updated request we return a maximum of 1000 objects.
        This is to avoid lambda timeouts when imorting in WCIVF.
        """
        queryset = super().filter_queryset(queryset)
        if not self.request.query_params.get("last_updated", None):
            return queryset
        return queryset.order_by("modified")[:1000]

    def list(self, request, *args, **kwargs):
        """
        If the last_updated param is used, a maximum of 1000 objects are
        returned per request.
        """
        # this method is defined only to add the docstring above to the API
        # documentation generated by swagger
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Http404 as e:
            try:
                lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
                instance = extra_models.PersonRedirect.objects.get(
                    old_person_id=self.kwargs[lookup_url_kwarg]
                )
                return HttpResponsePermanentRedirect(
                    reverse(
                        "person-detail",
                        kwargs={
                            "pk": instance.new_person_id,
                            "version": kwargs["version"],
                        },
                    )
                )
            except extra_models.PersonRedirect.DoesNotExist:
                raise Http404(e)

    @action(detail=True, methods=["get"], name="Person History")
    def history(self, request, pk=None, **kwargs):
        qs = (
            extra_models.LoggedAction.objects.filter(person_id=pk)
            .select_related("person", "user")
            .order_by("-created")
        )

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = LoggedActionSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], name="Versions")
    def versions(self, request, pk=None, **kwargs):
        return Response(json.loads(self.get_object().versions))

    serializer_class = people.api.next.serializers.PersonSerializer
    pagination_class = ResultsSetPagination
    filterset_class = PersonFilter


class PersonRedirectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = extra_models.PersonRedirect.objects.order_by("id")
    lookup_field = "old_person_id"
    serializer_class = people.api.next.serializers.PersonRedirectSerializer
    pagination_class = ResultsSetPagination
