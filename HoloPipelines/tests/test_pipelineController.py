import os
import pathlib
import subprocess


newCwd = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))).parent)


def test_main_missing_pipeline():
    output = subprocess.run(
        [
            "python",
            "pipeline_runner.py",
            "-c",
            "./core/pipelines/pipelines_list.json",
            "ThisPipelineIdDoesNotExist",
        ],
        cwd=newCwd,
    )
    assert 1 == output.returncode


def test_main_samplePipeline_missing_pipeline_with_extra_arguments():
    output = subprocess.run(
        [
            "python",
            "pipeline_runner.py",
            "-c",
            "./core/pipelines/pipelines_list.json",
            "ThisPipelineIdDoesNotExist",
            "-p",
            "0",
        ],
        cwd=newCwd,
    )
    assert 1 == output.returncode


def test_main_ls_normal():
    output = subprocess.run(
        [
            "python",
            "pipeline_runner.py",
            "-c",
            "./core/pipelines/pipelines_list.json",
            "--ls",
        ],
        cwd=newCwd,
    )
    assert 0 == output.returncode


def test_main_info_dicom2glb():
    output = subprocess.run(
        [
            "python",
            "pipeline_runner.py",
            "-c",
            "./core/pipelines/pipelines_list.json",
            "--info",
            "DICOM to glb",
        ],
        cwd=newCwd,
    )
    assert 0 == output.returncode


def test_main_info_for_missing_pipeline():
    output = subprocess.run(
        [
            "python",
            "pipeline_runner.py",
            "-c",
            "./core/pipelines/pipelines_list.json",
            "--info",
            "doesNotExist",
        ],
        cwd=newCwd,
    )
    assert 1 == output.returncode