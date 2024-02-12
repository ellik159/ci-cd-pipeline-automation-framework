"""Tests for pipeline generator"""

import pytest
from pathlib import Path
import tempfile

from src.generators.pipeline_generator import PipelineGenerator


def test_generator_creates_workflow_file():
    """Test that generator creates a workflow file"""
    with tempfile.TemporaryDirectory() as tmpdir:
        generator = PipelineGenerator('github')
        
        analysis = {
            'languages': ['python'],
            'has_docker': False,
            'has_tests': True,
            'package_manager': 'pip',
        }
        
        config = {
            'pipeline': {'name': 'Test Pipeline', 'triggers': ['push']},
            'security': {'trivy_enabled': True},
            'runtime': {'python_version': '3.9'},
        }
        
        output_file = generator.generate(analysis, config, tmpdir)
        
        assert Path(output_file).exists()
        assert 'ci-cd-pipeline.yml' in output_file


def test_generator_selects_python_template():
    """Test template selection for Python projects"""
    generator = PipelineGenerator('github')
    
    analysis = {'languages': ['python'], 'has_docker': False}
    template = generator._select_template(analysis)
    
    assert template == 'python-pipeline.yml.j2'


def test_generator_selects_docker_template():
    """Test template selection for Docker projects"""
    generator = PipelineGenerator('github')
    
    analysis = {'languages': ['python'], 'has_docker': True}
    template = generator._select_template(analysis)
    
    assert template == 'docker-pipeline.yml.j2'


def test_generator_unsupported_platform():
    """Test that unsupported platforms raise error"""
    with pytest.raises(ValueError):
        generator = PipelineGenerator('unsupported')
        generator.generate({}, {}, '/tmp')
