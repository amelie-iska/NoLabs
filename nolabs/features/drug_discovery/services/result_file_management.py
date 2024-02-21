import json
import os.path
import shutil
from typing import List

import numpy as np

from nolabs.domain.experiment import ExperimentId
from nolabs.infrastructure.settings import Settings
from nolabs.utils.pdb import PDBWriter, PDBReader

from nolabs.utils.sdf import SDFReader, SDFWriter
from nolabs.features.drug_discovery.data_models.target import TargetId
from nolabs.features.drug_discovery.data_models.ligand import LigandId
from nolabs.features.drug_discovery.data_models.result import JobId, UmolResultMetaData, \
    UmolDockingResultData, JobMetaData, DiffDockDockingResultData, DiffDockResultMetaData
from nolabs.features.drug_discovery.services.ligand_file_management import LigandsFileManagement


class ResultsFileManagement:
    def __init__(self, settings: Settings, ligand_file_management: LigandsFileManagement):
        self._settings = settings
        self.sdf_reader = SDFReader()
        self.sdf_writer = SDFWriter()
        self.pdb_writer = PDBWriter()
        self.pdb_reader = PDBReader()
        self._ligand_file_management = ligand_file_management

    def ensure_results_folder_exists(self, experiment_id: ExperimentId, target_id: TargetId, ligand_id: LigandId):
        if not os.path.isdir(self.results_folder(experiment_id, target_id, ligand_id)):
            os.mkdir(self.results_folder(experiment_id, target_id, ligand_id))

    def ensure_result_folder_exists(self, experiment_id: ExperimentId, target_id: TargetId, ligand_id: LigandId,
                                    job_id: JobId):
        result_folder = self.result_folder(experiment_id, target_id, ligand_id, job_id)
        if not os.path.isdir(result_folder):
            os.mkdir(result_folder)

    def results_folder(self, experiment_id: ExperimentId, target_id: TargetId, ligand_id: LigandId) -> str:
        parent_ligand_folder = self._ligand_file_management.ligand_folder(experiment_id, target_id, ligand_id)
        return os.path.join(parent_ligand_folder, 'results')

    def result_folder(self, experiment_id: ExperimentId, target_id: TargetId, ligand_id: LigandId,
                      job_id: JobId) -> str:
        return os.path.join(self.results_folder(experiment_id, target_id, ligand_id), job_id.value)

    def create_result_folder(
            self, experiment_id: ExperimentId,
            target_id: TargetId,
            ligand_id: LigandId,
            job_id: JobId
    ):
        self.ensure_results_folder_exists(experiment_id, target_id, ligand_id)
        results_dir = self.results_folder(experiment_id, target_id, ligand_id)
        if not os.path.exists(os.path.join(results_dir, job_id.value)):
            os.mkdir(os.path.join(results_dir, job_id.value))
            self.update_result_metadata(experiment_id, target_id, ligand_id, job_id, "target_id", target_id.value)
            self.update_result_metadata(experiment_id, target_id, ligand_id, job_id, "ligand_id", ligand_id.value)
            self.update_result_metadata(experiment_id, target_id, ligand_id, job_id, "job_id", job_id.value)

    def update_job_folding_method(self, experiment_id: ExperimentId,
                                  target_id: TargetId,
                                  ligand_id: LigandId,
                                  job_id: JobId, folding_method: str):
        self.update_result_metadata(experiment_id, target_id, ligand_id, job_id, "folding_method", folding_method)

    def update_job_docking_method(self, experiment_id: ExperimentId,
                                  target_id: TargetId,
                                  ligand_id: LigandId,
                                  job_id: JobId, docking_method: str):
        self.update_result_metadata(experiment_id, target_id, ligand_id, job_id, "docking_method", docking_method)

    def store_result_input_pocketIds(self,
                                     experiment_id: ExperimentId,
                                     target_id: TargetId,
                                     ligand_id: LigandId,
                                     job_id: JobId,
                                     pocket_ids: List[int]):
        self.ensure_results_folder_exists(experiment_id, target_id, ligand_id)
        result_dir = self.result_folder(experiment_id, target_id, ligand_id, job_id)
        pocket_file = os.path.join(result_dir, self._settings.drug_discovery_running_jobs_pocket_file_name)
        pocket_arr = np.asarray(pocket_ids)
        np.save(pocket_file, pocket_arr)

    def get_result_input_pocketIds(self,
                                   experiment_id: ExperimentId,
                                   target_id: TargetId,
                                   ligand_id: LigandId,
                                   job_id: JobId):
        self.ensure_results_folder_exists(experiment_id, target_id, ligand_id)
        result_dir = self.result_folder(experiment_id, target_id, ligand_id, job_id)
        pocket_file = os.path.join(result_dir, self._settings.drug_discovery_running_jobs_pocket_file_name)
        np.load(pocket_file)

    def check_binding_pocket_exist(self, experiment_id: ExperimentId, target_id: TargetId, ligand_id: LigandId,
                                   job_id: JobId) -> bool:
        result_dir = self.result_folder(experiment_id, target_id, ligand_id, job_id)
        pocket_file = os.path.join(result_dir, self._settings.drug_discovery_running_jobs_pocket_file_name)
        return os.path.exists(pocket_file)

    def store_umol_result_data(self, experiment_id: ExperimentId,
                          target_id: TargetId,
                          ligand_id: LigandId,
                          job_id: JobId,
                          result_data: UmolDockingResultData) -> UmolResultMetaData:

        self.create_result_folder(experiment_id, target_id, ligand_id, job_id)
        result_folder = self.result_folder(experiment_id, target_id, ligand_id, job_id)

        sdf_file_name = self._settings.drug_discovery_umol_docking_result_sdf_file_name
        sdf_file_path = os.path.join(result_folder, sdf_file_name)
        sdf_contents = result_data.predicted_sdf
        self.sdf_writer.write_sdf(sdf_contents, sdf_file_path)

        pdb_file_name = self._settings.drug_discovery_umol_docking_result_pdb_file_name
        pdb_file_path = os.path.join(result_folder, pdb_file_name)
        pdb_contents = result_data.predicted_pdb
        self.pdb_writer.write_pdb(pdb_contents, pdb_file_path)

        plddt_file_name = self._settings.drug_discovery_umol_docking_result_plddt_file_name
        plddt_file_path = os.path.join(result_folder, plddt_file_name)
        plddt_list = result_data.plddt_array
        np.save(plddt_file_path, np.asarray(plddt_list))

        return UmolResultMetaData(job_id=job_id.value, target_id=target_id.value, ligand_id=ligand_id.value)

    def store_diffdock_result_data(self, experiment_id: ExperimentId,
                          target_id: TargetId,
                          ligand_id: LigandId,
                          job_id: JobId,
                          result_data: DiffDockDockingResultData) -> DiffDockResultMetaData:

        self.create_result_folder(experiment_id, target_id, ligand_id, job_id)
        result_folder = self.result_folder(experiment_id, target_id, ligand_id, job_id)

        sdf_file_path = os.path.join(result_folder, result_data.predicted_sdf_file_name)
        self.sdf_writer.write_sdf(result_data.predicted_sdf_contents, sdf_file_path)

        pdb_file_name = self._settings.drug_discovery_diffdock_docking_result_pdb_file_name
        pdb_file_path = os.path.join(result_folder, pdb_file_name)
        pdb_contents = result_data.predicted_pdb
        if not os.path.exists(pdb_file_path):
            self.pdb_writer.write_pdb(pdb_contents, pdb_file_path)

        # Check if the JSON file already exists and has content
        json_file_path = self._settings.drug_discovery_diffdock_docking_results_metadata_file_name
        if os.path.exists(json_file_path) and os.path.getsize(json_file_path) > 0:
            # Load the existing content
            with open(json_file_path, 'r') as json_file:
                docking_results = json.load(json_file)
        else:
            docking_results = {}

        key = result_data.predicted_sdf_file_name  # Assume each result has a unique file name
        docking_results[key] = {
            "confidence": result_data.confidence,
            "scored_affinity": result_data.scored_affinity,
            "minimized_affinity": result_data.minimized_affinity
        }

        # Write the updated dictionary back to the JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(docking_results, json_file, indent=4)

        return DiffDockResultMetaData(job_id=job_id.value,
                                      target_id=target_id.value,
                                      ligand_id=ligand_id.value,
                                      confidence=result_data.confidence,
                                      ligand_file_name=result_data.predicted_sdf_file_name)

    def delete_result(self, experiment_id: ExperimentId,
                      target_id: TargetId,
                      ligand_id: LigandId,
                      job_id: JobId) -> JobId:
        self.results_folder(experiment_id, target_id, ligand_id)
        self.result_folder(experiment_id, target_id, ligand_id, job_id)
        result_folder = self.result_folder(experiment_id, target_id, ligand_id, job_id)
        shutil.rmtree(result_folder)

        return job_id

    def update_result_metadata(self, experiment_id: ExperimentId, target_id: TargetId, ligand_id: LigandId,
                               job_id: JobId, key: str, value: str):
        metadata_file = os.path.join(self.result_folder(experiment_id, target_id, ligand_id, job_id),
                                     self._settings.drug_discovery_docking_result_metadata_filename_name)
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
                metadata[key] = value
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f)
        else:
            metadata = {key: value}
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f)

    def get_result_metadata(self, experiment_id: ExperimentId, target_id: TargetId, ligand_id: LigandId,
                            job_id: JobId) -> UmolResultMetaData:
        metadata_file = os.path.join(self.result_folder(experiment_id, target_id, ligand_id, job_id),
                                     self._settings.drug_discovery_ligand_metadata_file_name)
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        result_metadata = UmolResultMetaData(job_id=metadata["job_id"],
                                             target_id=metadata["target_id"],
                                             ligand_id=metadata["ligand_id"])
        return result_metadata

    def get_job_metadata(self, experiment_id: ExperimentId, target_id: TargetId, ligand_id: LigandId,
                         job_id: JobId) -> JobMetaData:
        metadata_file = os.path.join(self.result_folder(experiment_id, target_id, ligand_id, job_id),
                                     self._settings.drug_discovery_ligand_metadata_file_name)
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        result_metadata = JobMetaData(job_id=metadata["job_id"],
                                      target_id=metadata["target_id"],
                                      ligand_id=metadata["ligand_id"],
                                      folding_method=metadata["folding_method"],
                                      docking_method=metadata["docking_method"])
        return result_metadata

    def get_jobs_list(self, experiment_id: ExperimentId,
                         target_id: TargetId, ligand_id: LigandId) -> List[JobMetaData]:
        results_folder = self.results_folder(experiment_id, target_id, ligand_id)
        jobs_list = []
        if not os.path.exists(results_folder):
            return jobs_list
        for t_id in os.listdir(results_folder):
            if os.path.isdir(os.path.join(results_folder, t_id)):
                job_id = JobId(t_id)
                jobs_list.append(self.get_job_metadata(experiment_id, target_id, ligand_id, job_id))

        return jobs_list

    def get_docking_result_data(self,
                                experiment_id: ExperimentId,
                                target_id: TargetId, ligand_id: LigandId,
                                job_id: JobId) -> UmolDockingResultData:
        result_folder = self.result_folder(experiment_id, target_id, ligand_id, job_id)

        sdf_file_name = self._settings.drug_discovery_umol_docking_result_sdf_file_name
        sdf_file_path = os.path.join(result_folder, sdf_file_name)
        sdf_contents = self.sdf_reader.read_sdf(sdf_file_path)

        pdb_file_name = self._settings.drug_discovery_umol_docking_result_pdb_file_name
        pdb_file_path = os.path.join(result_folder, pdb_file_name)
        pdb_contents = self.pdb_reader.read_pdb(pdb_file_path)

        plddt_file_name = self._settings.drug_discovery_umol_docking_result_plddt_file_name
        plddt_file_path = os.path.join(result_folder, plddt_file_name)
        plddt_list = np.load(plddt_file_path).tolist()

        return UmolDockingResultData(predicted_pdb=pdb_contents, predicted_sdf=sdf_contents, plddt_array=plddt_list)

    def check_result_data_available(self, experiment_id: ExperimentId,
                                    target_id: TargetId,
                                    ligand_id: LigandId,
                                    job_id: JobId) -> bool:
        result_folder = self.result_folder(experiment_id, target_id, ligand_id, job_id)
        if not os.path.exists(result_folder):
            return False

        sdf_file_name = self._settings.drug_discovery_umol_docking_result_sdf_file_name
        sdf_file_path = os.path.join(result_folder, sdf_file_name)
        if not os.path.exists(sdf_file_path):
            return False

        pdb_file_name = self._settings.drug_discovery_umol_docking_result_pdb_file_name
        pdb_file_path = os.path.join(result_folder, pdb_file_name)
        if not os.path.exists(pdb_file_path):
            return False

        plddt_file_name = self._settings.drug_discovery_umol_docking_result_plddt_file_name
        plddt_file_path = os.path.join(result_folder, plddt_file_name)
        if not os.path.exists(plddt_file_path):
            return False

        return True
