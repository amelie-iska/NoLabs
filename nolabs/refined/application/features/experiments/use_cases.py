__all__ = [
    'GetExperimentsMetadataFeature',
    'CreateExperimentFeature'
]

import uuid
from typing import List

from nolabs.refined.application.controllers.experiments.api_models import ExperimentMetadataResponse, \
    UpdateExperimentRequest
from nolabs.refined.domain.models.common import ExperimentId, ExperimentName, Experiment


def map_experiment_to_metadata(experiment: Experiment) -> ExperimentMetadataResponse:
    return ExperimentMetadataResponse(
        id=experiment.id,
        name=str(experiment.name),
        date=experiment.created_at
    )


class GetExperimentsMetadataFeature:
    def handle(self) -> List[ExperimentMetadataResponse]:
        experiments: List[Experiment] = Experiment.objects.all()

        result: List[ExperimentMetadataResponse] = []

        for experiment in experiments:
            result.append(map_experiment_to_metadata(experiment))

        return result


class CreateExperimentFeature:
    def handle(self) -> ExperimentMetadataResponse:
        experiment = Experiment(
            id=ExperimentId(uuid.uuid4()),
            name=ExperimentName('New experiment')
        )
        experiment.save()
        return map_experiment_to_metadata(experiment)


class DeleteExperimentFeature:
    def handle(self, experiment_id: uuid.UUID):
        assert experiment_id

        experiment = Experiment.objects.with_id(experiment_id)
        if experiment:
            experiment.delete()


class UpdateExperimentFeature:
    def handle(self, request: UpdateExperimentRequest):
        assert request

        experiment = Experiment.objects.get(id=request.id)

        if experiment and request.name:
            experiment.set_name(ExperimentName(request.name))

        experiment.save()
