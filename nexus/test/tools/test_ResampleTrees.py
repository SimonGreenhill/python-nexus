"""Tests for utils in bin directory"""
import os

from nexus import NexusReader, NexusWriter, NexusFormatException
from nexus.bin.nexus_treemanip import run_resample

EXAMPLE_DIR = os.path.join(os.path.split(os.path.dirname(__file__))[0], '../examples')

class Test_ResampleTrees:
    """Test nexus_treemanip.run_resample"""
    def setup(self):
        self.nexus = NexusReader(os.path.join(EXAMPLE_DIR, 'example.trees'))
        
    def test_resample(self):
        newnex = run_resample(2, self.nexus)
        assert len(newnex.trees.trees) == 1
        
    def test_resample_one(self):
        newnex = run_resample(1, self.nexus)
        assert len(newnex.trees.trees) == 3
    
