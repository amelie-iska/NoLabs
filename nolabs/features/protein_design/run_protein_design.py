import protein_design_microservice as microservice

from nolabs.exceptions import NoLabsException, ErrorCodes
from nolabs.domain.experiment import ExperimentId, ExperimentName
from nolabs.api_models.protein_design import RunProteinDesignRequest, RunProteinDesignResponse
from nolabs.infrastructure.settings import Settings
from nolabs.features.protein_design.services.file_management import FileManagement


class RunProteinDesignFeature:
    def __init__(self,
                 file_management: FileManagement,
                 settings: Settings):
        self._file_management = file_management
        self._settings = settings

    async def handle(self,
                     request: RunProteinDesignRequest) -> RunProteinDesignResponse:
        assert request

        experiment_id = ExperimentId(request.experiment_id)
        experiment_name = ExperimentName(request.experiment_name)
        pdb_content = await request.pdb_file.read()
        await request.pdb_file.seek(0)

        configuration = microservice.Configuration(
            host=self._settings.protein_design_experiments_folder
        )
        with microservice.ApiClient(configuration=configuration) as client:
            api_instance = microservice.DefaultApi(client)
            response = api_instance.run_rfdiffusion_endpoint_run_rfdiffusion_post(
                run_rfdiffusion_request=microservice.RunRfdiffusionRequest(
                    pdb_content=pdb_content,
                    hotspots=request.hotspots,
                    contig=request.contig,
                    timesteps=request.timesteps,
                    number_of_designs=request.number_of_desings
                )
            )

            if response.errors or not response.pdbs_contents:
                raise NoLabsException(', '.join(response.errors), ErrorCodes.protein_design_run_error)

            await self._file_management.update_metadata(
                experiment_id=experiment_id,
                experiment_name=experiment_name,
                run_protein_design_request=request
            )
            self._file_management.save_experiment(
                experiment_id=experiment_id,
                pdbs_content=response.pdbs_contents
            )
            return RunProteinDesignResponse(
                experiment_id=experiment_id.value,
                experiment_name=experiment_name.value,
                pdbs_content=response.pdbs_contents
            )