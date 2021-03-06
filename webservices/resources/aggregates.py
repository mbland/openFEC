import sqlalchemy as sa

from webservices import args
from webservices import docs
from webservices import spec
from webservices import utils
from webservices import filters
from webservices import schemas
from webservices.common import counts
from webservices.common import models
from webservices.common.views import ApiResource


@spec.doc(path_params=[utils.committee_param])
class AggregateResource(ApiResource):

    def build_query(self, committee_id, **kwargs):
        query = super().build_query(**kwargs)
        if committee_id is not None:
            query = query.filter(self.model.committee_id == committee_id)
        return query


@spec.doc(
    tags=['schedules/schedule_a'],
    description=docs.SIZE_DESCRIPTION,
)
class ScheduleABySizeView(AggregateResource):

    model = models.ScheduleABySize
    filter_multi_fields = [
        ('cycle', models.ScheduleABySize.cycle),
        ('size', models.ScheduleABySize.size),
    ]

    @args.register_kwargs(args.paging)
    @args.register_kwargs(args.schedule_a_by_size)
    @args.register_kwargs(
        args.make_sort_args(
            validator=args.IndexValidator(models.ScheduleABySize)
        )
    )
    @schemas.marshal_with(schemas.ScheduleABySizePageSchema())
    def get(self, committee_id=None, **kwargs):
        return super(ScheduleABySizeView, self).get(committee_id=committee_id, **kwargs)


@spec.doc(
    tags=['schedules/schedule_a'],
    description=(
        'Schedule A receipts aggregated by contributor state. To avoid double counting, '
        'memoed items are not included.'
    )
)
class ScheduleAByStateView(AggregateResource):

    model = models.ScheduleAByState
    filter_multi_fields = [
        ('cycle', models.ScheduleAByState.cycle),
        ('state', models.ScheduleAByState.state),
    ]

    @args.register_kwargs(args.paging)
    @args.register_kwargs(args.schedule_a_by_state)
    @args.register_kwargs(
        args.make_sort_args(
            validator=args.IndexValidator(models.ScheduleAByState)
        )
    )
    @schemas.marshal_with(schemas.ScheduleAByStatePageSchema())
    def get(self, committee_id=None, **kwargs):
        return super(ScheduleAByStateView, self).get(committee_id=committee_id, **kwargs)

    def build_query(self, committee_id, **kwargs):
        query = super().build_query(committee_id, **kwargs)
        if kwargs['hide_null']:
            query = query.filter(self.model.state_full != None)  # noqa
        return query


@spec.doc(
    tags=['schedules/schedule_a'],
    description=(
        'Schedule A receipts aggregated by contributor zip code. To avoid double '
        'counting, memoed items are not included.'
    )
)
class ScheduleAByZipView(AggregateResource):

    model = models.ScheduleAByZip
    filter_multi_fields = [
        ('cycle', models.ScheduleAByZip.cycle),
        ('zip', models.ScheduleAByZip.zip),
    ]

    @args.register_kwargs(args.paging)
    @args.register_kwargs(args.schedule_a_by_zip)
    @args.register_kwargs(
        args.make_sort_args(
            validator=args.IndexValidator(models.ScheduleAByZip)
        )
    )
    @schemas.marshal_with(schemas.ScheduleAByZipPageSchema())
    def get(self, committee_id=None, **kwargs):
        return super().get(committee_id=committee_id, **kwargs)


@spec.doc(
    tags=['schedules/schedule_a'],
    description=(
        'Schedule A receipts aggregated by contributor employer name. To avoid double '
        'counting, memoed items are not included.'
    )
)
class ScheduleAByEmployerView(AggregateResource):

    model = models.ScheduleAByEmployer
    filter_multi_fields = [
        ('cycle', models.ScheduleAByEmployer.cycle),
        ('employer', models.ScheduleAByEmployer.employer),
    ]

    @args.register_kwargs(args.paging)
    @args.register_kwargs(args.schedule_a_by_employer)
    @args.register_kwargs(
        args.make_sort_args(
            validator=args.IndexValidator(models.ScheduleAByEmployer)
        )
    )
    @schemas.marshal_with(schemas.ScheduleAByEmployerPageSchema())
    def get(self, committee_id=None, **kwargs):
        query = self.build_query(committee_id=committee_id, **kwargs)
        count = counts.count_estimate(query, models.db.session, threshold=5000)
        return utils.fetch_page(query, kwargs, model=self.model, count=count)


@spec.doc(
    tags=['schedules/schedule_a'],
    description=(
        'Schedule A receipts aggregated by contributor occupation. To avoid double '
        'counting, memoed items are not included.'
    )
)
class ScheduleAByOccupationView(AggregateResource):

    model = models.ScheduleAByOccupation
    filter_multi_fields = [
        ('cycle', models.ScheduleAByOccupation.cycle),
        ('occupation', models.ScheduleAByOccupation.occupation),
    ]

    @args.register_kwargs(args.paging)
    @args.register_kwargs(args.schedule_a_by_occupation)
    @args.register_kwargs(
        args.make_sort_args(
            validator=args.IndexValidator(models.ScheduleAByOccupation)
        )
    )
    @schemas.marshal_with(schemas.ScheduleAByOccupationPageSchema())
    def get(self, committee_id=None, **kwargs):
        query = self.build_query(committee_id=committee_id, **kwargs)
        count = counts.count_estimate(query, models.db.session, threshold=5000)
        return utils.fetch_page(query, kwargs, model=self.model, count=count)


@spec.doc(
    tags=['schedules/schedule_a'],
    description=(
        'Schedule A receipts aggregated by contributor FEC ID, if applicable. To avoid '
        'double counting, memoed items are not included.'
    )
)
class ScheduleAByContributorView(AggregateResource):

    model = models.ScheduleAByContributor
    filter_multi_fields = [
        ('cycle', models.ScheduleAByContributor.cycle),
        ('contributor_id', models.ScheduleAByContributor.contributor_id),
    ]

    @args.register_kwargs(args.paging)
    @args.register_kwargs(args.schedule_a_by_contributor)
    @args.register_kwargs(
        args.make_sort_args(
            validator=args.IndexValidator(models.ScheduleAByContributor)
        )
    )
    @schemas.marshal_with(schemas.ScheduleAByContributorPageSchema())
    def get(self, committee_id=None, **kwargs):
        return super().get(committee_id=committee_id, **kwargs)


@spec.doc(
    tags=['schedules/schedule_a'],
    description=(
        'Schedule A receipts aggregated by contributor type (individual or committee), if applicable. '
        'To avoid double counting, memoed items are not included.'
    )
)
class ScheduleAByContributorTypeView(AggregateResource):

    model = models.ScheduleAByContributorType
    filter_match_fields = [
        ('individual', models.ScheduleAByContributorType.individual),
    ]
    filter_multi_fields = [
        ('cycle', models.ScheduleAByContributorType.cycle),
    ]

    @args.register_kwargs(args.paging)
    @args.register_kwargs(args.schedule_a_by_contributor_type)
    @args.register_kwargs(
        args.make_sort_args(
            validator=args.IndexValidator(models.ScheduleAByContributorType)
        )
    )
    @schemas.marshal_with(schemas.ScheduleAByContributorTypePageSchema())
    def get(self, committee_id=None, **kwargs):
        return super().get(committee_id=committee_id, **kwargs)


@spec.doc(
    tags=['schedules/schedule_b'],
    description=(
        'Schedule B receipts aggregated by recipient name. To avoid '
        'double counting, memoed items are not included.'
    )
)
class ScheduleBByRecipientView(AggregateResource):

    model = models.ScheduleBByRecipient
    filter_multi_fields = [
        ('cycle', models.ScheduleBByRecipient.cycle),
        ('recipient_name', models.ScheduleBByRecipient.recipient_name),
    ]

    @args.register_kwargs(args.paging)
    @args.register_kwargs(args.schedule_b_by_recipient)
    @args.register_kwargs(
        args.make_sort_args(
            validator=args.IndexValidator(models.ScheduleBByRecipient)
        )
    )
    @schemas.marshal_with(schemas.ScheduleBByRecipientPageSchema())
    def get(self, committee_id=None, **kwargs):
        return super().get(committee_id=committee_id, **kwargs)


@spec.doc(
    tags=['schedules/schedule_b'],
    description=(
        'Schedule B receipts aggregated by recipient committee ID, if applicable. To avoid '
        'double counting, memoed items are not included.'
    )
)
class ScheduleBByRecipientIDView(AggregateResource):

    model = models.ScheduleBByRecipientID
    filter_multi_fields = [
        ('cycle', models.ScheduleBByRecipientID.cycle),
        ('recipient_id', models.ScheduleBByRecipientID.recipient_id),
    ]

    @args.register_kwargs(args.paging)
    @args.register_kwargs(args.schedule_b_by_recipient_id)
    @args.register_kwargs(
        args.make_sort_args(
            validator=args.IndexValidator(models.ScheduleBByRecipientID)
        )
    )
    @schemas.marshal_with(schemas.ScheduleBByRecipientIDPageSchema())
    def get(self, committee_id=None, **kwargs):
        return super().get(committee_id=committee_id, **kwargs)


@spec.doc(
    tags=['schedules/schedule_b'],
    description=(
        'Schedule B receipts aggregated by disbursement purpose category. To avoid double '
        'counting, memoed items are not included.'
    )
)
class ScheduleBByPurposeView(AggregateResource):

    model = models.ScheduleBByPurpose
    filter_multi_fields = [
        ('cycle', models.ScheduleBByPurpose.cycle),
        ('purpose', models.ScheduleBByPurpose.purpose),
    ]

    @args.register_kwargs(args.paging)
    @args.register_kwargs(args.schedule_b_by_purpose)
    @args.register_kwargs(
        args.make_sort_args(
            validator=args.IndexValidator(models.ScheduleBByPurpose)
        )
    )
    @schemas.marshal_with(schemas.ScheduleBByPurposePageSchema())
    def get(self, committee_id=None, **kwargs):
        return super().get(committee_id=committee_id, **kwargs)


@spec.doc(
    tags=['schedules/schedule_b'],
    description=(
        'Schedule E receipts aggregated by recipient candidate. To avoid double '
        'counting, memoed items are not included.'
    )
)
class ScheduleEByCandidateView(AggregateResource):

    model = models.ScheduleEByCandidate
    filter_multi_fields = [
        ('cycle', models.ScheduleEByCandidate.cycle),
        ('candidate_id', models.ScheduleEByCandidate.candidate_id),
    ]
    filter_match_fields = [
        ('support_oppose', models.ScheduleEByCandidate.support_oppose_indicator),
    ]
    query_options = [
        sa.orm.joinedload(models.ScheduleEByCandidate.candidate),
        sa.orm.joinedload(models.ScheduleEByCandidate.committee),
    ]

    @args.register_kwargs(args.paging)
    @args.register_kwargs(args.elections)
    @args.register_kwargs(args.schedule_e_by_candidate)
    @args.register_kwargs(
        args.make_sort_args(
            validator=args.IndexValidator(models.ScheduleEByCandidate)
        )
    )
    @schemas.marshal_with(schemas.ScheduleEByCandidatePageSchema())
    def get(self, committee_id=None, **kwargs):
        return super().get(committee_id=committee_id, **kwargs)

    def build_query(self, committee_id, **kwargs):
        query = super().build_query(committee_id, **kwargs)
        return filters.filter_election(query, kwargs, self.model.candidate_id, self.model.cycle)


@spec.doc(
    tags=['communication_cost'],
    description='Communication cost aggregated by candidate ID and committee ID.',
)
class CommunicationCostByCandidateView(AggregateResource):

    model = models.CommunicationCostByCandidate
    filter_multi_fields = [
        ('cycle', models.CommunicationCostByCandidate.cycle),
        ('candidate_id', models.CommunicationCostByCandidate.candidate_id),
    ]
    filter_match_fields = [
        ('support_oppose', models.CommunicationCostByCandidate.support_oppose_indicator),
    ]
    query_options = [
        sa.orm.joinedload(models.CommunicationCostByCandidate.candidate),
        sa.orm.joinedload(models.CommunicationCostByCandidate.committee),
    ]

    @args.register_kwargs(args.paging)
    @args.register_kwargs(args.elections)
    @args.register_kwargs(args.communication_cost_by_candidate)
    @args.register_kwargs(
        args.make_sort_args(
            validator=args.IndexValidator(models.CommunicationCostByCandidate)
        )
    )
    @schemas.marshal_with(schemas.CommunicationCostByCandidatePageSchema())
    def get(self, committee_id=None, **kwargs):
        return super().get(committee_id=committee_id, **kwargs)

    def build_query(self, committee_id, **kwargs):
        query = super().build_query(committee_id, **kwargs)
        return filters.filter_election(query, kwargs, self.model.candidate_id, self.model.cycle)


@spec.doc(
    tags=['electioneering'],
    description='Electioneering costs aggregated by candidate.',
)
class ElectioneeringByCandidateView(AggregateResource):

    model = models.ElectioneeringByCandidate
    filter_multi_fields = [
        ('cycle', models.ElectioneeringByCandidate.cycle),
        ('candidate_id', models.ElectioneeringByCandidate.candidate_id),
    ]

    @args.register_kwargs(args.paging)
    @args.register_kwargs(args.elections)
    @args.register_kwargs(args.electioneering_by_candidate)
    @args.register_kwargs(
        args.make_sort_args(
            validator=args.IndexValidator(models.ElectioneeringByCandidate)
        )
    )
    @schemas.marshal_with(schemas.ElectioneeringByCandidatePageSchema())
    def get(self, committee_id=None, **kwargs):
        return super().get(committee_id=committee_id, **kwargs)

    def build_query(self, committee_id, **kwargs):
        query = super().build_query(committee_id, **kwargs)
        return filters.filter_election(query, kwargs, self.model.candidate_id, self.model.cycle)
